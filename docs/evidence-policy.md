# Evidence and reproducibility policy

This repository is an infrastructure reference implementation. Configuration demonstrates engineering patterns; it does not establish production SLOs for an arbitrary workload.

## Infrastructure claims

Terraform, Kubernetes, Helm, networking, security-context, and observability claims should be backed by executable validation, manifests, runbooks, or reproducible deployment steps.

## Measured claims

Latency, availability, capacity, cost, recovery time, and deployment-frequency numbers require a stated environment, workload, measurement window, sample count, tooling, and commit. Preserve benchmark artifacts where practical.

## Reference configuration

Alert thresholds, resource requests, autoscaling values, and SLO examples are reference configuration until validated against the target workload.

## CI boundary

A green CI run proves only that Terraform/Helm/application/static checks configured for the repository passed. It does not prove that an AWS/EKS deployment is production-ready.
