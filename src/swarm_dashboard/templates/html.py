"""
HTML body structure for Swarm Dashboard.
"""

DASHBOARD_HTML_BODY = """
  <div id="app" class="app">
    <div class="main-panel">
      <header class="header">
        <div class="container">
          <div class="header-content">
            <h1 class="dashboard-title" id="swarm-name">Agent Swarm</h1>
            <div class="header-actions">
              <button class="theme-toggle" id="theme-toggle" title="Toggle theme" aria-label="Toggle theme">
                <svg id="theme-icon-light" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="5"></circle>
                  <line x1="12" y1="1" x2="12" y2="3"></line>
                  <line x1="12" y1="21" x2="12" y2="23"></line>
                  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                  <line x1="1" y1="12" x2="3" y2="12"></line>
                  <line x1="21" y1="12" x2="23" y2="12"></line>
                  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                </svg>
                <svg id="theme-icon-dark" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: none;">
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>

      <main class="container">
        <div class="stats-bar" id="stats-bar">
          <div class="stat-item running">
            <span class="stat-value" id="running-count">0</span>
            <span class="stat-label">Running</span>
          </div>
          <div class="stat-item idle">
            <span class="stat-value" id="idle-count">0</span>
            <span class="stat-label">Idle</span>
          </div>
          <div class="stat-item completed">
            <span class="stat-value" id="completed-count">0</span>
            <span class="stat-label">Completed</span>
          </div>
          <div class="stat-item pending">
            <span class="stat-value" id="pending-count">0</span>
            <span class="stat-label">Pending</span>
          </div>
          <div class="stat-item failed">
            <span class="stat-value" id="failed-count">0</span>
            <span class="stat-label">Failed</span>
          </div>
        </div>

        <div class="waves-container" id="waves-container">
          <!-- Waves and agents will be dynamically inserted here -->
        </div>
      </main>
    </div>

    <!-- Detail Panel (Slide-in Sidebar) -->
    <div class="detail-panel" id="detail-panel" aria-hidden="true">
      <div class="detail-panel-header">
        <div class="detail-panel-title">
          <h2 id="detail-title">Agent Details</h2>
          <p class="detail-panel-subtitle" id="detail-subtitle">agent-id</p>
        </div>
        <button class="detail-panel-close" id="detail-close" aria-label="Close panel">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      <div class="detail-panel-content" id="detail-content">
        <!-- Agent details will be dynamically inserted here -->
      </div>
    </div>

    <!-- Overlay for mobile -->
    <div class="overlay" id="overlay"></div>
  </div>

  <!-- Connection Status -->
  <div class="connection-status connected" id="connection-status">
    <span class="status-dot"></span>
    <span id="connection-text">Connected</span>
  </div>
"""
