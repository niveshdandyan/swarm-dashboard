"""
JSONL parsing and event extraction for Swarm Dashboard.

This module provides functions for parsing newline-delimited JSON (JSONL)
output files and extracting relevant information like tool usage,
live events, and files created.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from swarm_dashboard.config import (
    COMPLETION_MARKERS,
    MAX_CONTENT_LENGTH,
    MAX_LIVE_EVENTS,
)
from swarm_dashboard.tracker import parse_cache

logger = logging.getLogger(__name__)


def parse_json_lines(content: str) -> List[Dict[str, Any]]:
    """
    Parse content as newline-delimited JSON (NDJSON/JSONL).

    Each line is expected to be a valid JSON object. Invalid lines
    are silently skipped.

    Args:
        content: String content with one JSON object per line.

    Returns:
        List of parsed JSON objects.

    Example:
        >>> content = '{"type": "tool", "name": "Write"}\\n{"type": "result"}'
        >>> events = parse_json_lines(content)
        >>> len(events)
        2
    """
    events = []
    for line in content.split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def extract_tool_usage(events: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Extract tool usage statistics from parsed events.

    Counts how many times each tool (Read, Write, Bash, etc.) was used.

    Args:
        events: List of parsed event objects.

    Returns:
        Dictionary mapping tool names to usage counts.

    Example:
        >>> events = [{"name": "Write"}, {"name": "Write"}, {"name": "Read"}]
        >>> extract_tool_usage(events)
        {'Write': 2, 'Read': 1}
    """
    tools_used: Dict[str, int] = {}

    for event in events:
        # Direct tool invocation
        if "name" in event:
            tool_name = event["name"]
            tools_used[tool_name] = tools_used.get(tool_name, 0) + 1

        # Tool use in assistant messages
        if event.get("type") == "assistant" and "message" in event:
            msg = event["message"]
            if "content" in msg and isinstance(msg["content"], list):
                for item in msg["content"]:
                    if isinstance(item, dict) and item.get("type") == "tool_use":
                        tool_name = item.get("name", "unknown")
                        tools_used[tool_name] = tools_used.get(tool_name, 0) + 1

    return tools_used


def extract_live_events(
    events: List[Dict[str, Any]], max_events: int = MAX_LIVE_EVENTS
) -> List[Dict[str, Any]]:
    """
    Extract live events with timestamp preservation.

    Converts raw events into a normalized format suitable for
    displaying in the live activity feed.

    Args:
        events: List of parsed event objects.
        max_events: Maximum number of events to return.

    Returns:
        List of normalized event objects with type, tool, content, timestamp.
    """
    live_events = []

    for event in events[-max_events:]:
        live_event = {
            "type": event.get("type", "unknown"),
            "tool": event.get("name", ""),
            "content": str(event.get("content", ""))[:MAX_CONTENT_LENGTH],
            "timestamp": event.get("timestamp"),
            "uuid": event.get("uuid"),
        }

        # Handle assistant messages with tool_use
        if event.get("type") == "assistant" and "message" in event:
            msg = event["message"]
            if "content" in msg and isinstance(msg["content"], list):
                for item in msg["content"]:
                    if isinstance(item, dict):
                        if item.get("type") == "tool_use":
                            live_events.append(
                                {
                                    "type": "tool_use",
                                    "tool": item.get("name", ""),
                                    "content": str(item.get("input", ""))[
                                        :MAX_CONTENT_LENGTH
                                    ],
                                    "timestamp": event.get("timestamp"),
                                    "uuid": item.get("id"),
                                }
                            )
                        elif item.get("type") == "text":
                            live_events.append(
                                {
                                    "type": "text",
                                    "tool": "",
                                    "content": str(item.get("text", ""))[
                                        :MAX_CONTENT_LENGTH
                                    ],
                                    "timestamp": event.get("timestamp"),
                                    "uuid": event.get("uuid"),
                                }
                            )
        else:
            live_events.append(live_event)

    return live_events[-max_events:]


