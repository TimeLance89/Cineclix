class NFCAlarmCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._history = [];
    this._maxHistory = 10;
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

    // Update history when state changes
    if (this._lastState !== entity.state) {
      this._addToHistory(entity.state, entity.last_changed);
      this._lastState = entity.state;
    }

    this.updateCard(entity);
  }

  _addToHistory(state, timestamp) {
    const stateLabels = {
      'disarmed': 'Unscharf',
      'arming': 'Wird scharf...',
      'armed_away': 'Scharf',
      'pending': 'Eintrittsverzögerung',
      'triggered': 'ALARM!'
    };

    this._history.unshift({
      state: stateLabels[state] || state,
      timestamp: new Date(timestamp),
      stateKey: state
    });

    if (this._history.length > this._maxHistory) {
      this._history = this._history.slice(0, this._maxHistory);
    }
  }

  updateCard(entity) {
    const state = entity.state;
    const attributes = entity.attributes;
    
    const stateConfig = this._getStateConfig(state);
    
    const historyHTML = this._history.map(item => `
      <div class="history-item ${item.stateKey}">
        <span class="history-state">${item.state}</span>
        <span class="history-time">${this._formatTime(item.timestamp)}</span>
      </div>
    `).join('');

    this.shadowRoot.innerHTML = `
      <style>
        ha-card {
          padding: 16px;
          background: var(--ha-card-background, var(--card-background-color, white));
          border-radius: var(--ha-card-border-radius, 12px);
          box-shadow: var(--ha-card-box-shadow, 0 2px 8px rgba(0,0,0,0.1));
        }

        .card-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 20px;
        }

        .card-title {
          font-size: 24px;
          font-weight: 500;
          color: var(--primary-text-color);
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .status-icon {
          width: 32px;
          height: 32px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 18px;
        }

        .status-badge {
          padding: 6px 16px;
          border-radius: 20px;
          font-size: 14px;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        /* State Colors */
        .state-disarmed { background: #4caf50; color: white; }
        .state-arming { background: #ff9800; color: white; }
        .state-armed_away { background: #2196f3; color: white; }
        .state-pending { background: #ff9800; color: white; }
        .state-triggered { background: #f44336; color: white; animation: pulse 1s infinite; }

        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }

        .status-section {
          background: var(--secondary-background-color, #f5f5f5);
          border-radius: 12px;
          padding: 20px;
          margin-bottom: 20px;
        }

        .status-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 16px;
          margin-top: 16px;
        }

        .status-item {
          text-align: center;
        }

        .status-label {
          font-size: 12px;
          color: var(--secondary-text-color);
          text-transform: uppercase;
          letter-spacing: 0.5px;
          margin-bottom: 8px;
        }

        .status-value {
          font-size: 20px;
          font-weight: 600;
          color: var(--primary-text-color);
        }

        .progress-bar {
          width: 100%;
          height: 8px;
          background: var(--divider-color, #e0e0e0);
          border-radius: 4px;
          overflow: hidden;
          margin-top: 8px;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #2196f3, #4caf50);
          transition: width 1s linear;
        }

        .buttons-section {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
          gap: 12px;
          margin-bottom: 20px;
        }

        .action-button {
          padding: 14px 20px;
          border: none;
          border-radius: 8px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
          text-transform: uppercase;
          letter-spacing: 0.5px;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
        }

        .action-button:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .action-button:active {
          transform: translateY(0);
        }

        .btn-arm {
          background: #2196f3;
          color: white;
        }

        .btn-disarm {
          background: #4caf50;
          color: white;
        }

        .btn-test {
          background: var(--secondary-background-color, #e0e0e0);
          color: var(--primary-text-color);
        }

        .btn-disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .history-section {
          background: var(--secondary-background-color, #f5f5f5);
          border-radius: 12px;
          padding: 16px;
        }

        .history-title {
          font-size: 14px;
          font-weight: 600;
          color: var(--primary-text-color);
          margin-bottom: 12px;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .history-list {
          max-height: 200px;
          overflow-y: auto;
        }

        .history-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 10px 12px;
          margin-bottom: 6px;
          background: var(--card-background-color, white);
          border-radius: 8px;
          border-left: 4px solid;
        }

        .history-item.disarmed { border-left-color: #4caf50; }
        .history-item.arming { border-left-color: #ff9800; }
        .history-item.armed_away { border-left-color: #2196f3; }
        .history-item.pending { border-left-color: #ff9800; }
        .history-item.triggered { border-left-color: #f44336; }

        .history-state {
          font-weight: 500;
          color: var(--primary-text-color);
        }

        .history-time {
          font-size: 12px;
          color: var(--secondary-text-color);
        }

        .info-grid {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 12px;
          margin-top: 16px;
        }

        .info-item {
          background: var(--card-background-color, white);
          padding: 12px;
          border-radius: 8px;
          border-left: 3px solid var(--primary-color);
        }

        .info-label {
          font-size: 11px;
          color: var(--secondary-text-color);
          text-transform: uppercase;
          letter-spacing: 0.5px;
          margin-bottom: 4px;
        }

        .info-value {
          font-size: 16px;
          font-weight: 600;
          color: var(--primary-text-color);
        }

        /* Scrollbar Styling */
        .history-list::-webkit-scrollbar {
          width: 6px;
        }

        .history-list::-webkit-scrollbar-track {
          background: var(--divider-color, #e0e0e0);
          border-radius: 3px;
        }

        .history-list::-webkit-scrollbar-thumb {
          background: var(--primary-color);
          border-radius: 3px;
        }

        /* Responsive */
        @media (max-width: 600px) {
          .status-grid {
            grid-template-columns: 1fr;
          }
          
          .buttons-section {
            grid-template-columns: 1fr;
          }

          .info-grid {
            grid-template-columns: 1fr;
          }
        }
      </style>

      <ha-card>
        <div class="card-header">
          <div class="card-title">
            <div class="status-icon ${stateConfig.class}">
              ${stateConfig.icon}
            </div>
            ${this.config.name || 'NFC Alarmsystem'}
          </div>
          <div class="status-badge ${stateConfig.class}">
            ${stateConfig.label}
          </div>
        </div>

        <div class="status-section">
          <div class="status-label">Aktueller Status</div>
          <div class="status-grid">
            <div class="status-item">
              <div class="status-label">Zustand</div>
              <div class="status-value">${stateConfig.label}</div>
            </div>
            <div class="status-item">
              <div class="status-label">Seit</div>
              <div class="status-value">${this._getTimeSince(entity.last_changed)}</div>
            </div>
          </div>
          
          <div class="info-grid">
            <div class="info-item">
              <div class="info-label">Austrittsverzögerung</div>
              <div class="info-value">${attributes.exit_delay || 120}s</div>
            </div>
            <div class="info-item">
              <div class="info-label">Eintrittsverzögerung</div>
              <div class="info-value">${attributes.entry_delay || 30}s</div>
            </div>
          </div>
        </div>

        <div class="buttons-section">
          <button class="action-button btn-arm ${state !== 'disarmed' ? 'btn-disabled' : ''}" 
                  onclick="this.getRootNode().host._armAlarm()"
                  ${state !== 'disarmed' ? 'disabled' : ''}>
            🛡️ Scharfschalten
          </button>
          <button class="action-button btn-disarm ${state === 'disarmed' ? 'btn-disabled' : ''}"
                  onclick="this.getRootNode().host._disarmAlarm()"
                  ${state === 'disarmed' ? 'disabled' : ''}>
            ✅ Unscharfschalten
          </button>
          <button class="action-button btn-test"
                  onclick="this.getRootNode().host._testAlarm()">
            🔔 Test
          </button>
        </div>

        <div class="history-section">
          <div class="history-title">📊 Verlauf (letzte ${this._history.length} Ereignisse)</div>
          <div class="history-list">
            ${historyHTML || '<div style="text-align: center; padding: 20px; color: var(--secondary-text-color);">Noch keine Ereignisse</div>'}
          </div>
        </div>
      </ha-card>
    `;
  }

  _getStateConfig(state) {
    const configs = {
      'disarmed': {
        label: 'Unscharf',
        icon: '✅',
        class: 'state-disarmed'
      },
      'arming': {
        label: 'Wird scharf...',
        icon: '⏳',
        class: 'state-arming'
      },
      'armed_away': {
        label: 'Scharf',
        icon: '🛡️',
        class: 'state-armed_away'
      },
      'pending': {
        label: 'Eintrittsverzögerung',
        icon: '⚠️',
        class: 'state-pending'
      },
      'triggered': {
        label: 'ALARM!',
        icon: '🚨',
        class: 'state-triggered'
      }
    };

    return configs[state] || {
      label: state,
      icon: '❓',
      class: 'state-unknown'
    };
  }

  _formatTime(date) {
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // seconds

    if (diff < 60) return 'Gerade eben';
    if (diff < 3600) return `vor ${Math.floor(diff / 60)} Min.`;
    if (diff < 86400) return `vor ${Math.floor(diff / 3600)} Std.`;
    
    return date.toLocaleString('de-DE', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  _getTimeSince(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);

    if (diff < 60) return `${diff}s`;
    if (diff < 3600) return `${Math.floor(diff / 60)}m`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h`;
    return `${Math.floor(diff / 86400)}d`;
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
    // Show a test notification
    this._hass.callService('persistent_notification', 'create', {
      title: 'NFC Alarmsystem Test',
      message: 'Dies ist eine Testnachricht. Alle Funktionen arbeiten korrekt.',
      notification_id: 'nfc_alarm_test'
    });
  }

  render() {
    if (!this.shadowRoot.querySelector('ha-card')) {
      this.shadowRoot.innerHTML = `
        <ha-card>
          <div class="card-content" style="padding: 20px; text-align: center;">
            <p>Lade NFC Alarmsystem...</p>
          </div>
        </ha-card>
      `;
    }
  }

  getCardSize() {
    return 6;
  }

  static getStubConfig() {
    return {
      entity: 'alarm_control_panel.nfc_alarmsystem',
      name: 'NFC Alarmsystem'
    };
  }
}

customElements.define('nfc-alarm-card', NFCAlarmCard);

// Register the card with Home Assistant
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'nfc-alarm-card',
  name: 'NFC Alarm Card',
  description: 'Eine benutzerdefinierte Karte für das NFC Alarmsystem mit Statusanzeigen, Verlauf und Buttons',
  preview: true,
  documentationURL: 'https://github.com/yourusername/nfc_alarm_system'
});

console.info(
  '%c NFC-ALARM-CARD %c Version 1.0.1 ',
  'color: white; background: #2196f3; font-weight: 700;',
  'color: #2196f3; background: white; font-weight: 700;'
);
