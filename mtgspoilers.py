#!/usr/bin/env python

import argparse

from scryfall import ScryfallClient
from scryfall.models import Card, Set

from database import Database

from manager import Manager


def get_manager() -> Manager:
    api = ScryfallClient()
    db = Database()
    return Manager(db, api, None)

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
