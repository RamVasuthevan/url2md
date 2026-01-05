import click
from .command import convert_url_to_markdown


@click.command()
@click.argument("url")
@click.option(
    "--read-from-cache/--no-read-from-cache",
    default=True,
    help="Read from cache if available (default: True)",
)
@click.option(
    "--write-to-cache/--no-write-to-cache",
    default=True,
    help="Write result to cache (default: True)",
)
@click.version_option()
def cli(url: str, read_from_cache: bool, write_to_cache: bool):
    """Get the markdown representation of the contents of a URL"""
    try:
        content = convert_url_to_markdown(
            url,
            use_cache_read=read_from_cache,
            use_cache_write=write_to_cache,
        )
        click.echo(content)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()
