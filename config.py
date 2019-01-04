from __future__ import annotations
from os import environ

class MtgSpoilerConfig:

    __create_key = object()

    db_uri: str
    slack_webhook_url: str
    slack_channel: str
    debug: bool

    @classmethod
    def from_env(cls) -> MtgSpoilerConfig:
        config = MtgSpoilerConfig
        config.db_uri = environ.get('DATABASE_URL', 'sqlite://example.db')
        config.slack_webhook_url = environ['SLACK_WEBHOOK_URL']
        config.slack_channel = environ['SLACK_CHANNEL']
        config.debug = len(environ.get('DEBUG', '')) > 0
        return config
    
    def __init__(self, create_key):
        assert(create_key == MtgSpoilerConfig.__create_key)
