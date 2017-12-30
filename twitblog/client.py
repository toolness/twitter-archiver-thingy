from requests_oauthlib import OAuth1Session

from .config import get_config


def get_session() -> OAuth1Session:
    config = get_config()
    return OAuth1Session(
        config['ConsumerKey'],
        client_secret=config['ConsumerSecret'],
        resource_owner_key=config['AccessToken'],
        resource_owner_secret=config['AccessTokenSecret'],
    )
