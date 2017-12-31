from pathlib import Path

from configparser import ConfigParser, SectionProxy

from .session import TwitterSession


MY_DIR = Path(__file__).parent.resolve()

ROOT_DIR = MY_DIR.parent

CONFIG_FILE = ROOT_DIR / "config.ini"


def get_config() -> SectionProxy:
    config = ConfigParser()
    config.read(CONFIG_FILE)
    return config['twitblog']


def get_session() -> TwitterSession:
    config = get_config()
    return TwitterSession(
        client_key=config['ConsumerKey'],
        client_secret=config['ConsumerSecret'],
        resource_owner_key=config['AccessToken'],
        resource_owner_secret=config['AccessTokenSecret'],
    )
