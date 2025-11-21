# LifeHub – Technische Spezifikation (MVP)

## 0. Kurzbeschreibung

**LifeHub** ist eine webbasierte Plattform zur **Alltagsorganisation von Haushalten** (Familien, WGs, Paare, Einzelpersonen).
Kernelemente im MVP:

* Benutzerkonten & Login
* Haushalte mit Mitgliedern (Multi-Tenancy)
* Gemeinsamer Kalender
* Aufgaben / Chores
* Einkaufslisten
* Dashboard mit Übersicht

---

## 1. Rolle & Begriffe

* **User**: Registrierter Benutzer mit Login.
* **Household (Haushalt)**: Gruppe, in der gemeinsam organisiert wird. Ein User kann mehreren Haushalten angehören.
* **Mitglied**: User in einem Haushalt, mit Rolle:

  * `owner` – Besitzer/Administrator des Haushalts
  * `member` – normales Mitglied
* **Event**: Kalenderereignis eines Haushalts.
* **Task**: Aufgabe/To-Do im Haushalt.
* **Shopping List**: Einkaufsliste eines Haushalts.
* **Shopping Item**: Ein Eintrag in einer Einkaufsliste.

---

## 2. Gesamtarchitektur

### 2.1. Komponenten

* **Frontend (Web-App)**

  * Single-Page-App (z.B. React/Next.js)
  * Kommuniziert ausschließlich mit der Backend-API (JSON)

* **Backend (REST-API)**

  * HTTP+JSON, z.B. Node.js + Express oder vergleichbares Framework
  * JWT- oder Session-basierte Authentifizierung
  * Kapselt komplette Geschäftslogik

* **Datenbank**

  * Relational (z.B. PostgreSQL)
  * ORM empfohlen (z.B. Prisma, TypeORM, Sequelize), aber nicht zwingend

### 2.2. Repositories / Struktur (Vorschlag)

```
lifehub/
  backend/
    ... (siehe Abschnitt 6)
  frontend/
    ... (siehe Abschnitt 7)
```

---

## 3. Funktionaler Umfang (MVP)

### 3.1. Authentifizierung & Benutzerverwaltung

**Muss:**

* Registrierung mit E-Mail + Passwort
* Login mit E-Mail + Passwort
* Logout
* Passwort-Reset per E-Mail-Link (Token-basiert)
* Endpoint `/me`, um aktuelle User-Daten abzurufen

### 3.2. Haushalte (Households)

**Muss:**

* User kann Haushalt erstellen (wird `owner`)
* User kann eine Liste seiner Haushalte sehen
* User kann einen Haushalt auswählen („aktiver Haushalt“)
* `owner` kann andere per E-Mail einladen (Invitation mit Token)
* Eingeladene können Einladung annehmen:

  * Wenn bereits Account: Beitritt mit bestehendem Account
  * Wenn noch kein Account: Registrierung + Beitritt

### 3.3. Kalender

**Muss:**

* Events pro Haushalt
* Event-Felder:

  * Titel (Pflicht)
  * Beschreibung (optional)
  * Start-Datum/Zeit
  * End-Datum/Zeit
  * All-Day (optional, bool)
  * Erstellt von (User)
* Liste der Events nach Zeitraum (z.B. `from` / `to` Parameter)
* Erstellen, Bearbeiten, Löschen von Events durch Haushaltsmitglieder

### 3.4. Aufgaben / Tasks

**Muss:**

* Tasks pro Haushalt
* Task-Felder:

  * Titel (Pflicht)
  * Beschreibung (optional)
  * Fälligkeitsdatum (optional)
  * Verantwortlicher (`assigned_to`, optional)
  * Status: `open` oder `done`
  * Erstellt von (User)
* Liste der Tasks mit Filter:

  * nach Status (`open`, `done`)
  * nach Fälligkeitsdatum (von/bis)
* Erstellen, Bearbeiten, Löschen von Tasks
* Status wechseln (`open` ⇄ `done`)

### 3.5. Einkaufslisten

**Muss:**

* Pro Haushalt mehrere Einkaufslisten
* Felder Liste:

  * Name
  * Erstellt von
* Items:

  * Name
  * Menge (String, z.B. „2x“, „500g“)
  * Status `is_done` (true/false)
