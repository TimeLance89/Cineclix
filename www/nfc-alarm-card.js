class NFCAlarmCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }
    this.config = config;
    this.render();
  }

  set hass(hass) {
    this._hass = hass;
    const entity = hass.states[this.config.entity];
    
    if (!entity) {
      this.shadowRoot.innerHTML = `
        <ha-card>
          <div class="card-content">
            <p>Entity ${this.config.entity} not found</p>
          </div>
        </ha-card>
      `;
      return;
    }

    this.updateCard(entity);
  }

  updateCard(entity) {
    const state = entity.state;
    const attributes = entity.attributes;
    
    // Get configured sensors and lights from attributes
    const triggerSensors = attributes.trigger_sensors || [];
    const indicatorLights = attributes.indicator_lights || [];
    
    // Check if alarm is triggered
    const isTriggered = state === 'triggered';
    const isArmed = state === 'armed_away' || state === 'arming';
    const isPending = state === 'pending';
    
    // Build sensor list HTML
    const sensorListHTML = triggerSensors.map(sensorId => {
      const sensorState = this._hass.states[sensorId];
      if (!sensorState) return '';
      
      const sensorName = sensorState.attributes.friendly_name || sensorId;
      const sensorActive = sensorState.state === 'on';
      
      return `
        <div class="entity-row ${sensorActive ? 'active' : ''}">
          <div class="entity-info">
            <span class="entity-icon">${sensorActive ? '🔴' : '🟢'}</span>
            <span class="entity-name">${sensorName}</span>
          </div>
          <div class="entity-state">${sensorActive ? 'Aktiv' : 'Inaktiv'}</div>
        </div>
      `;
    }).join('');
    
    // Build indicator lights HTML
    const lightsHTML = indicatorLights.map(lightId => {
      const lightState = this._hass.states[lightId];
      if (!lightState) return '';
      
      const lightName = lightState.attributes.friendly_name || lightId;
      const lightOn = lightState.state === 'on';
      
      return `
        <div class="entity-row ${lightOn ? 'active' : ''}">
          <div class="entity-info">
            <span class="entity-icon">${lightOn ? '💡' : '⚫'}</span>
            <span class="entity-name">${lightName}</span>
          </div>
          <div class="entity-state">${lightOn ? 'An' : 'Aus'}</div>
        </div>
      `;
    }).join('');

    this.shadowRoot.innerHTML = `
      <style>
        ha-card {
          padding: 0;
          background: var(--ha-card-background, var(--card-background-color, white));
          border-radius: var(--ha-card-border-radius, 12px);
          box-shadow: var(--ha-card-box-shadow, 0 2px 8px rgba(0,0,0,0.1));
          overflow: hidden;
        }

        /* Alarm Warning Banner */
        .alarm-warning {
          background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
          color: white;
          padding: 20px;
          text-align: center;
          animation: pulse 2s infinite;
        }

        .alarm-warning h2 {
          margin: 0 0 8px 0;
          font-size: 24px;
          font-weight: 700;
        }

        .alarm-warning p {
          margin: 0;
          font-size: 14px;
          opacity: 0.95;
        }

        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.85; }
        }

        /* Status Section */
        .status-section {
          padding: 16px;
          border-bottom: 1px solid var(--divider-color, #e0e0e0);
        }

        .section-title {
          font-size: 14px;
          font-weight: 600;
          color: var(--primary-text-color);
          margin: 0 0 12px 0;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .status-grid {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 12px;
        }

        .status-item {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px;
          background: var(--secondary-background-color, #f5f5f5);
          border-radius: 8px;
        }

        .status-icon {
          font-size: 24px;
        }

        .status-info {
          flex: 1;
        }

        .status-label {
          font-size: 11px;
          color: var(--secondary-text-color);
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .status-value {
          font-size: 16px;
          font-weight: 600;
          color: var(--primary-text-color);
          margin-top: 2px;
        }

        .status-value.active {
          color: #4caf50;
        }

        .status-value.triggered {
          color: #f44336;
        }

        /* Buttons Section */
        .buttons-section {
          padding: 16px;
          border-bottom: 1px solid var(--divider-color, #e0e0e0);
        }

        .button-grid {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 12px;
        }

        .action-button {
          padding: 16px;
          border: none;
          border-radius: 8px;
          font-size: 13px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
          text-transform: uppercase;
          letter-spacing: 0.5px;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 8px;
          background: var(--primary-color);
          color: white;
        }

        .action-button:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .action-button:active {
          transform: translateY(0);
        }

        .action-button .button-icon {
          font-size: 24px;
        }

        .btn-arm {
          background: #2196f3;
        }

        .btn-disarm {
          background: #4caf50;
        }

        .btn-test {
          background: #ff9800;
        }

        .btn-acknowledge {
          background: #9c27b0;
        }

        .btn-disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        /* Entities Section */
        .entities-section {
          padding: 16px;
          border-bottom: 1px solid var(--divider-color, #e0e0e0);
        }

        .entity-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 12px;
          margin-bottom: 8px;
          background: var(--secondary-background-color, #f5f5f5);
          border-radius: 8px;
          transition: background 0.2s;
        }

        .entity-row:last-child {
          margin-bottom: 0;
        }

        .entity-row.active {
          background: rgba(244, 67, 54, 0.1);
          border-left: 4px solid #f44336;
        }

        .entity-info {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .entity-icon {
          font-size: 20px;
        }

        .entity-name {
          font-size: 14px;
          font-weight: 500;
          color: var(--primary-text-color);
        }

        .entity-state {
          font-size: 12px;
          color: var(--secondary-text-color);
          font-weight: 600;
          text-transform: uppercase;
        }

        .divider {
          height: 1px;
          background: var(--divider-color, #e0e0e0);
          margin: 12px 0;
        }

        /* Logbook Section */
        .logbook-section {
          padding: 16px;
        }

        .logbook-entries {
          max-height: 300px;
          overflow-y: auto;
        }

        .logbook-entry {
          display: flex;
          gap: 12px;
          padding: 12px;
          margin-bottom: 8px;
          background: var(--secondary-background-color, #f5f5f5);
          border-radius: 8px;
          border-left: 4px solid var(--primary-color);
        }

        .logbook-entry:last-child {
          margin-bottom: 0;
        }

        .logbook-time {
          font-size: 11px;
          color: var(--secondary-text-color);
          white-space: nowrap;
          min-width: 60px;
        }

        .logbook-content {
          flex: 1;
        }

        .logbook-entity {
          font-size: 13px;
          font-weight: 600;
          color: var(--primary-text-color);
          margin-bottom: 2px;
        }

        .logbook-state {
          font-size: 12px;
          color: var(--secondary-text-color);
        }

        .logbook-entries::-webkit-scrollbar {
          width: 6px;
        }

        .logbook-entries::-webkit-scrollbar-track {
          background: var(--divider-color, #e0e0e0);
          border-radius: 3px;
        }

        .logbook-entries::-webkit-scrollbar-thumb {
          background: var(--primary-color);
          border-radius: 3px;
        }

        /* Responsive */
        @media (max-width: 600px) {
          .button-grid {
            grid-template-columns: 1fr;
          }
          
          .status-grid {
            grid-template-columns: 1fr;
          }
        }
      </style>

      <ha-card>
        ${isTriggered ? `
          <div class="alarm-warning">
            <h2>🔴 ALARM AUSGELÖST</h2>
            <p>Quittiere den Alarm mit „Alarm quittieren" oder per NFC-Unscharf.</p>
          </div>
        ` : ''}

        <div class="status-section">
          <h3 class="section-title">Status</h3>
          <div class="status-grid">
            <div class="status-item">
              <span class="status-icon">${isArmed ? '🛡️' : '✅'}</span>
              <div class="status-info">
                <div class="status-label">Scharf</div>
                <div class="status-value ${isArmed ? 'active' : ''}">${isArmed ? 'Ja' : 'Nein'}</div>
              </div>
            </div>
            <div class="status-item">
              <span class="status-icon">${isTriggered ? '🚨' : '✅'}</span>
              <div class="status-info">
                <div class="status-label">Ausgelöst</div>
                <div class="status-value ${isTriggered ? 'triggered' : ''}">${isTriggered ? 'Ja' : 'Nein'}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="buttons-section">
          <div class="button-grid">
            <button class="action-button btn-arm ${isArmed ? 'btn-disabled' : ''}" 
                    onclick="this.getRootNode().host._armAlarm()"
                    ${isArmed ? 'disabled' : ''}>
              <span class="button-icon">🛡️</span>
              <span>Scharf (sofort)</span>
            </button>
            <button class="action-button btn-disarm ${!isArmed && !isTriggered ? 'btn-disabled' : ''}"
                    onclick="this.getRootNode().host._disarmAlarm()"
                    ${!isArmed && !isTriggered ? 'disabled' : ''}>
              <span class="button-icon">✅</span>
              <span>Unscharf</span>
            </button>
            <button class="action-button btn-test"
                    onclick="this.getRootNode().host._testAlarm()">
              <span class="button-icon">🔔</span>
              <span>Alarm testen</span>
            </button>
            <button class="action-button btn-acknowledge ${!isTriggered ? 'btn-disabled' : ''}"
                    onclick="this.getRootNode().host._acknowledgeAlarm()"
                    ${!isTriggered ? 'disabled' : ''}>
              <span class="button-icon">🔕</span>
              <span>Alarm quittieren</span>
            </button>
          </div>
        </div>

        ${sensorListHTML || lightsHTML ? `
          <div class="entities-section">
            <h3 class="section-title">Sensoren & Licht</h3>
            ${sensorListHTML}
            ${sensorListHTML && lightsHTML ? '<div class="divider"></div>' : ''}
            ${lightsHTML}
          </div>
        ` : ''}

        <div class="logbook-section">
          <h3 class="section-title">Verlauf (letzte 6 Stunden)</h3>
          <div class="logbook-entries" id="logbook-container">
            <div style="text-align: center; padding: 20px; color: var(--secondary-text-color);">
              Lade Verlauf...
            </div>
          </div>
        </div>
      </ha-card>
    `;

    // Load logbook after rendering
    this._loadLogbook(entity);
  }

  async _loadLogbook(entity) {
    const container = this.shadowRoot.getElementById('logbook-container');
    if (!container) return;

    try {
      const endTime = new Date();
      const startTime = new Date(endTime.getTime() - 6 * 60 * 60 * 1000); // 6 hours ago
      
      const entities = [this.config.entity];
      const attributes = entity.attributes;
      
      // Add trigger sensors to logbook
      if (attributes.trigger_sensors) {
        entities.push(...attributes.trigger_sensors);
      }
      
      const history = await this._hass.callWS({
        type: 'history/history_during_period',
        start_time: startTime.toISOString(),
        end_time: endTime.toISOString(),
        entity_ids: entities,
        minimal_response: false,
        no_attributes: false,
      });

      if (!history || history.length === 0) {
        container.innerHTML = `
          <div style="text-align: center; padding: 20px; color: var(--secondary-text-color);">
            Keine Ereignisse in den letzten 6 Stunden
          </div>
        `;
        return;
      }

      // Flatten and sort all state changes
      const allChanges = [];
      history.forEach(entityHistory => {
        if (entityHistory && entityHistory.length > 0) {
          entityHistory.forEach(state => {
            const entityState = this._hass.states[state.entity_id];
            const entityName = entityState ? entityState.attributes.friendly_name : state.entity_id;
            
            allChanges.push({
              time: new Date(state.last_changed),
              entity: entityName,
              state: this._formatState(state.state),
              entity_id: state.entity_id
            });
          });
        }
      });

      // Sort by time (newest first)
      allChanges.sort((a, b) => b.time - a.time);

      // Take only last 20 entries
      const recentChanges = allChanges.slice(0, 20);

      if (recentChanges.length === 0) {
        container.innerHTML = `
          <div style="text-align: center; padding: 20px; color: var(--secondary-text-color);">
            Keine Ereignisse in den letzten 6 Stunden
          </div>
        `;
        return;
      }

      container.innerHTML = recentChanges.map(change => `
        <div class="logbook-entry">
          <div class="logbook-time">${this._formatTime(change.time)}</div>
          <div class="logbook-content">
            <div class="logbook-entity">${change.entity}</div>
            <div class="logbook-state">${change.state}</div>
          </div>
        </div>
      `).join('');

    } catch (error) {
      console.error('Error loading logbook:', error);
      container.innerHTML = `
        <div style="text-align: center; padding: 20px; color: var(--error-color, #f44336);">
          Fehler beim Laden des Verlaufs
        </div>
      `;
    }
  }

  _formatState(state) {
    const stateMap = {
      'on': 'An',
      'off': 'Aus',
      'disarmed': 'Unscharf',
      'arming': 'Wird scharf...',
      'armed_away': 'Scharf',
      'pending': 'Eintrittsverzögerung',
      'triggered': 'Alarm ausgelöst'
    };
    return stateMap[state] || state;
  }

  _formatTime(date) {
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // seconds

    if (diff < 60) return 'Gerade';
    if (diff < 3600) return `${Math.floor(diff / 60)}m`;
    if (diff < 86400) return date.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' });
    
    return date.toLocaleString('de-DE', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  _armAlarm() {
    this._hass.callService('alarm_control_panel', 'alarm_arm_away', {
      entity_id: this.config.entity
    });
  }

  _disarmAlarm() {
    this._hass.callService('alarm_control_panel', 'alarm_disarm', {
      entity_id: this.config.entity
    });
  }

  _testAlarm() {
    // Trigger the alarm for testing
    this._hass.callService('alarm_control_panel', 'alarm_trigger', {
      entity_id: this.config.entity
    });
  }

  _acknowledgeAlarm() {
    // Disarm to acknowledge
    this._disarmAlarm();
  }

  render() {
    if (!this.shadowRoot.querySelector('ha-card')) {
      this.shadowRoot.innerHTML = `
        <ha-card>
          <div style="padding: 20px; text-align: center;">
            <p>Lade NFC Alarmsystem...</p>
          </div>
        </ha-card>
      `;
    }
  }

  getCardSize() {
    return 8;
  }

  static getStubConfig() {
    return {
      entity: 'alarm_control_panel.nfc_alarmsystem'
    };
  }
}

customElements.define('nfc-alarm-card', NFCAlarmCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'nfc-alarm-card',
  name: 'NFC Alarm Card',
  description: 'Erweiterte Karte für das NFC Alarmsystem mit Status, Buttons, Sensoren und Verlauf',
  preview: true,
  documentationURL: 'https://github.com/yourusername/nfc_alarm_system'
});

console.info(
  '%c NFC-ALARM-CARD %c Version 1.1.0 ',
  'color: white; background: #2196f3; font-weight: 700;',
  'color: #2196f3; background: white; font-weight: 700;'
);
