"""Verify security-critical Kubernetes posture claimed by this repository."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required for manifest verification") from exc

ROOT = Path(__file__).resolve().parents[1]
manifest_dir = ROOT / "kubernetes" / "base"
documents: list[dict] = []
for path in sorted(manifest_dir.glob("*.yaml")):
    for document in yaml.safe_load_all(path.read_text(encoding="utf-8")):
        if isinstance(document, dict):
            document["_source"] = path.name
            documents.append(document)

kinds = {doc.get("kind") for doc in documents}
required_kinds = {"Deployment", "Service", "HorizontalPodAutoscaler", "PodDisruptionBudget", "NetworkPolicy"}
missing = required_kinds - kinds
if missing:
    raise SystemExit(f"Missing Kubernetes resources: {', '.join(sorted(missing))}")

deploy = next(doc for doc in documents if doc.get("kind") == "Deployment")
pod = deploy["spec"]["template"]["spec"]
container = deploy["spec"]["template"]["spec"]["containers"][0]

security = container["securityContext"]
if security.get("runAsNonRoot") is not True:
    raise SystemExit("Deployment must enforce runAsNonRoot=true")
if security.get("readOnlyRootFilesystem") is not True:
    raise SystemExit("Deployment must enforce readOnlyRootFilesystem=true")
if security.get("allowPrivilegeEscalation") is not False:
    raise SystemExit("Deployment must disable privilege escalation")
if "ALL" not in (security.get("capabilities", {}).get("drop", [])):
    raise SystemExit("Deployment must drop ALL Linux capabilities")
if pod.get("automountServiceAccountToken") is not False:
    raise SystemExit("Deployment must disable automatic service-account token mounting")

for probe in ("livenessProbe", "readinessProbe", "startupProbe"):
    if probe not in container:
        raise SystemExit(f"Deployment must define {probe}")

network = next(doc for doc in documents if doc.get("kind") == "NetworkPolicy")
if set(network.get("spec", {}).get("policyTypes", [])) != {"Ingress", "Egress"}:
    raise SystemExit("NetworkPolicy must restrict both ingress and egress traffic")

print(
    "Kubernetes posture verified: "
    "non-root, read-only filesystem, dropped capabilities, "
    "disabled token automount, health probes, PDB/HPA, and bidirectional NetworkPolicy"
)
