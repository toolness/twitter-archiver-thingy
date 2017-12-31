from typing import Optional, Any


class Tweet:
    def __init__(self,
                 text: str,
                 screen_name: str,
                 in_reply_to: Optional[str],
                 original_json: Optional[Any]) -> None:
        self.text = text
        self.screen_name = screen_name
        self.in_reply_to = in_reply_to
        self.original_json = original_json

    @classmethod
    def from_json(cls, blob: Any) -> 'Tweet':
        return Tweet(
            text=blob['full_text'],
            screen_name=blob['user']['screen_name'],
            in_reply_to=blob['in_reply_to_status_id_str'],
            original_json=blob,
        )