* Items:

  * Hinzufügen, Umbenennen, Menge ändern
  * Gekauft/ungelöst togglen
  * Löschen

### 3.6. Dashboard

**Muss:**

* Für den aktuell ausgewählten Haushalt:

  * Nächste 5 kommenden Events (z.B. in den nächsten 7 Tagen)
  * Nächste 5 offenen Tasks (nach Fälligkeitsdatum sortiert)
  * 5 offene Shopping-Items der zuletzt aktualisierten Liste

---

## 4. Datenmodell (Datenbank)

### 4.1. Tabellenübersicht

Folgende Tabellen **müssen** existieren:

1. `users`
2. `households`
3. `household_members`
4. `invitations`
5. `calendar_events`
6. `tasks`
7. `shopping_lists`
8. `shopping_list_items`
9. `activity_log` (optional, aber empfohlen)

### 4.2. SQL-Schema (Basis)

Der Programmierer kann das in Migrationen oder ORM-Schema übersetzen.

```sql
CREATE TABLE users (
    id            UUID PRIMARY KEY,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    first_name    TEXT,
    last_name     TEXT,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE households (
    id          UUID PRIMARY KEY,
    name        TEXT NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE household_members (
    id           UUID PRIMARY KEY,
    user_id      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    role         TEXT NOT NULL CHECK (role IN ('owner', 'member')),
    created_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, household_id)
);

CREATE TABLE invitations (
    id           UUID PRIMARY KEY,
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    email        TEXT NOT NULL,
    token        TEXT NOT NULL UNIQUE,
    status       TEXT NOT NULL CHECK (status IN ('pending', 'accepted', 'expired')),
    created_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at   TIMESTAMP NOT NULL
);

CREATE TABLE calendar_events (
    id             UUID PRIMARY KEY,
    household_id   UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    title          TEXT NOT NULL,
    description    TEXT,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime   TIMESTAMP NOT NULL,
    all_day        BOOLEAN NOT NULL DEFAULT FALSE,
    created_by     UUID NOT NULL REFERENCES users(id),
    created_at     TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE tasks (
    id           UUID PRIMARY KEY,
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    title        TEXT NOT NULL,
    description  TEXT,
    due_date     DATE,
    assigned_to  UUID REFERENCES users(id),
    status       TEXT NOT NULL CHECK (status IN ('open', 'done')),
    created_by   UUID NOT NULL REFERENCES users(id),
    created_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE shopping_lists (
    id           UUID PRIMARY KEY,
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    name         TEXT NOT NULL,
    created_by   UUID NOT NULL REFERENCES users(id),
    created_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE shopping_list_items (
    id          UUID PRIMARY KEY,
    list_id     UUID NOT NULL REFERENCES shopping_lists(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    quantity    TEXT,
    is_done     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE activity_log (
    id           UUID PRIMARY KEY,
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    user_id      UUID REFERENCES users(id),
    type         TEXT NOT NULL,
    metadata     JSONB,
    created_at   TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## 5. REST-API-Spezifikation

### 5.1. Allgemein

* Alle Antworten im JSON-Format.
* Authentifizierte Routen erfordern z.B. Header:

  * `Authorization: Bearer <JWT>`
* Fehlerstruktur (Empfehlung):

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Fehlermeldung...",
    "details": {...}
  }
}
```

---

### 5.2. Auth

#### POST `/auth/register`

* **Body:**

```json
{
  "email": "user@example.com",
  "password": "Passwort123!",
  "first_name": "Max",
  "last_name": "Mustermann"
}
```

* **Antwort (201):**

```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "Max",
    "last_name": "Mustermann"
  },
  "token": "JWT_TOKEN"
}
```

* **Logik:**

  * E-Mail muss eindeutig sein
  * Passwort hashen
  * User erstellen
  * Optional direkt einen Standard-Haushalt „Mein Haushalt“ + Mitgliedschaft als `owner` anlegen

#### POST `/auth/login`

* **Body:**

```json
{
  "email": "user@example.com",
  "password": "Passwort123!"
}
```

* **Antwort (200):**

```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "Max",
    "last_name": "Mustermann"
  },
  "token": "JWT_TOKEN"
}
```

#### GET `/auth/me`

* **Header:** Authorization erforderlich
* **Antwort (200):** User-Objekt wie oben.

---

### 5.3. Haushalte

#### GET `/households` (auth)

