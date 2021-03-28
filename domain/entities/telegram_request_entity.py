from dataclasses import dataclass
from typing import Optional


@dataclass
class TelegramRequestEntity:
    chat_id: int
    user_id: int
    message: str
    user_id_reply_to: Optional[int] = None
