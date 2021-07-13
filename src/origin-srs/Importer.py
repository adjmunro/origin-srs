import os


class Importer:

    def __init__(self, path='..'):
        self.path = f'{path}/resources'
        self.data = []
        self.duplicates = []

        if not os.path.exists(self.path):
            os.mkdir(f'{self.path}')

    #     def fix(self, key, card, value):
    #         for filename in [f'{self.path}/{i}.txt' for i in card['tags'] if os.path.exists(f'{self.path}/{i}.txt')]:
    #
    #             with open(filename, 'r', encoding='UTF-8') as f:
    #                 s = f.read().replace(f'{key},{value}', f'{key},{card["value"]}')
    #
    #             with open(filename, 'w', encoding='UTF-8') as f:
    #                 f.write(s)

    def notify(self):
        if not self.duplicates:
            return

        for d in self.duplicates:
            k = d['key']
            print(f'\nWARNING: Key {k}(deck {d["deck"]} already found in {self.data[k]["deck"]}(0)!')
            print(
                f'(0)Value: {self.data[k]["value"]}\n(0)Notes: {self.data[k]["notes"]}\n(0)Tags: {self.data[k]["tags"]}')
            print(f'{"-" * 20}\n(1)Value: {d["value"]}\n(1)Notes: {d["notes"]}\n(1)Tags: {d["tags"]}')
            print('This card will not be added! Please rectify!')

    def read(self):
        for filename in os.listdir(f'{self.path}'):
            if '.txt' not in filename:
                continue

            print(f'Importing from {self.path}/{filename}')
            with open(f'{self.path}/{filename}', 'r', encoding='UTF-8') as f:
                txt = [i.split(',') for i in f.read().split('\n')]

            if txt == [['']]:
                continue

            # self.data.update({filename[:-4] : {}})
            # self.data[filename[:-4]].update({i[0].title() : i[1].title() for i in txt})

            for i in txt:
                card_data = {
                    'deck': filename.replace('.txt', ''),
                    'key': i[0].title(),
                    'value': i[1].title(),
                    'notes': i[2] if len(i) >= 3 and i[2] and i[2][0] != '#' else '',
                    'tags': [j for j in i if j and j[0] == '#']
                }

                if card_data['key'] in self.data:
                    self.duplicates.append(card_data)
                    continue

                self.data.append(card_data)

        self.notify()

        # print(self.data)


if __name__ == "__main__":
    from src.tests import Test

    Test.run()
