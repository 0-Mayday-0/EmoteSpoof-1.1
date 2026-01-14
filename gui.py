import PySimpleGUI as sg
from db import DbHandler
import os
import strings as strs
from asyncio import create_task, Task, gather, run

class Window(sg.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.emotes_db: DbHandler = DbHandler(10)
        self.layout = []
        self.current_page: int = self.emotes_db.current_page

    async def create_emotes_page(self):
        tasks: list[Task[None]] = [create_task(emote.save_to_cache()) for emote in self.emotes_db.emotes_pages()]

        await gather(*tasks)

        buttons: list[list[sg.Button]] = [[sg.Button(image_source=os.getenv(strs.Handler.Internal.IMG_CACHE_NAME))]]
        self.layout = [sg.Column(buttons)]

        self.finalize()

    def clear_cache(self):
        [os.remove(f'./img_cache/{emote.get_id()}{emote.get_extension().replace('?', '')}') for emote in self.emotes_db.emotes_pages()]

async def main():
    window = Window(title='Test')
    await window.create_emotes_page()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break


if __name__ == '__main__':
    run(main())