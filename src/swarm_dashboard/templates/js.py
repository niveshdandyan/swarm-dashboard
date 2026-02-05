"""
JavaScript for Swarm Dashboard.

Handles API polling, DOM updates, theme switching, and detail panel interactions.
"""

DASHBOARD_JS = """
    // State
    let selectedAgent = null;
    let lastData = null;

    // Theme handling
    function initTheme() {
      const saved = localStorage.getItem('swarm-dashboard-theme');
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const theme = saved || (prefersDark ? 'dark' : 'light');
      setTheme(theme);
    }

    function setTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('swarm-dashboard-theme', theme);

      const lightIcon = document.getElementById('theme-icon-light');
      const darkIcon = document.getElementById('theme-icon-dark');

      if (theme === 'dark') {
        lightIcon.style.display = 'none';
        darkIcon.style.display = 'block';
      } else {
        lightIcon.style.display = 'block';
        darkIcon.style.display = 'none';
      }
    }

    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme');
      setTheme(current === 'dark' ? 'light' : 'dark');
    }

    // Event listeners
    document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
    document.getElementById('detail-close').addEventListener('click', closeDetailPanel);
    document.getElementById('overlay').addEventListener('click', closeDetailPanel);

    // Fetch status from API
    async function fetchStatus() {
      try {
        const response = await fetch('/api/status');
        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        lastData = data;
        updateDashboard(data);
        setConnectionStatus(true);
      } catch (error) {
        console.error('Error fetching status:', error);
        setConnectionStatus(false);
      }
    }

    function setConnectionStatus(connected) {
      const el = document.getElementById('connection-status');
      const text = document.getElementById('connection-text');

      if (connected) {
        el.classList.remove('disconnected');
        el.classList.add('connected');
        text.textContent = 'Connected';
      } else {
        el.classList.remove('connected');
        el.classList.add('disconnected');
        text.textContent = 'Disconnected';
      }
    }

    // Update dashboard UI
    function updateDashboard(data) {
      // Update title
      document.getElementById('swarm-name').textContent = data.swarm_name || 'Agent Swarm';

      // Update stats
      document.getElementById('running-count').textContent = data.running_count || 0;
      document.getElementById('idle-count').textContent = data.idle_count || 0;
      document.getElementById('completed-count').textContent = data.completed_count || 0;
      document.getElementById('pending-count').textContent = data.pending_count || 0;
      document.getElementById('failed-count').textContent = data.failed_count || 0;

      // Update agents
      updateWavesAndAgents(data.agents || {});

      // Update detail panel if open
      if (selectedAgent && data.agents && data.agents[selectedAgent]) {
        fetchAgentDetails(selectedAgent);
      }
    }

    // Group agents by wave and render
    function updateWavesAndAgents(agents) {
      const container = document.getElementById('waves-container');

      // Group by wave
      const waves = {};
      Object.entries(agents).forEach(([id, agent]) => {
        const wave = agent.wave || 1;
        if (!waves[wave]) waves[wave] = [];
        waves[wave].push({ id, ...agent });
      });

      // Sort waves
      const sortedWaves = Object.keys(waves).sort((a, b) => Number(a) - Number(b));

      // Render
      container.innerHTML = sortedWaves.map(waveNum => {
        const waveAgents = waves[waveNum];
        return `
          <section class="wave-section">
            <div class="wave-header">
              <span class="wave-badge">Wave ${waveNum}</span>
              <h2 class="wave-title">${waveAgents.length} Agent${waveAgents.length !== 1 ? 's' : ''}</h2>
            </div>
            <div class="agents-grid">
              ${waveAgents.map(agent => createAgentCardHtml(agent)).join('')}
            </div>
          </section>
        `;
      }).join('');

      // Re-attach click handlers
      document.querySelectorAll('.agent-card').forEach(card => {
        card.addEventListener('click', () => selectAgent(card.dataset.agentId));
      });
    }

    // Create agent card HTML
    function createAgentCardHtml(agent) {
      const status = agent.status || 'pending';
      const progress = agent.progress || 0;
      const isSelected = selectedAgent === agent.id;
      const activityClass = agent.is_idle ? 'stale' : '';

      // Top 3 tools
      const toolsHtml = Object.entries(agent.tools_used || {})
        .slice(0, 3)
        .map(([tool, count]) => `<span class="tool-badge">${tool}: ${count}</span>`)
        .join('');

      return `
        <article class="agent-card ${status} ${isSelected ? 'selected' : ''}" data-agent-id="${agent.id}">
          <div class="agent-card-header">
            <h3 class="agent-role">${escapeHtml(agent.role || agent.id)}</h3>
            <span class="status-badge ${status}">
              <span class="status-dot"></span>
              ${status}
            </span>
          </div>
          <p class="agent-activity ${activityClass}">
            ${agent.last_activity_ago || 'No activity'}
          </p>
          <div class="progress-bar">
            <div class="progress-fill" style="width: ${progress}%"></div>
          </div>
          <div class="agent-tools">${toolsHtml}</div>
        </article>
      `;
    }

    // Select agent and show detail panel
    async function selectAgent(agentId) {
      selectedAgent = agentId;

      // Update UI
      document.querySelectorAll('.agent-card').forEach(card => {
        card.classList.toggle('selected', card.dataset.agentId === agentId);
      });

      document.getElementById('app').classList.add('detail-open');
      document.getElementById('detail-panel').classList.add('open');
      document.getElementById('detail-panel').setAttribute('aria-hidden', 'false');

      // Fetch details
      await fetchAgentDetails(agentId);
    }

    // Fetch agent details
    async function fetchAgentDetails(agentId) {
      try {
        const response = await fetch(`/api/agent/${agentId}`);
        if (!response.ok) throw new Error('Failed to fetch agent details');

        const details = await response.json();
        renderAgentDetails(agentId, details);
      } catch (error) {
        console.error('Error fetching agent details:', error);
      }
    }

    // Render agent details in panel
    function renderAgentDetails(agentId, details) {
      document.getElementById('detail-title').textContent = details.role || agentId;
      document.getElementById('detail-subtitle').textContent = agentId;

      const content = document.getElementById('detail-content');

      // Tool stats
      const toolsHtml = Object.entries(details.tools_used || {})
        .map(([tool, count]) => `
          <div class="tool-stat">
            <span class="tool-name">${tool}</span>
            <span class="tool-count">${count}</span>
          </div>
        `).join('') || '<p style="color: var(--color-text-secondary)">No tools used yet</p>';

      // Files
      const filesHtml = (details.files_created || [])
        .map(file => `
          <div class="file-item">
            <span class="file-icon">&#128196;</span>
            <span>${escapeHtml(file)}</span>
          </div>
        `).join('') || '<p style="color: var(--color-text-secondary); padding: var(--space-3);">No files created yet</p>';

      // Live events
      const eventsHtml = (details.live_events || [])
        .slice(-50)
        .reverse()
        .map(event => {
          const iconClass = event.type === 'tool' ? 'tool' :
                           event.type === 'thinking' ? 'thinking' : 'result';
          const icon = event.type === 'tool' ? '&#9889;' :
                      event.type === 'thinking' ? '&#128173;' : '&#10003;';

          let contentHtml = '';
          if (event.type === 'tool') {
            contentHtml = `
              <span class="activity-tool">${escapeHtml(event.tool || '')}</span>
              <div class="activity-text">${escapeHtml(event.content || '')}</div>
            `;
          } else {
            contentHtml = `<div class="activity-text">${escapeHtml(event.content || '')}</div>`;
          }

          return `
            <div class="activity-item">
              <div class="activity-icon ${iconClass}">${icon}</div>
              <div class="activity-content">${contentHtml}</div>
            </div>
          `;
        }).join('') || '<p style="color: var(--color-text-secondary); padding: var(--space-3);">No activity yet</p>';

      const lastActivityClass = details.is_idle ? 'stale' : '';

      content.innerHTML = `
        <div class="detail-section">
          <h3 class="detail-section-title">Status</h3>
          <div class="detail-info-grid">
            <div class="detail-info-item">
              <div class="detail-info-label">Status</div>
              <div class="detail-info-value">${details.status || 'Unknown'}</div>
            </div>
            <div class="detail-info-item">
              <div class="detail-info-label">Progress</div>
              <div class="detail-info-value">${details.progress || 0}%</div>
            </div>
            <div class="detail-info-item">
              <div class="detail-info-label">Wave</div>
              <div class="detail-info-value">${details.wave || 1}</div>
            </div>
            <div class="detail-info-item">
              <div class="detail-info-label">Events</div>
              <div class="detail-info-value">${details.total_events || 0}</div>
            </div>
            <div class="detail-info-item full-width">
              <div class="detail-info-label">Last Activity</div>
              <div class="detail-info-value ${lastActivityClass}">${details.last_activity_ago || 'Never'}</div>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h3 class="detail-section-title">Mission</h3>
          <p style="color: var(--color-text-secondary); padding: var(--space-3); background: var(--color-bg-secondary); border-radius: var(--radius-lg);">
            ${escapeHtml(details.mission || 'No mission specified')}
          </p>
        </div>

        <div class="detail-section">
          <h3 class="detail-section-title">Tools Used</h3>
          <div class="detail-tools-grid">${toolsHtml}</div>
        </div>

        <div class="detail-section">
          <h3 class="detail-section-title">Files Created</h3>
          <div class="files-list">${filesHtml}</div>
        </div>

        <div class="detail-section">
          <h3 class="detail-section-title">Live Activity Feed</h3>
          <div class="activity-feed">${eventsHtml}</div>
        </div>
      `;
    }

    // Close detail panel
    function closeDetailPanel() {
      selectedAgent = null;
      document.getElementById('app').classList.remove('detail-open');
      document.getElementById('detail-panel').classList.remove('open');
      document.getElementById('detail-panel').setAttribute('aria-hidden', 'true');

      document.querySelectorAll('.agent-card').forEach(card => {
        card.classList.remove('selected');
      });
    }

    // Escape HTML to prevent XSS
    function escapeHtml(text) {
      if (!text) return '';
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }

    // Initialize
    initTheme();
    fetchStatus();
    setInterval(fetchStatus, 2000);
"""
