import sys

import click

from twitblog.client import get_session


@click.group()
def cli() -> None:
    pass


@cli.command()
def test_api() -> None:
    """Test the Twitter API to make sure it works."""

    twitter = get_session()
    r = twitter.get('https://api.twitter.com/1.1/trends/available.json')
    if r.status_code == 200:
        click.echo("Cool, everything works.")
    else:
        click.echo(f'Failure! Got HTTP {r.status_code}. Response follows.')
        click.echo(repr(r.json()))
        sys.exit(1)


if __name__ == '__main__':
    cli()
