import pykakasi


def add(data):
    c = pykakasi.kakasi()

    for i in range(len(data)):
        result = c.convert(data[i][0])

        if len(data[i]) >= 3 and data[i][2] == '':
            data[i].pop(2)

        if not result and (len(data[i]) >= 3 and '#' in data[i][2]):
            hira = ''

            user_in = input(f'\nNo furigana found for {data[i][0]}.\n(Press Enter to confirm or type new furigana)\n> ')
            data[i].insert(2, user_in if user_in else hira)
            continue

        hira = data[i][0]
        for j in result:
            hira = hira.replace(j['orig'], j['hira'])

        if len(data[i]) >= 3 and data[i][2] == hira:
            continue

        elif len(data[i]) >= 3 and data[i][2] and data[i][2][0] != '#':
            user_in = input(
                f'\n{data[i][0]} already has a value of {data[i][2]}!\nIs this correct? Predicted furigana: {hira}\n(Press Enter to confirm or type new furigana)\n> ')

            if user_in:
                data[i][2] = user_in
            continue

        elif data[i][0] == hira:
            user_in = input(
                f'\nPredicted furigana of {data[i][0]} is the same! (Or none was found)\n(Press Enter to leave empty or type new furigana)\n> ')
            data[i].insert(2, user_in if user_in else '')
            continue

        user_in = input(f'\nIs {hira} correct for {data[i][0]}?\n(Press Enter to confirm or type new furigana)\n> ')
        data[i].insert(2, user_in if user_in else hira)

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
