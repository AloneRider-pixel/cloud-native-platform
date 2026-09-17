from portfolio_hardening.k8s_policy import validate_workload


def _manifest(read_only: bool = True, privileged: bool = False) -> dict:
    return {
        "kind": "Deployment",
        "spec": {
            "template": {
                "spec": {
                    "securityContext": {"runAsNonRoot": True},
                    "containers": [
                        {
                            "name": "api",
                            "securityContext": {"readOnlyRootFilesystem": read_only, "privileged": privileged},
                            "resources": {"requests": {"cpu": "100m"}, "limits": {"cpu": "500m"}},
                            "readinessProbe": {"httpGet": {"path": "/ready", "port": 8080}},
                            "livenessProbe": {"httpGet": {"path": "/health", "port": 8080}},
                        }
                    ],
                }
            }
        },
    }


def test_hardened_workload_passes() -> None:
    assert validate_workload(_manifest()) == []


def test_privileged_container_is_rejected() -> None:
    assert "api:privileged_forbidden" in validate_workload(_manifest(privileged=True))


def test_missing_runtime_controls_are_reported() -> None:
    findings = validate_workload(_manifest(read_only=False))
    assert "api:read_only_rootfs_required" in findings


def test_unknown_workload_without_containers_fails_closed() -> None:
    assert validate_workload({"kind": "Deployment"}) == ["no_containers"]
