from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import os
import re
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
AUTOMATION_DIR = REPO_ROOT / "automation"
RUNS_DIR = AUTOMATION_DIR / "runs"
DAILY_LOG = AUTOMATION_DIR / "DAILY_LOG.md"

SUSPICIOUS_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)aws_secret_access_key\s*="),
    re.compile(r"(?i)api[_-]?key\s*[:=]"),
    re.compile(r"(?i)secret\s*[:=]"),
    re.compile(r"(?i)password\s*[:=]"),
    re.compile(r"(?i)token\s*[:=]"),
    re.compile(r"-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----"),
]

EXCLUDE_DIRS = {".git", ".github", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}

@dataclass
class CheckResult:
    name: str
    ok: bool
    details: str

def run_cmd(cmd: list[str], cwd: Path = REPO_ROOT) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    out = (p.stdout or "") + (("\n" + p.stderr) if p.stderr else "")
    return p.returncode, out.strip()

def list_files() -> list[Path]:
    files: list[Path] = []
    for p in REPO_ROOT.rglob("*"):
        if not p.is_file():
            continue
        parts = set(p.parts)
        if any(d in parts for d in EXCLUDE_DIRS):
            continue
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip", ".7z", ".exe"}:
            continue
        files.append(p)
    return files

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()[:12]

def suspicious_scan(files: list[Path], max_findings: int = 50) -> list[str]:
    findings: list[str] = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for rx in SUSPICIOUS_PATTERNS:
            for m in rx.finditer(text):
                line_no = text[: m.start()].count("\n") + 1
                findings.append(f"- `{f.relative_to(REPO_ROOT)}` line {line_no}: matched `{rx.pattern}`")
                if len(findings) >= max_findings:
                    findings.append(f"- (truncated) reached {max_findings} findings")
                    return findings
    return findings

def main() -> int:
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S UTC")

    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    rc, sha = run_cmd(["git", "rev-parse", "--short", "HEAD"])
    sha = sha if rc == 0 else "unknown"
    rc, branch = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    branch = branch if rc == 0 else "unknown"

    checks: list[CheckResult] = []

    rc, out = run_cmd([sys.executable, "-m", "compileall", "-q", str(REPO_ROOT / "automation")])
    checks.append(CheckResult("python compileall (automation/)", rc == 0, out or "ok"))

    rc, out = run_cmd([sys.executable, "-m", "pip", "check"])
    checks.append(CheckResult("pip check", rc == 0, out or "ok"))

    files = list_files()
    findings = suspicious_scan(files)
    checks.append(CheckResult("lightweight secret-ish scan", len(findings) == 0, "no findings" if not findings else f"{len(findings)} finding(s)"))

    py_files = [f for f in files if f.suffix == ".py"]
    md_files = [f for f in files if f.suffix == ".md"]
    stats_block = "\n".join([
        f"- Total text files scanned: **{len(files)}**",
        f"- Python files: **{len(py_files)}**",
        f"- Markdown files: **{len(md_files)}**",
        f"- Python version: `{sys.version.split()[0]}`",
    ])

    checks_md = []
    overall_ok = True
    for c in checks:
        status = "✅ PASS" if c.ok else "❌ FAIL"
        overall_ok = overall_ok and c.ok
        details = c.details.replace("\n", "\n    ")
        checks_md.append(f"- **{c.name}**: {status}\n  - {details}")

    report_path = RUNS_DIR / f"{date_str}.md"
    report = f"""# Daily SOC Run — {date_str}

**Time:** {time_str}  
**Branch:** `{branch}`  
**Commit:** `{sha}`  
**Run ID:** `{sha256_text(date_str + time_str + sha)}`

## Summary
- Overall status: **{"PASS ✅" if overall_ok else "NEEDS ATTENTION ❌"}**

## Checks
{os.linesep.join(checks_md)}

## Repo stats
{stats_block}

## Findings
{"(none)" if not findings else os.linesep.join(findings)}
"""
    report_path.write_text(report, encoding="utf-8")

    DAILY_LOG.touch(exist_ok=True)
    one_liner = f"- {date_str} {time_str} — Daily SOC run: {'PASS ✅' if overall_ok else 'ATTN ❌'} (branch {branch}, {sha})\n"
    with DAILY_LOG.open("a", encoding="utf-8") as f:
        f.write(one_liner)

    print(f"Wrote {report_path.relative_to(REPO_ROOT)} and appended to {DAILY_LOG.relative_to(REPO_ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())