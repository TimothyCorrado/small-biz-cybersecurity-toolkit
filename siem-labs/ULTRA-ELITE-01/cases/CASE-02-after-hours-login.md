# CASE-02: After-Hours Login Detected

## Alert Name
User Authentication Outside Approved Business Hours

## Environment
State Government – End User Workstations

## Alert Description
A successful login was detected outside standard business hours for a non-service account.

## Log Sources
- Windows Security Event Log
  - Event ID 4624 – Successful Logon

## Detection Logic
- Login between 2300–0500 hours
- Non-service account
- No documented on-call role

## Triage Steps
1. Verified login timestamp and time zone
2. Checked user role and on-call status
3. Reviewed login location and workstation
4. Checked for post-login activity

## Analysis
User account logged in at 02:14 AM from a workstation normally used during business hours.

## Outcome
⚠️ Needs Verification

## Recommendation
Contact user to confirm activity. If unrecognized, reset credentials and investigate follow-on activity.

## Notes
Time-of-day analysis is an effective method to reduce false positives in SOC triage.
