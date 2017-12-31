import abc
import json
from typing import Any, Dict
from pathlib import Path


class Cache(abc.ABC):
    @abc.abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abc.abstractmethod
    def has(self, key: str) -> bool:
        pass

    @abc.abstractmethod
    def set(self, key: str, value: Any) -> None:
        pass

    def __contains__(self, item: str) -> bool:
        return self.has(item)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def __getitem__(self, key: str) -> Any:
        return self.get(key)


class InMemoryCache(Cache):
    def __init__(self) -> None:
        self._entries = {}  # type: Dict[str, Any]

    def get(self, key: str) -> Any:
        return self._entries.get(key)

    def has(self, key: str) -> bool:
        return key in self._entries

    def set(self, key: str, value: Any) -> None:
        self._entries[key] = value

class DiskCache(Cache):
    def __init__(self, path: Path) -> None:
        self.path = path
        if not self.path.exists():
            self.path.mkdir()

    def _keypath(self, key:str) -> Path:
        return self.path / f'{key}.json'

    def get(self, key: str) -> Any:
        path = self._keypath(key)
        if not path.exists():
            return None
        return json.loads(path.read_text())

    def has(self, key: str) -> bool:
        return self._keypath(key).exists()

    def set(self, key: str, value: Any) -> None:
        self._keypath(key).write_text(json.dumps(
            value,
            sort_keys=True,
            indent=2,
        ))
