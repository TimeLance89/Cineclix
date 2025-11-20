import argparse
import json
import os
import random
import threading
import uuid
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingTCPServer

ROOT = Path(__file__).parent

ROLES = [
    "Scout",
    "Hacker",
    "Medic",
    "Schütze",
]

ENCOUNTERS = [
    "Signal Storm",
    "Arc Spire",
    "Roving Drones",
    "Scrapper Squad",
    "Sky Harvester",
]

LOOT_TABLE = [
    {"name": "Supply Cache", "rarity": "Common", "effect": "+1 Supplies"},
    {"name": "Data Drive", "rarity": "Uncommon", "effect": "+1 Hack"},
    {"name": "Arc Battery", "rarity": "Rare", "effect": "+10 Moral"},
    {"name": "Exo-Armor", "rarity": "Epic", "effect": "-10 Damage"},
    {"name": "Anthem Core", "rarity": "Legendary", "effect": "+1 Loot Quality"},
]

sessions = {}
sessions_lock = threading.Lock()


def short_id() -> str:
    return uuid.uuid4().hex[:8]


def new_session() -> dict:
    session_id = short_id()
    encounter = random.choice(ENCOUNTERS)
    session = {
        "id": session_id,
        "round": 1,
        "threat": random.randint(1, 3),
        "morale": 100,
        "supplies": 3,
        "status": "active",
        "current_encounter": encounter,
        "players": {},
        "loot": [],
        "log": [f"Session {session_id} deployed at drop-ball. Encounter: {encounter}"],
    }
    sessions[session_id] = session
    return session


def join_session(name: str | None) -> tuple[str, str, dict]:
    display_name = name or f"Raider-{random.randint(100,999)}"
    with sessions_lock:
        target = None
        for sess in sessions.values():
            if sess["status"] == "active" and len(sess["players"]) < 4:
                target = sess
                break
        if target is None:
            target = new_session()
        player_id = short_id()
        role = ROLES[len(target["players"]) % len(ROLES)]
        target["players"][player_id] = {
            "id": player_id,
            "name": display_name,
            "role": role,
            "hp": 100,
            "morale": 100,
            "loot_bonus": random.choice(["+1 Recon", "+1 Hack", "+1 Med", "+1 Strike"]),
        }
        target["log"].append(f"{display_name} joined as {role}. Squad size: {len(target['players'])}.")
        return target["id"], player_id, target


def clamp(value: int, min_v: int, max_v: int) -> int:
    return max(min_v, min(max_v, value))


def resolve_action(session: dict, player_id: str, action: str) -> dict:
    player = session["players"].get(player_id)
    if not player:
        session["log"].append("Unbekannter Spieler; Aktion verworfen.")
        return session

    roll = random.random()
    session["round"] += 1

    if session["status"] != "active":
        session["log"].append(f"{player['name']} tried {action}, but session is {session['status']}.")
        return session

    if action == "scout":
        if roll > 0.3:
            session["current_encounter"] = random.choice(ENCOUNTERS)
            session["log"].append(f"{player['name']} scouts ahead: {session['current_encounter']} detected.")
        else:
            session["threat"] = clamp(session["threat"] + 1, 1, 4)
            session["log"].append(f"{player['name']} triggers patrols. Threat rises to {session['threat']}.")

    elif action == "strike":
        damage = random.randint(5, 25)
        player["hp"] = clamp(player["hp"] - damage, 0, 100)
        if roll > 0.4:
            session["threat"] = clamp(session["threat"] - 1, 1, 4)
            session["log"].append(f"{player['name']} lands a strike. Threat {session['threat']} (took {damage} dmg).")
        else:
            session["morale"] = clamp(session["morale"] - 10, 0, 120)
            session["log"].append(f"{player['name']} suppressed but failed. Morale {session['morale']} (took {damage} dmg).")

    elif action == "hack":
        if roll > 0.35:
            session["threat"] = clamp(session["threat"] - 1, 1, 4)
            session["supplies"] = clamp(session["supplies"] + 1, 0, 8)
            session["log"].append(f"{player['name']} hacks an Arc node. Threat {session['threat']}, supplies {session['supplies']}.")
        else:
            session["morale"] = clamp(session["morale"] - 8, 0, 120)
            session["log"].append(f"{player['name']} fails the hack. Morale {session['morale']}.")

    elif action == "loot":
        item = random.choices(LOOT_TABLE, weights=[50, 30, 12, 6, 2])[0]
        session["loot"].append(item)
        session["log"].append(f"{player['name']} loots: {item['name']} ({item['rarity']}).")
        if item["rarity"] in {"Legendary", "Epic"}:
            session["morale"] = clamp(session["morale"] + 5, 0, 120)

    elif action == "rest":
        heal = random.randint(8, 18)
        player["hp"] = clamp(player["hp"] + heal, 0, 100)
        session["morale"] = clamp(session["morale"] + 5, 0, 120)
        session["log"].append(f"{player['name']} stabilizes. +{heal} HP, morale {session['morale']}.")

    elif action == "extract":
        session["status"] = "extracted"
        session["log"].append(f"{player['name']} calls extraction. Raid ends with {len(session['loot'])} loot items.")

    # Escalation check
    if session["morale"] <= 0 or all(p["hp"] <= 0 for p in session["players"].values()):
        session["status"] = "wiped"
        session["log"].append("Squad wiped. Arc swarm overwhelms the team.")

    session["log"] = session["log"][-200:]
    return session


class RaidHandler(SimpleHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = HTTPStatus.OK) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith("/api/state"):
            query = self.path.split("?", 1)[-1] if "?" in self.path else ""
            params = dict(part.split("=") for part in query.split("&") if "=" in part)
            session_id = params.get("session_id")
            with sessions_lock:
                session = sessions.get(session_id) if session_id else None
                if session is None:
                    self._send_json({"error": "session not found"}, status=HTTPStatus.NOT_FOUND)
                else:
                    self._send_json({"state": session})
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/matchmake":
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            body = json.loads(raw.decode("utf-8")) if raw else {}
            name = body.get("name")
            with sessions_lock:
                session_id, player_id, session = join_session(name)
            self._send_json({
                "session_id": session_id,
                "player_id": player_id,
                "player_name": session["players"][player_id]["name"],
                "state": session,
            })
            return

        if self.path == "/api/action":
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            body = json.loads(raw.decode("utf-8")) if raw else {}
            session_id = body.get("session_id")
            player_id = body.get("player_id")
            action = body.get("action")
            if not session_id or not player_id or not action:
                self._send_json({"error": "missing fields"}, status=HTTPStatus.BAD_REQUEST)
                return
            with sessions_lock:
                session = sessions.get(session_id)
                if session is None:
                    self._send_json({"error": "session not found"}, status=HTTPStatus.NOT_FOUND)
                    return
                updated = resolve_action(session, player_id, action)
            self._send_json({"state": updated})
            return

        self._send_json({"error": "unknown route"}, status=HTTPStatus.NOT_FOUND)


def run_server(host: str, port: int) -> None:
    os.chdir(ROOT)
    with ThreadingTCPServer((host, port), lambda *args, **kwargs: RaidHandler(*args, directory=str(ROOT), **kwargs)) as httpd:
        print(f"Serving on http://{host}:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arc Raiders text raid server")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host")
    parser.add_argument("--port", type=int, default=8000, help="Port")
    args = parser.parse_args()
    run_server(args.host, args.port)
