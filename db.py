import tinydb as tdb
import os
from dotenv import load_dotenv
import strings as strs
from emote_handler import Emote, InvalidEmote

class DbHandler:
    def __init__(self, max_emotes: int):
        load_dotenv(strs.Handler.Internal.DOTENV_NAME)
        database_path: str = os.getenv(strs.Handler.Internal.EMOTE_DB_NAME)
        self._emote_db: tdb.TinyDB = tdb.TinyDB(database_path)
        self._query_object: tdb.Query = tdb.Query()
        self.max_emotes_ppage: int = max_emotes
        self.current_page: int = 1

    def add_emote(self, url) -> str:
        try:
            emote: Emote = Emote(url)
            emote_id: str = emote.get_id().replace('.', '')
            sanitized_url: str = emote.get_url()

            if len(self._emote_db.search(self._query_object[strs.Handler.Internal.EMOTE_ID] == emote_id)) > 0:
                return strs.Handler.External.ALREADY_EXISTS.format(id=emote_id)

            else:
                self._emote_db.insert({strs.Handler.Internal.EMOTE_ID: emote_id,
                                       strs.Handler.Internal.EMOTE_URL: sanitized_url})
                return strs.Handler.External.ADDED_SUCCESS.format(id=emote_id)

        except InvalidEmote as e:
            return str(e)

    def remove_emote(self, emote_id: str) -> str:
        self._emote_db.remove(self._query_object[strs.Handler.Internal.EMOTE_ID] == emote_id)
        return strs.Handler.External.REMOVED_SUCCESS.format(id=emote_id)

    def emotes_pages(self) -> list[Emote]:
        return [Emote(emote[strs.Handler.Internal.EMOTE_URL]) for emote in self._emote_db.all()[self.max_emotes_ppage-(self.max_emotes_ppage*self.current_page):self.max_emotes_ppage*self.current_page]]

    def next_page(self) -> None:
        self.current_page += 1

    def previous_page(self) -> None:
        self.current_page -= 1

def main() -> None:
    db: DbHandler = DbHandler(10)

    print(db.remove_emote("1119740756505145485"))

    print(db.emotes_pages())

if __name__ == '__main__':
    main()