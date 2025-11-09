# Changelog - HA Alarm Pro

## Version 0.5.0 - Neue Features

### ✅ Implementierte Funktionen

#### 1. Test-Service für Alarmtöne
- **Neuer Service:** `ha_alarm_pro.test_alarm_sound`
- Ermöglicht das Testen des konfigurierten Alarmtons ohne Auslösung des Alarms
- Verwendung:
  ```yaml
  service: ha_alarm_pro.test_alarm_sound
  data:
    entity_id: alarm_control_panel.ha_alarm_pro
  ```

#### 2. Erweiterte Audiodatei-Unterstützung
- **Unterstützte Formate:**
  - MP3 (.mp3)
  - WAV (.wav)
  - OGG (.ogg)
  - FLAC (.flac)
  - M4A (.m4a)
  - AAC (.aac)
- Automatische Erkennung aller Audiodateien in `/media/` und `/www/` Verzeichnissen
- Verbesserte Anzeige mit vollständigem Pfad in der Auswahlliste
- Unterstützung für benutzerdefinierte Pfadeingabe

#### 3. Mehrfachauswahl von Lichtquellen
- **Mehrere Indikator-Lichter:** Es können jetzt mehrere Lichtquellen gleichzeitig ausgewählt werden
- Alle ausgewählten Lichter werden synchron gesteuert:
  - Blinken beim Scharfschalten
  - Dauerblinken im Alarm-Modus
  - Verschiedene Farben je nach Status (gelb=Scharfschaltung, orange=Verzögerung, rot=Alarm)

### 🔧 Technische Änderungen

#### Geänderte Dateien:
1. **const.py**
   - Neue Konstante: `SERVICE_TEST_ALARM_SOUND`

2. **services.yaml**
   - Service-Definition für `test_alarm_sound` hinzugefügt

3. **__init__.py**
   - Service-Handler für `test_alarm_sound` implementiert
   - Event-System für Sound-Tests integriert

4. **alarm_control_panel.py**
   - Neue Methode: `_get_lights()` für Mehrfach-Licht-Unterstützung
   - Neue Methode: `_handle_test_sound()` für Sound-Tests
   - Angepasste Methoden:
     - `_flash_indicator()` - unterstützt jetzt mehrere Lichter
     - `_start_indicator_loop()` - unterstützt jetzt mehrere Lichter
     - `_stop_indicator_loop()` - unterstützt jetzt mehrere Lichter

5. **config_flow.py**
   - Erweiterte `_scan_mp3_paths()` Funktion für alle Audio-Formate
   - Aktivierte Mehrfachauswahl für Lichtquellen (`multiple: True`)
   - Verbesserte Label-Anzeige mit vollständigem Dateipfad

### 📋 Migration von Version 0.4.0

Die Integration ist vollständig abwärtskompatibel. Bestehende Konfigurationen mit einer einzelnen Lichtquelle funktionieren weiterhin ohne Änderungen.

**Optionale Schritte:**
1. Öffnen Sie die Konfiguration der Integration
2. Fügen Sie weitere Lichtquellen hinzu (optional)
3. Laden Sie neue Audiodateien in `/media/` oder `/www/` hoch (optional)
4. Testen Sie den Alarmton mit dem neuen Service

### 🎯 Verwendungsbeispiele

#### Alarmton testen (Automation)
```yaml
automation:
  - alias: "Test Alarm Sound bei Tastendruck"
    trigger:
      - platform: state
        entity_id: input_button.test_alarm
        to: "on"
    action:
      - service: ha_alarm_pro.test_alarm_sound
        data:
          entity_id: alarm_control_panel.ha_alarm_pro
```

#### Mehrere Lichter konfigurieren
In der Integration-Konfiguration können Sie jetzt mehrere Lichter auswählen:
- Wohnzimmer Deckenleuchte
- Flur LED-Strip
- Außenleuchte

Alle Lichter werden synchron beim Alarm aktiviert.

### 🐛 Bekannte Einschränkungen
- Die Mehrfach-Licht-Funktion erfordert, dass alle ausgewählten Lichter die gleichen Funktionen unterstützen (z.B. Farbwechsel)
- Media-Source URLs müssen manuell eingegeben werden (Format: `media-source://media_source/local/dateiname.mp3`)

---

## Version 0.4.0 (Vorherige Version)
- Basis-Funktionalität der Alarmanlage
- Einzelne Lichtquelle als Indikator
- MP3-Datei-Unterstützung
- NFC-Tag-Integration
- Entry/Exit-Delay-Sounds
