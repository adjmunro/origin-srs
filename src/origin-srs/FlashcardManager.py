import copy
import json
import os
from datetime import datetime as date
from datetime import timedelta


class FlashcardManager:

    def __init__(self, path='..', min_degree=-5, max_degree=10):
        self.path = f'{path}/json'
        self.min_degree = min_degree
        self.max_degree = max_degree

        if not os.path.exists(self.path):
            os.mkdir(f'{self.path}')

        self.cards = {}
        self.decks = set()
        self.tags = {'#all', '#new', '#due'}

        self.read()

    def add(self, im):
        for i, card_data in enumerate(im.data):
            k = card_data['key']

            default_card = {
                'order': i,
                'deck': card_data['deck'],
                'value': card_data['value'],
                'notes': card_data['notes'],
                'tags': ['#' + card_data['deck']] + card_data['tags'],
                'last_review': date.max,
                'next_review': date.max,
                'degree': self.min_degree
            }

            self.decks |= {default_card['deck']}
            self.tags |= set(default_card['tags'])

            if k in self.cards:
                for key, value in default_card.items():
                    # Add fields if missing
                    if key not in self.cards[k]:
                        self.cards[k][key] = value
                    # Alter field with warning for these elements
                    elif key in ['deck', 'value', 'notes'] and self.cards[k][key] != value:
                        print(
                            f'WARNING: The {key} of {k} has changed! There may be a duplicate key.\n{self.cards[k][key]}->{card_data[key]}')
                        self.cards[k][key] = value
                    # Alter field without warning for these elements
                    elif key in ['order', 'tags'] and self.cards[k][key] != value:
                        self.cards[k][key] = value
                    # Otherwise, don't alter the field (e.g. for review dates and degree)

                # Continue to next loop iteration as we already have this card in our deck
                continue

            # If new card, add it to the deck
            self.cards.update({k: default_card})

        self.write()

    def allow_extra_delay(self, key):
        if key not in self.cards or self.is_new(key):
            return False

        return self.cards[key]['degree'] >= 3

    def count_tag(self, tag, keys=None):
        return len(self.filter_tag(tag, keys=keys))

    def delete_lost_cards(self):
        lost = [k for k in self.cards if self.cards[k]['deck'] == 'lost']
        for i in lost:
            if input(f'Are you sure you want to delete {i}?\n{self.cards[i]}\n\'Y\' to confirm : ') == 'Y':
                del self.cards[i]

    def filter_deck(self, deck):
        return [key for key in self.cards.keys() if self.cards[key]['deck'] == deck]

    def filter_tag(self, tag, keys=None):
        if keys is None:  # NOTE DO NOT USE NOT KEYS AS THIS WILL FILL THE LIST IF IT WERE EMPTY
            keys = self.get_keys()
        return [i for i in keys if self.has_tag(i, tag)]

    def fix_cards(self):
        default_card = {
            'order': -1,
            'deck': 'lost',
            'value': '',
            'notes': '',
            'tags': ['#lost'],
            'last_review': date.max,
            'next_review': date.max,
            'degree': self.min_degree
        }

        for k in self.cards:

            for key, value in default_card.items():
                # Add fields if missing
                if key not in self.cards[k]:
                    self.cards[k][key] = value

            self.decks |= {self.cards[k]['deck']}
            self.tags |= set(self.cards[k]['tags'])

        # self.delete_lost_cards()

    def get(self, key, item=None):
        if not item:
            return key in self.cards

        if key not in self.cards or item not in self.cards[key].keys():
            return None

        return self.cards[key][item]

    def get_decks(self):
        return sorted(self.decks)

    def get_keys(self):
        return list(self.cards)

    def get_tags(self, deck=None, extra=True):
        if deck is None:
            tags = self.tags
        else:
            tags = set()
            for k in self.filter_deck(deck):
                tags |= set(self.cards[k]['tags'])

        if f'#{deck}' in tags:
            tags.remove(f'#{deck}')

        if extra:
            return sorted(tags)
        return sorted([t for t in tags if t not in ['#all', '#due', '#new', '#lost']])

    def has_tag(self, key, tag):
        if tag == '#all':
            return True
        if tag == '#due':
            return self.is_due(key)
        if tag == '#new':
            return self.is_new(key)

        return tag in self.cards[key]['tags']

    def is_due(self, key):
        return self.cards[key]['next_review'] <= date.now()

    def is_new(self, key):
        return self.cards[key]['last_review'] == date.max or self.cards[key]['next_review'] == date.max

    def mark(self, results):
        if not results:
            return

        for k, v in results.items():
            if v is None:
                continue

            self.cards[k]['last_review'] = date.now()
            self.cards[k]['degree'] = min(
                max(self.min_degree, self.cards[k]['degree'] + (v['avg_score'] / 2 if v['avg_score'] >= 1 else -1)),
                self.max_degree)
            self.cards[k]['next_review'] = self.cards[k]['last_review'] + timedelta(days=2 ** self.cards[k]['degree'])

    def read(self):
        if os.path.exists(f'{self.path}/cards.json'):
            with open(f'{self.path}/cards.json', 'r') as f:
                temp = json.load(f)

            for k in temp:
                temp[k]['last_review'] = eval(temp[k]['last_review'])
                temp[k]['next_review'] = eval(temp[k]['next_review'])

            self.cards = temp

        self.fix_cards()

    def tomorrow(self):
        for k in self.cards:
            if not self.is_new(k):
                self.cards[k]['next_review'] -= timedelta(days=1)

    def write(self):
        temp = copy.deepcopy(self.cards)

        for k in temp.keys():
            temp[k]['last_review'] = repr(temp[k]['last_review'])
            temp[k]['next_review'] = repr(temp[k]['next_review'])

        with open(f'{self.path}/cards.json', 'w') as f:
            f.write(json.dumps(temp))

    def yesterday(self):
        for k in self.cards:
            if not self.is_new(k):
                self.cards[k]['next_review'] += timedelta(days=1)


if __name__ == "__main__":
    from src.tests import Test

    Test.run()
