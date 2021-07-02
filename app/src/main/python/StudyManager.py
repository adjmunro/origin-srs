import random


# StudyManager uses a capacity-based SRS system
class StudyManager:

    def __init__(self, new_keys, review_keys=[], intro_size=5, sizes=[5, 10, 20, 40]):
        self.counter = intro_size
        self.intro_size = intro_size
        self.sizes = sizes
        self.tray_index = 0

        self.results = {k: [] for k in new_keys + review_keys}
        self.trays = [[k for k in new_keys]] + [[] for i in range(len(self.sizes) + 1)]
        self.trays[round(len(self.trays) / 2)] = review_keys

        self.views = 0
        self.success_rate = 0

    # Returns the key of the next card to study
    def __next__(self):
        # Finds the next tray to study if the current one has been emptied
        # Or if current tray is 'New' and counter has reached 0
        if not len(self.trays[self.tray_index]) or not (self.tray_index or self.counter):

            # Determines the capacity of each working tray
            filled = [len(self.trays[1:-1][i]) / self.sizes[i] for i in range(len(self.sizes))]

            # If all working trays are empty, but not the new cards tray, get more from the new cards tray
            # If all working trays are empty, and the new card tray is empty, declare the end of study
            # Otherwise, return the last index of the tray(s) with the highest capacity
            if not sum(filled):
                if len(self.trays[0]):
                    self.tray_index = 0
                    self.counter = min(self.intro_size, len(self.trays[0]))
                else:
                    return None

            # If any working tray has reached max capacity, study it! (back to front)
            elif 1 in filled:
                self.tray_index = len(filled) - filled[::-1].index(1)

            # If the first working tray is empty and no working tray is full
            # and there are still cards in the 'New' tray, study 'New' tray and reset counter
            elif len(self.trays[0]) and not len(self.trays[1]):
                self.counter = min(self.intro_size, len(self.trays[0]))
                self.tray_index = 0

            # If all else if false, study the tray with the highest capacity (back to front)
            else:
                self.tray_index = len(filled) - filled[::-1].index(max(filled))

            # If not 'New' tray (since one might want some to be introduced in order)
            # shuffle the tray before studying
            if self.tray_index:
                random.shuffle(self.trays[self.tray_index])

        # If counting new cards introduced, decrease counter
        if self.counter:
            self.counter -= 1

        # Returns the first element of the current tray
        return self.trays[self.tray_index][0]  # sorted(m.trays[:-1], key=lambda i: len(i), reverse=True)

    # Locates the current tray of a given key
    def find(self, key):
        for i in range(len(self.trays)):
            if key in self.trays[i]:
                return i

        return None

    # Returns the results of all cards studied
    def get(self):
        return {k: {
            'pass': len(v) - v.count(0),
            'fail': v.count(0),
            'attempts': len(v),
            'avg_score': sum(v) / len(v)
        } if len(v) > 0 else None
                for k, v in self.results.items()}

    # Marks a card based on number pressed and time taken to answer
    # and uses this mark to determine which tray it should be moved to
    def mark(self, key, difficulty, time):
        tray_number = self.find(key)

        if tray_number is None:
            return

        # To be counted as correct, it must be answered within a fraction of
        # the time limit, based on which number button was pressed (1-4)
        self.results[key].append(difficulty if (difficulty != 1 and time < 60 / difficulty) else 0)
        self.move(key, tray_number, (difficulty - 1) if self.results[key][-1] else -1)

        self.views += 1
        self.success_rate += min(1, self.results[key][-1])

        print(
            f'New {len(self.trays[0])}  |  Fin {len(self.trays[-1])}  |  Success Rate {self.success_rate / self.views * 100:.2f}%  |  Viewed {self.views}')
        print('  |  '.join([f'T{i + 1}({len(self.trays[i + 1])}/{self.sizes[i]})' for i in range(len(self.sizes))]))

    # Moves the key to the appropriate tray
    def move(self, key, source, diff):
        # Binds the target tray to only working trays (not new or finished)
        target = min(max(1, source + diff), len(self.trays) - 1)

        # Removes and appends to new tray
        # Note: if tray is the same, this moves it to the end of the queue
        self.trays[source].remove(key)
        self.trays[target].append(key)
        # print(f'{key}({self.results[key][-1]}) {source}->{target}', self.trays)


if __name__ == "__main__":
    test1 = "一,二,三,四,五,六,七,八,九,十,月,火,水,木,金,土,日".split(',')
    test2 = 'q,w,e,r,t,y'.split(',')

    m = StudyManager(test2, review_keys=test1)
    i = 0
    k = next(m)
    while k != None and i < 40:
        d = random.randint(1, 4)
        t = random.randint(1, 30)
        m.mark(k, d, t)
        k = next(m)
        i += 1

    print(m.get())
