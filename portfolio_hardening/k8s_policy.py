from __future__ import annotations

from typing import Any


def validate_workload(manifest: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    kind = manifest.get("kind", "")
    spec = manifest.get("spec", {})
    template = spec.get("template", {}) if isinstance(spec, dict) else {}
    pod_spec = template.get("spec", {}) if isinstance(template, dict) else {}
    containers = pod_spec.get("containers", []) if isinstance(pod_spec, dict) else []
    if kind in {"Deployment", "StatefulSet", "DaemonSet", "Job"} and not containers:
        return ["no_containers"]
    pod_security = pod_spec.get("securityContext", {}) if isinstance(pod_spec, dict) else {}
    if pod_security.get("runAsNonRoot") is not True:
        findings.append("run_as_non_root_required")
    for container in containers:
        security = container.get("securityContext", {})
        if security.get("privileged") is True:
            findings.append(f"{container.get('name', 'container')}:privileged_forbidden")
        if security.get("readOnlyRootFilesystem") is not True:
            findings.append(f"{container.get('name', 'container')}:read_only_rootfs_required")
        resources = container.get("resources", {})
        limits = resources.get("limits", {}) if isinstance(resources, dict) else {}
        requests = resources.get("requests", {}) if isinstance(resources, dict) else {}
        if not limits or not requests:
            findings.append(f"{container.get('name', 'container')}:resources_required")
        for probe_name in ("readinessProbe", "livenessProbe"):
            if not container.get(probe_name):
                findings.append(f"{container.get('name', 'container')}:{probe_name}_required")
    return sorted(set(findings))
