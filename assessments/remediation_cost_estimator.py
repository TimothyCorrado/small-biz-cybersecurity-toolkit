#!/usr/bin/env python3
"""
Remediation Cost Estimator
- Reads the same YAML used for the assessment
- Outputs a non-binding cost & effort estimate
- Intended for internal use or optional addendum
"""

import yaml
import os
import re
from datetime import date
from typing import Dict, Any, List

# ---- Cost Rules (YOU control these) ----
REMEDIATION_RULES = {
    "WPA2 or WPA3 in use": {
        "issue_when": "No",
        "fix": "Enable WPA2/WPA3 Wi-Fi encryption",
        "effort": "Low",
        "cost_range": "$0 – $150",
    },
    "Unique accounts per employee": {
        "issue_when": "No",
        "fix": "Create unique user accounts and remove shared logins",
        "effort": "Medium",
        "cost_range": "$150 – $500",
    },
    "Shared accounts in use": {
        "issue_when": "Yes",
        "fix": "Eliminate shared accounts and assign per-user credentials",
        "effort": "Medium",
        "cost_range": "$150 – $500",
    },
    "MFA on email": {
        "issue_when": "No",
        "fix": "Enable multi-factor authentication on email",
        "effort": "Low",
        "cost_range": "$0 – $100",
    },
    "MFA on critical systems": {
        "issue_when": "No",
        "fix": "Enable MFA on critical systems",
        "effort": "Medium",
        "cost_range": "$100 – $300",
    },
    "Backups stored offsite": {
        "issue_when": "No",
        "fix": "Configure offsite backups",
        "effort": "Medium",
        "cost_range": "$200 – $800",
    },
    "Server room restricted": {
        "issue_when": "No",
        "fix": "Restrict access to server/networking equipment",
        "effort": "Low",
        "cost_range": "$50 – $300",
    },
    "Workstations not publicly exposed": {
        "issue_when": "No",
        "fix": "Limit physical access to workstations",
        "effort": "Low",
        "cost_range": "$0 – $200",
    },
}

# ---- Helpers ----
def normalize(val: Any) -> str:
    if val is None:
        return "Unknown"
    v = str(val).strip().lower()
    if v in ("yes", "true", "enabled", "on"):
        return "Yes"
    if v in ("no", "false", "disabled", "off"):
        return "No"
    if v in ("unknown", "?"):
        return "Unknown"
    return val

# ---- Main ----
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate remediation cost estimate from assessment YAML.")
    parser.add_argument("-i", "--input", required=True, help="Path to assessment YAML file")
    parser.add_argument("-o", "--outdir", default="reports", help="Output directory")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    business = data.get("Business Name", "Unknown Business")
    findings: Dict[str, Any] = data.get("Findings", {})

    rows: List[str] = []

    for control, rule in REMEDIATION_RULES.items():
        actual = normalize(findings.get(control))
        if actual == rule["issue_when"]:
            rows.append(
                f"| {rule['fix']} | {rule['effort']} | {rule['cost_range']} |"
            )

    if not rows:
        rows.append("| No remediation required | — | $0 |")

    today = date.today().strftime("%m/%d/%Y")

    report = f"""# Remediation Effort & Cost Estimate
**Business:** {business}  
**Date:** {today}

> ⚠️ **Important:**  
> This document provides **non-binding, high-level estimates** for planning purposes only.  
> Actual costs may vary based on environment, vendor, licenses, and scheduling.

---

## Estimated Remediation Items

| Recommended Action | Estimated Effort | Estimated Cost Range |
|--------------------|------------------|----------------------|
{chr(10).join(rows)}

---

## Notes
- Most items involve configuration changes rather than new hardware
- Work can be completed incrementally
- Pricing may change if scope or environment differs

---

*Generated automatically from assessment responses*
"""

    safe_name = re.sub(r"[^A-Za-z0-9_]+", "_", business)
    os.makedirs(args.outdir, exist_ok=True)
    outpath = os.path.join(args.outdir, f"{safe_name}_Remediation_Estimate.md")

    with open(outpath, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"[OK] Cost estimate generated: {outpath}")

if __name__ == "__main__":
    main()
