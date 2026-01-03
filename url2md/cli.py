"""CLI interface for url2md"""

import click
import sys
import requests
from .command import url_to_markdown


@click.command()
@click.argument("url")
@click.option(
    "--no-cache",
    is_flag=True,
    help="Don't use cached content, fetch fresh from URL",
)
@click.option(
    "--extractor",
    type=click.Choice(["readability", "newspaper"], case_sensitive=False),
    default="readability",
    help="Extraction method: readability (default, title only) or newspaper (title, author, date)",
)
@click.version_option()
def cli(url, no_cache, extractor):
    """Get the markdown representation of the contents of a url"""

    try:
        # Convert URL to markdown
        markdown = url_to_markdown(url, use_cache=not no_cache, extractor_type=extractor)

        # Output markdown to stdout
        click.echo(markdown)

    except requests.exceptions.RequestException as e:
        click.echo(f"Error fetching URL: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
