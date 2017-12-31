from typing import Optional, Iterator, NamedTuple, Any, Mapping
from requests_oauthlib import OAuth1Session

from .tweet import Tweet
from .cache import Cache, InMemoryCache


BASE_URL = 'https://api.twitter.com/1.1'

BASE_PARAMS = {
    'tweet_mode': 'extended',
}

MAX_COUNT = '200'


class StatusStats(NamedTuple):
    min_id: Optional[str]
    max_id: Optional[str]

    @classmethod
    def empty(cls) -> 'StatusStats':
        return cls(None, None)

    @classmethod
    def from_cache(cls, cache_entry: Any) -> 'StatusStats':
        if cache_entry is None:
            return cls.empty()
        return cls(*cache_entry)

    def update(self, id_str: str) -> 'StatusStats':
        min_id = self.min_id
        max_id = self.max_id

        id_int = int(id_str)
        if min_id is None or id_int < int(min_id):
            min_id = id_str
        if max_id is None or id_int > int(max_id):
            max_id = id_str

        return self.__class__(min_id, max_id)

    def as_params(self, older: bool) -> Mapping[str, str]:
        if older:
            return {'max_id': self.min_id} if self.min_id else {}
        return {'since_id': self.max_id} if self.max_id else {}


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
            r = self.get(f'{BASE_URL}/statuses/show/{status_id}.json',
                         params=BASE_PARAMS)
            r.raise_for_status()
            self.cache[status_id] = r.json()
        return Tweet.from_json(self.cache[status_id])

    def iter_reply(self, status_id: Optional[str]) -> Iterator[Tweet]:
        while status_id is not None:
            tweet = self.get_tweet(status_id)
            status_id = tweet.in_reply_to
            yield tweet

    def iter_timeline(self, screen_name: str,
                      older: bool=False) -> Iterator[Tweet]:
        stats_key = f'timeline_{screen_name}'
        stats = StatusStats.from_cache(self.cache[stats_key])
        params = {
            'screen_name': screen_name,
            'count': MAX_COUNT,
            **stats.as_params(older),
            **BASE_PARAMS
        }

        r = self.get(f'{BASE_URL}/statuses/user_timeline.json', params=params)
        r.raise_for_status()

        for tweet in Tweet.from_json_list(r.json()):
            stats = stats.update(tweet.id_str)
            self.cache[stats_key] = stats
            self.cache[tweet.id_str] = tweet.original_json
            yield tweet

    def iter_favorites(self, older: bool=False) -> Iterator[Tweet]:
        stats = StatusStats.from_cache(self.cache['favorites'])
        params = {
            'count': MAX_COUNT,
            **stats.as_params(older),
            **BASE_PARAMS
        }

        r = self.get(f'{BASE_URL}/favorites/list.json', params=params)
        r.raise_for_status()

        for tweet in Tweet.from_json_list(r.json()):
            stats = stats.update(tweet.id_str)
            self.cache['favorites'] = stats
            self.cache[tweet.id_str] = tweet.original_json
            yield tweet