* Liefert alle Haushalte, in denen der User Mitglied ist.

* **Antwort (200):**

```json
[
  {
    "id": "uuid",
    "name": "Familie Meyer",
    "role": "owner"
  }
]
```

#### POST `/households` (auth)

* **Body:**

```json
{
  "name": "Familie Meyer"
}
```

* **Antwort (201):**

```json
{
  "id": "uuid",
  "name": "Familie Meyer"
}
```

* **Logik:**

  * Haushalt anlegen
  * Current User als `owner` in `household_members` eintragen

#### POST `/households/:householdId/invite` (auth, nur `owner`)

* **Body:**

```json
{
  "email": "gast@example.com"
}
```

* **Antwort (201):**

```json
{
  "id": "uuid",
  "email": "gast@example.com",
  "status": "pending"
}
```

* **Logik:**

  * Eintrag in `invitations` mit Token
  * E-Mail an Empfänger mit Link `https://domain/accept-invite?token=...`

#### POST `/households/accept-invite` (auth oder ohne auth)

* **Body:**

```json
{
  "token": "INVITE_TOKEN"
}
```

* **Fälle:**

  * User ist eingeloggt → wird als `member` in Haushalt hinzugefügt, Invitation `accepted`.
  * User ist nicht eingeloggt → API gibt Info zurück, zu welchem Haushalt die Einladung gehört → Frontend leitet zur Registrierung weiter; nach erfolgreicher Registrierung erneut `/accept-invite` aufrufen.

---

### 5.4. Kalender

#### GET `/households/:householdId/events` (auth)

* **Query-Parameter (optional):**

  * `from` (ISO-Datetime)
  * `to` (ISO-Datetime)

* **Antwort (200):**

```json
[
  {
    "id": "uuid",
    "title": "Arzttermin",
    "description": "Kinderarzt",
    "start_datetime": "2025-11-21T09:00:00Z",
    "end_datetime": "2025-11-21T09:30:00Z",
    "all_day": false
  }
]
```

#### POST `/households/:householdId/events` (auth)

* **Body:**

```json
{
  "title": "Arzttermin",
  "description": "Kinderarzt",
  "start_datetime": "2025-11-21T09:00:00Z",
  "end_datetime": "2025-11-21T09:30:00Z",
  "all_day": false
}
```

* **Antwort (201):** Event-Objekt.

* **Validierung:**

  * `end_datetime` muss nach `start_datetime` liegen.

#### PUT `/households/:householdId/events/:eventId` (auth)

* Body wie POST, Felder ersetzend.

#### DELETE `/households/:householdId/events/:eventId` (auth)

* Löscht Event.

---

### 5.5. Tasks

#### GET `/households/:householdId/tasks` (auth)

* **Query-Parameter (optional):**

  * `status` (open/done)
  * `due_from` (Date)
  * `due_to` (Date)

* **Antwort (200):**

```json
[
  {
    "id": "uuid",
    "title": "Müll rausbringen",
    "description": "",
    "due_date": "2025-11-22",
    "assigned_to": "user-uuid",
    "status": "open"
  }
]
```

#### POST `/households/:householdId/tasks` (auth)

* **Body:**

```json
{
  "title": "Müll rausbringen",
  "description": "",
  "due_date": "2025-11-22",
  "assigned_to": "user-uuid"  // optional
}
```

* **Antwort (201):** Task-Objekt.

#### PATCH `/households/:householdId/tasks/:taskId/status` (auth)

* **Body:**

```json
{
  "status": "done"
}
```

* **Antwort (200):** aktualisierte Task.

#### PUT `/households/:householdId/tasks/:taskId` (auth)

* Vollständiges Update.

#### DELETE `/households/:householdId/tasks/:taskId` (auth)

---

### 5.6. Einkaufslisten

#### GET `/households/:householdId/shopping-lists` (auth)

* **Antwort (200):**

```json
[
  {
    "id": "uuid",
    "name": "Wocheneinkauf"
  }
]
```

#### POST `/households/:householdId/shopping-lists` (auth)

* **Body:**

```json
{
  "name": "Wocheneinkauf"
}
```

* **Antwort (201):** Liste-Objekt.

#### GET `/households/:householdId/shopping-lists/:listId/items` (auth)

* **Antwort (200):**

