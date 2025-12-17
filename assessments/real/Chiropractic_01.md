# CYBERSECURITY ASSESSMENT REPORT
**Business:** Chiropractic01  
**Industry:** Healthcare  
**Employees:** 7  
**Date:** 12/16/2025  
**Consultant:** Timothy Corrado — Cybersecurity Analyst

---

## Executive Summary
This assessment provides a high-level evaluation of **Chiropractic01**’s cybersecurity posture.

The business demonstrates several strong security practices already in place; however, multiple **high-severity risks** were identified that could expose patient data, enable ransomware attacks, or create HIPAA compliance issues if not addressed.

---

## Security Snapshot
| Category | Score |
|--------|------|
| Overall Security Score | **56 / 100** |
| Network Security | **5 / 10** |
| Access Controls | **4 / 10** |
| Device Security | **6 / 10** |
| Business Processes | **9 / 10** |

---

## Severity Legend
- <span style="color:#d00000; font-weight:bold;">● High Severity</span> – Immediate attention required  
- <span style="color:#ff8c00; font-weight:bold;">● Medium Severity</span> – Important improvement  
- <span style="color:#808080; font-weight:bold;">○ Unknown</span> – Status not confirmed; may represent hidden risk  
- <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span> – Configured correctly; no action required  

---

# Top Risks
- <span style="color:#d00000; font-weight:bold;">● High Severity</span> Wi-Fi is not using WPA2 or WPA3 encryption  
- <span style="color:#d00000; font-weight:bold;">● High Severity</span> Shared user accounts and local admin access in use  
- <span style="color:#d00000; font-weight:bold;">● High Severity</span> Multi-Factor Authentication not enabled  
- <span style="color:#d00000; font-weight:bold;">● High Severity</span> No offsite backups available  
- <span style="color:#d00000; font-weight:bold;">● High Severity</span> Physical access to servers and workstations is unrestricted  

---

# Quick Wins (Complete Within 72 Hours)
- Enable **WPA2/WPA3** encryption on all Wi-Fi networks  
- Create **unique user accounts** for each employee  
- Enable **MFA on email accounts**  
- Restrict **server room access**  
- Confirm **guest Wi-Fi isolation**

---

# Detailed Findings

---

## Network / Wi-Fi
- Router firmware updated:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- Router admin password strong:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- WPA2 or WPA3 in use:  
  <span style="color:#d00000; font-weight:bold;">● High Severity</span>
- Guest Wi-Fi exists:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- Guest Wi-Fi isolated:  
  <span style="color:#808080; font-weight:bold;">○ Unknown</span>
- SSID names recorded:  
  <span style="color:#808080; font-weight:bold;">○ Unknown</span>
- Wi-Fi password complexity strong:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- WPS disabled:  
  <span style="color:#808080; font-weight:bold;">○ Unknown</span>
- UPnP disabled:  
  <span style="color:#808080; font-weight:bold;">○ Unknown</span>
- Firewall enabled on router:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>

---

## Devices / Workstations
- Windows updates current:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- Antivirus active:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- Local admin disabled:  
  <span style="color:#d00000; font-weight:bold;">● High Severity</span>
- BitLocker enabled:  
  <span style="color:#808080; font-weight:bold;">○ Unknown</span>
- Auto-lock screen enabled:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- Shared accounts in use:  
  <span style="color:#d00000; font-weight:bold;">● High Severity</span>
- RDP enabled anywhere:  
  <span style="color:#808080; font-weight:bold;">○ Unknown</span>
- Unsupported OS present:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- USB ports restricted:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>

---

## Accounts & Access Control
- Unique accounts per employee:  
  <span style="color:#d00000; font-weight:bold;">● High Severity</span>
- Password complexity enforced:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- Password expiration policy active:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- MFA on email:  
  <span style="color:#d00000; font-weight:bold;">● High Severity</span>
- MFA on critical systems:  
  <span style="color:#d00000; font-weight:bold;">● High Severity</span>
- Inactive accounts removed:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- Default accounts disabled:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>

---

## Backups & Data Protection
- Backups occur regularly:  
  <span style="color:#808080; font-weight:bold;">○ Unknown</span>
- Backups stored offsite:  
  <span style="color:#d00000; font-weight:bold;">● High Severity</span>
- Backup integrity tested:  
  <span style="color:#808080; font-weight:bold;">○ Unknown</span>
- Shared folders restricted:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- Everyone permissions found:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>

---

## Business Processes & Human Factors
- Incident response plan exists:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- Cybersecurity training done:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- Onboarding documented:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- Offboarding documented:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>

---

## Physical Security
- Networking equipment secured:  
  <span style="color:#2d6a4f; font-weight:bold;">✔ Secure / In Place</span>
- Server room restricted:  
  <span style="color:#d00000; font-weight:bold;">● High Severity</span>
- Workstations not publicly exposed:  
  <span style="color:#d00000; font-weight:bold;">● High Severity</span>

---

# Unknown Items (Requires Verification)
- Guest Wi-Fi isolation  
- SSID inventory  
- WPS configuration  
- UPnP configuration  
- BitLocker disk encryption  
- RDP exposure  
- Backup frequency  
- Backup integrity testing  

---

# Short-Term Recommendations (0–30 Days)
- Enable WPA2/WPA3 Wi-Fi encryption  
- Enforce unique user accounts  
- Enable MFA on all email accounts  
- Restrict physical access to servers  
- Implement offsite backups  

---

# Long-Term Improvements (30–180 Days)
- Deploy full-disk encryption (BitLocker)  
- Centralize identity management  
- Implement backup testing schedule  
- Perform annual cybersecurity review  

---

## Consultant
**Timothy Corrado**  
Cybersecurity Analyst  
Email: **TimothyCorrado@gmail.com**  
LinkedIn: **https://linkedin.com/in/timothy-corrado**

---

# END OF REPORT
