"""url2md - Get the markdown representation of the contents of a url"""

from .command import fetch_html, html_to_markdown, url_to_markdown
from .cache import (
    is_cached,
    get_from_cache,
    write_to_cache,
    get_cache_dir,
    get_cache_key,
    clear_cache,
)

__version__ = "0.1"
__all__ = [
    "fetch_html",
    "html_to_markdown",
    "url_to_markdown",
    "is_cached",
    "get_from_cache",
    "write_to_cache",
    "get_cache_dir",
    "get_cache_key",
    "clear_cache",
]
