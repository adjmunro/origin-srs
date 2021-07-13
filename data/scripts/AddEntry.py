class WordList:

    def __init__(self, filename, n_cols):
        self.filename = filename + '.txt' if '.txt' not in filename else filename
        self.n_cols = n_cols
        self.elements = {}
        self.other_files = {}
        self.other_keys = []
        self.read()
        self.add()

    def add(self):
        n = 0
        while n < self.n_cols:

            while n == 0:
                key = input(f'(key) 0: ')

                if key == '':
                    n += 1
                    continue

                if key in self.elements:
                    v = input(
                        f"Key '{key}' already exists in this file!\n{key} -> {self.elements[key]}\nEnter a new value (single column), or 'x' to cancel.")
                    if v != 'x':
                        self.elements[key] = [v]
                    continue

                if key in self.other_keys:
                    filename, value = self.find(key)
                    if input(
                            f"Key '{key}' found in '{filename}'!\n{key} -> {value}\nEnter 'y' if you still wish to add this key.") != 'y':
                        continue

                self.elements.update({key: []})

            for key in self.elements.keys():
                if '' in self.elements[key]:
                    self.elements[key].remove('')

                if len(self.elements[key]) >= self.n_cols - 1:
                    continue

                elem = input(f'({n}) [{key}] -> ')

                if elem == '':
                    n = self.n_cols
                    break

                self.elements[key].append(elem.replace(',', ';'))

            n += 1

        self.write()

    def find(self, key):
        for f, i in self.other_files.items():
            if key in i:
                return (f, i[key])
        return None

    def read(self):
        if os.path.exists(self.filename):
            print('Adding to existing file')

            with open(self.filename, 'r', encoding='UTF-8') as f:
                temp = [i.split(',') for i in f.read().split('\n') if i != '']
                self.elements = {i[0]: i[1:] for i in temp}

        for filename in os.listdir():
            if filename == self.filename or '.txt' not in filename:
                continue

            print(f'Scanning {filename}')
            with open(filename, 'r', encoding='UTF-8') as f:
                temp = [i.split(',') for i in f.read().split('\n') if i != '']

            self.other_files.update({filename: {i[0]: i[1:] for i in temp}})
            self.other_keys += self.other_files[filename].keys()

    def write(self):
        with open(self.filename, 'w', encoding='UTF-8') as f:
            f.write('\n'.join([','.join([k] + v) for k, v in self.elements.items()]))


if __name__ == "__main__":
    import os

    filename = input('Enter filename: ')
    while filename == '':
        filename = input('Enter filename: ')

    n_cols = input('Enter max number of columns: ')
    while not n_cols.isdigit():
        print(f'"{n_cols}" is invalid!')
        n_cols = input('Enter max number of columns: ')

    WordList(filename, int(n_cols))
