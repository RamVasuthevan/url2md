import requests
from typing import Optional
from .cache import read_from_cache, write_to_cache


def fetch_url(url: str) -> str:
    """
    Fetch the content of a URL.

    Args:
        url: The URL to fetch

    Returns:
        The HTML content of the URL

    Raises:
        requests.RequestException: If the request fails
    """
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def html_to_markdown(html: str) -> str:
    """
    Convert HTML content to markdown.

    Args:
        html: The HTML content to convert

    Returns:
        The markdown representation of the HTML

    Note:
        This is a placeholder. Consider using a library like html2text or markdownify
    """
    # TODO: Implement actual HTML to markdown conversion
    # For now, return the HTML as-is
    return html


def convert_url_to_markdown(
    url: str,
    use_cache_read: bool = True,
    use_cache_write: bool = True,
) -> str:
    """
    Convert a URL to markdown, optionally using cache.

    Args:
        url: The URL to convert
        use_cache_read: Whether to read from cache if available
        use_cache_write: Whether to write the result to cache

    Returns:
        The markdown representation of the URL content
    """
    # Try to read from cache first if enabled
    if use_cache_read:
        cached_content = read_from_cache(url)
        if cached_content:
            return cached_content

    # Fetch and convert the URL
    html = fetch_url(url)
    markdown = html_to_markdown(html)

    # Write to cache if enabled
    if use_cache_write:
        write_to_cache(url, markdown)

    return markdown
