# Changelog - HA Alarm Pro v0.5.1

## Bugfix-Release: Audiodatei-Erkennung verbessert

### Behobene Probleme

#### Audiodateien in Unterordnern werden jetzt erkannt

**Problem:** Audiodateien, die in Unterordnern des `/media/` Verzeichnisses gespeichert waren (z.B. `/media/growzelt/alarm_active.mp3`), wurden nicht in der Auswahlliste angezeigt.

**Lösung:** Die Scan-Funktion `_scan_mp3_paths()` wurde verbessert und enthält jetzt:
- Detailliertes Debug-Logging zur Fehlersuche
- Robustere Fehlerbehandlung für einzelne Dateien
- Bessere Anzeige von Dateien in Unterordnern mit Ordner-Icon (📁)
- Informative Log-Meldungen über die Anzahl gefundener Dateien

**Beispiel:** Eine Datei unter `/media/growzelt/alarm_active.mp3` wird jetzt angezeigt als:
- **Label:** `alarm_active.mp3 (📁 growzelt)`
- **Wert:** `/media/growzelt/alarm_active.mp3`

#### Verbesserte Media-Source URL Unterstützung

**Problem:** Media-Source URLs mussten manuell eingegeben werden und die Konvertierung zwischen verschiedenen Pfad-Formaten war nicht optimal.

**Lösung:** Die `_resolve_media()` Methode wurde erweitert:
- Automatische Konvertierung von `/media/` Pfaden zu `media-source://` URLs für bessere Kompatibilität
- Unterstützung für alle gängigen Pfad-Formate:
  - `/media/pfad/datei.mp3` → `media-source://media_source/local/pfad/datei.mp3`
  - `/local/pfad/datei.mp3` → direkte Verwendung
  - `media-source://...` → direkte Verwendung

### Technische Änderungen

#### Geänderte Dateien

**config_flow.py:**
- Erweiterte `_scan_mp3_paths()` Funktion mit Logging
- Verbesserte Label-Formatierung für Dateien in Unterordnern
- Robustere Fehlerbehandlung

**alarm_control_panel.py:**
- Erweiterte `_resolve_media()` Methode für automatische Pfad-Konvertierung
- Bessere Unterstützung für Media-Source URLs

**manifest.json:**
- Version auf 0.5.1 erhöht

### Debug-Logging aktivieren

Falls Audiodateien immer noch nicht angezeigt werden, können Sie Debug-Logging aktivieren, um die Ursache zu finden:

```yaml
# In configuration.yaml
logger:
  default: info
  logs:
    custom_components.ha_alarm_pro.config_flow: debug
```

Nach dem Neustart und Öffnen der Integration-Konfiguration finden Sie in den Logs detaillierte Informationen über:
- Welche Verzeichnisse gescannt werden
- Welche Dateien gefunden werden
- Eventuelle Fehler beim Scannen

### Installation

Diese Version ist ein Bugfix-Release und vollständig kompatibel mit Version 0.5.0. Sie können einfach die Dateien ersetzen und Home Assistant neu starten.

**Schritte:**
1. Entpacken Sie `HA_Alarm_Pro_v0.5.1.zip`
2. Ersetzen Sie den Ordner `custom_components/ha_alarm_pro`
3. Starten Sie Home Assistant neu
4. Öffnen Sie die Integration-Konfiguration
5. Ihre Audiodateien in Unterordnern sollten jetzt angezeigt werden

### Bekannte Einschränkungen

- Das Scannen erfolgt nur beim Öffnen der Konfiguration, nicht automatisch
- Nach dem Hinzufügen neuer Dateien muss die Konfiguration erneut geöffnet werden
- Sehr große Verzeichnisstrukturen können das Laden der Konfiguration verlangsamen

---

## Version 0.5.0 (Vorherige Version)

Siehe CHANGELOG.md für Details zu Version 0.5.0 mit den Hauptfunktionen:
- Test-Service für Alarmtöne
- Erweiterte Audiodatei-Unterstützung (MP3, WAV, OGG, FLAC, M4A, AAC)
- Mehrfachauswahl von Lichtquellen
