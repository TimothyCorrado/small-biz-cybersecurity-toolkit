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

## Architecture Mapping (AZ-900 Part 2)

- Azure Region → Physical location / data center boundary-
- Resource Group → Logical grouping and ownership
- Isolation → Test resources should be separated from production

## Azure Networking Takeaway (AZ-900)

Azure enforces network access through Network Security Groups, which function
like cloud firewalls. Access is controlled through explicit allow/deny rules,
and segmentation is achieved through VNets and subnets.

The same least-privilege principles apply as on-prem firewalls.