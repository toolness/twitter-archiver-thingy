from typing import Optional, Iterator
from requests_oauthlib import OAuth1Session

from .config import get_config
from .tweet import Tweet


class TwitterSession(OAuth1Session):
    def __init__(self, client_key: str, client_secret: str,
                 resource_owner_key: str,
                 resource_owner_secret: str) -> None:
        super().__init__(
            client_key=client_key,
            client_secret=client_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
        )

    def get_tweet(self, status_id: str) -> Tweet:
        r = self.get(
            f'https://api.twitter.com/1.1/statuses/show/{status_id}.json'
            f'?tweet_mode=extended'
        )
        r.raise_for_status()
        return Tweet.from_json(r.json())

    def iter_reply(self, status_id: Optional[str]) -> Iterator[Tweet]:
        while status_id is not None:
            tweet = self.get_tweet(status_id)
            status_id = tweet.in_reply_to
            yield tweet


def get_session() -> TwitterSession:
    config = get_config()
    return TwitterSession(
        client_key=config['ConsumerKey'],
        client_secret=config['ConsumerSecret'],
        resource_owner_key=config['AccessToken'],
        resource_owner_secret=config['AccessTokenSecret'],
    )
