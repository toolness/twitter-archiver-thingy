import sys

from configparser import ConfigParser, SectionProxy
from pathlib import Path

import click
from requests_oauthlib import OAuth1Session


CONFIG_FILE = Path("config.ini")


def get_config() -> SectionProxy:
    config = ConfigParser()
    config.read(CONFIG_FILE)
    return config['twitblog']


@click.group()
def cli() -> None:
    pass


@cli.command()
def test_api() -> None:
    """Test the Twitter API to make sure it works."""

    config = get_config()
    twitter = OAuth1Session(
        config['ConsumerKey'],
        client_secret=config['ConsumerSecret'],
        resource_owner_key=config['AccessToken'],
        resource_owner_secret=config['AccessTokenSecret'],
    )
    r = twitter.get('https://api.twitter.com/1.1/trends/available.json')
    if r.status_code == 200:
        click.echo("Cool, everything works.")
    else:
        click.echo(f'Failure! Got HTTP {r.status_code}. Response follows.')
        click.echo(repr(r.json()))
        sys.exit(1)


if __name__ == '__main__':
    cli()
