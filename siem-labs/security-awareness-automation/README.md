# Security Awareness Automation (Local Lab)
Local-only security awareness automation lab that simulates phishing clicks, logs user actions, triggers training/escalation actions, and generates metrics.

## What it demonstrates
- Click-event logging (CSV)
- Automation rules (training + escalation)
- Metrics output for reporting
- Evidence collection for interviews

## How to run
1) Start landing page server:
- `python src/landing-page/server.py`

2) Generate click events:
- Visit: `http://127.0.0.1:8000/click?user=user01&campaign=sim-001`

3) Run automation:
- `python src/automation/run_automation.py`

## Outputs
- Click log: `evidence/logs/click-events.csv`
- Actions log: `evidence/logs/sent-actions.log`
- Metrics: `evidence/logs/metrics-summary.csv`

## Evidence
Screenshots in: `evidence/screenshots/`