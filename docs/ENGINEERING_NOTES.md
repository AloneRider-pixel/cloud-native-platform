# Engineering Notes

## Engineering focus
Cloud-native operations with infrastructure as code, Kubernetes deployment, observability, CI/CD, and incident-response practices.

## Key design decisions
- **Terraform:** infrastructure is represented as reproducible code.
- **EKS + Helm:** application deployment is separated from infrastructure provisioning.
- **Prometheus/Grafana/Alertmanager:** metrics, dashboards, and alert routing are first-class operational concerns.
- **Health probes and autoscaling:** workload availability and capacity are modeled explicitly.
- **OIDC-based AWS access:** CI/CD uses an assumed AWS role instead of long-lived static credentials.
- **Manual production deployment:** production release requires explicit confirmation.

## Verification checklist
- Validate Terraform configuration before applying infrastructure.
- Build the application container locally.
- Validate Helm manifests.
- Deploy to a non-production environment before production.
- Exercise health checks and rollback procedures.
