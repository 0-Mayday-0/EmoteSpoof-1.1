import _tkinter
import tkinter as tk
from collections.abc import Coroutine
from tkinter import ttk
import strings as strs
from db import DbHandler
from tinydb import Query
from emote_handler import Emote
from icecream import ic
import os
from itertools import batched
import asyncio as ascio
from dotenv import load_dotenv
from PIL import *
from time import sleep as tsleep

class EmotesWindow(tk.Tk):
    def __init__(self, rows: int, cols: int) -> None:
        super().__init__()
        self._db_handle: DbHandler = DbHandler()
        self._query: Query = Query()
        self._rows: int = rows
        self._cols: int = cols
        self._buttons_per_page: int = rows * cols
        self._current_page: int = self._db_handle.current_page + 1
        self._pages_buttons: list[ttk.Button] = [ttk.Button(self, text=strs.Menu.External.NEXT_PAGE),
                                                 ttk.Button(self, text=strs.Menu.External.PREVIOUS_PAGE)]

        self._emotes_buttons: set[ttk.Button] = set()

        load_dotenv(f'./{strs.Handler.Internal.DOTENV_NAME}')

        ic("Created the switch pages buttons")

    def _place_pages_buttons(self) -> None:
        [button.grid(row=0, column=index) for index, button in enumerate(self._pages_buttons)]

    def _append_routine(self, emotes: list[Emote]) -> None:
        for v in emotes:
            ic(self._emotes_buttons)
            self._emotes_buttons.add(ttk.Button(self, image=tk.PhotoImage(
            file=f'{os.getenv(strs.Handler.Internal.IMG_CACHE_NAME)}/{repr(v)}.{v.get_extension()
            .replace('?', '')}'), command=v.copy_url))

    async def _cache_emotes(self, emotes: list[Emote]) -> None:

        for emote in emotes:
            await emote.save_to_cache()

        local_emotes: list[Emote] = []


        while len(local_emotes) < self._buttons_per_page:

            ic(self._emotes_buttons)
            try:
                local_emotes.append(emotes.pop(0))
            except _tkinter.TclError:
                ic("Caught!")
                continue
        self._append_routine(local_emotes)



        #(self._emotes_buttons.append(ttk.Button(self, image=f'./{strs.Handler.Internal.EMOTE_ID}{emote.get_extension()}' for emote in emotes))

    async def _generate_emote_page(self) -> None:
        self._place_pages_buttons()

        current_emotes: list[Emote] = [Emote(str(self._db_handle.get_db_obj.get(doc_id=i+1)[strs.Handler.Internal.EMOTE_URL])) for i in range(self._current_page * self._buttons_per_page)]

        await self._cache_emotes(current_emotes)

        grid_buttons: list[ttk.Button] = [ttk.Button(self, image=f'{os.getenv(strs.Handler.Internal.IMG_CACHE_NAME)}/'
                                                                 f'{k.get_id()}{k.get_extension()
                                          .replace('?', '')}') for k in current_emotes]




async def main() -> None:
    root = EmotesWindow(2,2)

    await root._generate_emote_page()

    root.mainloop()

    os.remove(f'./{strs.Handler.Internal.IMG_CACHE_NAME}/*')

if __name__ == '__main__':
    ascio.run(main())
