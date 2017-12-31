import sys
import re
from typing import Optional, Iterator

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


def show_tweets(iterator: Iterator[Tweet]) -> None:
    for tweet in iterator:
        click.echo(str(tweet))


@cli.command()
@click.argument('url')
def show_thread(url: str) -> None:
    '''
    Show a twitter thread.

    The given URL should be the *last* tweet in the thread.
    '''

    show_tweets(get_session().iter_reply(parse_status_url(url)))


@cli.command()
@click.option('--older', is_flag=True,
              help='Show older favorites, instead of newer ones.')
@click.option('--forever', is_flag=True,
              help='Repeat until all tweets are retrieved.')
def show_favorites(older: bool, forever: bool) -> None:
    '''
    Show the authenticating user's favorites.
    '''

    show_tweets(get_session().iter_favorites(older=older, forever=forever))


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

    show_tweets(get_session().iter_timeline(screen_name, older=older,
                                            forever=forever))


@cli.command()
def show_cached_tweets() -> None:
    '''
    Show all cached tweets.
    '''

    show_tweets(Tweet.from_cache(get_cache()))


@cli.command()
@click.argument('pattern')
def grep(pattern) -> None:
    print(repr(pattern))
    show_tweets(
        tweet for tweet in Tweet.from_cache(get_cache())
        if (re.search(pattern, tweet.text, re.I) or
            re.search(pattern, tweet.screen_name, re.I))
    )


if __name__ == '__main__':
    cli()
