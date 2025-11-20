import argparse
import json
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

SESSIONS: dict[str, dict] = {}
ROOT = Path(__file__).parent


def _current_ts() -> int:
    return int(time.time() * 1000)


class RaidHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _send_json(self, payload: dict, status: int = 200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _parse_session_id(self):
        parsed = urlparse(self.path)
        parts = parsed.path.rstrip("/").split("/")
        if len(parts) == 4 and parts[:3] == ["", "api", "session"]:
            return parts[3]
        return None

    def do_GET(self):
        session_id = self._parse_session_id()
        if session_id:
            state = SESSIONS.get(session_id)
            if not state:
                self._send_json({"error": "unknown session"}, status=404)
                return
            self._send_json({"sessionId": session_id, "state": state})
            return

        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        session_id = self._parse_session_id()
        if not session_id:
            self._send_json({"error": "invalid endpoint"}, status=404)
            return

        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json({"error": "invalid json"}, status=400)
            return

        state = payload.get("state") or payload
        state.setdefault("updatedAt", _current_ts())
        SESSIONS[session_id] = state
        self._send_json({"ok": True, "sessionId": session_id, "updatedAt": state["updatedAt"]})


def main():
    parser = argparse.ArgumentParser(description="Arc Raiders Text-Raid LAN Server")
    parser.add_argument("--host", default="127.0.0.1", help="Bind-Adresse, z. B. 0.0.0.0 für LAN")
    parser.add_argument("--port", type=int, default=8000, help="Port für HTTP & API")
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), RaidHandler)
    print(f"Arc Raiders LAN-Server läuft auf http://{args.host}:{args.port}")
    print("API: POST/GET /api/session/<sessionId> | Static Files: index.html, README.md")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer beendet.")


if __name__ == "__main__":
    main()
