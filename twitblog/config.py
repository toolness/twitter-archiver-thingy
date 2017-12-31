from pathlib import Path

from configparser import ConfigParser, SectionProxy


MY_DIR = Path(__file__).parent.resolve()

ROOT_DIR = MY_DIR.parent

CONFIG_FILE = ROOT_DIR / "config.ini"


def get_config() -> SectionProxy:
    config = ConfigParser()
    config.read(str(CONFIG_FILE))
    return config['twitblog']
