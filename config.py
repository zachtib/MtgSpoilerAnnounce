from __future__ import annotations
from dataclasses import dataclass
from os import environ

@dataclass
class MtgSpoilerConfig:

    db_uri: str
    slack_webhook_url: str
    slack_channel: str
    debug: bool
    batch_threshold: int = None
    batch_channel: str = None

    @classmethod
    def from_env(cls) -> MtgSpoilerConfig:
        config = MtgSpoilerConfig(
            db_uri = environ.get('DATABASE_URL', 'sqlite:///:memory:'),
            slack_webhook_url = environ.get('SLACK_WEBHOOK_URL', ''),
            slack_channel = environ.get('SLACK_CHANNEL', 'bot-testing'),
            debug = len(environ.get('DEBUG', '')) > 0
        )
        print(f'Loaded configuration: {config}')
        return config
