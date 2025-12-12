# CYBERSECURITY ASSESSMENT REPORT
**Business:** Riverbend Chiropractic  
**Industry:** Healthcare (Chiropractic)  
**Employees:** 6  
**Date:** 2024-12-XX (Simulated)  
**Consultant:** Timothy Corrado — Cybersecurity Analyst

---

## Executive Summary
Riverbend Chiropractic exhibits several high-severity cybersecurity weaknesses including no MFA, shared accounts, weak network security, and inadequate backup practices.  
These issues significantly increase the risk of ransomware, data breaches, credential compromise, and unauthorized access.

Immediate corrective action is required in the areas of authentication, Wi-Fi security, and backups.

---

## Security Snapshot
| Category | Score |
|---------|-------|
| **Overall Security Score** | **42 / 100** |
| Network Security | 4 / 10 |
| Access Controls | 3 / 10 |
| Device Security | 5 / 10 |
| Business Processes | 1 / 10 |

---

## Severity Legend
- <span style="color:#d00000; font-weight:bold;">● High Severity</span> – Immediate action required  
- <span style="color:#ff8c00; font-weight:bold;">● Medium Severity</span> – Needs timely improvement  
- <span style="color:#e0c200; font-weight:bold;">● Low Severity</span> – Hardening / best practice  
- <span style="color:#808080; font-weight:bold;">○ Unknown</span> – Requires verification  

---

# Top Risks
- <span style="color:#d00000; font-weight:bold;">●</span> No MFA on email or administrative accounts  
- <span style="color:#d00000; font-weight:bold;">●</span> Shared "FrontDesk" Windows login used by multiple employees  
- <span style="color:#d00000; font-weight:bold;">●</span> Backups stored onsite only and never tested  
- <span style="color:#ff8c00; font-weight:bold;">●</span> Router admin password never changed  
- <span style="color:#ff8c00; font-weight:bold;">●</span> Weak Wi-Fi password and unknown WPA2/WPA3 mode  

---

# Quick Wins (Complete Within 72 Hours)
These items provide the biggest security improvement with minimal effort:

- **Enable MFA on all email accounts immediately.**  
- **Change the router admin password to a long, unique passphrase.**  
- **Replace Wi-Fi password with a strong passphrase (14+ characters).**  
- **Enable automatic screen lock after 5–10 minutes on all Windows PCs.**  
- **Eliminate the shared “FrontDesk” account — create individual accounts for each employee.**  
- **Move the router into a restricted or locked area to prevent tampering.**

---

# Detailed Findings

## Network / Wi-Fi
- Router admin password changed: **No** <span style="color:#d00000; font-weight:bold;">●</span>  
  → **Action:** Change the router admin password immediately.

- WPA2/WPA3 encryption: **Unknown** <span style="color:#808080; font-weight:bold;">○</span>  
  → **Action:** Verify Wi-Fi is running WPA2 or WPA3. Older modes must be disabled.

- Guest Wi-Fi exists: **Yes**  

- Guest Wi-Fi isolation: **Unknown** <span style="color:#808080; font-weight:bold;">○</span>  
  → **Action:** Enable guest network isolation to prevent access to business devices.

- Wi-Fi password strength: **Weak** <span style="color:#ff8c00; font-weight:bold;">●</span>  
  → **Action:** Replace with a long passphrase immediately.

- Router firmware updated: **Unknown** <span style="color:#808080; font-weight:bold;">○</span>  
  → **Action:** Contact ISP or check router UI to confirm and apply updates.

### WPS & UPnP Security Notes

- <span style="color:#808080; font-weight:bold;">○ Unknown</span> WPS status  
  → **Action:** Disable WPS. It allows brute-force attacks against the Wi-Fi network.

- <span style="color:#808080; font-weight:bold;">○ Unknown</span> UPnP status  
  → **Action:** Disable UPnP. Malware can automatically open firewall ports if UPnP is enabled.

- Router physically secured: **No** <span style="color:#e0c200; font-weight:bold;">●</span>  
  → **Action:** Move router into a locked cabinet or restricted office.

---

## Devices / Workstations
- Total PCs: **4**  
- Windows updates current: **Unknown** <span style="color:#808080; font-weight:bold;">○</span>  
  → **Action:** Verify updates are enabled and install all pending updates.

- Antivirus: Windows Defender (baseline only)  
  → **Action:** Ensure Defender is active and updated automatically.

- Local admin restricted: **No** <span style="color:#ff8c00; font-weight:bold;">●</span>  
  → **Action:** Remove unnecessary admin rights immediately.

