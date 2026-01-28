# CASE-03: Suspicious Process Execution from User Directory

## Alert Name
Unusual Process Execution from User Profile Path

## Environment
State Government – Endpoint Monitoring

## Alert Description
A process was executed from a user directory commonly associated with malware delivery.

## Log Sources
- Sysmon
  - Event ID 1 – Process Creation

## Detection Logic
- Process executed from:
  - AppData\Local\Temp
  - Downloads
- Parent process was a web browser

## Triage Steps
1. Reviewed process path and filename
2. Checked parent process
3. Verified file hash against known software
4. Reviewed subsequent system activity

## Analysis
The process executed from a temporary directory following a browser download. No known software matched the file hash.

## Outcome
🚨 Escalated – Potential Malware Execution

## Recommendation
Isolate host and perform endpoint malware scan. Review user activity leading up to execution.

## Notes
Process location and parent-child relationships are key indicators during triage.
