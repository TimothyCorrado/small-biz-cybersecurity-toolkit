# CASE-05: Unauthorized Scheduled Task Creation

## Alert Name
Scheduled Task Created by Non-Admin User

## Environment
State Government – Windows Endpoint

## Alert Description
A scheduled task was created by a standard user account without administrative approval.

## Log Sources
- Windows Security Event Log
  - Event ID 4698 – Scheduled Task Created

## Detection Logic
- Task created by non-admin user
- Task executes from user directory
- Task set to run automatically

## Triage Steps
1. Reviewed task configuration and command
2. Verified user permissions
3. Checked execution frequency and triggers

## Analysis
Scheduled task execution from a user directory may indicate persistence behavior.

## Outcome
⚠️ Suspicious – Requires Further Review

## Recommendation
Validate task purpose with user. Remove task if unauthorized and monitor for re-creation.

## Notes
Persistence mechanisms often appear legitimate without proper context.
