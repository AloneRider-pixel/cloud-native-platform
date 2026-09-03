# ☁️ Cloud-Native DevOps / SRE Platform

**Production-grade infrastructure** for deploying, monitoring, and operating cloud-native applications on AWS with Kubernetes, Terraform, and full observability.

---

## 🏗️ Architecture

```
Developer → Git Push
              ↓
        GitHub Actions CI/CD
         ↓          ↓
    Build & Test   Terraform Plan
         ↓
    Docker Build
         ↓
    AWS ECR (Container Registry)
         ↓
    Kubernetes (EKS) + Helm
    ┌──────┼──────┐
    ↓      ↓      ↓
  App   App   App
  Pod   Pod   Pod
    └──────┼──────┘
           ↓
    ┌──────┴──────┐
    ↓              ↓
Prometheus     Grafana
(Metrics)    (Dashboard)
    ↓
Alertmanager → Slack/PagerDuty
```

---

## ✨ Features

### Infrastructure as Code
- **Terraform** — Full AWS infrastructure (VPC, EKS, RDS, ElastiCache, S3)
- **Modular Design** — Reusable Terraform modules for each component
- **State Management** — S3 backend with DynamoDB locking
- **Environment Separation** — dev, staging, production workspaces

### Container Orchestration
- **Kubernetes (EKS)** — Managed Kubernetes on AWS
- **Helm Charts** — Templated, versioned deployments
- **Rolling Updates** — Zero-downtime deployments
- **Health Probes** — Liveness and readiness checks
- **Resource Limits** — CPU/memory requests and limits
- **Autoscaling** — HPA based on CPU/memory/custom metrics
- **Pod Disruption Budgets** — Ensure availability during updates

### CI/CD Pipeline
- **GitHub Actions** — Automated build, test, and deploy
- **Multi-stage Docker** — Optimized production images
- **Container Registry** — AWS ECR with image scanning
- **GitOps-ready** — Manifest-based deployment
- **Rollback Strategy** — One-click rollback to previous version
- **Blue/Green Support** — Traffic switching for safe releases

### Observability
- **Prometheus** — Metrics collection with ServiceMonitors
- **Grafana** — Pre-configured dashboards for apps + infra
- **Alertmanager** — Alert routing to Slack, PagerDuty, email
- **Centralized Logging** — Structured JSON logs with correlation IDs
- **Distributed Tracing** — Request tracing across services
- **SLI/SLO Dashboard** — Service level indicators and objectives

### Security
- **Secrets Management** — Kubernetes Secrets + AWS Secrets Manager
- **RBAC** — Role-based access control
- **Network Policies** — Pod-to-pod traffic restrictions
- **Pod Security Standards** — Restricted security context
- **Image Scanning** — Automated vulnerability scanning in ECR
- **TLS/HTTPS** — Ingress with cert-manager

### Incident Management
- **Runbooks** — Step-by-step incident response procedures
- **Incident Simulation** — Chaos engineering with Litmus
- **Alert Escalation** — Multi-tier alert routing
- **Post-mortem Templates** — Structured incident review

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Cloud | AWS (EKS, RDS, ElastiCache, S3, ECR) |
| IaC | Terraform 1.6, Terragrunt |
| Containers | Docker, multi-stage builds |
| Orchestration | Kubernetes 1.28, Helm 3 |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus, Grafana, Alertmanager |
| Logging | Loki, Promtail |
| Ingress | Nginx Ingress Controller |
| Secrets | AWS Secrets Manager, Sealed Secrets |

---

## 🚀 Quick Start

### Prerequisites
- AWS CLI configured
- kubectl installed
- Helm 3 installed
- Terraform 1.6+

### 1. Provision Infrastructure

```bash
cd infrastructure/terraform
terraform init
terraform plan -var-file="environments/dev.tfvars"
terraform apply -var-file="environments/dev.tfvars"
```

### 2. Deploy Application

```bash
# Update kubeconfig
aws eks update-kubeconfig --name production-cluster --region ap-south-1

# Deploy with Helm
helm upgrade --install app ./helm/app \
  --namespace production \
  --create-namespace \
  --values helm/app/values-prod.yaml
```

### 3. View Dashboards

```bash
# Port-forward Grafana
kubectl port-forward svc/grafana -n monitoring 3000:80

# Access at http://localhost:3000 (admin/admin)
```

---

## 📁 Project Structure

```
cloud-native-platform/
├── infrastructure/
│   └── terraform/
│       ├── main.tf                  # Root module
│       ├── variables.tf             # Input variables
│       ├── outputs.tf               # Output values
│       ├── providers.tf             # AWS provider config
│       ├── modules/
│       │   ├── vpc/                 # VPC, subnets, NAT
│       │   ├── eks/                 # EKS cluster + node groups
│       │   ├── rds/                 # RDS PostgreSQL
│       │   ├── redis/               # ElastiCache Redis
│       │   └── monitoring/          # Prometheus + Grafana
│       └── environments/
│           ├── dev.tfvars
│           ├── staging.tfvars
│           └── production.tfvars
├── kubernetes/
│   ├── base/                        # Base manifests
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   ├── secret.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── ingress.yaml
│   │   ├── hpa.yaml
│   │   ├── pdb.yaml
│   │   └── network-policy.yaml
│   └── overlays/
│       ├── dev/
│       ├── staging/
│       └── production/
├── helm/
│   └── app/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       ├── values-staging.yaml
│       ├── values-prod.yaml
│       └── templates/
├── docker/
│   └── Dockerfile                   # Multi-stage production build
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   ├── rules/
│   │   └── service-monitor.yaml
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── datasources/
│   └── alertmanager/
│       └── alertmanager.yml
├── scripts/
│   ├── deploy.sh
│   ├── rollback.sh
│   └── health-check.sh
├── docs/
│   ├── architecture.md
│   ├── runbooks/
│   └── incident-response.md
├── .github/workflows/
│   ├── ci.yml                       # Build + Test
│   ├── deploy-staging.yml           # Deploy to staging
│   └── deploy-production.yml        # Deploy to production
└── README.md
```

---

## 📊 Monitoring Dashboards

| Dashboard | Metrics |
|-----------|---------|
| **Application** | Request rate, latency, errors, saturation |
| **Infrastructure** | CPU, memory, disk, network per node |
| **Kubernetes** | Pod status, restarts, resource usage |
| **Database** | Connections, queries/sec, replication lag |
| **SLO/SLI** | Error budget, availability, latency percentiles |

---

## 🚨 Alert Rules

| Alert | Condition | Severity |
|-------|-----------|----------|
| HighErrorRate | Error rate > 5% for 5m | Critical |
| HighLatency | P95 latency > 2s for 10m | Warning |
| PodCrashLoop | Pod restarts > 3 in 5m | Critical |
| NodeMemoryPressure | Memory > 90% for 5m | Warning |
| DiskSpaceLow | Disk > 85% used | Warning |
| CertificateExpiry | TLS cert expires < 7 days | Warning |

---

## 📝 License

MIT
