from tkinter import *


class Adder:

    def __init__(self, parent, path):
        self.parent = parent
        self.path = path + '/resources'

        self.elements = {}
        self.last_key = ''
        self.key = ''
        self.next_key = ''
        self.col = 0

        self.frame = None
        self.display_objects = []
        self.filename = 'default.txt'
        self.max_cols = 2

        self.draw()

    def __next__(self):
        if self.col == 0:
            return ''

        keys = [j for i in self.elements for j in self.elements[i]]

        if not len(keys):
            return ''

        if self.key == '':
            return keys[0]

        i = 1
        j = keys.index(self.key)
        key = keys[(j + i) % len(keys)]
        filename = self.find(key)[0]
        while len(self.elements[filename][key]) >= self.col - 1:
            i += 1
            key = keys[(j + i) % len(keys)]
            filename = self.find(key)[0]
            print(i)
            if i > len(keys):
                if self.finish():
                    self.destroy()
                    self.parent.import_cards()
                    self.parent.menu()
                    return None

                print('next')
                return next(self)

        return key

    def destroy(self):
        self.write()
        self.forget()

    def draw(self):
        self.forget()

        w = self.parent.winfo_width()
        padx = 20
        h = self.parent.winfo_height()
        midh = h / 2
        pady = 30
        stdh = 25

        self.v_alert = StringVar()
        self.v_cols = StringVar()
        self.v_elem = StringVar()
        self.v_last = StringVar()
        self.v_next = StringVar()
        self.v_prompt = StringVar()
        self.v_tag = StringVar()

        self.v_cols.set('2')
        self.v_tag.set('default.txt')

        self.frame = Frame(self.parent)
        self.display_objects = [
            Label(self.frame, text='Add', anchor=W,
                  font=(self.parent.config['font_face'], self.parent.config['home_font_size'] + 10)),
            Label(self.frame, textvariable=self.v_last,
                  font=(self.parent.config['font_face'], self.parent.config['home_font_size'] - 6)),
            Label(self.frame, textvariable=self.v_prompt, anchor=W,
                  font=(self.parent.config['font_face'], self.parent.config['home_font_size'] - 4)),
            Label(self.frame, textvariable=self.v_next,
                  font=(self.parent.config['font_face'], self.parent.config['home_font_size'] - 6)),
            Label(self.frame, textvariable=self.v_alert,
                  font=(self.parent.config['font_face'], self.parent.config['home_font_size'])),
            Entry(self.frame, textvariable=self.v_cols, justify=CENTER,
                  font=(self.parent.config['font_face'], self.parent.config['home_font_size'] - 6)),
            Entry(self.frame, textvariable=self.v_elem, justify=CENTER,
                  font=(self.parent.config['font_face'], self.parent.config['home_font_size'])),
            Entry(self.frame, textvariable=self.v_tag, justify=CENTER,
                  font=(self.parent.config['font_face'], self.parent.config['home_font_size'] - 6))
        ]

        self.frame.pack(fill=BOTH, expand=1)
        self.display_objects[0].place(x=(w - 330) / 2, y=46.25, width=64, height=pady)
        self.display_objects[1].place(x=0, y=h / 4, width=w, height=stdh)
        self.display_objects[2].place(x=padx, y=midh - pady, width=w - 2 * padx, height=stdh)
        self.display_objects[3].place(x=0, y=3 * h / 4, width=w, height=stdh)
        self.display_objects[5].place(x=w - padx - 180, y=midh + pady + 10, width=25, height=stdh)
        self.display_objects[6].place(x=padx, y=midh, width=w - 2 * padx, height=stdh + 10)
        self.display_objects[7].place(x=w - padx - 150, y=midh + pady + 10, width=150, height=stdh)

        self.refresh()

    def find(self, key):
        key = key.title()
        fm = self.parent.flashcard_manager

        for f, i in self.elements.items():
            if key in i:
                return (f, i[key])

        if fm.get(key):
            return (fm.get(key, 'tags'), fm.get(key, 'value'))

        return ('', '')

    def finish(self):
        self.col += 1
        self.refresh()
        return self.col >= self.max_cols

    def forget(self):
        if self.frame != None:
            self.frame.pack_forget()

        while self.display_objects:
            obj = self.display_objects.pop(0)
            obj.place_forget()
            obj.destroy()

    def refresh(self, back=False):
        bg = self.parent.get_colour()
        self.frame.config(bg=bg)
        for i in self.display_objects:
            i.config(fg='white', bg=bg)
        self.display_objects[4].config(fg='white', bg='red')

        self.v_cols.set(str(self.max_cols))
        self.v_elem.set('')

        if not back:
            self.last_key = self.key
            self.key = next(self)
            self.next_key = next(self)
        else:
            self.next_key = self.key
            self.key = self.last_key
            keys = [j for i in self.elements for j in self.elements[i]]
            self.last_key = '' if not len(keys) or self.key not in keys or keys.index(self.key) == '' else keys[
                (keys.index(self.key) - 1) % len(keys)]

        if self.key:
            self.filename = self.find(self.key)[0]
            self.v_tag.set(self.filename)

        if self.last_key:
            self.v_last.set(f'[{self.last_key}] -> {self.find(self.last_key)[1]}')
        else:
            self.v_last.set('')

        if self.key:
            self.v_prompt.set(f'({self.col}) [{self.key}] -> ')
        else:
            self.v_prompt.set('')

        if self.next_key:
            self.v_next.set(f'[{self.next_key}] -> {self.find(self.next_key)[1]}')
        else:
            self.v_next.set('')

    def submit(self):
        n_cols = self.v_cols.get()
        self.max_cols = 2 if not n_cols or not n_cols.isdigit() or int(n_cols) < 2 else int(n_cols)

        self.filename = self.v_tag.get() if self.filename else 'default.txt'
        if '.txt' not in self.filename:
            self.filename += '.txt'

        elem = self.v_elem.get()
        if elem == '':
            self.refresh()
            return

        if self.col == 0:
            result = self.find(elem)
            if result != ('', ''):
                self.v_alert.set(f"Key '{elem}' found in '{result[0]}'!\n{elem} -> {result[1]}")
                self.display_objects[4].place(x=0, y=self.parent.winfo_height() - 120, width=self.parent.winfo_width(),
                                              height=120)
                self.refresh()
                return

            if self.filename not in self.elements:
                self.elements.update({self.filename: {}})

            self.elements[self.filename].update({elem.title(): []})

        else:
            if self.filename not in self.elements:
                self.v_alert.set(f"'{self.filename}' not found!")
                self.display_objects[4].place(x=0, y=self.parent.winfo_height() - 120, width=self.parent.winfo_width(),
                                              height=120)
                self.refresh()
                return

            if self.key not in self.elements[self.filename]:
                self.v_alert.set(f"Key '{self.key}' not found!")
                self.display_objects[4].place(x=0, y=self.parent.winfo_height() - 120, width=self.parent.winfo_width(),
                                              height=120)
                self.refresh()
                return

            self.elements[self.filename][self.key].append(elem.lower())

        self.refresh()

    def write(self):
        for file in self.elements:
            with open(f'{self.path}/{file}', 'w', encoding='UTF-8') as f:
                f.write('\n'.join([','.join([k] + v) for k, v in self.elements[file].items()]))


if __name__ == "__main__":
    from src.tests import Test

    Test.run()
