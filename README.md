# Arc Raiders: Browser-Koop-Prototyp

Ein textbasiertes Koop-Loot-Spiel im Browser, inspiriert von der Stimmung und dem Loop von **Arc Raiders**. Das Spiel läuft rein clientseitig in HTML/JS und bietet gemeinsames Spielen über mehrere Tabs/Fenster derselben Domain (per `BroadcastChannel`) sowie einfache Session-Links für asynchrone Runden.

## Konzeptüberblick
- **Setting:** Widerstandstrupp gegen einfallende Maschinen („Arcs“). Klare Bedrohungslagen, wechselnde Wetter- und Signalbedingungen.
- **Loop:**
  1. **Scouten** – Lage erkunden, neue Bedrohungen oder Schwachstellen entdecken.
  2. **Koordinieren** – Unterdrücken, Hacken oder Versorgung sichern, um Moral zu halten.
  3. **Looten** – Kisten nach Encountern öffnen; Qualität hängt von Bedrohungsstufe & Team-Moral ab.
  4. **Reset** – Neues Ziel, Bedrohungsboard auffüllen, weiterziehen.
- **Rollen:** Späher, Hacker, Medic, Schütze; jede Rolle triggert eigene zufällige Events.
- **Bedrohungen:** Stufen 1–4; bringen Moral-Druck, benötigen koordinierte Aktionen.
- **Loot:** Seltenheitsstufen (Gewöhnlich → Legendär). Loot beeinflusst Aktionen (z. B. +Scout, +Hack).
- **Gemeinsam spielen:**
  - **Live-Koop:** Mehrere Tabs/Fenster nutzen denselben Host → Status-Sync via BroadcastChannel.
  - **Session-Link:** Aktuellen Status als Link kopieren; andere Spieler können diesen einfügen, um dieselbe Session zu laden.

## Spiel starten
1. `python -m http.server 8000` im Repo-Root starten.
2. Im Browser `http://localhost:8000` öffnen.
3. Squad aufstellen, Bedrohungen ziehen und Aktionen ausführen. Über „Status teilen“ kann der aktuelle Zustand synchronisiert werden.

## Steuerung & Hinweise
- Aktionen würfeln intern mit simplen Erfolgswahrscheinlichkeiten; Ergebnisse werden im Log dokumentiert.
- Moral und Supplies beeinflussen Loot-Qualität und Bedrohungsdruck.
- Das Spiel ist textbasiert und UI-first in Boxen aufgebaut, damit es auch ohne Grafik funktioniert.

## Entwicklung
- Kein Build-Setup nötig; Vanilla HTML/CSS/JS.
- State wird unter `localStorage['arc-raiders-session']` abgelegt und per `BroadcastChannel` synchronisiert.

