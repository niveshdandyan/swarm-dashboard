"""Tests for parser module."""



from swarm_dashboard.parser import (
    extract_files_created,
    extract_live_events,
    extract_tool_usage,
    format_time_ago,
    parse_json_lines,
)


class TestParseJsonLines:
    """Tests for parse_json_lines function."""

    def test_parse_valid_jsonl(self):
        """Test parsing valid JSONL content."""
        content = '{"a": 1}\n{"b": 2}\n{"c": 3}'
        events = parse_json_lines(content)
        assert len(events) == 3
        assert events[0] == {"a": 1}
        assert events[1] == {"b": 2}
        assert events[2] == {"c": 3}

    def test_parse_with_empty_lines(self):
        """Test parsing JSONL with empty lines."""
        content = '{"a": 1}\n\n{"b": 2}\n\n'
        events = parse_json_lines(content)
        assert len(events) == 2

    def test_parse_with_invalid_json(self):
        """Test parsing JSONL with invalid lines."""
        content = '{"a": 1}\nnot json\n{"b": 2}'
        events = parse_json_lines(content)
        assert len(events) == 2  # Invalid line skipped

    def test_parse_empty_content(self):
        """Test parsing empty content."""
        events = parse_json_lines("")
        assert len(events) == 0


class TestExtractToolUsage:
    """Tests for extract_tool_usage function."""

    def test_extract_direct_tools(self):
        """Test extracting direct tool invocations."""
        events = [
            {"name": "Read"},
            {"name": "Write"},
            {"name": "Read"},
            {"name": "Bash"},
        ]
        tools = extract_tool_usage(events)
        assert tools["Read"] == 2
        assert tools["Write"] == 1
        assert tools["Bash"] == 1

    def test_extract_tools_from_assistant_messages(self):
        """Test extracting tools from assistant messages."""
        events = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "tool_use", "name": "Read"},
                        {"type": "tool_use", "name": "Write"},
                    ]
                },
            }
        ]
        tools = extract_tool_usage(events)
        assert tools["Read"] == 1
        assert tools["Write"] == 1

    def test_extract_empty_events(self):
        """Test extracting from empty events."""
        tools = extract_tool_usage([])
        assert tools == {}


class TestExtractFilesCreated:
    """Tests for extract_files_created function."""

    def test_extract_write_files(self):
        """Test extracting files from Write events."""
        events = [
            {"name": "Write", "input": {"file_path": "/test/a.py"}},
            {"name": "Write", "input": {"file_path": "/test/b.py"}},
        ]
        files = extract_files_created(events)
        assert "/test/a.py" in files
        assert "/test/b.py" in files

    def test_extract_edit_files(self):
        """Test extracting files from Edit events."""
        events = [
            {"name": "Edit", "input": {"file_path": "/test/c.py"}},
        ]
        files = extract_files_created(events)
        assert "/test/c.py" in files

    def test_deduplicate_files(self):
        """Test that duplicate files are removed."""
        events = [
            {"name": "Write", "input": {"file_path": "/test/a.py"}},
            {"name": "Edit", "input": {"file_path": "/test/a.py"}},
        ]
        files = extract_files_created(events)
        assert files.count("/test/a.py") == 1

    def test_max_files_limit(self):
        """Test max files limit."""
        events = [
            {"name": "Write", "input": {"file_path": f"/test/{i}.py"}}
            for i in range(30)
        ]
        files = extract_files_created(events, max_files=10)
        assert len(files) == 10


class TestExtractLiveEvents:
    """Tests for extract_live_events function."""

    def test_extract_events(self):
        """Test extracting live events."""
        events = [
            {"type": "tool", "name": "Read", "content": "test"},
        ]
        live = extract_live_events(events)
        assert len(live) == 1
        assert live[0]["type"] == "tool"

    def test_max_events_limit(self):
        """Test max events limit."""
        events = [{"type": "tool", "name": f"Tool{i}"} for i in range(50)]
        live = extract_live_events(events, max_events=10)
        assert len(live) == 10


class TestFormatTimeAgo:
    """Tests for format_time_ago function."""

    def test_format_none(self):
        """Test formatting None."""
        assert format_time_ago(None) == "Unknown"

    def test_format_seconds(self):
        """Test formatting seconds."""
        from datetime import datetime, timedelta, timezone

        now = datetime.now(timezone.utc)
        dt = now - timedelta(seconds=30)
        result = format_time_ago(dt)
        assert "s ago" in result

    def test_format_minutes(self):
        """Test formatting minutes."""
        from datetime import datetime, timedelta, timezone

        now = datetime.now(timezone.utc)
        dt = now - timedelta(minutes=5)
        result = format_time_ago(dt)
        assert "m ago" in result

    def test_format_hours(self):
        """Test formatting hours."""
        from datetime import datetime, timedelta, timezone

        now = datetime.now(timezone.utc)
        dt = now - timedelta(hours=2)
        result = format_time_ago(dt)
        assert "h ago" in result
