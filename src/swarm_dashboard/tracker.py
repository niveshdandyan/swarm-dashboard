"""
File tracking and caching utilities for Swarm Dashboard.

This module provides efficient file position tracking for incremental reads
and a bounded LRU-style cache for parsed output results.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional, Tuple

from swarm_dashboard.config import MAX_CACHE_SIZE

logger = logging.getLogger(__name__)


class FilePositionTracker:
    """
    Tracks file positions for incremental reading.

    Instead of re-reading entire files on each poll, this class tracks
    the last read position and only reads new content. This significantly
    reduces I/O overhead for large, frequently-updated files.

    Example:
        tracker = FilePositionTracker()
        new_content = tracker.get_new_content("/path/to/file.jsonl")
        if new_content:
            process(new_content)
    """

    def __init__(self) -> None:
        """Initialize the file position tracker."""
        self._positions: Dict[str, int] = {}
        self._sizes: Dict[str, int] = {}
        self._mtimes: Dict[str, float] = {}

    def get_new_content(self, filepath: str) -> Optional[str]:
        """
        Get new content from a file since the last read.

        Args:
            filepath: Path to the file to read.

        Returns:
            New content if available, None if no new content or file doesn't exist.
        """
        if not os.path.exists(filepath):
            return None

        try:
            stat = os.stat(filepath)
            current_size = stat.st_size
            current_mtime = stat.st_mtime

            last_pos = self._positions.get(filepath, 0)
            last_size = self._sizes.get(filepath, 0)
            last_mtime = self._mtimes.get(filepath, 0)

            # File was truncated - start from beginning
            if current_size < last_size:
                last_pos = 0

            # No changes since last read
            if current_mtime == last_mtime and current_size == last_size:
                return None

            # Read new content
            with open(filepath, encoding="utf-8", errors="ignore") as f:
                f.seek(last_pos)
                content = f.read()
                new_pos = f.tell()

            # Update tracking state
            self._positions[filepath] = new_pos
            self._sizes[filepath] = current_size
            self._mtimes[filepath] = current_mtime

            return content

        except Exception as e:
            logger.error(f"Error reading new content from {filepath}: {e}")
            return None

    def reset(self, filepath: Optional[str] = None) -> None:
        """
        Reset tracking state for a file or all files.

        Args:
            filepath: Specific file to reset, or None to reset all files.
        """
        if filepath:
            self._positions.pop(filepath, None)
            self._sizes.pop(filepath, None)
            self._mtimes.pop(filepath, None)
        else:
            self._positions.clear()
            self._sizes.clear()
            self._mtimes.clear()

    def get_position(self, filepath: str) -> int:
        """Get the current tracked position for a file."""
        return self._positions.get(filepath, 0)

    def get_tracked_files(self) -> list[str]:
        """Get list of all tracked files."""
        return list(self._positions.keys())


class BoundedParseCache:
    """
    LRU-style cache for parsed output results.

    Prevents memory bloat by limiting the number of cached entries.
    When the cache is full, the oldest entry (by mtime) is evicted.

    Example:
        cache = BoundedParseCache(max_size=50)
        result = cache.get(filepath, mtime)
        if result is None:
            result = parse_file(filepath)
            cache.put(filepath, mtime, result)
    """

    def __init__(self, max_size: int = MAX_CACHE_SIZE) -> None:
        """
        Initialize the bounded cache.

        Args:
            max_size: Maximum number of entries to cache.
        """
        self._cache: Dict[Tuple[str, float], Dict[str, Any]] = {}
        self._max_size = max_size

    def get(self, filepath: str, mtime: float) -> Optional[Dict[str, Any]]:
        """
        Get a cached result if available.

        Args:
            filepath: Path to the file.
            mtime: Modification time of the file.

        Returns:
            Cached result or None if not in cache.
        """
        return self._cache.get((filepath, mtime))

    def put(self, filepath: str, mtime: float, result: Dict[str, Any]) -> None:
        """
        Store a result in the cache.

        If cache is full, evicts the oldest entry (by mtime).

        Args:
            filepath: Path to the file.
            mtime: Modification time of the file.
            result: Parsed result to cache.
        """
        key = (filepath, mtime)

        # Evict oldest if at capacity
        if len(self._cache) >= self._max_size and key not in self._cache:
            oldest_key = min(self._cache.keys(), key=lambda k: k[1])
            del self._cache[oldest_key]

        self._cache[key] = result

    def invalidate(self, filepath: Optional[str] = None) -> None:
        """
        Invalidate cache entries.

        Args:
            filepath: Specific file to invalidate, or None to clear all.
        """
        if filepath:
            keys_to_remove = [k for k in self._cache.keys() if k[0] == filepath]
            for key in keys_to_remove:
                del self._cache[key]
        else:
            self._cache.clear()

    @property
    def size(self) -> int:
        """Get the current number of cached entries."""
        return len(self._cache)

    @property
    def max_size(self) -> int:
        """Get the maximum cache size."""
        return self._max_size


# Global instances for convenience
file_tracker = FilePositionTracker()
parse_cache = BoundedParseCache()
