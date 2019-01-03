from typing import List
from models import Card

import requests

class SlackClient:
    webhook_url: str
    channel: str
    batch_threshold: int
    batch_channel: int


    def __init__(self, webhook_url, channel, batch_threshold=None, batch_channel=None):
        self.webhook_url = webhook_url
        self.channel = channel
        self.batch_threshold = batch_threshold
        self.batch_channel = batch_channel


    @property
    def batch_enabled(self):
        return self.batch_threshold is not None and self.batch_channel is not None


    def post_cards(self, cards: List[Card]):
        if self.batch_enabled and len(cards) >= self.batch_threshold:
            self._post_batch(cards)
        else:
            for card in cards:
                self._post_card(self._channel, card)

    
    def _post_batch(self, cards: List[Card]):
        for card in cards:
            self._post_card(self._batch_channel, card)

        self._post(self._channel, {
            'text': f'{len(cards)} new cards posted to #{self._batch_channel}',
        })


    def _post_card(self, channel: str, card: Card):
        message = f'<{card.image_url}|{card.name}>'
        if not self._is_card_english(card.name) and card.source_url:
            message = f'<{card.source_url}|{card.name}>'
        self._post(channel, {
            'text': message,
        })
 
    def _post(self, channel: str, payload: dict):
        payload['channel'] = channel
        requests.post(_webhook_url, data=url(payload))

    @staticmethod
    def _is_card_english(card_name):
        return not (card_name[0] == '"' and card_name[-1] == '"')


