# CASE-06: PowerShell Encoded Command Execution

## Alert Name
PowerShell Encoded Command Detected

## Environment
State Government – Endpoint Monitoring

## Alert Description
PowerShell was executed using an encoded command, which can indicate obfuscation.

## Log Sources
- PowerShell Operational Log
- Sysmon
  - Event ID 1 – Process Creation

## Detection Logic
- PowerShell executed with -EncodedCommand flag
- User not identified as system administrator
- No approved script documentation

## Triage Steps
1. Decoded PowerShell command
2. Reviewed command intent
3. Checked for network or file activity following execution

## Analysis
Encoded PowerShell commands are not inherently malicious but require context. Activity did not align with documented administrative tasks.

## Outcome
🚨 Escalated – Potential Malicious Activity

## Recommendation
Isolate host and review full PowerShell execution history. Reset user credentials if necessary.

## Notes
Encoded PowerShell usage is high-signal and low-volume in government environments.
