# LifeHub Specification Repository

Dieses Repository enthält die technische Spezifikation des LifeHub-MVP – einer webbasierten Plattform für die Alltagsorganisation von Haushalten. Die vollständige Spezifikation liegt unter `docs/TECHNICAL_SPECIFICATION.md`.

## Inhalt
- Zentraler Überblick über das Funktionsspektrum (Auth, Haushalte, Kalender, Aufgaben, Einkaufslisten, Dashboard)
- Datenbankschema als Referenz für Migrationen/ORM
- API-Endpoints mit Beispiel-Payloads und Antworten
- Empfohlene Projektstrukturen für Backend (Node.js/TypeScript/Express) und Frontend (Next.js)

## Nutzung
Verwende die Spezifikation als Grundlage für Implementierung, Backlog-Planung oder Architektur-Reviews. Ergänzende Notizen oder Änderungen sollten als separate Commits/PRs in den `docs`-Ordner aufgenommen werden.

## Backend-MVP (In-Memory)

Im Ordner `backend/` liegt ein lauffähiger Express/TypeScript-Prototyp des Backends, der die wichtigsten Routen des MVP in In-Memory-Datenstrukturen umsetzt.

### Schnellstart
1. Abhängigkeiten installieren: `cd backend && npm install`
2. Entwicklungsserver starten: `npm run dev`
3. Beispielendpunkte:
   - `POST /auth/register` und `POST /auth/login` für Registrierung/Login
   - `GET /households` und `POST /households` für Haushaltsverwaltung
   - `POST /households/:householdId/events` u.a. für Kalenderereignisse
   - `POST /households/:householdId/tasks` u.a. für Aufgaben
   - `POST /households/:householdId/shopping-lists` u.a. für Einkaufslisten
   - `GET /households/:householdId/dashboard` für die Übersicht

> Hinweis: Der Prototyp nutzt keine persistente Datenbank. Alle Daten liegen nur im Speicher und werden beim Neustart zurückgesetzt. Für eine produktionsreife Version müssen die Services an eine echte Datenbank angebunden werden.
