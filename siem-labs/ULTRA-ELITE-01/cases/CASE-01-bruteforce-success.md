# CASE-01: Multiple Failed Logons Followed by Successful Authentication

## Alert Name
Excessive Failed Logons Followed by Successful Authentication

## Environment
State Government – Windows Domain Environment

## Alert Description
This alert triggered after a user account experienced multiple failed authentication attempts followed by a successful logon within a short time window.

## Log Sources
- Windows Security Event Log
  - Event ID 4625 – Failed Logon
  - Event ID 4624 – Successful Logon

## Detection Logic
- 10 or more failed logon attempts within 10 minutes
- Followed by a successful logon
- Same username and host

## Triage Steps
1. Reviewed logon failure count and timestamps
2. Identified logon type used during success event
3. Checked source IP and workstation
4. Reviewed historical login behavior for the account

## Analysis
The successful authentication occurred shortly after multiple failed attempts. Logon type indicated an interactive login from an internal workstation.

## Outcome
⚠️ Suspicious – Requires user verification

## Recommendation
Confirm with the user whether the login activity was expected. Monitor account for additional failed logons or privilege changes.

## Notes
This alert is common in government environments due to legacy systems and password complexity requirements.
