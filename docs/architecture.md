# Architecture Documentation

## Overview
This document describes the cloud-native architecture of the application platform.

## Infrastructure

### AWS Resources
- **VPC**: 10.0.0.0/16 with public and private subnets across 3 AZs
- **EKS**: Managed Kubernetes cluster v1.28 with auto-scaling node groups
- **RDS**: PostgreSQL 16 (multi-AZ in production)
- **ElastiCache**: Redis 7.0 for caching
- **ECR**: Container registry with image scanning
- **S3**: Application data storage with versioning

### Network Architecture
```
Internet → ALB (Ingress) → EKS Pods → RDS/Redis
                              ↓
                         Prometheus/Grafana (Monitoring)
```

## Application Deployment

### Container Strategy
- Multi-stage Docker builds (build → production)
- Non-root execution (UID 1000)
- Read-only root filesystem
- Minimal image size (~150MB)

### Kubernetes Configuration
- **Namespace**: production
- **Replicas**: 3 (min) to 10 (max) via HPA
- **Resources**: 250m-500m CPU, 256Mi-512Mi memory
- **Probes**: Liveness, readiness, and startup probes
- **PDB**: Minimum 2 pods available during disruption
- **Network Policy**: Restricted ingress/egress

### Deployment Strategy
- Rolling updates (maxSurge: 1, maxUnavailable: 0)
- Zero-downtime deployments
- Automatic rollback on failure
- Image tag pinning (SHA-based)

## Monitoring

### Metrics
- Prometheus scrapes application /metrics endpoint
- Custom metrics: request rate, latency, errors
- Infrastructure metrics: CPU, memory, disk, network

### Dashboards
- Application: request rate, latency percentiles, error rate
- Infrastructure: node health, pod status, resource utilization
- SLO/SLI: availability, error budget

### Alerts
| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| HighErrorRate | >5% errors for 5m | Critical | Page on-call |
| HighLatency | P95 >2s for 10m | Warning | Slack alert |
| PodCrashLoop | >3 restarts in 5m | Critical | Page on-call |
| NodeMemory | >90% for 5m | Warning | Slack alert |
| DiskSpace | <15% free | Warning | Slack alert |

## Security

### Container Security
- Non-root user
- Read-only filesystem
- No privilege escalation
- All capabilities dropped

### Network Security
- Network policies restrict pod communication
- TLS termination at ingress
- Secrets managed via Kubernetes Secrets + AWS Secrets Manager

### CI/CD Security
- Image scanning on push to ECR
- GitHub Actions with OIDC (no long-lived credentials)
- Infrastructure changes via Terraform with state locking
