# Contributing to Cloud-Native Platform

This repository is a production-oriented Kubernetes, Terraform, and SRE portfolio project.

## Development workflow

1. Create a focused branch from `main`.
2. Validate Terraform formatting and configuration before opening a pull request.
3. Validate Helm/Kubernetes manifests and application tests locally.
4. Keep deployment changes separate from application changes when practical.
5. Never commit cloud credentials, kubeconfigs, state files, or production secrets.

## Quality expectations

- Prefer infrastructure as code and reproducible deployments.
- Keep environment-specific values isolated from reusable modules.
- Preserve health probes, resource limits, security controls, and observability.
- Use least-privilege IAM and GitHub OIDC rather than long-lived cloud keys where possible.
- Document operational trade-offs and rollback behavior.

## Pull requests

Include affected infrastructure, validation commands, deployment impact, rollback considerations, and any security implications.
