import csv
import os
from datetime import datetime, timedelta, timezone
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
EVIDENCE_LOG_DIR = os.path.join(PROJECT_ROOT, "evidence", "logs")

CLICK_LOG = os.path.join(EVIDENCE_LOG_DIR, "click-events.csv")
ACTIONS_LOG = os.path.join(EVIDENCE_LOG_DIR, "sent-actions.log")
METRICS_CSV = os.path.join(EVIDENCE_LOG_DIR, "metrics-summary.csv")

WINDOW_DAYS = 30

def parse_iso(ts: str) -> datetime:
    # expects ISO from server.py, includes timezone
    return datetime.fromisoformat(ts)

def ensure_paths():
    os.makedirs(EVIDENCE_LOG_DIR, exist_ok=True)
    if not os.path.exists(CLICK_LOG):
        raise FileNotFoundError(f"Missing click log: {CLICK_LOG}. Run server and click first.")

def load_clicks_since(cutoff: datetime):
    clicks = []
    with open(CLICK_LOG, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ts = parse_iso(row["timestamp_utc"])
            except Exception:
                continue
            if ts >= cutoff:
                clicks.append({
                    "ts": ts,
                    "user": row.get("user", "unknown").strip('"'),
                    "campaign": row.get("campaign", "sim-000").strip('"'),
                })
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

def main():
    ensure_paths()
    cutoff = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)
    clicks = load_clicks_since(cutoff)

    clicks_by_user = defaultdict(list)
    clicks_by_campaign = defaultdict(int)

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

    print("[+] Automation run complete")
    print(f"[+] Read clicks from:  {CLICK_LOG}")
    print(f"[+] Wrote actions to:  {ACTIONS_LOG}")
    print(f"[+] Wrote metrics to:  {METRICS_CSV}")

if __name__ == "__main__":
    main()