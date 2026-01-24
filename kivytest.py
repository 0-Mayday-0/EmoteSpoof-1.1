from db import DbHandler
from tinydb import Query
from custom_error import InvalidEmote
import os
from emote_handler import Emote
from itertools import batched
import strings as strs
from asyncio import create_task, Task, gather, run, get_event_loop
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

class EmotesPack(GridLayout):
    def __init__(self, rows: int, cols: int):
        super().__init__()
        self.cols = cols
        self.rows = rows
        self.max_buttons: int = rows * cols
        self._db: DbHandler = DbHandler(10)
        self._query: Query = Query()

        self.add_widget(Button(text="Next page"))
        self.add_widget(Button(text="Previous page"))

        [self.add_widget(Button(text=i)) for i in range(self.max_buttons)]

    async def create_page(self) -> None:
        current_page_buttons: list[Button] = []


        current_cache = [await Emote(self._db.get_db_obj.get(doc_id=i+1)[strs.Handler.Internal.EMOTE_URL]).save_to_cache() for i in range(self.max_buttons)]

        for i in current_cache:
            self.add_widget(Button(text=str(i)))

class EmotesApp(App):
    async def build(self) -> EmotesPack:
        return EmotesPack(3,3)

async def main() -> None:

   await EmotesApp().async_run()

if __name__ == '__main__':
    loop = get_event_loop()

    loop.run_until_complete(main())
    loop.close()