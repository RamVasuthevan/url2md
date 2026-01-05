"""url2md - Get the markdown representation of the contents of a url"""

from .command import fetch_html, html_to_markdown, url_to_markdown, get_extractor
from .cache import (
    is_cached,
    get_from_cache,
    write_to_cache,
    delete_from_cache,
    get_cache_dir,
    get_cache_key,
    clear_cache,
)
from .extractor import (
    Extractor,
    ReadabilityExtractor,
    NewspaperExtractor,
    ArticleMetadata,
    ArticleContent,
)

__version__ = "0.1"
__all__ = [
    "fetch_html",
    "html_to_markdown",
    "url_to_markdown",
    "get_extractor",
    "is_cached",
    "get_from_cache",
    "write_to_cache",
    "delete_from_cache",
    "get_cache_dir",
    "get_cache_key",
    "clear_cache",
    "Extractor",
    "ReadabilityExtractor",
    "NewspaperExtractor",
    "ArticleMetadata",
    "ArticleContent",
]
