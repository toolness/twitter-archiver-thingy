import sys
from typing import Optional

import click

from twitblog.config import get_session, get_cache
from twitblog.tweet import Tweet
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
def show_thread(url: str) -> None:
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
@click.option('--forever', is_flag=True,
              help='Repeat until all tweets are retrieved.')
def show_favorites(older: bool, forever: bool) -> None:
    '''
    Show the authenticating user's favorites.
    '''

    twitter = get_session()
    for tweet in twitter.iter_favorites(older=older, forever=forever):
        click.echo(f'{tweet.id_str} @{tweet.screen_name}: {tweet.text}')


@cli.command()
@click.argument('screen_name')
@click.option('--older', is_flag=True,
              help='Show older tweets, instead of newer ones.')
@click.option('--forever', is_flag=True,
              help='Repeat until all tweets are retrieved.')
def show_timeline(screen_name: str, older: bool, forever: bool) -> None:
    '''
    Show the timeline of the given user.
    '''

    twitter = get_session()
    for tweet in twitter.iter_timeline(screen_name, older=older,
                                       forever=forever):
        click.echo(f'{tweet.id_str} @{tweet.screen_name}: {tweet.text}')


@cli.command()
def show_cached_tweets() -> None:
    '''
    Show all cached tweets.
    '''

    for tweet in Tweet.from_cache(get_cache()):
        click.echo(f'{tweet.id_str} @{tweet.screen_name}: {tweet.text}')


if __name__ == '__main__':
    cli()
