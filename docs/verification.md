# Verification & Evidence

| Area | Evidence | Reproduction |
|---|---|---|
| Terraform syntax | .github/workflows/ci.yml | terraform fmt -check -recursive && terraform validate |
| Helm correctness | .github/workflows/ci.yml | helm lint ./helm/app |
| Application tests | .github/workflows/ci.yml | Pytest and Ruff |
| Container build | .github/workflows/ci.yml | Docker Buildx |
| Security analysis | .github/workflows/codeql.yml | CodeQL |
| Workflow supply-chain posture | .github/workflows/scorecard.yml | OpenSSF Scorecard |

## Secret handling

Production credentials are not stored in Kubernetes base manifests. The committed file is an example only; real values should arrive through a secret manager or another encrypted deployment mechanism.

## Publication rule

SRE metrics are not presented as measured unless workload, environment, observation window, and calculation method are recorded.