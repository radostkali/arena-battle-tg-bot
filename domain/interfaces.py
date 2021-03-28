from abc import ABC, abstractmethod
from typing import Optional

from domain.entities import RankChoices, UserEntity


class IUserDAO(ABC):

    @abstractmethod
    def try_to_get_user_entity_by_user_id(self, user_id: int) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def try_to_get_user_entity_by_username(self, username: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def create_user(
            self,
            user_id: int,
            chat_id: int,
            username: str,
    ) -> UserEntity:
            pass

    @abstractmethod
    def update_rate_rank(
            self,
            user_id: int,
            rate: int,
            rank: RankChoices,
            wins: int,
            looses: int,
    ):
        pass

    @abstractmethod
    def fetch_users_usernames(self) -> list[UserEntity]:
        pass
