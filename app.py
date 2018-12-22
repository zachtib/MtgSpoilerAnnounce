import sys

import requests

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
db = SQLAlchemy(app)

slack_webhook_url = environ['SLACK_WEBHOOK_URL']
channel = environ['SLACK_CHANNEL']


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


def post_card(card):
    response = requests.post(slack_webhook_url, data=str({
        'channel': channel,
        'text': f'{card["name"]}: {card["image_uris"]["normal"]}',
    }))


def check_for_new_cards(exp):
    r = requests.get(f'https://api.scryfall.com/cards/search?order=spoiled&q=e={exp}&unique=prints')
    if r.status_code != 200:
        return
    json = r.json()
    known_cards = Card.query.filter_by(expansion=exp).all()
    known_card_names = [card.name for card in known_cards]
    for card in json['data']:
        if card['name'] not in known_card_names:
            post_card(card)
            db.session.add(Card(name=card['name'], expansion=exp))
    db.session.commit()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        code = sys.argv[1]
        print(code)
        check_for_new_cards(code)
    else:
        app.run()
