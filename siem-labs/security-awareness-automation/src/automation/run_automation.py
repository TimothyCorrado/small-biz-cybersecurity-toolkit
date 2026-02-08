import csv
import os
import json
from datetime import datetime, timedelta, timezone
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
EVIDENCE_LOG_DIR = os.path.join(PROJECT_ROOT, "evidence", "logs")

CLICK_LOG = os.path.join(EVIDENCE_LOG_DIR, "click-events.csv")
CLICK_JSONL = os.path.join(EVIDENCE_LOG_DIR, "click-events.jsonl")
ACTIONS_LOG = os.path.join(EVIDENCE_LOG_DIR, "sent-actions.log")
METRICS_CSV = os.path.join(EVIDENCE_LOG_DIR, "metrics-summary.csv")

WINDOW_DAYS = 30

def parse_iso(ts: str) -> datetime:
    # expects ISO from server.py, includes timezone
    return datetime.fromisoformat(ts)

def ensure_paths():
    os.makedirs(EVIDENCE_LOG_DIR, exist_ok=True)
    # ensure at least one of the click logs exists
    if not (os.path.exists(CLICK_JSONL) or os.path.exists(CLICK_LOG)):
        raise FileNotFoundError(
            f"Missing click log: {CLICK_JSONL} or {CLICK_LOG}. Run server and click first."
        )

def load_clicks_since(cutoff: datetime):
    clicks = []
    # Prefer JSON Lines report if present
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
                    clicks.append(
                        {
                            "ts": ts,
                            "user": event.get("user", "unknown"),
                            "campaign": event.get("campaign", "sim-000"),
                        }
                    )
    else:
        # Fall back to CSV
        with open(CLICK_LOG, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    ts = parse_iso(row["timestamp_utc"])
                except Exception:
                    continue
                if ts >= cutoff:
                    clicks.append(
                        {
                            "ts": ts,
                            "user": row.get("user", "unknown").strip('"'),
                            "campaign": row.get("campaign", "sim-000").strip('"'),
                        }
                    )
    return clicks


def append_action(line: str):
    now = datetime.now(timezone.utc).isoformat()
    with open(ACTIONS_LOG, "a", encoding="utf-8") as f:
        f.write(f"{now} {line}\n")

def write_metrics(total_clicks: int, unique_users: int, repeat_users: int, by_campaign: dict):
    # overwrite each run to keep it clean
    with open(METRICS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["generated_utc", datetime.now(timezone.utc).isoformat()])
        w.writerow([])
        w.writerow(["metric", "value"])
        w.writerow(["total_clicks_last_30d", total_clicks])
        w.writerow(["unique_users_last_30d", unique_users])
        w.writerow(["repeat_click_users_last_30d", repeat_users])
        w.writerow([])
        w.writerow(["campaign", "clicks_last_30d"])
        for camp, cnt in sorted(by_campaign.items(), key=lambda x: x[0]):
            w.writerow([camp, cnt])
for c in clicks:
        clicks_by_user[c["user"]].append(c)
        clicks_by_campaign[c["campaign"]] += 1

    # Trigger rules
    repeat_users = 0
    for user, events in clicks_by_user.items():
        # sort by time
        events = sorted(events, key=lambda x: x["ts"])
        count = len(events)
        last_campaign = events[-1]["campaign"] if events else "sim-000"

        if count == 1:
            append_action(f"TRAINING_SENT user={user} campaign={last_campaign} clicks_30d={count}")
        elif count >= 2:
            repeat_users += 1
            append_action(f"ESCALATED user={user} campaign={last_campaign} clicks_30d={count}")

    write_metrics(
        total_clicks=len(clicks),
        unique_users=len(clicks_by_user),
        repeat_users=repeat_users,
        by_campaign=dict(clicks_by_campaign)
    )

    # Report which click log was used
    log_src = CLICK_JSONL if os.path.exists(CLICK_JSONL) else CLICK_LOG
    print("[+] Automation run complete")
    print(f"[+] Read clicks from:  {log_src}")
    print(f"[+] Wrote actions to:  {ACTIONS_LOG}")
    print(f"[+] Wrote metrics to:  {METRICS_CSV}")

if __name__ == "__main__":
    main()
