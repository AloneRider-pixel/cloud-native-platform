import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from app.main import Handler


def _start_server() -> tuple[ThreadingHTTPServer, threading.Thread]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def _get(server: ThreadingHTTPServer, path: str) -> tuple[int, dict[str, str], bytes]:
    with urllib.request.urlopen(
        f"http://127.0.0.1:{server.server_port}{path}",
        timeout=3,
    ) as response:
        headers = {key.lower(): value for key, value in response.headers.items()}
        return response.status, headers, response.read()


def test_health_and_readiness_contracts() -> None:
    server, _ = _start_server()
    try:
        status, headers, body = _get(server, "/health")
        assert status == 200
        assert headers["content-type"].startswith("application/json")
        assert json.loads(body) == {"status": "healthy"}

        status, _, body = _get(server, "/ready")
        assert status == 200
        assert json.loads(body) == {"status": "ready"}
    finally:
        server.shutdown()
        server.server_close()


def test_metrics_contract() -> None:
    server, _ = _start_server()
    try:
        status, headers, body = _get(server, "/metrics")
        assert status == 200
        assert headers["content-type"].startswith("text/plain; version=0.0.4")
        assert b"cloud_native_app_up 1" in body
    finally:
        server.shutdown()
        server.server_close()


def test_unknown_route_returns_json_404() -> None:
    server, _ = _start_server()
    try:
        try:
            _get(server, "/does-not-exist")
        except urllib.error.HTTPError as error:
            assert error.code == 404
            assert json.loads(error.read()) == {"error": "not found"}
        else:
            raise AssertionError("Expected a 404 response")
    finally:
        server.shutdown()
        server.server_close()
