"""Minimal reference application used by the cloud-native platform deployment."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def _respond(self, status: int, body: dict) -> None:
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._respond(200, {"status": "healthy"})
        elif self.path == "/ready":
            self._respond(200, {"status": "ready"})
        elif self.path == "/metrics":
            payload = b"# HELP cloud_native_app_up Application availability\n# TYPE cloud_native_app_up gauge\ncloud_native_app_up 1\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        elif self.path == "/":
            self._respond(200, {"service": "cloud-native-platform", "status": "running"})
        else:
            self._respond(404, {"error": "not found"})

    def log_message(self, format: str, *args: object) -> None:
        return


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
