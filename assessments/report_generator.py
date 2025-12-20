#!/usr/bin/env python3
"""
SMB Report Generator
- Reads a Markdown template
- Reads findings from YAML/JSON
- Outputs a filled-in Markdown report

Template path (default): assessment_template.md
"""

from __future__ import annotations

import subprocess
import sys
import argparse
import datetime as dt
import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

try:
    import yaml  # pip install pyyaml
except ImportError:
    yaml = None


TEMPLATE_DEFAULT = "assessment_template.md"

LABELS = {
    "high": '<span style="color:#d00000; font-weight:bold;">● High Severity</span>',
    "medium": '<span style="color:#ff8c00; font-weight:bold;">● Medium Severity</span>',
    "unknown": '<span style="color:#808080; font-weight:bold;">○ Unknown</span>',
    "secure": '<span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>',
}

# Map each field to a category and an "expected good" value.
# If actual != expected, we assign severity based on "bad impact" rules below.
FIELD_RULES: Dict[str, Dict[str, Any]] = {
    # Network / Wi-Fi
    "Router firmware updated": {"section": "network", "good": "Yes", "bad_sev": "medium","win_tag": "patching"},
    "Router admin password strong": {"section": "network", "good": "Yes", "bad_sev": "high","win_tag": "password_hygiene"},
    "WPA2 or WPA3 in use": {"section": "network", "good": "Yes", "bad_sev": "high"},
    "Guest Wi-Fi exists": {"section": "network", "good": "Yes", "bad_sev": "medium"},  # "No" may be OK; treat as medium improvement
    "Guest Wi-Fi isolated": {"section": "network", "good": "Yes", "bad_sev": "high"},
    "SSID names recorded": {"section": "network", "good": "Yes", "bad_sev": "medium"},
    "Wi-Fi password complexity strong": {"section": "network", "good": "Yes", "bad_sev": "medium"},
    "WPS disabled": {"section": "network", "good": "Yes", "bad_sev": "high"},
    "UPnP disabled": {"section": "network", "good": "Yes", "bad_sev": "high"},
    "Firewall enabled on router": {"section": "network", "good": "Yes", "bad_sev": "high","win_tag": "network_protection"},

    # Devices / Workstations
    "Windows Update current": {"section": "device", "good": "Yes", "bad_sev": "high","win_tag": "patching"},
    "Antivirus active": {"section": "device", "good": "Yes", "bad_sev": "high","win_tag": "endpoint_protection"},
    "Local admin disabled": {"section": "device", "good": "Yes", "bad_sev": "high"},
    "BitLocker enabled": {"section": "device", "good": "Yes", "bad_sev": "medium"},
    "Auto-lock screen enabled": {"section": "device", "good": "Yes", "bad_sev": "medium","win_tag": "workstation_hardening"},
    "Shared accounts in use": {"section": "device", "good": "No", "bad_sev": "high"},  # good is "No"
    "RDP enabled anywhere": {"section": "device", "good": "No", "bad_sev": "high"},
    "Unsupported OS present": {"section": "device", "good": "No", "bad_sev": "high"},
    "USB ports restricted": {"section": "device", "good": "Yes", "bad_sev": "medium","win_tag": "data_loss_prevention"},

    # Accounts / Access Controls
    "Unique accounts per employee": {"section": "access", "good": "Yes", "bad_sev": "high"},
    "Password complexity enforced": {"section": "access", "good": "Yes", "bad_sev": "medium","win_tag": "password_hygiene"},
    "Password expiration policy active": {"section": "access", "good": "Yes", "bad_sev": "low"},  # informational; will be treated as secure/medium only
    "MFA on email": {"section": "access", "good": "Yes", "bad_sev": "high"},
    "MFA on critical systems": {"section": "access", "good": "Yes", "bad_sev": "high"},
    "Inactive accounts removed": {"section": "access", "good": "Yes", "bad_sev": "medium","win_tag": "account_hygiene"},
    "Default accounts disabled": {"section": "access", "good": "Yes", "bad_sev": "high","win_tag": "account_hygiene"},

    # Backups / Data Protection
    "Backups occur regularly": {"section": "backup", "good": "Yes", "bad_sev": "high"},
    "Backups stored offsite": {"section": "backup", "good": "Yes", "bad_sev": "high"},
    "Backup integrity tested": {"section": "backup", "good": "Yes", "bad_sev": "medium"},
    "Shared folders restricted": {"section": "backup", "good": "Yes", "bad_sev": "medium","win_tag": "data_access"},
    "Everyone permissions found": {"section": "backup", "good": "No", "bad_sev": "high","win_tag": "data_access"},

    # Business Processes
    "Incident Response Plan exists": {"section": "process", "good": "Yes", "bad_sev": "medium"},
    "Cybersecurity training done": {"section": "process", "good": "Yes", "bad_sev": "medium","win_tag": "user_training"},
    "Onboarding documented": {"section": "process", "good": "Yes", "bad_sev": "low","win_tag": "on_offboarding"},
    "Offboarding documented": {"section": "process", "good": "Yes", "bad_sev": "high","win_tag": "on_offboarding"},

    # Physical Security
    "Networking equipment secured": {"section": "physical", "good": "Yes", "bad_sev": "medium","win_tag": "physical_security"},
    "Server room restricted": {"section": "physical", "good": "Yes", "bad_sev": "high"},
    "Workstations not publicly exposed": {"section": "physical", "good": "Yes", "bad_sev": "high"},
}

