"""Article extraction interface and implementations"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from readability import Document
from newspaper import Article


@dataclass
class ArticleMetadata:
    """Article metadata container"""
    title: Optional[str] = None
    author: Optional[str] = None
    date: Optional[datetime] = None


@dataclass
class ArticleContent:
    """Article content container"""
    html: str
    metadata: ArticleMetadata


class Extractor(ABC):
    """Abstract base class for article extractors"""

    @abstractmethod
    def extract(self, html: str, url: str = "") -> ArticleContent:
        """
        Extract article content and metadata from HTML.

        Args:
            html: The full HTML content
            url: Optional URL for the article

        Returns:
            ArticleContent with cleaned HTML and metadata
        """
        pass

    def format_metadata(self, metadata: ArticleMetadata) -> str:
        """
        Format metadata as markdown. Each extractor can override this.

        Args:
            metadata: The metadata to format

        Returns:
            Formatted markdown string with title, author, and date
        """
        lines = []

        if metadata.title:
            lines.append(f"# {metadata.title}")
            lines.append("")

        if metadata.date or metadata.author:
            meta_parts = []
            if metadata.date:
                meta_parts.append(metadata.date.strftime("%B %d, %Y"))
            if metadata.author:
                meta_parts.append(f"By {metadata.author}")

            lines.append(" ".join(meta_parts))
            lines.append("")

        return "\n".join(lines)


class ReadabilityExtractor(Extractor):
    """Extractor using readability-lxml"""

    def extract(self, html: str, url: str = "") -> ArticleContent:
        """
        Extract using readability-lxml.

        Extracts:
        - Title: ✅
        - Author: ❌ (not available)
        - Date: ❌ (not available)
        - Content: ✅ (main article HTML)

        Args:
            html: The full HTML content
            url: Optional URL (not used by readability)

        Returns:
            ArticleContent with cleaned HTML and metadata
        """
        doc = Document(html)

        metadata = ArticleMetadata(
            title=doc.title() if doc.title() else None,
            author=None,
            date=None
        )

        cleaned_html = doc.summary()

        return ArticleContent(
            html=cleaned_html,
            metadata=metadata
        )


class NewspaperExtractor(Extractor):
    """Extractor using newspaper3k"""

    def extract(self, html: str, url: str = "") -> ArticleContent:
        """
        Extract using newspaper3k.

        Extracts:
        - Title: ✅
        - Author: ✅
        - Date: ✅
        - Content: ✅ (main article text converted to simple HTML)

        Args:
            html: The full HTML content
            url: Optional URL for the article (helps with extraction)

        Returns:
            ArticleContent with cleaned HTML and metadata
        """
        article = Article(url if url else "")
        article.set_html(html)
        article.parse()

        # newspaper3k returns a list of authors, join them
        author = None
        if article.authors:
            author = ", ".join(article.authors)

        metadata = ArticleMetadata(
            title=article.title if article.title else None,
            author=author,
            date=article.publish_date
        )

        # newspaper3k extracts plain text, wrap it in simple HTML
        text = article.text if article.text else ""

        # Remove common byline artifacts that newspaper3k might leave
        # (it extracts author separately, but sometimes leaves "By" in text)
        if text.startswith("By\n\n") or text.startswith("By "):
            text = text[text.index('\n\n') + 2:] if '\n\n' in text else text[3:]

        # Split by double newlines to preserve paragraphs
        paragraphs = text.split('\n\n')
        html_paragraphs = [f"<p>{p.strip()}</p>" for p in paragraphs if p.strip()]
        cleaned_html = "\n".join(html_paragraphs)

        return ArticleContent(
            html=cleaned_html,
            metadata=metadata
        )
