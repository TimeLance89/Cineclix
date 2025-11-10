# Bugfix Notes - Version 1.0.1

## Problem

Der ImportError in Version 1.0.0 wurde durch die Verwendung veralteter Konstanten verursacht:

```
ImportError: cannot import name 'STATE_ALARM_ARMED_AWAY' from 'homeassistant.const'
```

## Ursache

In neueren Versionen von Home Assistant (ab ca. 2023.x) wurden die Alarm-Zustandskonstanten von `homeassistant.const` in eine Enum-Klasse `AlarmControlPanelState` in `homeassistant.components.alarm_control_panel.const` verschoben.

Die alte Methode:
```python
from homeassistant.const import (
    STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_DISARMED,
    STATE_ALARM_PENDING,
    STATE_ALARM_TRIGGERED,
    STATE_ALARM_ARMING,
)
```

## Lösung

Verwendung der offiziellen Enum-Klasse:

```python
from homeassistant.components.alarm_control_panel.const import (
    AlarmControlPanelState,
)
```

### Geänderte Zustandsreferenzen

Alle State-Referenzen wurden aktualisiert:

- `STATE_ALARM_DISARMED` → `AlarmControlPanelState.DISARMED`
- `STATE_ALARM_ARMING` → `AlarmControlPanelState.ARMING`
- `STATE_ALARM_ARMED_AWAY` → `AlarmControlPanelState.ARMED_AWAY`
- `STATE_ALARM_PENDING` → `AlarmControlPanelState.PENDING`
- `STATE_ALARM_TRIGGERED` → `AlarmControlPanelState.TRIGGERED`

## Betroffene Dateien

1. **alarm_control_panel.py**
   - Import-Statement aktualisiert
   - Alle State-Zuweisungen geändert (ca. 15 Stellen)
   - Alle State-Vergleiche aktualisiert

2. **const.py**
   - Veraltete State-Definitionen entfernt
   - Nur noch Farbcodes und Konfigurationskonstanten

3. **manifest.json**
   - Version auf 1.0.1 erhöht

4. **CHANGELOG.md**
   - Bugfix dokumentiert

## Kompatibilität

Die korrigierte Version ist kompatibel mit:
- Home Assistant Core 2023.1.0 und höher
- Alle neueren Versionen, die die `AlarmControlPanelState` Enum verwenden

## Testing

Nach der Korrektur sollte die Integration ohne ImportError laden:

1. Kopieren Sie die korrigierten Dateien nach `custom_components/nfc_alarm_system/`
2. Starten Sie Home Assistant neu
3. Die Integration sollte ohne Fehler laden
4. Überprüfen Sie die Logs auf Warnungen

## Weitere Hinweise

Diese Änderung ist eine **Breaking Change** nur für sehr alte Home Assistant Versionen (vor 2023.1.0). Für moderne Installationen ist dies die korrekte Implementierung.

Falls Sie eine ältere Home Assistant Version verwenden (was nicht empfohlen wird), müssen Sie entweder:
- Home Assistant aktualisieren (empfohlen)
- Oder zur Version 1.0.0 mit manuellen Anpassungen zurückkehren