# For "What You’re Doing Well" Section
WIN_TAG_TEXT = {
    "patching": "Automatic system and security updates are being maintained",
    "password_hygiene": "Strong password practices are in place",
    "network_protection": "Basic network protection (router firewall) is enabled",
    "endpoint_protection": "Workstations have antivirus protection enabled",
    "workstation_hardening": "Workstations are configured with basic security hardening (auto-lock)",
    "data_loss_prevention": "Data-loss risk is reduced through removable media controls (USB restrictions)",
    "account_hygiene": "Account cleanup practices are in place (inactive/default accounts handled correctly)",
    "data_access": "File sharing permissions are controlled (no broad public access)",
    "user_training": "Staff cybersecurity awareness training has been completed",
    "on_offboarding": "Employee onboarding and offboarding procedures are documented",
    "physical_security": "Networking equipment is physically secured",
}

# Friendly “why it matters” snippets for the most important fields (optional but improves report)
WHY: Dict[str, str] = {
    "WPA2 or WPA3 in use": "Wi-Fi encryption protects traffic from interception. Weak/legacy Wi-Fi settings increase risk of unauthorized access.",
    "Shared accounts in use": "Shared logins reduce accountability and make investigations and compliance harder.",
    "Unique accounts per employee": "Unique logins support accountability, least privilege, and safer offboarding.",
    "MFA on email": "Email is a common entry point for phishing and ransomware; MFA blocks most account takeover attempts.",
    "Backups stored offsite": "Offsite backups protect against ransomware, theft, and disasters affecting on-site systems.",
    "Server room restricted": "Physical access can bypass many cybersecurity controls.",
    "Local admin disabled": "Admin rights increase blast radius if a workstation is compromised.",
    "RDP enabled anywhere": "Exposed remote access is frequently targeted for ransomware intrusion.",
}

SECTION_TITLES = {
    "network": "Network / Wi-Fi",
    "device": "Devices / Workstations",
    "access": "Accounts & Access Control",
    "backup": "Backups & Data Protection",
    "process": "Business Processes & Human Factors",
    "physical": "Physical Security",
}

@dataclass
class FindingLine:
    key: str
    value: str
    label_html: str
    note: str | None = None