```json
[
  {
    "id": "uuid",
    "name": "Milch",
    "quantity": "2x",
    "is_done": false
  }
]
```

#### POST `/households/:householdId/shopping-lists/:listId/items` (auth)

* **Body:**

```json
{
  "name": "Milch",
  "quantity": "2x"
}
```

#### PATCH `/households/:householdId/shopping-lists/:listId/items/:itemId` (auth)

* **Body (Teilupdate):**

```json
{
  "name": "Milch (Hafer)",
  "quantity": "1x",
  "is_done": true
}
```

#### DELETE `/households/:householdId/shopping-lists/:listId/items/:itemId` (auth)

---

### 5.7. Dashboard

#### GET `/households/:householdId/dashboard` (auth)

* **Antwort (200):**

```json
{
  "upcoming_events": [
    { "id": "...", "title": "...", "start_datetime": "..." }
  ],
  "open_tasks": [
    { "id": "...", "title": "...", "due_date": "..." }
  ],
  "shopping_items": [
    {
      "list_id": "...",
      "list_name": "Wocheneinkauf",
      "item_id": "...",
      "name": "Milch",
      "quantity": "2x"
    }
  ]
}
```

* **Logik:**

  * Events: nächste X (z.B. 5) innerhalb der nächsten 7 Tage
  * Tasks: `status = open`, sortiert nach `due_date` (NULL zuletzt)
  * Shopping Items: `is_done = false`, aus der zuletzt geänderten Liste oder aus allen Listen (z.B. max. 5 Einträge)

---

## 6. Backend-Projektstruktur (konkret)

Beispiel mit Node.js + TypeScript + Express.

```
backend/
  package.json
  tsconfig.json
  .env.example

  src/
    app.ts
    server.ts

    config/
      env.ts
      db.ts

    middleware/
      authMiddleware.ts
      errorHandler.ts

    modules/
      auth/
        auth.routes.ts
        auth.controller.ts
        auth.service.ts
      users/
        users.routes.ts
        users.controller.ts
        users.service.ts
      households/
        households.routes.ts
        households.controller.ts
        households.service.ts
      calendar/
        calendar.routes.ts
        calendar.controller.ts
        calendar.service.ts
      tasks/
        tasks.routes.ts
        tasks.controller.ts
        tasks.service.ts
      shopping/
        shopping.routes.ts
        shopping.controller.ts
        shopping.service.ts
      dashboard/
        dashboard.routes.ts
        dashboard.controller.ts
        dashboard.service.ts

    utils/
      password.ts      // Hash/Verify
      jwt.ts           // Erstellen/Validieren von JWT
      validation.ts    // Request-Validierung
```

### 6.1. Wichtige Dateien & Aufgaben

* `src/app.ts`

  * Express-App erstellen
  * JSON-Parser, CORS
  * Routen registrieren (`/auth`, `/households`, `/tasks`, …)
  * Error-Handler registrieren

* `src/server.ts`

  * `app` importieren
  * Port aus ENV holen
  * Server starten

* `src/config/env.ts`

  * `process.env` lesen
  * fehlende Variablen validieren (z.B. `JWT_SECRET`, `DATABASE_URL`)

* `src/config/db.ts`

  * Verbindung zur Datenbank (ORM-Client) aufsetzen
  * Exporte für Nutzung in Services

* `src/middleware/authMiddleware.ts`

  * JWT aus `Authorization`-Header parsen
  * Token validieren
  * Falls gültig → `req.user = { id, email }` setzen
  * Sonst 401 zurückgeben bei geschützten Routen

* `src/middleware/errorHandler.ts`

  * Alle Fehler abfangen
  * Standardisierte JSON-Antwort zurückgeben

* `modules/*/*.routes.ts`

  * Definieren der Routen mit HTTP-Methode und Pfad
  * Aufrufe an Controller-Funktionen

* `modules/*/*.controller.ts`

  * Request-Parameter/Body validieren
  * Service-Funktionen aufrufen
  * HTTP-Statuscodes setzen

* `modules/*/*.service.ts`

  * Geschäftslogik
  * DB-Aufrufe
  * Berechtigungsprüfung (Household-Zugehörigkeit)

* `utils/password.ts`

  * Funktionen `hashPassword(plain)` und `verifyPassword(plain, hash)`

* `utils/jwt.ts`

  * `createToken(user)`
  * `verifyToken(token)`

