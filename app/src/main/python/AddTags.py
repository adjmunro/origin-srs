def add(data):
    new_tag = input('Enter a new tag, or press enter to exit.\n> ')
    while new_tag:
        data = tag(data, get(data), get(data, False), new_tag)
        new_tag = input('\nEnter a new tag, or press enter to exit.\n> ')

    return data


def find(data, key):
    try:
        return [i[0] for i in data].index(key)
    except ValueError:
        return -1


def get(data, start=True):
    i = None
    while i is None:
        i = input(
            f'\nEnter a {"start" if start else "end"} line number (1->{len(data)} incl.), key (incl.), or press enter for line {1 if start else len(data)}.\n> ')
        if not i:
            i = 0 if start else len(data) - 1
        elif i.isdigit():
            i = int(i) - 1
            if i < 0 or i > len(data):
                print(f'\nIndex out of range (1->{len(data)})')
                i = None
            elif input(f'\nLine {i + 1}: {data[int(i)][0]}\nPress Enter to confirm. (Or type any key to cancel)\n> '):
                i = None
                print('Canceled.')
        else:
            i = find(data, i)
            if i == -1:
                print('\nKey not found.')
                i = None

    return i


def tag(data, start, end, tag):
    if tag[0] != '#':
        tag = '#' + tag

    while start <= end:
        if tag not in data[start]:
            data[start].append(tag)

        start += 1

    return data


def read(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        return [i.split(',') for i in f.read().split('\n')]


def write(filename, data):
    if data:
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write('\n'.join([','.join(i) for i in data]))


if __name__ == "__main__":
    filename = input('Enter filename: ')
    while filename == '':
        filename = input('Enter filename: ')

    if '.txt' not in filename:
        filename += '.txt'

    data = add(read(filename))
    write(filename, data)
