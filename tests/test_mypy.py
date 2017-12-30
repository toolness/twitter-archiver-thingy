from pathlib import Path
import subprocess


ROOT_DIR = Path(__file__).parent.parent.resolve()


def test_mypy():
    subprocess.check_call(
        ['mypy', 'cli.py', 'twitblog'],
        cwd=str(ROOT_DIR),
    )
