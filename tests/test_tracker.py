"""Tests for tracker module."""

import os
import time

import pytest

from swarm_dashboard.tracker import BoundedParseCache, FilePositionTracker


class TestFilePositionTracker:
    """Tests for FilePositionTracker class."""

    def test_get_new_content_nonexistent_file(self):
        """Test getting content from nonexistent file."""
        tracker = FilePositionTracker()
        content = tracker.get_new_content("/nonexistent/file.txt")
        assert content is None

    def test_get_new_content_first_read(self, temp_dir):
        """Test first read gets all content."""
        tracker = FilePositionTracker()
        filepath = os.path.join(temp_dir, "test.txt")

        with open(filepath, "w") as f:
            f.write("line1\nline2\nline3")

        content = tracker.get_new_content(filepath)
        assert content == "line1\nline2\nline3"

    def test_get_new_content_incremental(self, temp_dir):
        """Test incremental reads only get new content."""
        tracker = FilePositionTracker()
        filepath = os.path.join(temp_dir, "test.txt")

        # Initial write
        with open(filepath, "w") as f:
            f.write("line1\n")

        content1 = tracker.get_new_content(filepath)
        assert content1 == "line1\n"

        # Append more content
        time.sleep(0.01)  # Ensure mtime changes
        with open(filepath, "a") as f:
            f.write("line2\n")

        content2 = tracker.get_new_content(filepath)
        assert content2 == "line2\n"

    def test_get_new_content_no_changes(self, temp_dir):
        """Test no new content when file unchanged."""
        tracker = FilePositionTracker()
        filepath = os.path.join(temp_dir, "test.txt")

        with open(filepath, "w") as f:
            f.write("content")

        tracker.get_new_content(filepath)  # First read
        content = tracker.get_new_content(filepath)  # Second read
        assert content is None  # No changes

    def test_reset_specific_file(self, temp_dir):
        """Test resetting tracker for specific file."""
        tracker = FilePositionTracker()
        filepath = os.path.join(temp_dir, "test.txt")

        with open(filepath, "w") as f:
            f.write("content")

        tracker.get_new_content(filepath)
        tracker.reset(filepath)

        # Should get all content again after reset
        content = tracker.get_new_content(filepath)
        assert content == "content"

    def test_reset_all_files(self, temp_dir):
        """Test resetting tracker for all files."""
        tracker = FilePositionTracker()

        for i in range(3):
            filepath = os.path.join(temp_dir, f"test{i}.txt")
            with open(filepath, "w") as f:
                f.write(f"content{i}")
            tracker.get_new_content(filepath)

        tracker.reset()
        assert tracker.get_tracked_files() == []


class TestBoundedParseCache:
    """Tests for BoundedParseCache class."""

    def test_put_and_get(self):
        """Test storing and retrieving from cache."""
        cache = BoundedParseCache(max_size=10)
        result = {"tools": {"Read": 5}}

        cache.put("/test/file.txt", 1000.0, result)
        retrieved = cache.get("/test/file.txt", 1000.0)

        assert retrieved == result

    def test_get_miss(self):
        """Test cache miss returns None."""
        cache = BoundedParseCache()
        result = cache.get("/nonexistent", 0.0)
        assert result is None

    def test_eviction_on_full(self):
        """Test LRU eviction when cache is full."""
        cache = BoundedParseCache(max_size=3)

        # Fill cache
        cache.put("/file1", 100.0, {"a": 1})
        cache.put("/file2", 200.0, {"b": 2})
        cache.put("/file3", 300.0, {"c": 3})

        # Add one more - should evict oldest (file1)
        cache.put("/file4", 400.0, {"d": 4})

        assert cache.get("/file1", 100.0) is None  # Evicted
        assert cache.get("/file2", 200.0) is not None
        assert cache.get("/file4", 400.0) is not None

    def test_invalidate_specific_file(self):
        """Test invalidating specific file."""
        cache = BoundedParseCache()
        cache.put("/file1", 100.0, {"a": 1})
        cache.put("/file1", 200.0, {"a": 2})  # Different mtime
        cache.put("/file2", 100.0, {"b": 1})

        cache.invalidate("/file1")

        assert cache.get("/file1", 100.0) is None
        assert cache.get("/file1", 200.0) is None
        assert cache.get("/file2", 100.0) is not None

    def test_invalidate_all(self):
        """Test invalidating all entries."""
        cache = BoundedParseCache()
        cache.put("/file1", 100.0, {"a": 1})
        cache.put("/file2", 100.0, {"b": 1})

        cache.invalidate()

        assert cache.size == 0

    def test_size_property(self):
        """Test size property."""
        cache = BoundedParseCache()
        assert cache.size == 0

        cache.put("/file1", 100.0, {})
        cache.put("/file2", 100.0, {})
        assert cache.size == 2
