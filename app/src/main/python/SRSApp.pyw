#! python3
import json
import os
import random
from datetime import datetime as date
from tkinter import *

import Adder
import FlashcardManager
import Importer
import StudyManager
from FilteredDeck import FilteredDeck

MENU = 0
LOAD = 1
FRONT = 2
BACK = 3
ADD = 4


class SRSApp(Tk):

    def __init__(self, path='..'):
        super().__init__()

        self.title('Flashcards')
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.geometry(f'450x400+{(self.winfo_screenwidth() - 500) // 2}+140')
        self.update_idletasks()

        self.bind("<KeyPress>", self.key_pressed)
        self.focus_set()

        self.path = path

        self.config = {
            'min_degree': -5,
            'max_degree': 10,
            'new_card_limit': 10,
            'review_card_limit': 15,
            'intro_size': 5,
            'sizes': [5, 10, 20, 40],  # REMEMBER IF YOU"RE TRYING TO CHANGE THIS, CHANGE THE JSON FILE
            'front_font_size': 48,
            'back_font_size': 32,
            'sub_font_size': 24,
            'home_font_size': 18,
            'font_face': 'Times New Roman',
            'fg': 'white',
            'fg_due': 'green',
            'fg_new': 'blue'
        }
        self.read()  # Remember to delete JSON file if default config changes!

        self.flashcard_manager = FlashcardManager.FlashcardManager(path, self.config['min_degree'],
                                                                   self.config['max_degree'])
        self.study_manager = None

        self.fronttext = StringVar()
        self.backtext = StringVar()
        self.subtext = StringVar()
        self.frame = Frame(self)
        self.frontlabel = Label(self, textvariable=self.fronttext,
                                font=(self.config['font_face'], self.config['front_font_size']), fg=self.config['fg'])
        self.backlabel = Label(self, textvariable=self.backtext,
                               font=(self.config['font_face'], self.config['back_font_size']), fg=self.config['fg'])
        self.sublabel = Label(self, textvariable=self.subtext,
                              font=(self.config['font_face'], self.config['sub_font_size']), fg=self.config['fg'])

        # Initialise an empty deck
        self.card_menu()
        # self.add()

    def add(self):
        self.forget_card_menu()
        self.screen_state = ADD
        self.adder = Adder.Adder(self, self.path)

    def card_back(self):
        self.screen_state = BACK
        self.backtext.set(self.flashcard_manager.get(self.current_card, 'value'))
        self.backlabel.config(bg=self.get_colour(), wraplength=self.winfo_width() - 20)
        self.backlabel.pack(fill=BOTH, expand=1)

        notes = self.flashcard_manager.get(self.current_card, 'notes')
        if notes:
            self.subtext.set(notes)
            self.sublabel.config(bg=self.get_colour(), wraplength=self.winfo_width() - 20)
            self.sublabel.pack(fill=BOTH, expand=1)

    def card_front(self):
        self.current_card = next(self.study_manager)

        if self.current_card == None:
            self.card_menu()
            return

        self.screen_state = FRONT
        self.start_time = date.now()

        self.fronttext.set(self.current_card)
        self.frontlabel.config(bg=self.get_colour(), wraplength=self.winfo_width() - 20)
        self.frontlabel.pack(fill=BOTH, expand=1)

        self.backlabel.pack_forget()
        self.sublabel.pack_forget()

    def card_menu(self):
        self.screen_state = MENU
        self.current_card = ''

        if self.study_manager:
            self.flashcard_manager.mark(self.study_manager.get())
            self.flashcard_manager.write()
            self.study_manager = None

        self.frontlabel.pack_forget()
        self.backlabel.pack_forget()
        self.sublabel.pack_forget()
        self.frame.pack(fill=BOTH, expand=1)

        bg = self.get_colour()
        self.frame.config(bg=bg)

        fm = self.flashcard_manager

        w = self.winfo_width()
        self.header = Label(self.frame, text='Decks', anchor=W, fg=self.config['fg'],
                            font=(self.config['font_face'], self.config['home_font_size'] + 10), bg=bg)
        self.header.place(x=60, y=50, width=w - 120, height=35)
        self.hr_line = Label(self.frame, text='- ' * (w // 23), fg=self.config['fg'],
                             font=(self.config['font_face'], self.config['home_font_size']), bg=bg)
        self.hr_line.place(x=60, y=3.5 * 46.25, width=w - 120, height=30)
        self.progress = Label(self.frame, text=f'{fm.count_tag("#new")} Unseen | {len(fm.get_keys())} Total', anchor=E,
                              fg=self.config['fg'], bg=bg,
                              font=(self.config['font_face'], self.config['home_font_size'] - 6))
        self.progress.place(x=0, y=self.winfo_height() - 32, width=w - 10, height=30)

        self.card_menu_objects = [
            FilteredDeck(self, self.frame, title='all', keys=fm.get_keys(), n_margin=2, func=self.load_deck, bg=bg),
            FilteredDeck(self, self.frame, title='due', keys=fm.filter_tag('#due'), n_margin=2.5, func=self.load_deck,
                         bg=bg),
            FilteredDeck(self, self.frame, title='new', keys=fm.filter_tag('#new'), n_margin=3, func=self.load_deck,
                         bg=bg)
        ]

        for i, d in enumerate(fm.get_decks()):
            self.card_menu_objects.append(
                FilteredDeck(self, self.frame, title=d, keys=fm.filter_deck(d), n_margin=4 + i * 0.5,
                             func=self.card_load, val=d, bg=bg)
            )

    def card_load(self, deck):
        self.screen_state = LOAD
        self.forget_card_menu()
        self.frame.pack(fill=BOTH, expand=1)

        bg = self.get_colour()
        self.frame.config(bg=bg)

        fm = self.flashcard_manager
        k = fm.filter_deck(deck)
        self.current_deck = deck

        w = self.winfo_width()
        self.header = Label(self.frame, text=deck.title().replace('_', ' '), anchor=W, fg=self.config['fg'],
                            font=(self.config['font_face'], self.config['home_font_size'] + 10), bg=bg)
        self.header.place(x=60, y=50, width=w - 120, height=40)
        self.hr_line = Label(self.frame, text='- ' * (w // 23), fg=self.config['fg'],
                             font=(self.config['font_face'], self.config['home_font_size']), bg=bg)
        self.hr_line.place(x=60, y=3.5 * 46.25, width=w - 120, height=30)
        self.progress = Label(self.frame, text=f'{fm.count_tag("#new", keys=k)} Unseen | {len(k)} Total', anchor=E,
                              fg=self.config['fg'], bg=bg,
                              font=(self.config['font_face'], self.config['home_font_size'] - 6))
        self.progress.place(x=0, y=self.winfo_height() - 32, width=w - 10, height=30)

        self.card_menu_objects = [
            FilteredDeck(self, self.frame, title='all', keys=k, n_margin=2, func=self.load_deck, bg=bg),
            FilteredDeck(self, self.frame, title='due', keys=fm.filter_tag('#due', keys=k), n_margin=2.5,
                         func=self.load_deck, bg=bg),
            FilteredDeck(self, self.frame, title='new', keys=fm.filter_tag('#new', keys=k), n_margin=3,
                         func=self.load_deck, bg=bg)
        ]

        for i, t in enumerate(fm.get_tags(deck, False)):
            self.card_menu_objects.append(
                FilteredDeck(self, self.frame, title=t, keys=fm.filter_tag(t), n_margin=4 + i * 0.5,
                             func=self.load_deck, bg=bg)
            )

    def close(self):
        if self.study_manager:
            self.flashcard_manager.mark(self.study_manager.get())

        self.write()
        self.flashcard_manager.write()
        self.destroy()

    def forget_card_menu(self):
        self.frame.pack_forget()
        self.header.place_forget()
        self.hr_line.place_forget()
        self.progress.place_forget()
        while self.card_menu_objects:
            obj = self.card_menu_objects.pop(0)
            obj.destroy()

    def get_colour(self):
        return '#' + ''.join([hex(random.randint(50, 200))[-2:] for i in range(3)])

    def import_cards(self):
        importer = Importer.Importer(self.path)
        importer.read()
        self.flashcard_manager.add(importer)
        self.flashcard_manager.read()
        self.card_menu()

    def key_pressed(self, e):
        self.forget_card_menu()
        # print(e.keysym)

        if self.screen_state == ADD:
            if e.keysym == 'Escape' and self.adder.finish():
                self.adder.destroy()
                self.import_cards()
                self.card_menu()
            elif e.keysym == 'Return':
                self.adder.submit()

        elif e.keysym == 'Escape':
            self.card_menu()

        elif self.screen_state == MENU:
            if e.keysym == 'a':
                self.add()
            elif e.keysym == 'I':
                # hard import cards (hence the need for shift as well) soft import with 'i'
                self.import_cards()
            elif e.keysym == 'r':
                self.flashcard_manager.read()
                self.card_menu()
            elif e.keysym == 'Right':
                self.flashcard_manager.tomorrow()
                self.card_menu()
            elif e.keysym == 'Left':
                self.flashcard_manager.yesterday()
                self.card_menu()
            else:
                # Any other key just reloads/refreshes card_menu
                self.card_menu()

        elif self.screen_state == LOAD:
            if e.keysym == 'Right':
                self.flashcard_manager.tomorrow()
            elif e.keysym == 'Left':
                self.flashcard_manager.yesterday()

            self.card_load(self.current_deck)

        elif self.screen_state == FRONT:
            self.elapsed_time = min(max(1, (date.now() - self.start_time).seconds), 60)
            self.card_back()

        elif self.screen_state == BACK:
            if e.keysym in ['1', '2', '3'] or (
                    e.keysym == '4' and self.flashcard_manager.allow_extra_delay(self.current_card)):
                self.study_manager.mark(self.current_card, int(e.keysym), self.elapsed_time)
                self.card_front()

            elif e.keysym in ['space', 'Return']:
                self.study_manager.mark(self.current_card, 2, self.elapsed_time)
                self.card_front()

    def load_deck(self, keys):
        self.forget_card_menu()

        new = self.flashcard_manager.filter_tag('#new', keys=keys)[:self.config['new_card_limit']]
        due = self.flashcard_manager.filter_tag('#due', keys=keys)[:self.config['review_card_limit']]
        self.study_manager = StudyManager.StudyManager(new, due, self.config['intro_size'], self.config['sizes'])

        self.card_front()

    def read(self):
        if not os.path.exists(f'{self.path}/json/config.json'):
            self.write()
            return

        with open(f'{self.path}/json/config.json', 'r') as f:
            self.config = json.load(f)

    def write(self):
        if not os.path.exists(f'{self.path}/json'):
            os.mkdir(f'{self.path}/json')

        with open(f'{self.path}/json/config.json', 'w') as f:
            f.write(json.dumps(self.config))


if __name__ == "__main__":
    #     import Test
    #     Test.run()
    app = SRSApp()
    app.mainloop()