---

## 7. Frontend-Projektstruktur (konkret)

Beispiel mit Next.js (App Router) + TypeScript.

```
frontend/
  package.json
  next.config.mjs
  tsconfig.json
  .env.local.example

  app/
    layout.tsx            // Basislayout, z.B. Header/Footer für öffentliche Seiten
    page.tsx              // Landing / einfache Marketingseite

    auth/
      login/page.tsx
      register/page.tsx

    app/                  // geschützter Bereich (nach Login)
      layout.tsx          // Layout mit Sidebar, Topbar
      page.tsx            // Dashboard des aktiven Haushalts

      households/
        page.tsx          // Übersicht, Haushalt auswählen, neuen Haushalt anlegen

      calendar/
        page.tsx          // Monats-/Wochenansicht

      tasks/
        page.tsx          // Tasks-Liste, Filter

      shopping/
        page.tsx          // Einkaufslisten & Items

      settings/
        page.tsx          // Profil (Name), evtl. Sprache

  components/
    layout/
      Sidebar.tsx
      Topbar.tsx
    calendar/
      CalendarView.tsx
      EventModal.tsx
    tasks/
      TaskList.tsx
      TaskItem.tsx
      TaskForm.tsx
    shopping/
      ShoppingList.tsx
      ShoppingListItem.tsx
    common/
      Button.tsx
      Input.tsx
      Select.tsx
      Modal.tsx
      Spinner.tsx

  lib/
    api.ts        // Wrapper um fetch/axios, Basis-URL, Token-Header
    auth.ts       // Login/Logout, currentUser holen
    types.ts      // TypeScript-Interfaces für User, Household, Task, Event, etc.

  styles/
    globals.css   // Grundstyles (oder Tailwind-Konfig)
```

### 7.1. Wichtige Screens (Feinbeschreibung)

**1. Login (`/auth/login`)**

* Formular: E-Mail, Passwort
* Button „Einloggen“
* Bei Erfolg: Token speichern, Redirect auf `/app`

**2. Registrierung (`/auth/register`)**

* Formular: E-Mail, Passwort, Vorname, Nachname
* Bei Erfolg:

  * Account anlegen
  * Standard-Haushalt erstellen oder Einladung annehmen
  * Redirect auf `/app`

**3. Haushalts-Auswahl (`/app/households`)**

* Liste aller Haushalte, in denen User Mitglied ist
* Buttons:

  * „Haushalt öffnen“
  * „Neuen Haushalt erstellen“ (Modal mit Name)

**4. Dashboard (`/app`)**

* Zeigt Daten von **aktivem Haushalt**:

  * Widget „Nächste Termine“
  * Widget „Offene Aufgaben“
  * Widget „Einkaufsliste“

**5. Kalender (`/app/calendar`)**

* Kalenderansicht (z.B. simplifizierte Wochen-/Monatsansicht)
* Klick auf Tag → Eventliste
* Button „+ Event“ → Modal mit Feldern zu Event
* CRUD über API

**6. Tasks (`/app/tasks`)**

* Filterleiste: `Status` (open/done), `Fällig ab/bis`
* Liste der Tasks
* Checkbox für Status (toggle open/done)
* Button „Neue Aufgabe“ (Modal)

**7. Einkaufslisten (`/app/shopping`)**

* Links: Liste der Shopping-Listen
* Rechts: Items der ausgewählten Liste
* Schnell-Input für neues Item (Name + Menge)
* Checkbox für `is_done`

---

## 8. Nicht-funktionale Anforderungen

* **Sicherheit**

  * Passwörter **niemals** im Klartext speichern (bcrypt/argon2)
  * JWT/Session sicher handhaben
  * Zugang zu Ressourcen nur für Mitglieder des jeweiligen Haushalts

* **Performance**

  * MVP muss keine extreme Skalierung haben
  * Pagination bei großen Listen optional, aber vorbereiten

* **Codequalität**

  * Typisierung (z.B. TypeScript) dringend empfohlen
  * Fehlerbehandlung zentral (Backend Error-Handler)
  * Logging für Fehler (mind. auf Serverseite)

* **Konfiguration**

  * `.env` für Secrets:

    * `DATABASE_URL`
    * `JWT_SECRET`
    * `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD` (für E-Mails, optional zuerst)