def extract_files_created(
    events: List[Dict[str, Any]], max_files: int = 20
) -> List[str]:
    """
    Extract list of files created from events.

    Looks for Write, Edit, and NotebookEdit tool invocations.

    Args:
        events: List of parsed event objects.
        max_files: Maximum number of files to return.

    Returns:
        List of file paths that were created/modified.
    """
    files: set[str] = set()

    for event in events:
        # Direct tool invocation
        if event.get("name") in ("Write", "Edit", "NotebookEdit"):
            input_data = event.get("input", {})
            if isinstance(input_data, dict):
                filepath = input_data.get("file_path") or input_data.get(
                    "notebook_path"
                )
                if filepath:
                    files.add(filepath)

        # Tool use in assistant messages
        if event.get("type") == "assistant" and "message" in event:
            msg = event["message"]
            if "content" in msg and isinstance(msg["content"], list):
                for item in msg["content"]:
                    is_write_tool = (
                        isinstance(item, dict)
                        and item.get("type") == "tool_use"
                        and item.get("name") in ("Write", "Edit", "NotebookEdit")
                    )
                    if is_write_tool:
                        input_data = item.get("input", {})
                        if isinstance(input_data, dict):
                            filepath = input_data.get(
                                "file_path"
                            ) or input_data.get("notebook_path")
                            if filepath:
                                files.add(filepath)

    return list(files)[:max_files]


def parse_agent_output(
    output_file: Optional[str], use_cache: bool = True
) -> Dict[str, Any]:
    """
    Parse an agent output file with caching.

    This is the main entry point for parsing agent output. It handles
    file reading, caching, completion detection, and event extraction.

    Args:
        output_file: Path to the output file (JSONL format).
        use_cache: Whether to use the parse cache.

    Returns:
        Dictionary with keys: tools_used, last_activity, activity,
        progress, is_complete, total_events, files_created, live_events.
    """
    result: Dict[str, Any] = {
        "tools_used": {},
        "last_activity": None,
        "activity": "Working...",
        "progress": 0,
        "is_complete": False,
        "total_events": 0,
        "files_created": [],
        "live_events": [],
    }

    if not output_file or not os.path.exists(output_file):
        return result

    try:
        mtime = os.path.getmtime(output_file)
        result["last_activity"] = datetime.fromtimestamp(mtime, tz=timezone.utc)

        # Check cache
        if use_cache:
            cached = parse_cache.get(output_file, mtime)
            if cached is not None:
                return cached

        # Read file content
        with open(output_file, encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if not content:
            return result

        # Check completion markers
        for marker in COMPLETION_MARKERS:
            if marker in content:
                result["is_complete"] = True
                result["progress"] = 100
                break

        # Parse JSON lines
        events = parse_json_lines(content)
        result["total_events"] = len(events)

        if events:
            result["tools_used"] = extract_tool_usage(events)
            result["live_events"] = extract_live_events(events)
            result["files_created"] = extract_files_created(events)

            # Estimate progress from event count
            if not result["is_complete"]:
                result["progress"] = min(90, len(events) // 5)

            # Set activity description
            event_count = len(events)
            result["activity"] = f"{event_count} events"

        # Cache result
        if use_cache:
            parse_cache.put(output_file, mtime, result)

        return result

    except Exception as e:
        logger.error(f"Error parsing agent output {output_file}: {e}")
        return result


def read_json_file(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Read and parse a JSON file.

    Args:
        filepath: Path to the JSON file.

    Returns:
        Parsed JSON content or None if read fails.
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
            return data
    except Exception:
        return None


def get_file_mtime(filepath: str) -> Optional[datetime]:
    """
    Get the modification time of a file.

    Handles symlinks by resolving to the real path.

    Args:
        filepath: Path to the file.

    Returns:
        Modification time as datetime, or None if unavailable.
    """
    try:
        if os.path.islink(filepath):
            real_path = os.path.realpath(filepath)
            if os.path.exists(real_path):
                return datetime.fromtimestamp(
                    os.path.getmtime(real_path), tz=timezone.utc
                )
        if os.path.exists(filepath):
            return datetime.fromtimestamp(os.path.getmtime(filepath), tz=timezone.utc)
    except Exception:
        pass
    return None


def format_time_ago(dt: Optional[datetime]) -> str:
    """
    Format a datetime as a human-readable "X ago" string.

    Args:
        dt: Datetime to format.

    Returns:
        Human-readable string like "5s ago", "2m ago", "1h ago".
    """
    if not dt:
        return "Unknown"

    now = datetime.now(timezone.utc)
    diff = now - dt
    seconds = int(diff.total_seconds())

    if seconds < 0:
        return "Just now"
    elif seconds < 60:
        return f"{seconds}s ago"
    elif seconds < 3600:
        return f"{seconds // 60}m ago"
    elif seconds < 86400:
        return f"{seconds // 3600}h ago"
    else:
        return f"{seconds // 86400}d ago"
