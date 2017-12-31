import sys
from typing import Optional

import click

from twitblog.config import get_session
from twitblog.util import parse_status_url


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


@cli.command()
@click.argument('url')
def show_thread(url) -> None:
    '''
    Show a twitter thread.

    The given URL should be the *last* tweet in the thread.
    '''

    twitter = get_session()
    for tweet in twitter.iter_reply(parse_status_url(url)):
        click.echo(tweet.text)


@cli.command()
@click.option('--older', is_flag=True,
              help='Show older favorites, instead of newer ones.')
def show_favorites(older: bool) -> None:
    '''
    Show the authenticating user's favorites.
    '''

    twitter = get_session()
    for tweet in twitter.iter_favorites(older=older):
        click.echo(f'{tweet.id_str} @{tweet.screen_name}: {tweet.text}')


if __name__ == '__main__':
    cli()
