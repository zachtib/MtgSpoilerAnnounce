import json
import re
from logging import Logger
from typing import List

import requests

from config import MtgSpoilerConfig
from models import Card

p = re.compile(r'{(\w+)}')


def format_mana(manacost: str) -> str:
    return p.sub(r":mana-\1:", manacost)


class SlackClient:
    webhook_url: str
    channel: str
    batch_threshold: int
    batch_channel: str
    debug: bool
    logger: Logger

    def __init__(self, config: MtgSpoilerConfig, logger: Logger):
        self.webhook_url = config.slack_webhook_url
        self.channel = config.slack_channel
        self.batch_threshold = config.batch_threshold
        self.batch_channel = config.batch_channel
        self.debug = config.debug
        self.logger = logger

    @property
    def batch_enabled(self):
        return self.batch_threshold > 0 and self.batch_channel is not None

    def post_cards(self, cards: List[Card]) -> List[Card]:
        if self.batch_enabled and len(cards) >= self.batch_threshold:
            return self._post_batch(cards)
        else:
            return [card for card in cards if self._post_card(self.channel, card)]

    def _post_batch(self, cards: List[Card]) -> List[Card]:
        successes = [card for card in cards if self._post_card(self.batch_channel, card)]
        self._post(self.channel, {
            'text': f'{len(successes)} new cards posted to #{self.batch_channel}',
        })
        return successes

    def _post_card(self, channel: str, card: Card) -> bool:
        self.logger.debug(f'Posting card {card.name} to Slack')
        return self._post(channel, {
            'text': self.format_card(card),
        })

    def _post(self, channel: str, payload: dict) -> bool:
        payload['channel'] = channel
        if self.debug:
            print(f'SlackClient: Would post {payload} to {channel}')
        else:
            try:
                payload = json.dumps(payload)
                self.logger.debug(payload)
                r = requests.post(self.webhook_url, data=str(payload))
                if r.status_code != 200:
                    self.logger.error(f'Error from Slack: Status {r.status_code}: {r.content}')
                    return False
            except Exception as err:
                self.logger.error(err)
                return False
        return True

    @staticmethod
    def format_card(card: Card) -> str:
        return f'{card.name} {format_mana(card.mana_cost)}\n{card.type_line}\n{format_mana(card.oracle_text)}{card.power_toughness}\n<{card.image_url}|Image>'

    @staticmethod
    def _is_card_english(card):
        return not (card.name[0] == '"' and card.name[-1] == '"')
