import os
import shutil

import SRSApp

path = ''

test_words = """月曜日,monday,げつようび,#weekdays
火曜日,tuesday,かようび,#weekdays,#ka
水曜日,wednesday,すいようび,#weekdays
木曜日,thursday,もくようび,#weekdays
金曜日,friday,きんようび,#weekdays
土曜日,saturday,どようび,#weekdays
日曜日,sunday,にちようび,#weekdays
カタカナ,katakana,#katakana,#ka
ドキドキする,heart throbbing,,#verb,#katakana"""

test_heisig = """one,一,#heisig,#kanji,#number
two,二,#heisig,#kanji,#number
three,三,#heisig,#kanji,#number
four,四,#heisig,#kanji,#number
five,五,#heisig,#kanji,#number
six,六,#heisig,#kanji,#number
seven,七,#heisig,#kanji,#number
eight,八,#heisig,#kanji,#number
nine,九,#heisig,#kanji,#number
ten,十,#heisig,#kanji,#number
moon,月,#heisig,#kanji,#element
fire,火,#heisig,#kanji,#element
water,水,#heisig,#kanji,#element
tree,木,#heisig,#kanji,#element
gold,金,#heisig,#kanji,#element
earth,土,#heisig,#kanji,#element
sun,日,#heisig,#kanji,#element"""


def run():
    print('Removing', path)
    if os.path.exists(path):
        shutil.rmtree(path)

    print('Creating', path)
    os.mkdir(path)
    write_tests(path)

    print('Testing App')
    app = SRSApp.SRSApp(path)
    app.import_cards()
    app.mainloop()


def write_tests(path):
    path = f'{path}/resources'

    print('Creating', path)
    os.mkdir(path)

    print('Writing Test Decks')
    with open(f'{path}/test_blank.txt', 'w', encoding='UTF-8') as f:
        f.write('')

    with open(f'{path}/test_words.txt', 'w', encoding='UTF-8') as f:
        f.write(test_words)

    with open(f'{path}/test_heisig.txt', 'w', encoding='UTF-8') as f:
        f.write(test_heisig)


if __name__ == "__main__":
    run()
