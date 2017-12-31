import re
from typing import Optional, Any, Iterator

from .cache import Cache


class Tweet:
    def __init__(self,
                 id_str: str,
                 text: str,
                 screen_name: str,
                 in_reply_to: Optional[str],
                 original_json: Optional[Any]) -> None:
        self.id_str = id_str
        self.text = text
        self.screen_name = screen_name
        self.in_reply_to = in_reply_to
        self.original_json = original_json

    def __str__(self) -> str:
        return f'{self.id_str} @{self.screen_name}: {self.text}'

    @classmethod
    def from_json(cls, blob: Any) -> 'Tweet':
        return Tweet(
            id_str=blob['id_str'],
            text=blob['full_text'],
            screen_name=blob['user']['screen_name'],
            in_reply_to=blob['in_reply_to_status_id_str'],
            original_json=blob,
        )

    @classmethod
    def from_json_list(cls, blob_list: Any) -> Iterator['Tweet']:
        for blob in blob_list:
            yield cls.from_json(blob)

    @classmethod
    def from_cache(cls, cache: Cache) -> Iterator['Tweet']:
        for key in cache.iterkeys():
            if re.match(r'^[0-9]+$', key):
                yield cls.from_json(cache.get(key))
