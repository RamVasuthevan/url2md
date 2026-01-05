"""Core command functions for url2md"""

import requests
import html2text
from pathlib import Path
from dotenv import load_dotenv
from .cache import get_from_cache, write_to_cache
from .extractor import (
    Extractor,
    ReadabilityExtractor,
    NewspaperExtractor,
    ArticleMetadata,
    ArticleContent
)

# Load .env file from current directory or user's home
load_dotenv()
load_dotenv(Path.home() / ".env")

# Constants
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REQUEST_TIMEOUT = 30


def fetch_html(url, use_cache_read=True, use_cache_write=True):
    """
    Fetch HTML content from a URL.

    Args:
        url: The URL to fetch
        use_cache_read: Whether to read from cached content if available
        use_cache_write: Whether to write fetched content to cache

    Returns:
        str: The HTML content

    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    # Add https:// if not present
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    # Check cache first
    if use_cache_read:
        cached_html = get_from_cache(url)
        if cached_html:
            return cached_html

    # Fetch from URL
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    html = response.text

    # Save to cache
    if use_cache_write:
        write_to_cache(url, html)

    return html


def get_extractor(extractor_type: str = "readability") -> Extractor:
    """
    Get an extractor instance by type.

    Args:
        extractor_type: "readability" or "newspaper"

    Returns:
        Extractor instance

    Raises:
        ValueError: If extractor_type is not recognized
    """
    if extractor_type == "readability":
        return ReadabilityExtractor()
    elif extractor_type == "newspaper":
        return NewspaperExtractor()
    else:
        raise ValueError(f"Unknown extractor: {extractor_type}. Use 'readability' or 'newspaper'")


def html_to_markdown(html, url="", extractor_type="readability",
                     ignore_links=False, ignore_images=False):
    """
    Convert HTML to markdown using the specified extractor.

    Args:
        html: The HTML content to convert
        url: URL of the page (used for metadata extraction)
        extractor_type: "readability" or "newspaper" (default: "readability")
        ignore_links: Whether to ignore links in the output
        ignore_images: Whether to ignore images in the output

    Returns:
        str: The markdown content with metadata formatted by the extractor
    """
    # Get the extractor
    extractor = get_extractor(extractor_type)

    # Extract content and metadata
    article = extractor.extract(html, url)

    markdown_parts = []

    # Extractor formats its own metadata
    metadata_md = extractor.format_metadata(article.metadata)
    if metadata_md:
        markdown_parts.append(metadata_md)

    # Convert HTML to markdown
    h = html2text.HTML2Text()
    h.ignore_links = ignore_links
    h.ignore_images = ignore_images

    content_md = h.handle(article.html)
    markdown_parts.append(content_md)

    return "\n".join(markdown_parts)


def url_to_markdown(url, use_cache_read=True, use_cache_write=True, extractor_type="readability"):
    """
    Convert a URL to markdown in one step.

    The extractor automatically handles metadata formatting:
    - ReadabilityExtractor: includes title
    - NewspaperExtractor: includes title, author, and date

    Args:
        url: The URL to convert
        use_cache_read: Whether to read from cached content if available
        use_cache_write: Whether to write fetched content to cache
        extractor_type: "readability" or "newspaper" (default: "readability")

    Returns:
        str: The markdown content with metadata

    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    html = fetch_html(url, use_cache_read=use_cache_read, use_cache_write=use_cache_write)
    return html_to_markdown(html, url=url, extractor_type=extractor_type)
