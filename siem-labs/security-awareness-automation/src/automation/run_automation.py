import csv
import os
import json
from datetime import datetime, timedelta, timezone
from collections import defaultdict

# Determine important directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
EVIDENCE_LOG_DIR = os.path.join(PROJECT_ROOT, "evidence", "logs")

# Log file paths
CLICK_LOG = os.path.join(EVIDENCE_LOG_DIR, "click-events.csv")
CLICK_JSONL = os.path.join(EVIDENCE_LOG_DIR, "click-events.jsonl")
ACTIONS_LOG = os.path.join(EVIDENCE_LOG_DIR, "sent-actions.log")
METRICS_CSV = os.path.join(EVIDENCE_LOG_DIR, "metrics-summary.csv")

WINDOW_DAYS = 30

def parse_iso(ts: str) -> datetime:
    """Parse an ISO timestamp with timezone."""
    return datetime.fromisoformat(ts)

def ensure_paths() -> None:
    """Ensure the evidence directory exists."""
    os.makedirs(EVIDENCE_LOG_DIR, exist_ok=True)

def load_clicks_since(cutoff: datetime):
    """Load click events occurring at or after the cutoff from JSONL or CSV."""
    ensure_paths()
    clicks = []
    # Prefer JSONL if available
    if os.path.exists(CLICK_JSONL):
        with open(CLICK_JSONL, "r", encoding="utf-8") as f_jsonl:
            for line in f_jsonl:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except Exception:
                    continue
                ts_str = event.get("timestamp_utc")
                if not ts_str:
                    continue
                try:
                    ts = parse_iso(ts_str)
                except Exception:
                    continue
                if ts >= cutoff:
                    clicks.append({
                        "ts": ts,
                        "user": event.get("user", "unknown"),
                        "campaign": event.get("campaign", "sim-000"),
                    })
    elif os.path.exists(CLICK_LOG):
        # Fallback to CSV
        with open(CLICK_LOG, "r", encoding="utf-8") as f_csv:
            reader = csv.DictReader(f_csv)
            for row in reader:
                ts_str = row.get("timestamp_utc")
                if not ts_str:
                    continue
                try:
                    ts = parse_iso(ts_str)
                except Exception:
                    continue
                if ts >= cutoff:
                    clicks.append({
                        "ts": ts,
                        "user": row.get("user", "unknown").strip('"'),
                        "campaign": row.get("campaign", "sim-000").strip('"'),
                    })
    return clicks

def append_action(line: str) -> None:
    """Append an action line to the actions log with timestamp."""
    now = datetime.now(timezone.utc).isoformat()
    with open(ACTIONS_LOG, "a", encoding="utf-8") as f:
        f.write(f"{now} {line}\n")

def write_metrics(total_clicks: int, unique_users: int, repeat_users: int, by_campaign: dict) -> None:
    """Write metrics summary to CSV. This overwrites the existing file each run."""
    with open(METRICS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        # Header with generation time
        w.writerow(["generated_utc", datetime.now(timezone.utc).isoformat()])
        w.writerow([])
        # Metric section
        w.writerow(["metric", "value"])
        w.writerow(["total_clicks_last_30d", total_clicks])
        w.writerow(["unique_users_last_30d", unique_users])
        w.writerow(["repeat_click_users_last_30d", repeat_users])
        w.writerow([])
        # Campaign breakdown
        w.writerow(["campaign", "clicks_last_30d"])
        for camp, cnt in sorted(by_campaign.items(), key=lambda x: x[0]):
            w.writerow([camp, cnt])

def main() -> None:
    cutoff = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)
    clicks = load_clicks_since(cutoff)

    # Aggregate clicks by user and campaign
    clicks_by_user = defaultdict(list)
    clicks_by_campaign = defaultdict(int)

    for c in clicks:
        clicks_by_user[c["user"]].append(c)
        clicks_by_campaign[c["campaign"]] += 1

    # Apply training/escalation rules
    repeat_users = 0
    for user, events in clicks_by_user.items():
        events = sorted(events, key=lambda x: x["ts"])
        count = len(events)
        last_campaign = events[-1]["campaign"] if events else "sim-000"

        if count == 1:
            append_action(f"TRAINING_SENT user={user} campaign={last_campaign} clicks_30d={count}")
        elif count >= 2:
            repeat_users += 1
            append_action(f"ESCALATED user={user} campaign={last_campaign} clicks_30d={count}")

    # Write metrics summary
    write_metrics(
        total_clicks=len(clicks),
        unique_users=len(clicks_by_user),
        repeat_users=repeat_users,
        by_campaign=dict(clicks_by_campaign)
    )

    # Log summary paths
    log_src = CLICK_JSONL if os.path.exists(CLICK_JSONL) else CLICK_LOG
    print("[+] Automation run complete")
    print(f"[+] Read clicks from:  {log_src}")
    print(f"[+] Wrote actions to:  {ACTIONS_LOG}")
    print(f"[+] Wrote metrics to:  {METRICS_CSV}")

if __name__ == "__main__":
    main()
