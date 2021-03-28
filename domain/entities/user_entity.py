from dataclasses import dataclass
from typing import Optional


@dataclass
class UserEntity:
    id: int
    user_id: int
    chat_id: int
    username: Optional[str]
    rank: str
    rate: int
    wins: int
    looses: int
    admin: bool
