import PySimpleGUI as sg
from db import DbHandler
from tinydb import Query
from custom_error import InvalidEmote
import os
from emote_handler import Emote
from itertools import batched
import strings as strs
from asyncio import create_task, Task, gather, run

class Window(sg.Window):
    def __init__(self, rows: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.emotes_db: DbHandler = DbHandler(10)
        self._query_obj: Query = Query()
        self.expand: bool = True
        self.current_page: int = 0
        self.rows: int = rows
        self._temp: list[Emote] = [Emote(i[strs.Handler.Internal.EMOTE_URL]) for i in self.emotes_db.get_db_obj.all()]


        self.emotes_pages: list[tuple[Emote, ...]] = list(batched(self._temp, self.rows))
        del self._temp


    async def create_emotes_page(self):
        print(self.emotes_pages)

        for emote in self.emotes_pages[self.current_page]:
            await emote.save_to_cache()

        current_layout: list[list[sg.Button]] = [[sg.Button(image_filename=f'./{os.getenv(strs.Handler.Internal.IMG_CACHE_NAME)}/{eid.get_id()}{eid.get_extension().replace('?', '')}',
                                                            enable_events=True,
                                                            key=eid) for eid in self.emotes_pages[self.current_page]]]

        pages_buttons: list[list[sg.Button]] = [[sg.Button(button_text=strs.Menu.External.PREVIOUS_PAGE,
                                                           key=strs.Menu.Internal.PV_PAGE_EVENT),
            sg.Button(button_text=strs.Menu.External.NEXT_PAGE,
                      key=strs.Menu.Internal.NX_PAGE_EVENT)]]

        self.layout(rows=current_layout + pages_buttons)

        self.finalize()

    def clear_cache(self):
        [os.remove(f'./img_cache/{emote.get_id()}{emote.get_extension().replace('?', '')}') for emote in self.emotes_db.emotes_pages()]

    def next_page(self):
        if self.current_page + 1 == len(self.emotes_pages):
            pass
        else:
            self.current_page += 1

    def previous_page(self):
        if self.current_page == 0:
            pass
        else:
            self.current_page -= 1

    @property
    def get_current_page(self):
        return self.current_page

async def main():
    window = Window(title='Test', rows=5)
    await window.create_emotes_page()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == strs.Menu.Internal.NX_PAGE_EVENT:
            window.clear_cache()
            window.next_page()

            await window.create_emotes_page()

        if event == strs.Menu.Internal.PV_PAGE_EVENT:
            window.clear_cache()
            window.previous_page()

            await window.create_emotes_page()

        if type(event) == Emote:
            event.copy_url()


if __name__ == '__main__':
    run(main())