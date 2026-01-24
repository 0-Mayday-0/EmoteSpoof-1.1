import PySimpleGUI as sg
from db import DbHandler
from tinydb import Query
from custom_error import InvalidEmote
import os
from emote_handler import Emote
from itertools import batched
import strings as strs
from asyncio import create_task, Task, gather, run

class EmoteWindow(sg.Window):
    def __init__(self, cols: int, max_per_page: int, max_rows: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.emotes_db: DbHandler = DbHandler(10)
        self._query_obj: Query = Query()
        self.expand: bool = True
        self.layouts: list[list[sg.Column]] = []
        self.current_page: int = 0
        self.max_per_page: int = max_per_page
        self.max_rows: int = max_rows
        self.cols: int = cols
        self._temp: list[Emote] = [Emote(i[strs.Handler.Internal.EMOTE_URL]) for i in self.emotes_db.get_db_obj.all()]
        self.emotes_buttons: list[sg.Button] = []
        self.buttons_pages: list[tuple[sg.Button, ...]] = []


    async def create_emotes_page(self):

        for emote in self._temp:
            await emote.save_to_cache()

        self.emotes_buttons: list[sg.Button] = [sg.Button(image_filename=f'./{os.getenv(strs.Handler.Internal.IMG_CACHE_NAME)}/{emote.get_id()}{emote.get_extension().replace('?', '')}',
                                                          enable_events=True, key=emote, expand_x=self.expand,
                                                          expand_y=self.expand) for emote in self._temp]

        self.buttons_pages: list[tuple[sg.Button, ...]] = list(batched(self.emotes_buttons, self.max_per_page))

        for index, page in enumerate(self.buttons_pages):
            temp_layout = []

            for button in page:
                temp_layout.append(button)

            temp_layout = list(batched(temp_layout, self.cols))


            self.layouts.append([sg.Column(temp_layout, key=index)])



        '''current_layout: list[list[sg.Button]] = [[sg.Button(image_filename=f'./{os.getenv(strs.Handler.Internal.IMG_CACHE_NAME)}/{eid.get_id()}{eid.get_extension().replace('?', '')}',
                                                            enable_events=True,
                                                            key=eid) for eid in self.emotes_pages[self.current_page]]]'''

        pages_buttons: list[list[sg.Button]] = [[sg.Button(button_text=strs.Menu.External.PREVIOUS_PAGE,
                                                           key=strs.Menu.Internal.PV_PAGE_EVENT),
                                                sg.Button(button_text=strs.Menu.External.NEXT_PAGE,
                                                key=strs.Menu.Internal.NX_PAGE_EVENT)]]

        self.layout(rows=[self.layouts] + pages_buttons)

        self.finalize()

        for i, v in enumerate(self.buttons_pages):
            if i == 0:
                continue
            else:
                self[self.current_page+i].update(visible=False)


    @staticmethod
    def clear_cache():
        os.system('del /f /s /q img_cache')


    async def next_page(self):
        if self.current_page + 1 == len(self.buttons_pages):
            pass
        else:
            self.current_page += 1
            self[self.current_page-1].update(visible=False)
            self[self.current_page].update(visible=True)

    async def previous_page(self):
        if self.current_page == 0:
            pass
        else:
            self.current_page -= 1
            self[self.current_page+1].update(visible=False)
            self[self.current_page].update(visible=True)

    @property
    def get_current_page(self):
        return self.current_page


async def mainloop(title: str, cols: int, max_rows: int, max_per_page: int) -> None:
    emote_window = EmoteWindow(title=title, cols=cols, max_rows=max_rows, max_per_page=max_per_page , resizable=True)
    await emote_window.create_emotes_page()

    while True:
        event, values = emote_window.read()

        if event == sg.WIN_CLOSED:
            emote_window.clear_cache()
            break

        if event == strs.Menu.Internal.NX_PAGE_EVENT:
            await emote_window.next_page()

        if event == strs.Menu.Internal.PV_PAGE_EVENT:
            await emote_window.previous_page()

        if type(event) == Emote:
            event.copy_url()

async def main():
    await mainloop(title="Emotes", cols=2, max_rows=3, max_per_page=10)



if __name__ == '__main__':
    run(main())