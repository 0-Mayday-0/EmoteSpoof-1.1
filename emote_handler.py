import re
from custom_error import InvalidEmote
from requests import get
import strings as strs
from PIL import Image
import io

class Emote:
    def __init__(self, url: str) -> None:
        try:
            self._protocol: str = re.search(r'(https://)', url).group()
            self._subdomain: str = re.search(r'(cdn\.)', url).group()
            self._root_domain: str = re.search(r'(discordapp\.)', url).group()
            self._top_level_domain: str = re.search(r'(com/)', url).group()
            self._slug: str = re.search(r'emojis/', url).group()
            self._emote_ID: str = re.search(r'\d{19}\.', url).group()
            self._extension: str = re.search(r'((gif)|(png)|(jpg)|(jpeg)|(jfif))\?', url).group()
            self._config: str = re.search(r'(v=\d&size=\d{2}&quality=lossless)', url).group()

        except AttributeError:
            raise InvalidEmote(strs.Handler.External.INVALID_URL)


    def _get_privates(self) -> list[str]:
        return [self._protocol,
                self._subdomain,
                self._root_domain,
                self._top_level_domain,
                self._slug,
                self._emote_ID,
                self._extension,
                self._config]

    def _assemble_url(self) -> str:
        return (f'{self._protocol}{self._subdomain}{self._root_domain}{self._top_level_domain}{self._slug}'
                f'{self._emote_ID}{self._extension}{self._config}')

    def fetch_emote_img(self) -> Image:
        return Image.open(io.BytesIO(get(self._assemble_url()).content))

    def __bytes__(self) -> bytes:
        return b''.join([bytes(i.encode('UTF-8')) for i in self._get_privates()])

def main():
    test_emote: Emote = Emote("https://cdn.discordapp.com/emojis/1110989171809583156.gif?v=1&size=48&quality=lossless")

    

if __name__ == "__main__":
    main()