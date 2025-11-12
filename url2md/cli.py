import click
import requests
import html2text
import sys


@click.command()
@click.argument("url")
@click.option(
    "--user-agent",
    default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    help="User agent string for requests",
)
@click.version_option()
def cli(url, user_agent):
    """Get the markdown representation of the contents of a url"""

    # Add https:// if not present
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    try:
        # Make request to fetch HTML
        headers = {"User-Agent": user_agent}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # Convert HTML to markdown
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        markdown = h.handle(response.text)

        # Output markdown to stdout
        click.echo(markdown)

    except requests.exceptions.RequestException as e:
        click.echo(f"Error fetching URL: {e}", err=True)
        sys.exit(1)
