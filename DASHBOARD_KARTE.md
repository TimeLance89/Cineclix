# Dashboard-Karte für NFC Alarm System

Die NFC Alarm System Integration enthält eine **benutzerdefinierte Dashboard-Karte** mit professionellem Design und umfangreichen Funktionen.

## Features der Dashboard-Karte

### 🎨 Visuelles Design
- **Modernes Card-Design** im Home Assistant Stil
- **Alarm-Warnung** bei Auslösung (rotes Banner mit Puls-Animation)
- **Farbcodierte Statusanzeigen** für Scharf/Ausgelöst
- **Responsive Design** für Desktop, Tablet und Mobile
- **Dark Mode Unterstützung** (automatisch)

##### 📊 Statusanzeigen
- **Scharf-Status** mit Icon (Schild/Häkchen)
- **Ausgelöst-Status** mit Icon (Sirene/Häkchen)
- **Ja/Nein Anzeige** für jeden Status

### 🏛️ Interaktive Buttons (4 Buttons)
- **Scharf (sofort)** - Alarm sofort scharfschalten (nur wenn unscharf)
- **Unscharf** - Alarm deaktivieren (nur wenn scharf/ausgelöst)
- **Alarm testen** - Testalarm auslösen (immer verfügbar)
- **Alarm quittieren** - Alarm bestätigen und deaktivieren (nur wenn ausgelöst)
- Buttons werden automatisch aktiviert/deaktiviert je nach Status

### 📝 Sensoren & Licht
- **Echtzeit-Anzeige** aller konfigurierten Sensoren
- **Status-Icons** (Rot = Aktiv, Grün = Inaktiv)
- **Indikator-Lichter** mit An/Aus Status
- **Automatische Aktualisierung** bei Zustandsänderungen

### 📈 Logbook/Verlauf
- **Letzte 6 Stunden** Ereignisse
- **Alle Entities** (Alarm + Sensoren)
- **Zeitstempel** mit relativer Anzeige
- **Scrollbare Liste** (max. 20 Einträge)
- **Automatisches Laden** aus Home Assistant History

## Installation der Dashboard-Karte

### Schritt 1: Datei kopieren

Die Datei `nfc-alarm-card.js` muss in das `www` Verzeichnis von Home Assistant kopiert werden:

```
/config/www/nfc-alarm-card.js
```

**Vollständiger Pfad:**
```
/config/
├── configuration.yaml
├── custom_components/
│   └── nfc_alarm_system/
└── www/                        ← Hier
    └── nfc-alarm-card.js      ← Die Karte
```

**Falls der `www` Ordner nicht existiert:**
```bash
mkdir /config/www
```

### Schritt 2: Ressource in Home Assistant registrieren

1. Öffnen Sie Home Assistant
2. Gehen Sie zu **Einstellungen** → **Dashboards**
3. Klicken Sie auf die **drei Punkte** (⋮) oben rechts
4. Wählen Sie **Ressourcen**
5. Klicken Sie auf **+ Ressource hinzufügen**
6. Geben Sie ein:
   - **URL:** `/local/nfc-alarm-card.js`
   - **Ressourcentyp:** `JavaScript-Modul`
7. Klicken Sie auf **Erstellen**

### Schritt 3: Browser-Cache leeren

**Wichtig:** Nach dem Hinzufügen der Ressource:
1. Drücken Sie `Strg + Shift + R` (Windows/Linux)
2. Oder `Cmd + Shift + R` (Mac)
3. Oder leeren Sie den Browser-Cache manuell

### Schritt 4: Karte zum Dashboard hinzufügen

#### Methode 1: Über die UI (Visueller Editor)

1. Gehen Sie zu Ihrem Dashboard
2. Klicken Sie auf **Bearbeiten** (oben rechts)
3. Klicken Sie auf **+ Karte hinzufügen**
4. Scrollen Sie nach unten zu **Benutzerdefiniert: NFC Alarm Card**
5. Wählen Sie die Karte aus
6. Konfigurieren Sie die Karte (siehe unten)
7. Klicken Sie auf **Speichern**

#### Methode 2: Über YAML

1. Gehen Sie zu Ihrem Dashboard
2. Klicken Sie auf **Bearbeiten**
3. Klicken Sie auf die **drei Punkte** (⋮) oben rechts
4. Wählen Sie **Roher Konfigurationseditor**
5. Fügen Sie folgendes hinzu:

```yaml
type: custom:nfc-alarm-card
entity: alarm_control_panel.nfc_alarmsystem
name: Mein Alarmsystem
```

## Konfiguration

### Basis-Konfiguration

```yaml
type: custom:nfc-alarm-card
entity: alarm_control_panel.nfc_alarmsystem
name: NFC Alarmsystem
```

### Parameter

| Parameter | Typ | Erforderlich | Standard | Beschreibung |
|-----------|-----|--------------|----------|--------------|
| `type` | string | ✅ Ja | - | Muss `custom:nfc-alarm-card` sein |
| `entity` | string | ✅ Ja | - | Entity-ID des Alarmsystems |
| `name` | string | ⚪ Nein | "NFC Alarmsystem" | Angezeigter Name der Karte |

### Beispiel-Konfigurationen

#### Minimal
```yaml
type: custom:nfc-alarm-card
entity: alarm_control_panel.nfc_alarmsystem
```

#### Mit eigenem Namen
```yaml
type: custom:nfc-alarm-card
entity: alarm_control_panel.nfc_alarmsystem
name: Hausalarm EG
```

