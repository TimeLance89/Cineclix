# Changelog - HA Alarm Pro v0.7.0

## Automatisches Dashboard-System

Diese Version implementiert ein vollautomatisches Dashboard-System, das die konfigurierten Sensoren und Lichter dynamisch aus der Integration übernimmt. **Keine manuelle YAML-Bearbeitung mehr erforderlich!**

## Hauptfunktionen

### Dynamischer Dashboard-Generator

Die Integration generiert jetzt automatisch eine vollständige Dashboard-Konfiguration basierend auf deinen Einstellungen. Alle konfigurierten Sensoren, Lichter und andere Entitäten werden automatisch in das Dashboard integriert.

**Wie es funktioniert:**

Nach der Konfiguration der Integration kannst du mit einem einzigen Service-Aufruf ein fertiges Dashboard-YAML erhalten, das exakt auf deine Konfiguration zugeschnitten ist. Die Integration liest deine konfigurierten Eingangssensoren und Indikator-Lichter aus und erstellt automatisch eine Lovelace-Konfiguration mit allen notwendigen Karten und Buttons.

### Neuer Service: get_dashboard_yaml

Der Service `ha_alarm_pro.get_dashboard_yaml` generiert das Dashboard-YAML und zeigt es als Benachrichtigung an. Du musst nur noch den Code kopieren und in dein Dashboard einfügen.

**Verwendung:**
```yaml
service: ha_alarm_pro.get_dashboard_yaml
```

Nach dem Aufruf erscheint eine Benachrichtigung mit dem vollständigen YAML-Code, der alle deine konfigurierten Entitäten enthält.

### Dashboard-Konfiguration-Sensor

Ein neuer Sensor `sensor.ha_alarm_pro_dashboard_config` wird automatisch erstellt und bietet:
- Aktuellen Status des Dashboard-Generators
- Vollständiges Dashboard-YAML als Attribut `config_yaml`
- JSON-Konfiguration als Attribut `dashboard_config`
- Automatische Aktualisierung bei Konfigurationsänderungen

**Zugriff über Entwicklerwerkzeuge:**
1. Gehe zu Entwicklerwerkzeuge → Zustände
2. Suche nach `sensor.ha_alarm_pro_dashboard_config`
3. Das Attribut `config_yaml` enthält das fertige Dashboard-YAML

### Automatische Entitäts-Integration

Das generierte Dashboard enthält automatisch:

**Eingangssensoren:**
Alle in der Integration konfigurierten Sensoren werden automatisch in der Sektion "Sensoren & Indikatoren" angezeigt. Die Entity-IDs werden in lesbare Namen konvertiert (z.B. `binary_sensor.aqara_vibration_sensor_t1_belegung` wird zu "Aqara Vibration Sensor T1 Belegung").

**Indikator-Lichter:**
Alle konfigurierten Lichter erscheinen ebenfalls automatisch in der Sensoren-Sektion mit einem Divider zur Trennung von den Sensoren.

**Logbook-Integration:**
Das Logbook wird automatisch mit allen konfigurierten Sensoren befüllt, sodass die Historie aller relevanten Ereignisse angezeigt wird.

**Steuerungsbuttons:**
Alle sechs Steuerungsbuttons (Scharf Abwesend/Zuhause, Unscharf, Alarm testen, Alarm quittieren, Sound testen) sind vorkonfiguriert und sofort funktionsfähig.

## Technische Implementierung

### Neue Dateien

**lovelace.py:**
Enthält den Dashboard-Generator mit Funktionen zum Erstellen aller Dashboard-Komponenten:
- `generate_dashboard_config()` - Hauptfunktion zur Dashboard-Generierung
- `_build_alarm_warning()` - Conditional Card für Alarm-Warnung
- `_build_status_card()` - Status-Anzeige mit Attributen
- `_build_control_buttons()` - Alle Steuerungsbuttons
- `_build_sensors_card()` - Dynamische Sensoren- und Lichter-Karte
- `_build_logbook()` - Logbook mit konfigurierten Entitäten
- `_get_friendly_name()` - Konvertierung von Entity-IDs zu lesbaren Namen

**sensor.py:**
Implementiert den Dashboard-Konfiguration-Sensor:
- `AlarmProDashboardSensor` - Sensor-Entity mit Dashboard-Konfiguration
- Stellt YAML und JSON als Attribute bereit
- Aktualisiert sich bei Konfigurationsänderungen

**dashboard_service.py:**
Service-Handler für Dashboard-Generierung:
- `handle_get_dashboard_yaml()` - Generiert YAML und zeigt Benachrichtigung
- Integration mit Home Assistant Notification-System

### Geänderte Dateien

**__init__.py:**
- Hinzugefügt: Sensor-Platform zu PLATFORMS
- Hinzugefügt: Dashboard-Service-Setup in `async_setup_entry()`
- Integration des Dashboard-Service-Moduls

**services.yaml:**
- Neuer Service: `get_dashboard_yaml`
- Beschreibung und Dokumentation

