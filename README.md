This is a command-line utility that provides a variety of tools for
archiving Twitter data.

## Quick start

This requires Python 3.6.4 or higher.

```
python3 -m venv venv
source venv/bin/activate           # Or 'venv\Scripts\activate' on Windows.
pip install -r requirements.txt
cp config.sample.ini config.ini    # Use 'copy' instead of 'cp' on Windows.
```

Now edit `config.ini` as needed.  You will need to create a Twitter app
at https://apps.twitter.com/ to do this.

You can test to make sure Twitter connectivity works with:

```
python cli.py test_api
```

You can also run the test suite:

```
pytest
```
