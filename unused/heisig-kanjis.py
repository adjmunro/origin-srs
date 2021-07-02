import_ed = 6

with open('heisig-kanjis.csv', 'r', encoding='utf-8') as f:
    hk = [i.split(',') for i in f.read().split('\n')]

# print(hk)

kanji = hk[0].index('kanji')
n = hk[0].index(f'id_{import_ed}th_ed')
keyword = hk[0].index(f'keyword_{import_ed}th_ed')
components = hk[0].index('components')

s = '\n'.join(
    [','.join(j[1:]) for j in sorted([[int(i[n]), i[keyword], i[kanji]] for i in hk if len(i) > 2 and i[n].isdigit()])])

# print(s)

with open(f'../resources/heisig_{import_ed}th_edition.txt', 'w', encoding='utf-8') as f:
    f.write(s)
