from typing import Optional, Iterator
from requests_oauthlib import OAuth1Session

from .tweet import Tweet
from .cache import Cache, InMemoryCache


class TwitterSession(OAuth1Session):
    def __init__(self, client_key: str, client_secret: str,
                 resource_owner_key: str,
                 resource_owner_secret: str,
                 cache: Optional[Cache] = None) -> None:
        super().__init__(
            client_key=client_key,
            client_secret=client_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
        )
        if cache is None:
            cache = InMemoryCache()
        self.cache = cache

    def get_tweet(self, status_id: str) -> Tweet:
        if status_id not in self.cache:
            r = self.get(
                f'https://api.twitter.com/1.1/statuses/show/{status_id}.json'
                f'?tweet_mode=extended'
            )
            r.raise_for_status()
            self.cache[status_id] = r.json()
        return Tweet.from_json(self.cache[status_id])

    def iter_reply(self, status_id: Optional[str]) -> Iterator[Tweet]:
        while status_id is not None:
            tweet = self.get_tweet(status_id)
            status_id = tweet.in_reply_to
            yield tweet