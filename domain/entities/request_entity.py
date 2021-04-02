from dataclasses import dataclass
from typing import Optional


@dataclass
class RequestEntity:
    chat_id: int
    user_id: int
    message: str
    user_id_reply_to: Optional[int] = None
