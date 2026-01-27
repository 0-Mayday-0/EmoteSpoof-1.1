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
from time import sleep as tsleep
import shutil

class EmotesWindow(tk.Tk):
    def __init__(self, rows: int, cols: int) -> None:
        super().__init__()
        self._db_handle: DbHandler = DbHandler()
        self._query: Query = Query()
        self._rows: int = rows
        self._cols: int = cols
        self._buttons_per_page: int = rows * cols
        self._current_page: int = self._db_handle.current_page + 1
        self._current_emotes: list[Emote] = []
        self._pages_buttons: list[ttk.Button] = []

        self._emotes_buttons: set[ttk.Button] = set()
        self._current_images: list[tk.PhotoImage] = []

        load_dotenv(f'./{strs.Handler.Internal.DOTENV_NAME}')

        ic(strs.Menu.Debug.CREATED_SWITCH)

    async def _previous_page(self) -> None:
        if self._current_page == 0:
            ic("No more pages")
            pass
        else:
            self._destroy_page()
            self._current_page -= 1
            ic(self._current_page)
            await self._generate_emote_page()

    async def _next_page(self) -> None:
        if self._current_page+1 > self._buttons_per_page:
            ic("No more pages")
            pass
        else:
            self._destroy_page()
            self._current_page += 1
            ic(self._current_page)
            await self._generate_emote_page()

    def _invoke_previous_page(self) -> None:
        ascio.run(self._previous_page())

    def _invoke_next_page(self) -> None:
        ascio.run(self._next_page())

    def _place_pages_buttons(self) -> None:
        self._pages_buttons = [ttk.Button(self, text=strs.Menu.External.PREVIOUS_PAGE, command=self._invoke_previous_page),
                               ttk.Button(self, text=strs.Menu.External.NEXT_PAGE, command=self._invoke_next_page)]
        [button.grid(row=0, column=index) for index, button in enumerate(self._pages_buttons)]


    @staticmethod
    async def _cache_emotes(emotes: list[Emote]) -> list[tk.PhotoImage]:

        try:
            os.mkdir(f'./{os.getenv(strs.Handler.Internal.IMG_CACHE_NAME)}')

        except FileExistsError as e:
            ic(e)


        for emote in emotes:
            await emote.save_to_cache()


        return [tk.PhotoImage(file=f'{os.getenv(strs.Handler.Internal.IMG_CACHE_NAME)}/{eid.get_id()}'
                                   f'{eid.get_extension().replace('?', '')}') for eid in emotes]

    def _destroy_page(self) -> None:
        for i in self.slaves():
            ic(i)


    async def _generate_emote_page(self) -> None:
        self._place_pages_buttons()

        self._current_emotes: list[Emote] = [Emote(str(self._db_handle.get_db_obj.get(doc_id=i+1)
                                                 [strs.Handler.Internal.EMOTE_URL])) for i in range
                                                 (self._current_page * self._buttons_per_page)]


        self._current_images: list[tk.PhotoImage] = await self._cache_emotes(self._current_emotes)

        grid_buttons: list[ttk.Button] = [ttk.Button(self, image=image, width=48, command=emote.copy_url) for image, emote in zip(self._current_images, self._current_emotes)]

        for x, v in enumerate(grid_buttons):
            for y, v1 in enumerate(grid_buttons):
                v.grid(row=y, column=x)


    @staticmethod
    def clear_cache() -> None:
        shutil.rmtree(f'./{os.getenv(strs.Handler.Internal.IMG_CACHE_NAME)}')


async def main() -> None:
    root = EmotesWindow(2,2)

    await root._generate_emote_page()

    root.mainloop()

    root.clear_cache()

if __name__ == '__main__':
    ascio.run(main())
