from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
LOG_DIR = os.path.join(PROJECT_ROOT, "evidence", "logs")
CLICK_LOG_PATH = os.path.join(LOG_DIR, "click-events.csv")
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

def ensure_log_file():
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(CLICK_LOG_PATH):
        with open(CLICK_LOG_PATH, "w", encoding="utf-8") as f:
            f.write("timestamp_utc,user,campaign,client_ip,user_agent,path\n")

def append_click_event(user: str, campaign: str, client_ip: str, user_agent: str, path: str):
    ensure_log_file()
    ts = datetime.now(timezone.utc).isoformat()
    # very simple CSV escaping for commas
    def esc(s: str) -> str:
        return '"' + s.replace('"', '""') + '"'
    line = f"{ts},{esc(user)},{esc(campaign)},{esc(client_ip)},{esc(user_agent)},{esc(path)}\n"
    with open(CLICK_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)

        if parsed.path in ["/", "/index.html"]:
            self._serve_file(INDEX_PATH, content_type="text/html; charset=utf-8")
            return

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
                path=self.path
            )

            # show same landing page after logging
            self._serve_file(INDEX_PATH, content_type="text/html; charset=utf-8")
            return

        self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Not found")

    def _serve_file(self, filepath: str, content_type: str):
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

def main():
    ensure_log_file()
    host = "127.0.0.1"
    port = 8000
    print(f"[+] Landing page running: http://{host}:{port}/")
    print(f"[+] Click endpoint:       http://{host}:{port}/click?user=user01&campaign=sim-001")
    print(f"[+] Logging to:           {CLICK_LOG_PATH}")
    HTTPServer((host, port), Handler).serve_forever()

if __name__ == "__main__":
    main()