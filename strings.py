from dataclasses import dataclass

@dataclass(frozen=True)
class Handler:

    @dataclass(frozen=True)
    class Internal:
        IMAGE_MODE: str = 'RGB'

    @dataclass(frozen=True)
    class External:
        INVALID_URL: str = "The emote URL is invalid."