- BitLocker enabled: **No** <span style="color:#ff8c00; font-weight:bold;">●</span>  
  → **Action:** Enable BitLocker encryption on every workstation.

- Auto-lock enabled: **No** <span style="color:#ff8c00; font-weight:bold;">●</span>  
  → **Action:** Configure auto-lock timer on all PCs.

- Shared Windows accounts: **Yes** <span style="color:#d00000; font-weight:bold;">●</span>  
  → **Action:** Remove shared accounts and create unique user accounts.

- RDP status: **Unknown** <span style="color:#808080; font-weight:bold;">○</span>  
  → **Action:** Verify RDP is disabled unless explicitly required.

- USB unrestricted: **Yes** <span style="color:#ff8c00; font-weight:bold;">●</span>  
  → **Action:** Restrict USB drive usage or implement an acceptable-use policy.

---

## Accounts & Access Control
- Unique logins (computers): **No** <span style="color:#d00000; font-weight:bold;">●</span>  
  → **Action:** Assign each employee their own Windows login.

- Password complexity: **No** <span style="color:#ff8c00; font-weight:bold;">●</span>  
  → **Action:** Enforce strong password rules (minimum 12 characters).

- MFA on email: **No** <span style="color:#d00000; font-weight:bold;">●</span>  
  → **Action:** Enable MFA immediately for all accounts.

- Inactive accounts removed: **No** <span style="color:#ff8c00; font-weight:bold;">●</span>  
  → **Action:** Remove all unused or stale accounts now.

- Default accounts disabled: **Unknown** <span style="color:#808080; font-weight:bold;">○</span>  
  → **Action:** Verify Guest and built-in Administrator accounts are disabled.

---

## Backups & Data Protection
- Backups performed: **Manual only** <span style="color:#ff8c00; font-weight:bold;">●</span>  
  → **Action:** Replace manual backups with automated daily backups.

- Offsite/cloud backups: **No** <span style="color:#d00000; font-weight:bold;">●</span>  
  → **Action:** Implement cloud/offsite backup immediately.

- Backup restore tested: **No** <span style="color:#ff8c00; font-weight:bold;">●</span>  
  → **Action:** Perform a full backup recovery test.

- “Everyone” permissions likely present  
  → **Action:** Remove “Everyone” access and apply role-based permissions.

---

## Business Processes
- Cybersecurity training: **No** <span style="color:#d00000; font-weight:bold;">●</span>  
  → **Action:** Begin staff cybersecurity/phishing training.

- Incident response plan: **No** <span style="color:#d00000; font-weight:bold;">●</span>  
  → **Action:** Create a written incident response plan.

- Onboarding process: **No** <span style="color:#ff8c00; font-weight:bold;">●</span>  
  → **Action:** Document account creation and access procedures.

- Offboarding process: **No** <span style="color:#ff8c00; font-weight:bold;">●</span>  
  → **Action:** Create a written account removal checklist.

---

## Physical Security
- Router/network gear secured: **No** <span style="color:#e0c200; font-weight:bold;">●</span>  
  → **Action:** Move equipment to a locked or restricted location.

- Front desk workstation exposed: **Yes** <span style="color:#e0c200; font-weight:bold;">●</span>  
  → **Action:** Add privacy filters or reposition monitors.

---

# Unknown Items (Requires Verification)
These settings could not be confirmed and may represent hidden vulnerabilities:

- WPA2/WPA3 encryption status  
- Guest Wi-Fi isolation  
- Router firmware status  
- WPS enabled/disabled  
- UPnP enabled/disabled  
- RDP enabled or disabled  
- Windows update configuration  
- Default admin/guest account status  

**Action:** Verify and correct all unknown configuration items. Treat them as risks until confirmed secure.

---

# Short-Term Recommendations (0–30 Days)
- Enable MFA on all accounts  
- Replace shared logins with individual accounts  
- Strengthen Wi-Fi password  
- Verify WPA2/WPA3 and disable WPS/UPnP  
- Enable auto-lock and BitLocker  
- Secure router physically  
- Verify RDP is disabled

---

# Long-Term Improvements (30–180 Days)
- Implement automated offsite/cloud backup solution  
- Develop a written incident response plan  
- Build documented onboarding/offboarding procedures  
- Conduct annual cybersecurity training  
- Review permission structure for shared folders  

---

## Consultant
**Timothy Corrado**  
Cybersecurity Analyst  
Email: **TimothyCorrado@gmail.com**  
LinkedIn: https://linkedin.com/in/timothy-corrado

---

# END OF REPORT
