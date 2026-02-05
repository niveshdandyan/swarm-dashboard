"""
CSS styles for Swarm Dashboard.

Capybara-inspired natural color palette with light/dark theme support.
"""

DASHBOARD_CSS = """
/* ==============================================
   DESIGN TOKENS - CSS Custom Properties
   ============================================== */
:root {
  /* Colors - Background */
  --color-bg-primary: #F9F6F1;
  --color-bg-secondary: #F0EEE7;
  --color-bg-card: #FFFFFF;
  --color-bg-overlay: rgba(0, 0, 0, 0.5);

  /* Colors - Text */
  --color-text-primary: #111827;
  --color-text-secondary: #6b7280;
  --color-text-muted: #9ca3af;
  --color-text-inverse: #ffffff;

  /* Colors - Border */
  --color-border: #e5e7eb;
  --color-border-muted: #d1d5db;
  --color-border-focus: #FF6B4A;

  /* Colors - Accent (Coral) */
  --color-coral: #FF6B4A;
  --color-coral-light: #FF7A5C;
  --color-coral-hover: #e55a3a;
  --color-coral-bg: rgba(255, 107, 74, 0.1);

  /* Colors - Status (Capybara-Inspired Natural Palette) */
  --color-success: #7D9B76;
  --color-success-bg: rgba(125, 155, 118, 0.12);
  --color-warning: #D4A76A;
  --color-warning-bg: rgba(212, 167, 106, 0.12);
  --color-error: #C67A6B;
  --color-error-bg: rgba(198, 122, 107, 0.12);
  --color-status-running: #FF6B4A;
  --color-status-idle: #7BA3A8;
  --color-status-pending: #9B8B7A;
  --color-status-complete: #7D9B76;

  /* Typography */
  --font-heading: 'Instrument Serif', Georgia, serif;
  --font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
  --font-mono: 'Courier Prime', 'SF Mono', Monaco, 'Courier New', monospace;

  /* Font Sizes */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;
  --font-size-4xl: 2.25rem;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;

  /* Border Radius */
  --radius-sm: 0.125rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
  --shadow-card: 0 1px 3px rgba(0, 0, 0, 0.03);
  --shadow-card-hover: 0 8px 24px rgba(0, 0, 0, 0.1);

  /* Gradients */
  --gradient-coral: linear-gradient(135deg, #FF6B4A 0%, #FF8A6B 100%);
  --gradient-success: linear-gradient(135deg, #7D9B76 0%, #8FAD82 50%, #9AAD7A 100%);
  --gradient-idle: linear-gradient(135deg, #7BA3A8 0%, #8EB3B8 100%);
  --gradient-warm-bg: linear-gradient(180deg, #F9F6F1 0%, #F0EEE7 100%);

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-default: 200ms ease;
  --transition-slow: 300ms ease;
}

/* Dark Mode */
[data-theme="dark"] {
  --color-bg-primary: #121212;
  --color-bg-secondary: #1a1a1a;
  --color-bg-card: #2a2a2a;
  --color-bg-overlay: rgba(0, 0, 0, 0.7);
  --color-text-primary: #ffffff;
  --color-text-secondary: #9ca3af;
  --color-text-muted: #6b7280;
  --color-text-inverse: #111827;
  --color-border: #374151;
  --color-border-muted: #4b5563;
  --color-coral-bg: rgba(255, 107, 74, 0.15);
  --color-success-bg: rgba(125, 155, 118, 0.15);
  --color-warning-bg: rgba(212, 167, 106, 0.15);
  --color-error-bg: rgba(198, 122, 107, 0.15);
  --shadow-card: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-card-hover: 0 8px 24px rgba(0, 0, 0, 0.3);
  --gradient-warm-bg: linear-gradient(180deg, #121212 0%, #1a1a1a 100%);
}

/* ==============================================
   BASE STYLES - Reset & Typography
   ============================================== */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  min-height: 100vh;
}

body {
  font-family: var(--font-body);
  font-size: var(--font-size-base);
  line-height: 1.5;
  color: var(--color-text-primary);
  background: var(--gradient-warm-bg);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ==============================================
   LAYOUT - Container & Grid
   ============================================== */
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: margin-right var(--transition-slow);
}

.app.detail-open .main-panel {
  margin-right: 500px;
}

.main-panel {
  flex: 1;
  transition: margin-right var(--transition-slow);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--space-6);
}

/* ==============================================
   HEADER SECTION
   ============================================== */
.header {
  padding: var(--space-8) 0 var(--space-6);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--space-6);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-4);
}

.dashboard-title {
  font-family: var(--font-heading);
  font-size: var(--font-size-4xl);
  font-weight: 400;
  color: var(--color-text-primary);
  letter-spacing: -0.02em;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-bg-card);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: var(--transition-fast);
}

.theme-toggle:hover {
  border-color: var(--color-coral);
  color: var(--color-coral);
}

/* ==============================================
   STATS BAR
   ============================================== */
.stats-bar {
  display: flex;
  align-items: center;
  gap: var(--space-6);
  padding: var(--space-4) 0;
  margin-bottom: var(--space-6);
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.stat-value {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--color-text-primary);
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.stat-item.running .stat-value { color: var(--color-status-running); }
.stat-item.idle .stat-value { color: var(--color-status-idle); }
.stat-item.completed .stat-value { color: var(--color-success); }
.stat-item.pending .stat-value { color: var(--color-status-pending); }
.stat-item.failed .stat-value { color: var(--color-error); }

/* ==============================================
   AGENTS GRID
   ============================================== */
.waves-container {
  margin-bottom: var(--space-8);
}

.wave-section {
  margin-bottom: var(--space-8);
}

.wave-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.wave-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-1) var(--space-3);
  background: var(--color-coral-bg);
  color: var(--color-coral);
  font-size: var(--font-size-sm);
  font-weight: 600;
  border-radius: var(--radius-full);
}

.wave-title {
  font-family: var(--font-heading);
  font-size: var(--font-size-xl);
  color: var(--color-text-primary);
}

.agents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-4);
}

/* ==============================================
   AGENT CARD
   ============================================== */
.agent-card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  cursor: pointer;
  transition: var(--transition-default);
  box-shadow: var(--shadow-card);
}

.agent-card:hover {
  border-color: var(--color-coral);
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-2px);
}

.agent-card.selected {
  border-color: var(--color-coral);
  box-shadow: 0 0 0 2px var(--color-coral-bg);
}

.agent-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.agent-role {
  font-family: var(--font-heading);
  font-size: var(--font-size-lg);
  color: var(--color-text-primary);
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.running {
  background: var(--color-coral-bg);
  color: var(--color-coral);
}

.status-badge.idle {
  background: rgba(123, 163, 168, 0.15);
  color: var(--color-status-idle);
}

.status-badge.completed {
  background: var(--color-success-bg);
  color: var(--color-success);
}

.status-badge.pending {
  background: rgba(155, 139, 122, 0.15);
  color: var(--color-status-pending);
}

.status-badge.failed {
  background: var(--color-error-bg);
  color: var(--color-error);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: var(--radius-full);
  background: currentColor;
}

.status-badge.running .status-dot {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.agent-activity {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
}

.agent-activity.stale {
  color: var(--color-warning);
}

/* Progress Bar */
.progress-bar {
  height: 6px;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-full);
  overflow: hidden;
  margin-bottom: var(--space-3);
}

.progress-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width var(--transition-slow);
}

.agent-card.running .progress-fill {
  background: var(--gradient-coral);
}

.agent-card.idle .progress-fill {
  background: var(--gradient-idle);
}

.agent-card.completed .progress-fill {
  background: var(--gradient-success);
}

.agent-card.pending .progress-fill {
  background: var(--color-status-pending);
}

.agent-card.failed .progress-fill {
  background: var(--color-error);
}

/* Tools Used */
.agent-tools {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
}

.tool-badge {
  font-family: var(--font-mono);
  font-size: var(--font-size-xs);
  padding: var(--space-1) var(--space-2);
  background: var(--color-bg-secondary);
  color: var(--color-text-secondary);
  border-radius: var(--radius-md);
}

/* ==============================================
   DETAIL PANEL (Slide-in Sidebar)
   ============================================== */
.detail-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 500px;
  height: 100vh;
  background: var(--color-bg-card);
  border-left: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-xl);
  transform: translateX(100%);
  transition: transform var(--transition-slow);
  z-index: 300;
  overflow: hidden;
}

.detail-panel.open,
.app.detail-open .detail-panel {
  transform: translateX(0);
}

.detail-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-6);
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}

.detail-panel-title h2 {
  font-family: var(--font-heading);
  font-size: var(--font-size-xl);
  color: var(--color-text-primary);
}

.detail-panel-subtitle {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.detail-panel-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  border-radius: var(--radius-lg);
  transition: var(--transition-fast);
}

.detail-panel-close:hover {
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
}

.detail-panel-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-6);
}

.detail-section {
  margin-bottom: var(--space-6);
}

.detail-section:last-child {
  margin-bottom: 0;
}

.detail-section-title {
  font-size: var(--font-size-sm);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-text-muted);
  margin-bottom: var(--space-3);
  padding-bottom: var(--space-2);
  border-bottom: 1px solid var(--color-border);
}

.detail-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
}

.detail-info-item {
  background: var(--color-bg-secondary);
  padding: var(--space-3);
  border-radius: var(--radius-lg);
}

.detail-info-item.full-width {
  grid-column: 1 / -1;
}

.detail-info-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  text-transform: uppercase;
}

.detail-info-value {
  font-size: var(--font-size-base);
  font-weight: 500;
  color: var(--color-text-primary);
  margin-top: var(--space-1);
}

.detail-tools-grid {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.tool-stat {
  background: var(--color-bg-secondary);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.tool-name {
  font-size: var(--font-size-sm);
}

.tool-count {
  font-size: var(--font-size-sm);
  color: var(--color-coral);
  font-weight: 600;
}

/* Activity Feed */
.activity-feed {
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  max-height: 400px;
  overflow-y: auto;
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
}

.activity-item {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  gap: var(--space-3);
  align-items: flex-start;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  font-size: var(--font-size-xs);
}

.activity-icon.tool {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.activity-icon.thinking {
  background: rgba(123, 163, 168, 0.2);
  color: #7BA3A8;
}

.activity-icon.result {
  background: var(--color-success-bg);
  color: var(--color-success);
}

.activity-content {
  flex: 1;
  overflow: hidden;
  word-break: break-word;
}

.activity-tool {
  color: var(--color-coral);
  font-weight: 500;
}

.activity-text {
  color: var(--color-text-secondary);
  margin-top: var(--space-1);
}

/* Files List */
.files-list {
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.file-item {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
}

.file-item:last-child {
  border-bottom: none;
}

.file-icon {
  color: var(--color-text-muted);
}

/* Overlay */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  visibility: hidden;
  transition: var(--transition-slow);
  z-index: 200;
}

.app.detail-open .overlay {
  opacity: 1;
  visibility: visible;
}

/* Connection Status */
.connection-status {
  position: fixed;
  bottom: var(--space-4);
  left: var(--space-4);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  box-shadow: var(--shadow-md);
  z-index: 100;
}

.connection-status.connected {
  border-color: var(--color-success);
}

.connection-status.disconnected {
  border-color: var(--color-error);
  color: var(--color-error);
}

.connection-status .status-dot {
  width: 8px;
  height: 8px;
  border-radius: var(--radius-full);
}

.connection-status.connected .status-dot {
  background: var(--color-success);
  animation: pulse 2s ease-in-out infinite;
}

.connection-status.disconnected .status-dot {
  background: var(--color-error);
}

/* ==============================================
   RESPONSIVE STYLES
   ============================================== */
@media screen and (max-width: 1024px) {
  .container {
    padding: 0 var(--space-4);
  }

  .app.detail-open .main-panel {
    margin-right: 400px;
  }

  .detail-panel {
    width: 400px;
  }

  .agents-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }

  .dashboard-title {
    font-size: var(--font-size-3xl);
  }
}

@media screen and (max-width: 768px) {
  .app.detail-open .main-panel {
    margin-right: 0;
  }

  .detail-panel {
    width: 100%;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .stats-bar {
    gap: var(--space-4);
  }

  .agents-grid {
    grid-template-columns: 1fr;
  }

  .detail-info-grid {
    grid-template-columns: 1fr;
  }
}
"""
