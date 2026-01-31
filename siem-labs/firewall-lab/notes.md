## Provider Responsibility (Cloud Perspective)
- Physical data centers
- Hardware
- Underlying network infrastructure
- Hypervisor / base platform

## Customer Responsibility
- Firewall rules
- Network segmentation
- Allowed and blocked traffic
- Logging configuration
- Monitoring and response

## Common Failure Points
- Overly permissive rules
- No logging enabled
- No review of deny logs
- Assumption that blocking equals security

## Lab Design Decisions
- Default-deny outbound traffic
- Explicit allow rules for required services
- Logging enabled for all denies
- Focus on understanding noise vs signal