def load_input(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")

    ext = os.path.splitext(path)[1].lower().strip(".")
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    if ext in ("yaml", "yml"):
        if yaml is None:
            raise RuntimeError("pyyaml not installed. Run: pip install pyyaml")
        return yaml.safe_load(raw) or {}
    if ext == "json":
        return json.loads(raw)
    raise ValueError("Input must be .yaml/.yml or .json")

def normalize_value(v: Any) -> str:
    if v is None:
        return "Unknown"
    s = str(v).strip()
    # Accept common variants
    s_low = s.lower()
    if s_low in ("yes", "y", "true", "enabled", "on"):
        return "Yes"
    if s_low in ("no", "n", "false", "disabled", "off"):
        return "No"
    if s_low in ("unknown", "unk", "?"):
        return "Unknown"
    return s  # allow custom strings

def classify(field: str, value: str) -> Tuple[str, str]:
    """
    Returns (severity_key, label_html)
    severity_key in {"high","medium","unknown","secure"}
    """
    value = normalize_value(value)

    if value == "Unknown":
        return "unknown", LABELS["unknown"]

    rule = FIELD_RULES.get(field)
    if not rule:
        # If not mapped, treat "Yes" as secure, "No" as medium (safe default)
        if value == "Yes":
            return "secure", LABELS["secure"]
        return "medium", LABELS["medium"]

    good = normalize_value(rule["good"])
    if value == good:
        return "secure", LABELS["secure"]

    # Determine severity for a "bad" value
    bad_sev = rule.get("bad_sev", "medium")
    if bad_sev == "high":
        return "high", LABELS["high"]
    return "medium", LABELS["medium"]

def build_wins_section(wins: set[str]) -> str:
    if not wins:
        return "- No major baseline controls were confirmed during this assessment."

    lines = []
    for tag in sorted(wins):
        text = WIN_TAG_TEXT.get(tag)
        if text:
            lines.append(f"- {text}")

    return "\n".join(lines)


def build_section_lines(findings: Dict[str, Any]) -> Tuple[Dict[str, List[FindingLine]], List[str], List[str]]:
    sections: Dict[str, List[FindingLine]] = {k: [] for k in SECTION_TITLES.keys()}
    unknown_items: List[str] = []
    top_risks: List[str] = []
    wins: set[str] = set()

    for key, val in findings.items():
        # skip non-boolean meta fields
        if key in ("Business Name", "Industry", "Employees", "Total workstations"):
            continue

        v = normalize_value(val)
        sev, label = classify(key, v)

        # ✅ Collect wins for SMB-friendly summary
        if sev == "secure":
            rule = FIELD_RULES.get(key)
            if rule and "win_tag" in rule:
                wins.add(rule["win_tag"])

        note = WHY.get(key)
        sections_key = FIELD_RULES.get(key, {}).get("section", "process")  # default-ish

        sections.setdefault(sections_key, [])
        sections[sections_key].append(FindingLine(key=key, value=v, label_html=label, note=note))

        if sev == "unknown":
            unknown_items.append(key)

        if sev == "high":
            # keep top risks short, client-friendly
            top_risks.append(f'- {LABELS["high"]} {key}')
        elif sev == "medium" and key in (
            "Guest Wi-Fi isolated",
            "WPS disabled",
            "UPnP disabled",
            "BitLocker enabled",
            "Backup integrity tested",
        ):
            # promote some medium/unknown-adjacent items into “Top Risks” if relevant
            top_risks.append(f'- {LABELS["medium"]} {key}')

    # Stable ordering: keep the order defined in FIELD_RULES when possible
    order_index = {k: i for i, k in enumerate(FIELD_RULES.keys())}

    for sec, lines in sections.items():
        lines.sort(key=lambda x: order_index.get(x.key, 9999))

    # De-dup top risks while keeping order
    seen = set()
    top_risks_dedup = []
    for r in top_risks:
        if r not in seen:
            top_risks_dedup.append(r)
            seen.add(r)

    return sections, unknown_items, top_risks_dedup, wins

def score_from_findings(findings: Dict[str, Any]) -> Tuple[int, Dict[str, int]]:
    """
    Simple scoring:
    - Start at 100.
    - High: -12
    - Medium: -6
    - Unknown: -4
    Minimum 0.

    Category scores out of 10 derived from % of secure items in that category.
    """
    total = 100
    counts_by_section = {k: {"secure": 0, "total": 0} for k in SECTION_TITLES.keys()}

    for key, val in findings.items():
        if key in ("Business Name", "Industry", "Employees", "Total workstations"):
            continue

        v = normalize_value(val)
        sev, _ = classify(key, v)

        # total score penalties
        if sev == "high":
            total -= 12
        elif sev == "medium":
            total -= 6
        elif sev == "unknown":
            total -= 4

        sec = FIELD_RULES.get(key, {}).get("section", "process")
        if sec not in counts_by_section:
            counts_by_section[sec] = {"secure": 0, "total": 0}
        counts_by_section[sec]["total"] += 1
        if sev == "secure":
            counts_by_section[sec]["secure"] += 1

    total = max(0, min(100, total))

    # Convert to /10 category scores
    cat_scores = {}
    for sec, c in counts_by_section.items():
        if c["total"] == 0:
            cat_scores[sec] = 10
        else:
            pct = c["secure"] / c["total"]
            cat_scores[sec] = int(round(pct * 10))

    # Derive overall score from category snapshot
    visible_categories = ["network", "access", "device", "process"]
    overall_10 = sum(cat_scores.get(k, 0) for k in visible_categories) / len(visible_categories)
    total = int(round((overall_10 / 10) * 100))

    return total, cat_scores

def render_findings_block(lines: List[FindingLine]) -> str:
    out = []
    for line in lines:
        out.append(f"- {line.key}: **{line.value}**  \n  {line.label_html}")
        if line.note and (line.value != "Yes" or "High Severity" in line.label_html or "Unknown" in line.label_html):
            # only include notes when it adds value
            out.append(f"  - *Why it matters:* {line.note}")
    return "\n".join(out) if out else "_No findings recorded._"

def build_quick_wins(findings: Dict[str, Any]) -> str:
    """
    Auto-generate quick wins based on high/unknown items.
    """
    wins = []

    def add_once(text: str):
        if text not in wins:
            wins.append(text)

    # High-priority quick wins
    if normalize_value(findings.get("WPA2 or WPA3 in use")) != "Yes":
        add_once("- Enable **WPA2/WPA3** on all Wi-Fi networks")
    if normalize_value(findings.get("MFA on email")) != "Yes":
        add_once("- Enable **MFA** for all email accounts")
    if normalize_value(findings.get("Unique accounts per employee")) != "Yes":
        add_once("- Create **unique accounts** per employee and remove shared logins")
    if normalize_value(findings.get("Shared accounts in use")) != "No":
        add_once("- Eliminate **shared accounts** and assign per-user credentials")
    if normalize_value(findings.get("Backups stored offsite")) != "Yes":
        add_once("- Configure **offsite backups** (cloud or rotated external drive stored offsite)")
    if normalize_value(findings.get("Server room restricted")) != "Yes":
        add_once("- Restrict **server/networking access** (locked closet/room, limited key access)")

    # Unknown verification items
    unknown_fields = [
        "Guest Wi-Fi isolated",
        "WPS disabled",
        "UPnP disabled",
        "BitLocker enabled",
        "RDP enabled anywhere",
        "Backups occur regularly",
        "Backup integrity tested",
        "SSID names recorded",
    ]
    if any(normalize_value(findings.get(f)) == "Unknown" for f in unknown_fields):
        add_once("- Verify all **Unknown** configurations (router settings + backup checks)")

    return "\n".join(wins) if wins else "- No immediate quick wins identified."

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate SMB cybersecurity assessment report from template + findings.")
    parser.add_argument("--input", "-i", required=True, help="Path to input YAML/JSON file containing business + findings.")
    parser.add_argument("--template", "-t", default=TEMPLATE_DEFAULT, help=f"Path to template markdown (default: {TEMPLATE_DEFAULT})")
    parser.add_argument("--outdir", "-o", default="reports", help="Output directory (default: reports)")
    parser.add_argument("--pdf", action="store_true", help="Also generate a PDF version of the report")
    parser.add_argument("--md2pdf", default="md_to_pdf.py", help="Path to md_to_pdf.py (default: md_to_pdf.py)")
    parser.add_argument("--wkhtmltopdf", default=None, help="Optional path to wkhtmltopdf binary (if not in PATH)")
    args = parser.parse_args()

    data = load_input(args.input)

    business = data.get("Business Name") or data.get("business_name") or "UNKNOWN_BUSINESS"
    industry = data.get("Industry") or data.get("industry") or "UNKNOWN_INDUSTRY"
    employees = data.get("Employees") or data.get("employees") or "?"
    findings = data.get("Findings") or data.get("findings") or {}

    # Allow findings to be merged with top-level key-values if user prefers flat input
    # (If they put everything under Findings, perfect. If not, it still works.)
    merged_findings = {}
    merged_findings.update(findings)

    # Also merge any known keys at the top-level as findings if present
    for k in FIELD_RULES.keys():
        if k in data and k not in merged_findings:
            merged_findings[k] = data[k]

    # Compute sections & scores
    sections, unknown_items, top_risks, wins = build_section_lines(merged_findings)
    total_score, cat_scores = score_from_findings(merged_findings)

    # Build content blocks
    top_risks_block = "\n".join(top_risks) if top_risks else f"- {LABELS['secure']} No high severity risks identified"
    quick_wins_block = build_quick_wins(merged_findings)
    wins_block = build_wins_section(wins)

    network_block = render_findings_block(sections.get("network", []))
    device_block = render_findings_block(sections.get("device", []))
    access_block = render_findings_block(sections.get("access", []))
    backup_block = render_findings_block(sections.get("backup", []))
    process_block = render_findings_block(sections.get("process", []))
    physical_block = render_findings_block(sections.get("physical", []))

    unknown_items_block = "\n".join([f"- {u}" for u in unknown_items]) if unknown_items else "- None"

    short_term = "\n".join([
        "- Enable WPA2/WPA3 Wi-Fi encryption",
        "- Enforce unique user accounts and remove shared logins",
        "- Enable MFA on email and any critical systems",
        "- Implement offsite backups and define backup frequency",
        "- Restrict physical access to networking/server equipment",
        "- Verify and resolve all Unknown items",
    ])

    long_term = "\n".join([
        "- Deploy full-disk encryption (BitLocker) on all workstations",
        "- Centralize identity and access management (least privilege)",
        "- Establish monthly backup test/restore checks",
        "- Perform quarterly account access reviews and annual security review",
        "- Document remote access policy and restrict/monitor any RDP usage",
    ])

    # Load template
    if not os.path.exists(args.template):
        raise FileNotFoundError(f"Template not found: {args.template}")

    with open(args.template, "r", encoding="utf-8") as f:
        template = f.read()

    today = dt.date.today().strftime("%m/%d/%Y")

    replacements = {
        "{{BUSINESS_NAME}}": str(business),
        "{{INDUSTRY}}": str(industry),
        "{{EMPLOYEES}}": str(employees),
        "{{DATE}}": today,
        "{{SCORE_TOTAL}}": str(total_score),
        "{{SCORE_NETWORK}}": str(cat_scores.get("network", 0)),
        "{{SCORE_ACCESS}}": str(cat_scores.get("access", 0)),
        "{{SCORE_DEVICE}}": str(cat_scores.get("device", 0)),
        "{{SCORE_PROCESSES}}": str(cat_scores.get("process", 0)),
        "{{TOP_RISKS}}": top_risks_block,
        "{{QUICK_WINS}}": quick_wins_block,
        "{{WINS_SECTION}}": wins_block,
        "{{NETWORK_FINDINGS}}": network_block,
        "{{DEVICE_FINDINGS}}": device_block,
        "{{ACCESS_FINDINGS}}": access_block,
        "{{BACKUP_FINDINGS}}": backup_block,
        "{{PROCESS_FINDINGS}}": process_block,
        "{{PHYSICAL_FINDINGS}}": physical_block,
        "{{UNKNOWN_ITEMS}}": unknown_items_block,
        "{{SHORT_TERM_RECOMMENDATIONS}}": short_term,
        "{{LONG_TERM_RECOMMENDATIONS}}": long_term,
    }

    report = template
    for k, v in replacements.items():
        report = report.replace(k, v)

    # Fallback: replace {{TODAY}} if user used it in content
    report = report.replace("{{TODAY}}", today)

    # Output file
    safe_name = re.sub(r"[^A-Za-z0-9_\-]+", "_", str(business)).strip("_")
    os.makedirs(args.outdir, exist_ok=True)
    outpath = os.path.join(args.outdir, f"{safe_name}_SMB_Report.md")

    with open(outpath, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"[OK] Generated report: {outpath}")

     # Optional: also generate PDF
    if args.pdf:
        pdf_outpath = os.path.splitext(outpath)[0] + ".pdf"

        cmd = [sys.executable, args.md2pdf, outpath, pdf_outpath]
        if args.wkhtmltopdf:
            cmd += ["--wkhtmltopdf", args.wkhtmltopdf]

        try:
            subprocess.run(cmd, check=True)
            print(f"[OK] Generated PDF: {pdf_outpath}")
        except subprocess.CalledProcessError as e:
            print("[!] PDF generation failed.")
            print(f"    Command: {' '.join(cmd)}")
            raise

if __name__ == "__main__":
    main()
