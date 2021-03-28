from dataclasses import dataclass
from typing import Optional


@dataclass
class TelegramResponseEntity:
    chat_id: int
    user_id: int
    text: str
    parse_mode: Optional[str] = None
    disable_web_page_preview: bool = True

    def __hash__(self):
        return hash(str(self))
