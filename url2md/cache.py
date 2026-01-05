"""Cache management for url2md"""

import hashlib
import os
from pathlib import Path
from typing import Optional


def get_cache_dir() -> Path:
    """Get the cache directory path from environment variable or default."""
    cache_path = os.getenv("URL2MD_CACHE_DIR")

    if cache_path:
        cache_dir = Path(cache_path).expanduser()
    else:
        import tempfile
        cache_dir = Path(tempfile.gettempdir()) / "url2md"

    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_cache_key(url: str) -> str:
    """Generate a cache key from a URL."""
    return hashlib.sha256(url.encode()).hexdigest()


def is_cached(url: str) -> bool:
    """
    Check if a URL's content is in the cache.

    Args:
        url: The URL to check

    Returns:
        bool: True if cached, False otherwise
    """
    cache_dir = get_cache_dir()
    cache_key = get_cache_key(url)
    cache_file = cache_dir / cache_key

    return cache_file.exists()


def get_from_cache(url: str) -> Optional[str]:
    """
    Get HTML content from cache if it exists.

    Args:
        url: The URL to look up in cache

    Returns:
        str or None: The cached HTML content, or None if not found
    """
    if not is_cached(url):
        return None

    cache_dir = get_cache_dir()
    cache_key = get_cache_key(url)
    cache_file = cache_dir / cache_key

    return cache_file.read_text(encoding='utf-8')


def write_to_cache(url: str, html: str) -> None:
    """
    Write HTML content to cache.

    Args:
        url: The URL to use as cache key
        html: The HTML content to cache
    """
    cache_dir = get_cache_dir()
    cache_key = get_cache_key(url)
    cache_file = cache_dir / cache_key
    cache_file.write_text(html, encoding='utf-8')


def delete_from_cache(url: str) -> None:
    """
    Delete cached content for a URL.

    Args:
        url: The URL to remove from the cache
    """
    cache_dir = get_cache_dir()
    cache_key = get_cache_key(url)
    cache_file = cache_dir / cache_key
    if cache_file.exists():
        cache_file.unlink()


def clear_cache() -> None:
    """Clear all cached content."""
    cache_dir = get_cache_dir()
    for cache_file in cache_dir.glob("*"):
        if cache_file.is_file():
            cache_file.unlink()
