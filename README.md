# LifeHub – digitales Alltags-Cockpit

Beta-taugliches Frontend für **LifeHub**, die zentrale Plattform für Familien, Paare, WGs und Einzelpersonen. Kalender, Aufgaben, Einkaufslisten, Nachrichten und Haushaltsbuch laufen in einer einzigen Web-App zusammen.

## Features
- Dashboard mit Quick Actions, Abschnitt-Navigation und responsivem Layout
- Kalenderverwaltung mit Terminerstellung, Personen und Konfliktcheck-Platzhalter
- Aufgabenverwaltung mit Prioritäten, Fälligkeitsdaten und Statuswechsel
- Einkaufsliste pro Laden mit Abhak-Status
- Haushaltsbuch mit Kategorisierung und Monats-Summe
- Nachrichtenboard mit Pinn-Funktion und Roadmap, die Tasks erzeugen kann
- Clientseitige Speicherung via `localStorage` – keine Build-Tools nötig

## Nutzung
1. Repository klonen oder herunterladen.
2. `index.html` im Browser öffnen. Es wird kein zusätzlicher Server oder Build-Prozess benötigt.
3. Neue Einträge über die Formulare hinzufügen; Daten werden automatisch im Browser gespeichert.
4. Roadmap-Punkte lassen sich direkt als Aufgaben übernehmen, um die nächsten Sprints zu planen.

## Nächste Schritte
- Echte Authentifizierung & Rollenrechte
- Backend/Persistence (z. B. Supabase/Firebase) anbinden
- Push-Benachrichtigungen, PWA/Offline und Kalender-ICS-Import fertigstellen
- Komponenten ggf. nach React/Vite migrieren
