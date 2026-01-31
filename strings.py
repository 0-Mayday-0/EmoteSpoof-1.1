from dataclasses import dataclass

@dataclass(frozen=True)
class Handler:

    @dataclass(frozen=True)
    class Internal:
        DOTENV_NAME: str = 'paths.env'
        IMG_CACHE_NAME: str = 'IMAGE_CACHE'
        EMOTE_DB_NAME: str = 'EMOTE_DB'
        IMAGE_MODE: str = 'RGB'
        EMOTE_ID: str = 'emote_id'
        EMOTE_URL: str = 'emote_url'
        SUPPORTED_EXTENSIONS: str = r'((gif)|(png))\?'

    @dataclass(frozen=True)
    class External:
        INVALID_URL: str = "The emote URL is invalid."
        ADDED_SUCCESS: str = "The emote with id {id} was added successfully."
        ALREADY_EXISTS: str = "The emote with id {id} already exists."
        REMOVED_SUCCESS: str = "The emote with id {id} was removed successfully."


@dataclass(frozen=True)
class Menu:
    @dataclass(frozen=True)
    class Internal:
        NX_PAGE_EVENT: str = 'nx'
        PV_PAGE_EVENT: str = 'pv'

    @dataclass(frozen=True)
    class External:
        NEXT_PAGE: str = "Next page"
        PREVIOUS_PAGE: str = "Previous page"
        NO_MORE_PAGES: str = "No more pages"
