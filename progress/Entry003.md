01/02/2026:

Officially the new year. Gameplanning for @HONEYPOT-01

## Planning
- Initialize repo structure for a honeypot lab
- Add Cowrie docker-compose deployment
- Create runbook + evidence folders + export script

## Why it matters
- Demonstrates practical attack telemetry collection and triage workflows
- Produces recruiter-friendly artifacts (CSV exports + evidence trail)

## Next steps after that
- Start honeypot and verify logs generate
- Capture real attempts (or simulate safely from a test box)
- Build summary script: top IPs, top usernames/passwords, common commands

01/03/2026:

Applied to 10 different jobs on linkedin, looking at requirements needed for some positions. Set up a reminder to reach out to employers to check on the status of applications. Should be another way to set myself apart from the competition.

01/04/2026:

Tracking my crypto through a google sheet, and using the crypto portfolio I created to view and take screenshots of. Plan to generate crypto as I go, and put money to the side each week, while I work Lyft and go business to business locally to do assessments.

01/05/2026:

Goal is to get a real assessment done tomorrow, working to get past conflicts 

01/06/2026:

Reached out to people to on linkedin, and saved info from tek systems, will reach out tomorrow.

01/07/2026: Left voicemail at tek systems, and filled out a form for them to reach out to me. Over thinking the SMB process, and must just take action and fix mistakes as I go.

01/08/2026:

Got Interview in Lincoln, NE next Tuesday for IT Security Engineer I! Preparing starts now, with researching the role, polishing up my knowledge, and researching the interviewers.

01/12/2026: Interview prep, and studying questions that may be asked. And researched the position. Will practice a bit more before the interview tomorrow at 3pm.

01/13/2026: Completed interview, some questions studied popped up, some did not. It was over all great practice. will hear back next week if I got the position.

01/14/2026: Applied to a few more jobs, and another job for the same title, but different agency within NE State, just to make sure I get a job for sure soon, since Lyft is thinning on funds due to more drivers taking in to the market.

01/15/2026: Connected with recruiters on linkedin, and messaged them! One is a USMC vet and a recruiter for fiserv.

01/16/2026: Got intel to apply to remedy staffing, and GXO. Will apply over the weekend, and was told to go to remedy staffing in person after setting up my profile, they will work quicker that way.

01/17/2026: Applied for remedy, and building profile. Going to go there in person on monday.

01/18/2026: Remedy has walk-ins on Tuesdays and Thursdays, so I will be walking in Tuesday.

01/19/2026: Practiced interview questions. Going to remedy staffing tomorrow

01/20/2026: Found out that remedy staffing is only industrial, wearhouse, and physical labor jobs. Meeting with a guy I met from linkedin tomorrow morning that's with teksystems. I also got an interview at nebraska state at another agency on Friday at 3PM which is huge. Thanks to the practice I have from last interview there, I will be able to dial in, and get done much better.

01/22/2026: Utilized yesterday and today to interview prep. Meeting with teksystems recruiter went well, did a mock interview, and he told me I did great. Now just some other areas to polish for interview taking, and more questions to make sure I have down and answer confidently, and I will be able to do the best at this interview.

01/26/2026: Completed interview, debriefing with what I would need to do to be a better candidate. Automation, and SIEM practice would be good. SIEMulate SOC day work. Using more Splunk, and other tools.

01/27/2026: Building a firewall simulation, and listening to professor messer for updates with technology, and polishing up fundamentals of security. Following what professor messer is recommending with a firewall sim, to generate reports. It also was an interview question, that asked, "What my experience is with a firewall". Having a better answer for that will be good as well.

01/28/2026: Got the firewall skelton and walkthrough put together, ready to start that and have firewall experience. Then will be able to say: 
“I don’t have production enterprise firewall access yet, but I built a firewall lab where I configured outbound and inbound rules, enabled logging, generated blocked traffic, and analyzed the logs the same way a SOC would. I focused on understanding what normal noise looks like versus potentially risky patterns.”

01/29/2026: Will be working on getting my Azure Fundamentals certificate while I do this Firewall lab, since that seems to be important for government work, which is my goal to get into.

NOTES 02/01/2026 completion log:

Installed a firewall from scratch
Debugged virtualization conflicts
Fixed bootloader issues
Repaired a broken Windows network stack
Verified L3 connectivity
Brought up a production-grade firewall UI


Understanding of implicit deny
DNS flow awareness
Rule order importance
Layered troubleshooting (ICMP → DNS → HTTPS)

Removed default allow rules
Applied least privilege
Identified DNS flow dependencies
Used ICMP as a diagnostic tool
Validated behavior with testing
Confirmed logs and statefulness

“After removing the default allow rule, I selectively re-enabled outbound ICMP for diagnostics, DNS for name resolution, and HTTP/HTTPS for web access. I validated the behavior by testing raw IP connectivity, DNS resolution, and reviewing blocked traffic in the firewall logs.”

“I built a pfSense firewall lab where I removed permissive default rules and implemented least-privilege outbound access. I explicitly allowed ICMP for diagnostics, DNS for name resolution, and HTTP/HTTPS for web access, validating functionality through command-line testing and firewall logs.”

Generated unauthorized traffic
Observed it being blocked
Correlated endpoint behavior with firewall logs

ALERT-01: Blocked Outbound Traffic
Source Host: 192.168.50.50
Destination: 8.8.8.8 (DNS)
Action: Blocked (Implicit Deny)
Assessment: Endpoint attempted outbound DNS traffic outside allowed policy. Traffic was correctly blocked by firewall.
Recommendation: Validate endpoint DNS configuration and user activity.

02/06/2025: proxmox - VM software, I was told it'll "change my life", looking into it!

