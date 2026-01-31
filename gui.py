import PySimpleGUI as sg
from db import DbHandler
from tinydb import Query
from custom_error import InvalidEmote
import os
from emote_handler import Emote
from itertools import batched
import strings as strs
from requests import get as rqget


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

def main():
    w: EmoteWindow = EmoteWindow("Emote Window", 4, 2)

    w.create_buttons()

    while True:
        event, values = w.read()

        if event == sg.WIN_CLOSED:
            break

        if event == strs.Menu.Internal.NX_PAGE_EVENT:
            w.next_page()

        if event == strs.Menu.Internal.PV_PAGE_EVENT:
            w.previous_page()

        if type(event) == Emote:
            event.copy_url()

    w.close()

if __name__ == "__main__":
    main()