#### Mehrere Alarmsysteme
```yaml
# Karte 1
type: custom:nfc-alarm-card
entity: alarm_control_panel.alarm_erdgeschoss
name: Alarm Erdgeschoss

# Karte 2
type: custom:nfc-alarm-card
entity: alarm_control_panel.alarm_obergeschoss
name: Alarm Obergeschoss
```

## Verwendung

### Status-Anzeigen

Die Karte zeigt den aktuellen Status mit farbcodierten Badges:

- 🟢 **Grün (Unscharf)**: Alarm ist deaktiviert
- 🟡 **Gelb (Wird scharf...)**: Exit Delay läuft
- 🔵 **Blau (Scharf)**: Alarm ist aktiviert
- 🟠 **Orange (Eintrittsverzögerung)**: Entry Delay läuft
- 🔴 **Rot (ALARM!)**: Alarm wurde ausgelöst (pulsierend)

### Buttons

#### Scharfschalten
- Aktiviert den Alarm
- Nur verfügbar wenn Status = "Unscharf"
- Startet die Austrittsverzögerung

#### Unscharfschalten
- Deaktiviert den Alarm
- Nur verfügbar wenn Status ≠ "Unscharf"
- Stoppt alle laufenden Prozesse

#### Test
- Sendet eine Test-Benachrichtigung
- Immer verfügbar
- Zum Testen der Funktionalität

### Verlauf

Der Verlauf zeigt die letzten 10 Zustandsänderungen:
- **Farbcodierte Balken** am linken Rand
- **Zustandsname** (z.B. "Scharf", "Unscharf")
- **Zeitstempel** (relativ: "vor 5 Min." oder absolut: "10.11. 14:30")

## Fehlerbehebung

### Karte erscheint nicht in der Liste

**Lösung:**
1. Überprüfen Sie, ob die Datei in `/config/www/` liegt
2. Überprüfen Sie die Ressourcen-URL: `/local/nfc-alarm-card.js`
3. Leeren Sie den Browser-Cache (Strg + Shift + R)
4. Starten Sie Home Assistant neu

### "Custom element doesn't exist: nfc-alarm-card"

**Lösung:**
1. Überprüfen Sie, ob die Ressource korrekt registriert ist
2. Typ muss "JavaScript-Modul" sein
3. Leeren Sie den Browser-Cache
4. Öffnen Sie die Browser-Konsole (F12) und suchen Sie nach Fehlern

### Karte zeigt "Entity not found"

**Lösung:**
1. Überprüfen Sie die Entity-ID in der Konfiguration
2. Stellen Sie sicher, dass die Integration installiert ist
3. Überprüfen Sie unter **Entwicklerwerkzeuge** → **Zustände**, ob die Entity existiert

### Buttons funktionieren nicht

**Lösung:**
1. Überprüfen Sie die Browser-Konsole (F12) auf JavaScript-Fehler
2. Stellen Sie sicher, dass die Entity-ID korrekt ist
3. Testen Sie die Services manuell unter **Entwicklerwerkzeuge** → **Dienste**

### Verlauf wird nicht angezeigt

**Lösung:**
- Der Verlauf wird erst nach Zustandsänderungen gefüllt
- Lösen Sie eine Zustandsänderung aus (Scharf/Unscharf schalten)
- Der Verlauf wird im Browser-Speicher gehalten (verschwindet bei Neuladen)

## Anpassungen

### Farben ändern

Die Karte verwendet CSS-Variablen von Home Assistant. Sie können diese in Ihrem Theme überschreiben:

```yaml
# In Ihrer theme.yaml
my-theme:
  # Primärfarbe für Akzente
  primary-color: "#2196f3"
  
  # Hintergrundfarben
  card-background-color: "#ffffff"
  secondary-background-color: "#f5f5f5"
  
  # Textfarben
  primary-text-color: "#212121"
  secondary-text-color: "#727272"
```

### Maximale Verlaufseinträge ändern

Bearbeiten Sie die Datei `nfc-alarm-card.js`:

```javascript
// Zeile 6
this._maxHistory = 10;  // Ändern Sie diese Zahl
```

## Beispiel-Dashboard

### Vollständiges Dashboard-Layout

```yaml
views:
  - title: Sicherheit
    path: security
    cards:
      - type: custom:nfc-alarm-card
        entity: alarm_control_panel.nfc_alarmsystem
        name: Hausalarm
      
      - type: entities
        title: Sensoren
        entities:
          - binary_sensor.haustuer
          - binary_sensor.fenster_wohnzimmer
          - binary_sensor.fenster_schlafzimmer
      
      - type: history-graph
        title: Alarm-Historie
        entities:
          - alarm_control_panel.nfc_alarmsystem
        hours_to_show: 24
```

## Updates

### Karte aktualisieren

1. Ersetzen Sie die Datei `/config/www/nfc-alarm-card.js` mit der neuen Version
2. Leeren Sie den Browser-Cache (Strg + Shift + R)
3. Die Karte wird automatisch neu geladen

### Version prüfen

Öffnen Sie die Browser-Konsole (F12) nach dem Laden der Seite. Sie sollten sehen:

```
 NFC-ALARM-CARD  Version 1.0.1
```

## Support

Bei Problemen mit der Dashboard-Karte:
1. Überprüfen Sie die Browser-Konsole (F12) auf Fehler
2. Überprüfen Sie die Home Assistant Logs
3. Stellen Sie sicher, dass die Ressource korrekt registriert ist
4. Erstellen Sie ein Issue auf GitHub mit:
   - Browser und Version
   - Home Assistant Version
   - Fehlermeldungen aus der Konsole
   - Screenshot der Karte
