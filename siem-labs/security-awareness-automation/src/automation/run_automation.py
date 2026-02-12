import csv
import os
import json
from datetime import datetime, timedelta, timezone
from collections import defaultdict

# Determine important directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
EVIDENCE_LOG_DIR = os.path.join(PROJECT_ROOT, "evidence", "logs")

# Added function for ServiceNow ticket logging
def append_ticket(user: str, campaign: str, count: int) -> None:
    """Append a ServiceNow ticket line to the tickets log with timestamp."""
    now = datetime.now(timezone.utc).isoformat()
    with open(SERVICENOW_TICKETS_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{now}] user={user} campaign={campaign} clicks_30d={count}\n")

# Log file paths
CLICK_LOG = os.path.join(EVIDENCE_LOG_DIR, "click-events.csv")
CLICK_JSONL = os.path.join(EVIDENCE_LOG_DIR, "click-events.jsonl")
ACTIONS_LOG = os.path.join(EVIDENCE_LOG_DIR, "sent-actions.log")
METRICS_CSV = os.path.join(EVIDENCE_LOG_DIR, "metrics-summary.csv")
# New log file for ServiceNow tickets
SERVICENOW_TICKETS_LOG = os.path.join(EVIDENCE_LOG_DIR, "servicenow-tickets.log")

WINDOW_DAYS = 30

def parse_iso(ts: str) -> datetime:
    """Parse an ISO timestamp with timezone."""
    return datetime.fromisoformat(ts)

def ensure_paths() -> None:
    """Ensure the evidence directory exists."""
    os.makedirs(EVIDENCE_LOG_DIR, exist_ok=True)

def load_clicks_since(cutoff: datetime) -> list[dict]:
    """Load clicks from either the JSONL or CSV log since the cutoff."""
    clicks = []
    if os.path.exists(CLICK_JSONL):
        with open(CLICK_JSONL, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    item = json.loads(line)
                    ts = parse_iso(item["ts"])
                    if ts >= cutoff:
                        clicks.append(item)
                except Exception:
                    continue
    elif os.path.exists(CLICK_LOG):
        with open(CLICK_LOG, "r", encoding="utf-8") as f:
            header = f.readline()  # skip header
            for line in f:
                ts_str, user, campaign = line.strip().split(",")
                ts = parse_iso(ts_str)
                if ts >= cutoff:
                    clicks.append({"ts": ts_str, "user": user, "campaign": campaign})
    return clicks

def append_action(user: str, campaign: str, action: str) -> None:
    """Append an action entry to the sent-actions log."""
    now = datetime.now(timezone.utc).isoformat()
    with open(ACTIONS_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{now}] user={user} campaign={campaign} action={action}\n")

def write_metrics(clicks: list[dict]) -> None:
    """Write summary metrics to the CSV file."""
    from collections import Counter

    users = [c["user"] for c in clicks]
    campaigns = [c["campaign"] for c in clicks]
    repeat_users = [user for user, count in Counter(users).items() if count > 1]

    with open(METRICS_CSV, "w", encoding="utf-8") as f:
        f.write(
            "generated_utc,total_clicks,unique_users,repeat_users,total_campaigns,\"
            "\n"
        )
        f.write(
            f"{datetime.now(timezone.utc).isoformat()},{len(clicks)},{len(set(users))},"
            f"{len(repeat_users)},{len(set(campaigns))}\n"
        )


def main() -> None:
    ensure_paths()
    cutoff = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)
    clicks = load_clicks_since(cutoff)

    # Organize clicks by user
    clicks_by_user: dict[str, list[dict]] = defaultdict(list)
    for click in clicks:
        clicks_by_user[click["user"]].append(click)

    # Process each user's clicks
    for user, user_clicks in clicks_by_user.items():
        count = len(user_clicks)
        last_campaign = user_clicks[-1]["campaign"]
        if count == 1:
            append_action(user, last_campaign, "training")
        elif count >= 2:
            append_action(user, last_campaign, "escalated")
            append_ticket(user, last_campaign, count)

    write_metrics(clicks)
    log_src = CLICK_JSONL if os.path.exists(CLICK_JSONL) else CLICK_LOG
    print(f"[+] Read clicks from: {log_src}")
    print("[+] Actions log written to: sent-actions.log")
    print("[+] ServiceNow tickets log written to: servicenow-tickets.log")
    print("[+] Metrics saved to metrics-summary.csv")


if __name__ == "__main__":
    main()
