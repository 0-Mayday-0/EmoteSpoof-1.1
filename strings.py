from dataclasses import dataclass

@dataclass(frozen=True)
class Handler:

    @dataclass(frozen=True)
    class Internal:
        DOTENV_NAME: str = 'paths.env'
        IMG_CACHE_NAME: str = 'IMAGE_CACHE'
        IMAGE_MODE: str = 'RGB'

    @dataclass(frozen=True)
    class External:
        INVALID_URL: str = "The emote URL is invalid."