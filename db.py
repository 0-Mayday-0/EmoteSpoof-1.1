import tinydb as tdb
import os
from dotenv import load_dotenv
import strings as strs
from emote_handler import Emote, InvalidEmote

class DbHandler:
    def __init__(self):
        load_dotenv(strs.Handler.Internal.DOTENV_NAME)
        database_path: str = os.getenv(strs.Handler.Internal.EMOTE_DB_NAME)
        self._emote_db: tdb.TinyDB = tdb.TinyDB(database_path)
        self._query_object: tdb.Query = tdb.Query()

    def add_emote(self, url) -> str:
        try:
            emote: Emote = Emote(url)
            emote_id: str = emote.get_id()
            sanitized_url: str = emote.get_url()

            if len(self._emote_db.search(self._query_object[emote_id] == sanitized_url)) > 0:
                return strs.Handler.External.ALREADY_EXISTS.format(id=emote_id.replace('.', ''))

            else:
                self._emote_db.insert({emote_id: sanitized_url})
                return strs.Handler.External.ADDED_SUCCESS.format(id=emote_id.replace('.', ''))

        except InvalidEmote as e:
            return str(e)


def main() -> None:
    db: DbHandler = DbHandler()

    print(db.add_emote("https://cdn.discordapp.com/emojis/864309722199228436.png?v=1&size=48&quality=lossless"))

if __name__ == '__main__':
    main()