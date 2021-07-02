with open('./all_heisig_6th_edition_kanji.txt', 'r', encoding='utf-8') as f:
    kanji = f.read().split()

print(kanji)

with open('../resources/all_heisig_6th_edition_kanji.txt', 'w', encoding='utf-8') as f:
    f.write(',' + '\n,'.join(kanji))
