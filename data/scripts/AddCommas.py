def add(filename, n_cols):
    with open(filename, 'r', encoding='UTF-8') as f:
        lines = f.read().split('\n')

    for i, line in enumerate(lines):
        if line.count(',') + 1 < n_cols:
            lines[i] = line + ','

    with open(filename, 'w', encoding='UTF-8') as f:
        f.write('\n'.join(lines))


if __name__ == "__main__":
    import os

    filename = input('Enter filename: ')
    while filename not in os.listdir():
        print(f'"{filename}" not found!')
        filename = input('Enter filename: ')

    n_cols = input('Enter max number of columns: ')
    while not n_cols.isdigit():
        print(f'"{n_cols}" is invalid!')
        n_cols = input('Enter max number of columns: ')

    add(filename, int(n_cols))
