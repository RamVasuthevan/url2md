"""Core command functions for url2md"""

import requests
import html2text
from pathlib import Path
from dotenv import load_dotenv
from readability import Document
from .cache import get_from_cache, write_to_cache

# Load .env file from current directory or user's home
load_dotenv()
load_dotenv(Path.home() / ".env")

# Constants
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REQUEST_TIMEOUT = 30


def fetch_html(url, use_cache=True):
    """
    Fetch HTML content from a URL.

    Args:
        url: The URL to fetch
        use_cache: Whether to use cached content if available

    Returns:
        str: The HTML content

    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    # Add https:// if not present
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    # Check cache first
    if use_cache:
        cached_html = get_from_cache(url)
        if cached_html:
            return cached_html

    # Fetch from URL
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    html = response.text

    # Save to cache
    if use_cache:
        write_to_cache(url, html)

    return html


def extract_main_content(html):
    """
    Extract the main article content from HTML using Readability.

    Args:
        html: The HTML content to extract from

    Returns:
        str: The main content HTML (without ads, navigation, etc.)
    """
    doc = Document(html)
    return doc.summary()


def html_to_markdown(html, ignore_links=False, ignore_images=False, main_content_only=True):
    """
    Convert HTML to markdown.

    Args:
        html: The HTML content to convert
        ignore_links: Whether to ignore links in the output
        ignore_images: Whether to ignore images in the output
        main_content_only: Whether to extract only main content (default: True)

    Returns:
        str: The markdown content
    """
    # Extract main content if requested
    if main_content_only:
        html = extract_main_content(html)

    h = html2text.HTML2Text()
    h.ignore_links = ignore_links
    h.ignore_images = ignore_images

    return h.handle(html)


def url_to_markdown(url, use_cache=True, main_content_only=True):
    """
    Convert a URL to markdown in one step.

    Args:
        url: The URL to convert
        use_cache: Whether to use cached content if available
        main_content_only: Whether to extract only main content (default: True)

    Returns:
        str: The markdown content

    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    html = fetch_html(url, use_cache=use_cache)
    return html_to_markdown(html, main_content_only=main_content_only)
