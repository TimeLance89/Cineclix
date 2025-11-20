# Arc Raiders: Textbasierter Browser-Koop

Ein kooperatives Loot-/Extraction-Spiel, das den Ablauf von **Arc Raiders** als textbasierte Browser-Erfahrung nachbildet. Spieler verbinden sich über den Browser, werden automatisch in eine laufende Runde gesteckt und interagieren über klare Status-Boxen und Aktionen.

## Konzept und Loop
- **Sofort losspielen:** Beim Aufruf der Seite wird automatisch eine Sitzung gesucht/erstellt. Keine Lobby-Klicks nötig – wie bei Arc Raiders startet die Operation nahtlos.
- **Arc-ähnlicher Ablauf:**
  1. **Drop & Recon:** Spieler landen, scouten Bedrohungen und legen Rollen fest.
  2. **Engagement:** Strike-/Hack-/Suppress-Aktionen drücken die Bedrohungsstufe, Moral und Supplies.
  3. **Loot:** Nach Encountern werden Drop- und Arc-Kisten geöffnet; Qualität hängt von Bedrohung/Moral ab.
  4. **Extraction:** Bei kritischer Moral oder erfolgreichem Loot entscheidet das Squad über Extraktion.
- **Rollen & Teamplay:** Späher, Hacker, Medic, Schütze – jede Rolle hat eigene Boni auf Aktionen.
- **Bedrohungen:** Mehrstufige Arcs (1–4). Höhere Stufen erhöhen Risiko für Schaden und Moralverlust.
- **Text-UI:** Panels/Boxen für Status (Squad, Bedrohung, Loot, Log). Aktionen erfolgen über Buttons/Formulare, damit das Spiel komplett ohne Grafik spielbar ist.

## Features
- **Automatisches Matchmaking:** Der Server bündelt eingehende Spieler sofort in Sessions (max. 4). Die Runde beginnt automatisch, sobald ein Spieler verbunden ist.
- **Synchrones Play:** Gemeinsamer State pro Session; alle Aktionen laufen serverseitig und werden an alle Clients zurückgegeben.
- **Fallback auf Browser-Only:** Falls der Server nicht erreichbar ist, zeigt die UI einen Hinweis und erlaubt ein Solo-Probelauf (nicht synchronisiert).
- **Ohne Build-Tooling:** Nur HTML/CSS/JS und ein kleiner Python-Server.

## Schnellstart
1. Optional: Python-Umgebung aktivieren.
2. Server starten:
   ```bash
   python server.py --host 0.0.0.0 --port 8000
   ```
3. Im Browser `http://localhost:8000` öffnen. Jeder weitere Spieler öffnet denselben Link; der Server steckt alle automatisch in Sessions.

## Steuerung
- **Aktionen:** Scout, Strike, Hack, Loot, Rest, Extract – jeweils mit serverseitigem Würfeln/Risiko.
- **Log:** Zeigt den gesamten Rundenverlauf; neue Einträge erscheinen automatisch beim Polling.
- **Status-Boxen:**
  - **Session:** ID, Runde, Bedrohung, Moral, Supplies.
  - **Squad:** Rollen & Vitalwerte.
  - **Loot:** Aktive Funde und deren Qualität.

## Entwicklungshinweise
- Kein Build-Step; nur statische Dateien.
- State-Management im Server unter `sessions` (In-Memory). Wenn du persistieren willst, ersetze den Store durch eine Datei-/Redis-Schicht.
- Actions/Balance liegen in `server.py` in `resolve_action` und den Loot-/Encounter-Tabellen.

