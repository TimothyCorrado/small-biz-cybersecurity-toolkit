# CASE-04: Service Account Interactive Login

## Alert Name
Service Account Used for Interactive Logon

## Environment
State Government – Domain Services

## Alert Description
A service account was used to perform an interactive login from a workstation.

## Log Sources
- Windows Security Event Log
  - Event ID 4624 – Successful Logon

## Detection Logic
- Account name matches service account naming convention
- Logon type indicates interactive or remote desktop
- Source system is a workstation

## Triage Steps
1. Confirmed account type and intended use
2. Reviewed logon type and source system
3. Checked historical login behavior

## Analysis
Service accounts should not be used for interactive logons. This behavior increases risk of credential misuse.

## Outcome
🚨 Escalated – Credential Misuse Risk

## Recommendation
Disable interactive logon for the service account and rotate credentials. Notify system owner.

## Notes
Service account misuse often indicates misconfiguration or compromised credentials.
