import hashlib
import os
from pathlib import Path
from typing import Optional


def get_cache_dir() -> Path:
    """Get or create the cache directory."""
    cache_dir = Path.home() / ".cache" / "url2md"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_cache_key(url: str) -> str:
    """Generate a cache key from a URL."""
    return hashlib.sha256(url.encode()).hexdigest()


def get_cache_path(url: str) -> Path:
    """Get the cache file path for a given URL."""
    cache_dir = get_cache_dir()
    cache_key = get_cache_key(url)
    return cache_dir / f"{cache_key}.md"


def read_from_cache(url: str) -> Optional[str]:
    """
    Read cached markdown content for a URL.

    Args:
        url: The URL to look up in the cache

    Returns:
        The cached markdown content if it exists, None otherwise
    """
    cache_path = get_cache_path(url)
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")
    return None


def write_to_cache(url: str, content: str) -> None:
    """
    Write markdown content to the cache for a URL.

    Args:
        url: The URL to cache content for
        content: The markdown content to cache
    """
    cache_path = get_cache_path(url)
    cache_path.write_text(content, encoding="utf-8")


def delete_from_cache(url: str) -> None:
    """
    Delete cached content for a URL.

    Args:
        url: The URL to remove from the cache
    """
    cache_path = get_cache_path(url)
    if cache_path.exists():
        cache_path.unlink()
