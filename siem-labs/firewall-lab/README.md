# pfSense Firewall Lab – Least Privilege Enforcement & Security Monitoring

## Overview
This lab demonstrates hands-on firewall deployment, policy-based traffic control, and security monitoring using **pfSense**.  
The focus of the lab was to implement **least-privilege network access**, validate enforcement, and review security logs in a manner consistent with **state and government security operations**.

The lab emphasizes **defense-in-depth, auditability, and controlled network access** rather than default-permissive configurations.

---

## Lab Objectives
- Deploy and configure a perimeter firewall with clear WAN/LAN separation
- Remove default permissive firewall rules
- Enforce **least-privilege outbound network access**
- Validate security controls through controlled testing
- Review and interpret firewall logs for operational and security relevance

---

## Environment
- **Firewall Platform:** pfSense Community Edition (2.8.1)
- **Virtualization Platform:** VirtualBox
- **Client System:** Windows 10
- **Internal Network:** 192.168.50.0/24
- **Firewall LAN Address:** 192.168.50.1

---

## Network Architecture
- **WAN Interface:** DHCP (simulated external network)
- **LAN Interface:** Internal trusted network (LAB-LAN)
- pfSense functions as the default gateway and centralized enforcement point for outbound traffic.

This design reflects common state network architectures where egress traffic is tightly controlled and monitored.

---

## Firewall Policy Design (Least Privilege)

### Default Policy
- Removed the default **“allow all LAN to any”** rule
- Implemented an **implicit deny** posture for all unspecified traffic
- Ensured rule order enforces policy predictably and consistently

### Authorized Outbound Traffic
Only the following traffic types are explicitly permitted:

1. **ICMP – Diagnostic Traffic**
   - Purpose: Network troubleshooting and operational verification
   - Protocol: ICMP
   - Source: Internal LAN
   - Destination: Any

2. **DNS – Name Resolution**
   - Purpose: Required for application and system functionality
   - Protocol: TCP/UDP
   - Port: 53
   - Source: Internal LAN
   - Destination: Any

3. **HTTP/HTTPS – Web Access**
   - Purpose: Standard user and system web communication
   - Protocol: TCP
   - Ports: 80, 443
   - Source: Internal LAN
   - Destination: Any

All other outbound traffic is **explicitly denied by policy and logged**.

---

## Validation & Testing

### Authorized Traffic Validation
From an internal workstation:
- Verified ICMP connectivity
- Confirmed DNS resolution
- Confirmed HTTPS web access

Authorized traffic functioned as expected.

---

### Policy Enforcement Testing
Controlled testing was performed to validate enforcement:
- Diagnostic traffic was temporarily restricted
- Unauthorized outbound traffic was generated
- Endpoint behavior and firewall response were observed

Unauthorized traffic was blocked as designed.

---

## Security Logging & Monitoring

Firewall activity was reviewed under:
> Status → System Logs → Firewall


Observed log data included:
- **Action:** Block
- **Interface:** LAN
- **Source Address:** 192.168.50.x
- **Destination Address:** External IPs
- **Rule:** Default deny IPv4

### Operational Interpretation
> Internal systems attempting outbound connections outside approved policy were blocked and logged, providing clear visibility for security operations and audit review.

---

## Key Outcomes
- Least-privilege network access was successfully enforced
- Firewall rules behaved predictably under both normal and restricted conditions
- Logging provided actionable visibility into denied traffic
- Security controls were validated through controlled testing

---

## Skills Demonstrated
- Firewall deployment and configuration
- Policy-based network access control
- Least-privilege enforcement
- Security logging and monitoring
- Operational validation and troubleshooting

---

## Documentation & Evidence
The `/screenshots` directory contains:
- Firewall rule configuration
- Allowed traffic validation
- Blocked traffic and corresponding firewall logs
- pfSense system status dashboard
- Evidence of blocked lateral movement between internal segments (phase 4)

---

## Interview Summary
> “I deployed and configured a pfSense firewall, removed default permissive rules, enforced least-privilege outbound access, and validated security controls by generating and reviewing blocked traffic. I then analyzed firewall logs to assess policy enforcement from an operational security perspective.”

---

## Future Enhancements
- Implement additional internal network segmentation
- Forward firewall logs to a centralized SIEM
- Correlate firewall events with endpoint telemetry
