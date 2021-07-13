from tkinter import *


class FilteredDeck:

    def __init__(self, parent, frame, title, keys, n_margin, bg, func, val=None):
        self.parent = parent
        self.frame = frame
        self.title = title.title().replace('_', ' ')

        self.func = func
        self.val = val if val else keys

        self.items = []
        self.due = parent.flashcard_manager.count_tag("#due", keys=keys)
        self.new = parent.flashcard_manager.count_tag("#new", keys=keys)

        w = self.parent.winfo_width()
        self.n_margin = n_margin
        self.we_margin = 80
        self.centre = w / 2
        self.height_constant = 46.25  # self.parent.winfo_height() (400-30) / 8
        self.label_height = 30
        self.number_width = 65
        self.label_width = w - 2 * (self.number_width + self.we_margin)
        #         self.margin = (w - 2*self.label_width) / 2
        #         self.due_lmargin = w - self.margin - self.label_width
        #         self.new_lmargin = w - self.margin - self.number_width

        self.draw(bg)

    def destroy(self):
        for i in self.items:
            i.place_forget()
            i.destroy()

    def draw(self, bg):
        self.destroy()

        # Make Labels
        self.items = [
            Label(self.frame, text=self.title, anchor=CENTER, fg=self.parent.config['fg'], bg=bg,
                  font=(self.parent.config['font_face'], self.parent.config['home_font_size'])),
            Label(self.frame, text=str(self.due), anchor=W, fg=self.parent.config['fg_due'], bg=bg,
                  font=(self.parent.config['font_face'], self.parent.config['home_font_size'])),
            Label(self.frame, text=str(self.new), anchor=E, fg=self.parent.config['fg_new'], bg=bg,
                  font=(self.parent.config['font_face'], self.parent.config['home_font_size'])),
        ]

        # Place Labels
        self.items[0].place(x=self.centre - (self.label_width / 2), y=self.height_constant * self.n_margin,
                            width=self.label_width, height=self.label_height)
        self.items[1].place(x=self.centre - (self.label_width / 2) - self.number_width,
                            y=self.height_constant * self.n_margin, width=self.number_width, height=self.label_height)
        self.items[2].place(x=self.centre + (self.label_width / 2), y=self.height_constant * self.n_margin,
                            width=self.number_width, height=self.label_height)

        # Bind Labels
        for i in self.items:
            if self.val:
                i.bind("<Button-1>", lambda e, val=self.val: self.func(val))


if __name__ == "__main__":
    from src.tests import Test

    Test.run()
