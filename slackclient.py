from typing import List
from models import Card
from config import MtgSpoilerConfig

import requests
import re

p = re.compile(r'\{(\w+)\}')


def format_mana(manacost: str) -> str:
    return p.sub(r":mana-\1:", manacost.lower())


class SlackClient:
    webhook_url: str
    channel: str
    batch_threshold: int
    batch_channel: int
    debug: bool


    def __init__(self, config: MtgSpoilerConfig):
        self.webhook_url = config.slack_webhook_url
        self.channel = config.slack_channel
        self.batch_threshold = config.batch_threshold
        self.batch_channel = config.batch_channel
        self.debug = config.debug


    @property
    def batch_enabled(self):
        return self.batch_threshold > 0 and self.batch_channel is not None


    def post_cards(self, cards: List[Card]):
        if self.batch_enabled and len(cards) >= self.batch_threshold:
            self._post_batch(cards)
        else:
            for card in cards:
                self._post_card(self.channel, card)

    
    def _post_batch(self, cards: List[Card]):
        for card in cards:
            self._post_card(self.batch_channel, card)

        self._post(self.channel, {
            'text': f'{len(cards)} new cards posted to #{self.batch_channel}',
        })


    def _post_card(self, channel: str, card: Card):
        message: str
        if self._is_card_english(card):
            message = f'<{card.image_url}|{card.name}>'
        else:
            message = f'{card.name}: {card.source_url}'
        self._post(channel, {
            'text': card.format_slack(),
        })
 
    def _post(self, channel: str, payload: dict):
        payload['channel'] = channel
        if self.debug:
            print(f'SlackClient: Would post {payload} to {channel}')
        else:
            requests.post(self.webhook_url, data=str(payload))
    
    @staticmethod
    def format_card(card: Card) -> str:
        return f'<{card.image_url}|{card.name}> {format_mana(card.mana_cost)}\n{card.type_line}\n{format_mana(card.oracle_text)}{card.power_toughness}'
    
    @staticmethod
    def _is_card_english(card):
        return not (card.name[0] == '"' and card.name[-1] == '"')


