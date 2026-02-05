"""
HTML/CSS/JS templates for Swarm Dashboard.

This module provides the embedded dashboard templates that are served
by the HTTP server. Separating templates into modules allows for easier
maintenance and testing.
"""

from swarm_dashboard.templates.css import DASHBOARD_CSS
from swarm_dashboard.templates.html import DASHBOARD_HTML_BODY
from swarm_dashboard.templates.js import DASHBOARD_JS


def get_dashboard_html() -> str:
    """
    Get the complete dashboard HTML page.

    Combines the CSS, HTML body, and JavaScript into a single
    self-contained HTML document.

    Returns:
        Complete HTML document as a string.
    """
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Swarm Dashboard v6 - Capybara-Inspired Color Palette">
  <title>Swarm Dashboard v6</title>

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">

  <style>
{DASHBOARD_CSS}
  </style>
</head>
<body>
{DASHBOARD_HTML_BODY}
  <script>
{DASHBOARD_JS}
  </script>
</body>
</html>"""


__all__ = [
    "DASHBOARD_CSS",
    "DASHBOARD_HTML_BODY",
    "DASHBOARD_JS",
    "get_dashboard_html",
]
