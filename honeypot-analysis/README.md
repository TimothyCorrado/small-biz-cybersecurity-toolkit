# @HONEYPOT-01 — Cowrie SSH Honeypot + Attack Telemetry

A controlled honeypot lab that captures credential stuffing, brute-force attempts, and attacker command behavior via Cowrie (SSH/Telnet). Includes export scripts and investigation-ready artifacts.

## Goals
- Deploy a safe SSH honeypot to capture real-world attacker behavior
- Collect structured telemetry (JSON) and export to analyst-friendly formats (CSV)
- Produce repeatable evidence and a clean write-up for recruiters

## Architecture
- Cowrie container exposes SSH on port 2222 (honeypot service)
- Logs stored in container volume, exported to `evidence/logs/`
- Scripts convert raw JSON events into CSV + summaries

## Deliverables
- [ ] Running honeypot (docker compose)
- [ ] Captured authentication attempts and commands
- [ ] Exported CSV of sessions/events
- [ ] Short incident-style report with findings

## Quick Start
```bash
cd honeypot
docker compose up -d
docker logs honeypot-cowrie --tail 50