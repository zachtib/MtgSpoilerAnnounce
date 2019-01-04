#!/usr/bin/env python

import argparse

from config import MtgSpoilerConfig
from database import Database
from manager import Manager
from models import Card, Set
from scryfall import ScryfallClient
from slackclient import SlackClient


def get_manager() -> Manager:
    config = MtgSpoilerConfig.from_env()
    api = ScryfallClient(config)
    db = Database(config)
    slack = SlackClient(config)
    return Manager(config, db, api, slack)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--watch', nargs='+')
    parser.add_argument('--unwatch', nargs='+')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    manager = get_manager()

    if (args.watch):
        manager.watch_sets(args.watch)
    if (args.unwatch):
        manager.unwatch_sets(args.unwatch)
