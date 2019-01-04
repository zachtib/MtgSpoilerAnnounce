import sys

import requests

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

from mtgspoilers import get_manager
from config import MtgSpoilerConfig
from database import Database
from manager import Manager
from models import Card, Set
from scryfall import ScryfallClient
from slackclient import SlackClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
db = SQLAlchemy(app)

config = MtgSpoilerConfig.from_env()
api = ScryfallClient()
slack = SlackClient(config.slack_webhook_url, config.slack_channel)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    expansion = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def hello():
    return 'OK'


@app.route('/<exp>')
def hello_world(exp):
    check_for_new_cards(exp)
    return 'OK'


def check_for_new_cards(exp):
    api_cards = api.get_cards_from_set(exp)
    known_cards = Card.query.filter_by(expansion=exp).all()
    known_card_names = [card.name for card in known_cards]

    new_cards = list(filter(lambda x: x.name not in known_card_names, api_cards))

    slack.post_cards(new_cards)
    for card in new_cards:
        db.session.add(Card(name=card.name, expansion=exp))

    db.session.commit()


if __name__ == '__main__':
    db.create_all()
    if len(sys.argv) > 1:
        code = sys.argv[1]
        print(code)
        check_for_new_cards(code)
    else:
        app.run()
