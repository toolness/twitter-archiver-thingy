import re


def parse_status_url(url: str) -> str:
    '''

    >>> url = 'https://twitter.com/amzeratul/status/946768612404187136'
    >>> parse_status_url(url)
    '946768612404187136'
    '''

    return url.split('/')[-1]
