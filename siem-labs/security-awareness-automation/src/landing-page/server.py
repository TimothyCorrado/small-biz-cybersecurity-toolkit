from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone
import os
import json

# Base paths for the landing page server. BASE_DIR is the directory of this file,
# PROJECT_ROOT is two levels up (so that ``evidence`` sits alongside ``src``),
# and LOG_DIR points to ``evidence/logs`` for storing click events.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
LOG_DIR = os.path.join(PROJECT_ROOT, "evidence", "logs")
CLICK_LOG_PATH = os.path.join(LOG_DIR, "click-events.csv")
# Path for the SIEM report; JSON Lines is a common SIEM ingestion format
SIEM_REPORT_PATH = os.path.join(LOG_DIR, "click-events.jsonl")
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

def ensure_log_file() -> None:
    """Ensure the log directory and output files exist.

    A CSV header is created for backward compatibility, and an empty JSONL
    report file is created for SIEM ingestion.
    """
    os.makedirs(LOG_DIR, exist_ok=True)
    # Create CSV header if it doesn't exist (legacy)
    if not os.path.exists(CLICK_LOG_PATH):
        with open(CLICK_LOG_PATH, "w", encoding="utf-8") as f:
            f.write("timestamp_utc,user,campaign,client_ip,user_agent,path\n")
    # Touch the SIEM report file to ensure it exists
    if not os.path.exists(SIEM_REPORT_PATH):
        open(SIEM_REPORT_PATH, "a", encoding="utf-8").close()

def append_click_event(user: str, campaign: str, client_ip: str, user_agent: str, path: str) -> None:
    """Append a click event to the SIEM report (JSON Lines)."""
    ensure_log_file()
    ts = datetime.now(timezone.utc).isoformat()
    event = {
        "timestamp_utc": ts,
        "user": user,
        "campaign": campaign,
        "client_ip": client_ip,
        "user_agent": user_agent,
        "path": path,
    }
    # Write event as a JSON object on its own line. This format is ingestible by many SIEMs.
    with open(SIEM_REPORT_PATH, "a", encoding="utf-8") as f_jsonl:
        json.dump(event, f_jsonl)
        f_jsonl.write("\n")

class Handler(BaseHTTPRequestHandler):
    """Simple HTTP handler that serves a landing page and logs click events."""

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)

        # Serve the landing page at root or /index.html
        if parsed.path in ["/", "/index.html"]:
            self._serve_file(INDEX_PATH, content_type="text/html; charset=utf-8")
            return

        # Handle click events. The query string may include ``user`` and ``campaign``.
        if parsed.path == "/click":
            user = (qs.get("user", ["unknown"])[0] or "unknown").strip()
            campaign = (qs.get("campaign", ["sim-000"])[0] or "sim-000").strip()

            client_ip = self.client_address[0]
            user_agent = self.headers.get("User-Agent", "unknown")

            append_click_event(
                user=user,
                campaign=campaign,
                client_ip=client_ip,
                user_agent=user_agent,
                path=self.path,
            )

            # After logging, display the same landing page to the visitor
            self._serve_file(INDEX_PATH, content_type="text/html; charset=utf-8")
            return

        # Fallback: return a 404 for any other paths
        self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Not found")

    def _serve_file(self, filepath: str, content_type: str) -> None:
        """Helper to read a file from disk and send it as the HTTP response."""
        try:
            with open(filepath, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Server misconfigured: file missing")

def main() -> None:
    """Start the HTTP server and print useful information to stdout."""
    ensure_log_file()
    host = "127.0.0.1"
    port = 8000
    print(f"[+] Landing page running: http://{host}:{port}/")
    print(f"[+] Click endpoint:       http://{host}:{port}/click?user=user01&campaign=sim-001")
    print(f"[+] Logging to:           {CLICK_LOG_PATH}")
    HTTPServer((host, port), Handler).serve_forever()

if __name__ == "__main__":
    main()
