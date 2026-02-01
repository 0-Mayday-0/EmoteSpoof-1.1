import PySimpleGUI as sg
from db import DbHandler
from tinydb import Query
from custom_error import InvalidEmote
import os
from emote_handler import Emote
from itertools import batched
import strings as strs
from requests import get as rqget
import tkinter.messagebox as messagebox


global_rows, global_cols = 5, 5

class EmoteWindow(sg.Window):
    def __init__(self, title: str, rows: int, cols: int, expand: bool = True) -> None:
        super().__init__(title)

        self._rows = rows
        self._cols = cols
        self._expand = expand
        self._layouts: list[list[sg.Column]] = []
        self.db: DbHandler = DbHandler()
        self._max_emotes: int = rows * cols
        self._current_page: int = 0
        self._pager: list[sg.Button] = [sg.Button(button_text=strs.Menu.External.PREVIOUS_PAGE,
                                                  key=strs.Menu.Internal.PV_PAGE_EVENT),
                                        sg.Button(button_text=strs.Menu.External.NEXT_PAGE,
                                                  key=strs.Menu.Internal.NX_PAGE_EVENT)]
        self._all_emotes: list[Emote] = [Emote(i[strs.Handler.Internal.EMOTE_URL]) for i in self.db.get_db_obj.all()]

        self._all_buttons: list[sg.Button] = [sg.Button(image_data=rqget(emote.get_url()).content,
                                                        key=emote,
                                                        expand_y=self._expand,
                                                        expand_x=self._expand) for emote in self._all_emotes]

        self._button_pages: list[tuple[sg.Button, ...]] = list(batched(self._all_buttons, self._max_emotes))

        del self._all_emotes, self._all_buttons


    def create_buttons(self):
        for i, v in enumerate(self._button_pages):
            curr_layout = []
            for button in v:
                curr_layout.append(button)

            curr_layout = list(batched(curr_layout, self._cols))

            self._layouts.append(sg.Column(curr_layout, key=i, expand_y=self._expand, expand_x=self._expand))

        self.layout(rows=[self._pager] + [self._layouts])

        self.finalize()

        for i, v in enumerate(self._button_pages):
            if i == 0:
                continue
            self[self._current_page+i].update(visible=False)

    def next_page(self):

        try:
            if self._current_page + 1 == len(list(self._button_pages)):
                raise IndexError
            else:
                self[self._current_page].update(visible=False)
                self._current_page += 1

            self[self._current_page].update(visible=True)
        except IndexError:
            print(strs.Menu.External.NO_MORE_PAGES)



    def previous_page(self):
        try:
            if self._current_page - 1 < 0:
                raise IndexError
            else:
                self[self._current_page].update(visible=False)
                self._current_page -= 1

            self[self._current_page].update(visible=True)
        except IndexError:
            print(strs.Menu.External.NO_MORE_PAGES)

class MainMenu(sg.Window):
    def __init__(self, title: str) -> None:
        super().__init__(title)
        self._buttons: list[sg.Button] = [sg.Button(button_text=strs.Menu.External.ADD_EMOTE, key=strs.Menu.Internal.ADD_EVENT),
                                          sg.Button(button_text=strs.Menu.External.REMOVE_EMOTE, key=strs.Menu.Internal.RM_EVENT),
                                          sg.Button(button_text=strs.Menu.External.EMOTES, key=strs.Menu.Internal.EMOTES_EVENT)]

        self.layout(rows=[self._buttons])

class AddEmote(sg.Window):
    def __init__(self, title: str) -> None:
        super().__init__(title)
        self._db: DbHandler = DbHandler()
        self._buttons: list[sg.Button] = [sg.Button(button_text=strs.Menu.External.ADD_EMOTE, key=strs.Menu.Internal.ADD_EVENT)]
        self._url_input: list[sg.Input] = [sg.Input(key=strs.Menu.Internal.URL_KEY)]

        self.layout(rows=[self._buttons] + [self._url_input])

    def read_url(self):
        try:
            e: Emote = Emote(self[strs.Menu.Internal.URL_KEY].get())
            self[strs.Menu.Internal.URL_KEY].update('')
            self._db.add_emote(e.get_url())

        except InvalidEmote:
            messagebox.showerror(title=strs.Menu.External.INVALID_URL ,message=strs.Handler.External.INVALID_URL)



def run_emotes() -> None:
    w: EmoteWindow = EmoteWindow("Emote Window", global_rows, global_cols)

    w.create_buttons()

    while True:
        event, values = w.read()

        if event == sg.WIN_CLOSED:
            w.close()
            run_main()
            break

        if event == strs.Menu.Internal.NX_PAGE_EVENT:
            w.next_page()

        if event == strs.Menu.Internal.PV_PAGE_EVENT:
            w.previous_page()

        if type(event) == Emote:
            event.copy_url()


def run_add() -> None:
    add_window: AddEmote = AddEmote("Add Emote")

    while True:
        event, values = add_window.read()

        if event == sg.WIN_CLOSED:
            add_window.close()
            run_main()
            break

        if event == strs.Menu.Internal.ADD_EVENT:
            add_window.read_url()

def run_remove() -> None:
    remove_window: EmoteWindow = EmoteWindow("Remove Emote", global_rows, global_cols)

    remove_window.create_buttons()

    while True:
        event, values = remove_window.read()

        if event == sg.WIN_CLOSED:
            remove_window.close()
            run_main()
            break

        if event == strs.Menu.Internal.NX_PAGE_EVENT:
            remove_window.next_page()

        if event == strs.Menu.Internal.PV_PAGE_EVENT:
            remove_window.previous_page()

        if type(event) == Emote:
            success: str = remove_window.db.remove_emote(event.get_id().replace('.', ''))
            messagebox.showinfo(title=strs.Menu.External.REMOVED, message=success)

def run_main() -> None:
    mm: MainMenu = MainMenu("Main Menu")

    while True:
        event, values = mm.read()

        if event == sg.WIN_CLOSED:
            break

        if event == strs.Menu.Internal.ADD_EVENT:
            mm.close()
            run_add()

        if event == strs.Menu.Internal.RM_EVENT:
            mm.close()
            run_remove()

        if event == strs.Menu.Internal.EMOTES_EVENT:
            mm.close()
            run_emotes()
    mm.close()

def main():
    run_main()

if __name__ == "__main__":
    main()