**manifest.json:**
- Version auf 0.7.0 erhöht
- Requirement hinzugefügt: `PyYAML` für YAML-Generierung

## Verwendungsbeispiel

### Schritt-für-Schritt Anleitung

**Schritt 1: Integration konfigurieren**

Richte die Integration ein mit:
- Eingangssensoren: `binary_sensor.aqara_vibration_sensor_t1_belegung`, `binary_sensor.aqara_vibration_sensor_t1_belegung_2`
- Indikator-Licht: `light.hue_color_lamp_3`
- Media Player: `media_player.kuche`
- Alarmton: `/media/growzelt/civil-defense-siren-128262.mp3`

**Schritt 2: Dashboard-YAML generieren**

Rufe den Service auf:
```yaml
service: ha_alarm_pro.get_dashboard_yaml
```

**Schritt 3: YAML kopieren**

Eine Benachrichtigung erscheint mit dem fertigen YAML, das automatisch deine Sensoren und Lichter enthält:

```yaml
type: vertical-stack
cards:
  - type: conditional
    conditions:
      - entity: alarm_control_panel.ha_alarm_pro
        state: triggered
    card:
      type: markdown
      content: |
        ## 🔴 ALARM AUSGELÖST
        ...
  - type: entities
    title: Sensoren & Indikatoren
    entities:
      - entity: binary_sensor.aqara_vibration_sensor_t1_belegung
        name: Aqara Vibration Sensor T1 Belegung
      - entity: binary_sensor.aqara_vibration_sensor_t1_belegung_2
        name: Aqara Vibration Sensor T1 Belegung 2
      - type: divider
      - entity: light.hue_color_lamp_3
        name: Hue Color Lamp 3
  ...
```

**Schritt 4: Dashboard hinzufügen**

Füge das YAML in dein Dashboard ein - fertig!

## Vorteile

**Keine manuelle Konfiguration:**
Du musst keine Entity-IDs mehr manuell in YAML-Dateien eintragen. Alles wird automatisch aus deiner Integration-Konfiguration übernommen.

**Automatische Anpassung:**
Wenn du deine Konfiguration änderst (z.B. neue Sensoren hinzufügst), generierst du einfach neues YAML und das Dashboard wird automatisch aktualisiert.

**Konsistenz:**
Alle konfigurierten Entitäten werden garantiert im Dashboard angezeigt. Keine vergessenen Sensoren oder Tippfehler mehr.

**Lesbare Namen:**
Entity-IDs werden automatisch in menschenlesbare Namen konvertiert, sodass dein Dashboard professionell aussieht.

**Einfache Updates:**
Bei Änderungen einfach Service aufrufen, neues YAML kopieren und einfügen. Keine komplexe YAML-Bearbeitung erforderlich.

## Migration von v0.6.0

Wenn du bereits v0.6.0 verwendest und das Dashboard manuell konfiguriert hast:

1. Installiere v0.7.0
2. Rufe `ha_alarm_pro.get_dashboard_yaml` auf
3. Vergleiche das generierte YAML mit deinem manuellen Dashboard
4. Ersetze dein Dashboard mit dem generierten YAML (optional)

Das generierte Dashboard sollte identisch oder besser sein als dein manuelles Dashboard, da es automatisch alle konfigurierten Entitäten enthält.

## Bekannte Einschränkungen

**Manuelle Dashboard-Erstellung erforderlich:**
Das Dashboard wird noch nicht vollautomatisch im Frontend registriert. Du musst das YAML einmal kopieren und einfügen. Eine vollautomatische Registrierung ist für zukünftige Versionen geplant.

**Statisches YAML:**
Nach dem Einfügen ist das Dashboard statisch. Bei Konfigurationsänderungen muss neues YAML generiert und eingefügt werden. Live-Updates sind für zukünftige Versionen geplant.

**Einfaches Layout:**
Das generierte Dashboard verwendet ein Standard-Layout. Benutzerdefinierte Layouts und Themes sind für zukünftige Versionen geplant.

## Roadmap

Geplante Features für zukünftige Versionen:
- Vollautomatische Dashboard-Registrierung ohne manuelles Kopieren
- Live-Updates bei Konfigurationsänderungen
- Mehrere Dashboard-Layouts (kompakt, erweitert, mobil)
- Theme-Unterstützung
- Dashboard-Editor-Integration
- Drag-and-Drop Konfiguration

## Kompatibilität

- **Abwärtskompatibel:** Ja, vollständig kompatibel mit v0.6.0 und v0.5.x
- **Konfiguration:** Keine Änderungen erforderlich
- **Datenmigration:** Nicht erforderlich
- **Home Assistant:** Mindestversion 2023.1.0 empfohlen

---

## Vollständige Versionshistorie

**v0.7.0** - Automatisches Dashboard-System
**v0.6.0** - Dashboard-Integration (manuell)
**v0.5.1** - Bugfix: Audiodatei-Erkennung in Unterordnern
**v0.5.0** - Test-Services, erweiterte Audioformate, Mehrfach-Lichtquellen
**v0.4.0** - Basis-Funktionalität
