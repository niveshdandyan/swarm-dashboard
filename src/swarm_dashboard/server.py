"""
HTTP server for Swarm Dashboard.

Provides a lightweight HTTP server with API endpoints for
monitoring agent swarms.
"""

from __future__ import annotations

import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from swarm_dashboard.agents import AgentStatusManager
from swarm_dashboard.config import Config
from swarm_dashboard.templates import get_dashboard_html

logger = logging.getLogger(__name__)


class DashboardHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for the dashboard.

    Handles the following endpoints:
    - GET /           - Dashboard HTML page
    - GET /api/status - Swarm status JSON
    - GET /api/agent/{id} - Agent details JSON
    - GET /health     - Health check
    """

    # Class-level references set by DashboardServer
    config: Config
    agent_manager: AgentStatusManager

    def do_GET(self) -> None:
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            if path == "/" or path == "/index.html":
                self._send_dashboard()
            elif path == "/api/status":
                self._send_status()
            elif path.startswith("/api/agent/"):
                agent_id = path[len("/api/agent/") :]
                self._send_agent_details(agent_id)
            elif path == "/health":
                self._send_health()
            else:
                self._send_not_found()
        except Exception as e:
            logger.error(f"Error handling request {path}: {e}")
            self._send_error(500, str(e))

    def _send_dashboard(self) -> None:
        """Send the dashboard HTML page."""
        html = get_dashboard_html()
        self._send_response(200, html.encode("utf-8"), "text/html; charset=utf-8")

    def _send_status(self) -> None:
        """Send the swarm status as JSON."""
        status = self.agent_manager.get_swarm_status()
        self._send_json(status)

    def _send_agent_details(self, agent_id: str) -> None:
        """Send details for a specific agent."""
        details = self.agent_manager.get_agent_details(agent_id)
        self._send_json(details)

    def _send_health(self) -> None:
        """Send health check response."""
        self._send_json({"status": "ok", "version": "v6"})

    def _send_not_found(self) -> None:
        """Send 404 response."""
        self._send_json({"error": "Not found"}, 404)

    def _send_error(self, code: int, message: str) -> None:
        """Send error response."""
        self._send_json({"error": message}, code)

    def _send_json(self, data: Dict[str, Any], status: int = 200) -> None:
        """Send JSON response."""
        body = json.dumps(data, indent=2).encode("utf-8")
        self._send_response(status, body, "application/json")

    def _send_response(
        self, status: int, body: bytes, content_type: str
    ) -> None:
        """Send HTTP response."""
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        """Log HTTP requests."""
        logger.debug(f"{self.address_string()} - {format % args}")


class DashboardServer:
    """
    Dashboard HTTP server.

    Wraps HTTPServer with configuration and lifecycle management.

    Example:
        config = Config.from_env()
        server = DashboardServer(config)
        server.serve_forever()
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize the dashboard server.

        Args:
            config: Dashboard configuration.
        """
        self.config = config
        self.agent_manager = AgentStatusManager(config)

        # Set class-level references for handler
        DashboardHandler.config = config
        DashboardHandler.agent_manager = self.agent_manager

        # Create server
        self._server: Optional[HTTPServer] = None

    def serve_forever(self) -> None:
        """Start the server and block until shutdown."""
        self._server = HTTPServer(
            ("0.0.0.0", self.config.port), DashboardHandler
        )
        logger.info(f"Dashboard running at http://localhost:{self.config.port}/")
        try:
            self._server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        finally:
            self.shutdown()

    def shutdown(self) -> None:
        """Shutdown the server."""
        if self._server:
            self._server.shutdown()
            self._server = None

    @property
    def server_address(self) -> tuple[str, int]:
        """Get the server address."""
        if self._server:
            return self._server.server_address
        return ("0.0.0.0", self.config.port)


def run_server(config: Optional[Config] = None) -> None:
    """
    Run the dashboard server.

    Convenience function for starting the server with default or
    provided configuration.

    Args:
        config: Optional configuration. Uses environment if not provided.
    """
    if config is None:
        config = Config.from_env()

    server = DashboardServer(config)
    server.serve_forever()
