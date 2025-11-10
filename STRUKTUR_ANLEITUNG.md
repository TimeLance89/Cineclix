# Struktur-Anleitung für NFC Alarm System

## Korrekte Verzeichnisstruktur für Home Assistant

Nach dem Entpacken der ZIP-Datei sollte die Struktur wie folgt aussehen:

### Für HACS Installation

Wenn Sie HACS verwenden, wird die Struktur automatisch korrekt erstellt. Die Integration wird nach:
```
/config/custom_components/nfc_alarm_system/
```
installiert.

### Für Manuelle Installation

#### Schritt 1: ZIP entpacken

Entpacken Sie `nfc_alarm_system.zip`. Sie erhalten einen Ordner `nfc_alarm_system/` mit folgender Struktur:

```
nfc_alarm_system/
├── custom_components/
│   └── nfc_alarm_system/
│       ├── __init__.py
│       ├── alarm_control_panel.py
│       ├── config_flow.py
│       ├── const.py
│       ├── manifest.json
│       ├── services.yaml
│       ├── strings.json
│       └── translations/
│           └── de.json
├── README.md
├── INSTALLATION.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── PROJEKT_STRUKTUR.md
├── BUGFIX_NOTES.md
├── LICENSE
├── hacs.json
└── .gitignore
```

#### Schritt 2: Nur den Integrations-Ordner kopieren

**WICHTIG:** Kopieren Sie NUR den Ordner `custom_components/nfc_alarm_system/` nach Home Assistant!

**Zielverzeichnis in Home Assistant:**
```
/config/custom_components/nfc_alarm_system/
```

#### Schritt 3: Finale Struktur in Home Assistant

Nach dem Kopieren sollte Ihre Home Assistant Installation so aussehen:

```
/config/
├── configuration.yaml
├── automations.yaml
├── scripts.yaml
└── custom_components/
    └── nfc_alarm_system/          ← Die Integration
        ├── __init__.py
        ├── alarm_control_panel.py
        ├── config_flow.py
        ├── const.py
        ├── manifest.json
        ├── services.yaml
        ├── strings.json
        └── translations/
            └── de.json
```

## Wichtige Hinweise

### ✅ Richtig

```
/config/custom_components/nfc_alarm_system/__init__.py
/config/custom_components/nfc_alarm_system/manifest.json
/config/custom_components/nfc_alarm_system/alarm_control_panel.py
...
```

### ❌ Falsch

```
# Nicht den gesamten nfc_alarm_system Ordner kopieren!
/config/custom_components/nfc_alarm_system/custom_components/nfc_alarm_system/...

# Nicht die Dateien direkt in custom_components kopieren!
/config/custom_components/__init__.py
/config/custom_components/manifest.json
...
```

## Dateibeschreibung

### Kern-Dateien (müssen in custom_components/nfc_alarm_system/ sein)

| Datei | Beschreibung | Erforderlich |
|-------|--------------|--------------|
| `__init__.py` | Hauptinitialisierung der Integration | ✅ Ja |
| `manifest.json` | Integration Metadaten | ✅ Ja |
| `alarm_control_panel.py` | Alarm Panel Entity (Hauptlogik) | ✅ Ja |
| `config_flow.py` | UI-Konfigurationsflow | ✅ Ja |
| `const.py` | Konstanten | ✅ Ja |
| `strings.json` | UI-Texte (Englisch) | ✅ Ja |
| `translations/de.json` | Deutsche Übersetzungen | ⚪ Optional |
| `services.yaml` | Service-Definitionen | ⚪ Optional |

### Dokumentations-Dateien (nicht in Home Assistant kopieren)

| Datei | Beschreibung | Verwendung |
|-------|--------------|------------|
| `README.md` | Hauptdokumentation | Zum Lesen |
| `INSTALLATION.md` | Installationsanleitung | Zum Lesen |
| `CHANGELOG.md` | Versionshistorie | Zum Lesen |
| `PROJEKT_STRUKTUR.md` | Technische Übersicht | Zum Lesen |
| `BUGFIX_NOTES.md` | Bugfix-Details | Zum Lesen |
| `CONTRIBUTING.md` | Entwickler-Richtlinien | Zum Lesen |
| `LICENSE` | MIT Lizenz | Zum Lesen |
| `hacs.json` | HACS Konfiguration | Nur für HACS |
| `.gitignore` | Git Ignore | Nur für Git |

## Installations-Checkliste

- [ ] ZIP-Datei heruntergeladen
- [ ] ZIP-Datei entpackt
- [ ] Ordner `custom_components/nfc_alarm_system/` identifiziert
- [ ] Nur den Ordner `nfc_alarm_system/` nach `/config/custom_components/` kopiert
- [ ] Home Assistant neu gestartet
- [ ] Integration über UI hinzugefügt (Einstellungen → Geräte & Dienste)
- [ ] Konfiguration abgeschlossen
- [ ] Funktionstest durchgeführt

## Verifizierung

### Überprüfen Sie die Installation

1. Verbinden Sie sich mit Ihrem Home Assistant System
2. Navigieren Sie zu `/config/custom_components/`
3. Überprüfen Sie, ob der Ordner `nfc_alarm_system/` existiert
4. Überprüfen Sie, ob die Datei `manifest.json` direkt in diesem Ordner liegt

**Terminal-Befehl (SSH):**
```bash
ls -la /config/custom_components/nfc_alarm_system/
```

**Erwartete Ausgabe:**
```
__init__.py
alarm_control_panel.py
config_flow.py
const.py
manifest.json
services.yaml
strings.json
translations/
```

### Logs überprüfen

Nach dem Neustart von Home Assistant:

1. Gehen Sie zu **Einstellungen** → **System** → **Protokolle**
2. Suchen Sie nach "nfc_alarm_system"
3. Es sollten keine Fehler erscheinen

**Erfolgreiche Meldung:**
```
Setting up nfc_alarm_system
```

**Fehler-Meldung (falls falsch installiert):**
```
Unable to find component nfc_alarm_system
```

## Häufige Fehler

### Fehler 1: "Unable to find component"

**Ursache:** Falsche Verzeichnisstruktur

**Lösung:** 
- Überprüfen Sie, ob die Dateien direkt in `/config/custom_components/nfc_alarm_system/` liegen
- Nicht in einem Unterordner!

### Fehler 2: "Invalid manifest"

**Ursache:** `manifest.json` fehlt oder ist beschädigt

**Lösung:**
- Stellen Sie sicher, dass `manifest.json` vorhanden ist
- Überprüfen Sie, ob die Datei gültig ist (JSON-Format)

### Fehler 3: ImportError

**Ursache:** Alte Version oder fehlende Dateien

**Lösung:**
- Verwenden Sie Version 1.0.1 oder höher
- Stellen Sie sicher, dass alle Dateien kopiert wurden

## Support

Bei Problemen:
1. Überprüfen Sie diese Struktur-Anleitung
2. Lesen Sie die INSTALLATION.md
3. Prüfen Sie die Logs in Home Assistant
4. Erstellen Sie ein Issue auf GitHub mit:
   - Ihrer Verzeichnisstruktur (ls -la Ausgabe)
   - Fehlermeldungen aus den Logs
   - Home Assistant Version
