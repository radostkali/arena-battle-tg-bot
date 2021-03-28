from typing import Optional

from sqlalchemy import select, update

from infrastructure.models import User
from infrastructure.database import Database

from domain.entities import UserEntity
from domain.interfaces import IUserDAO


class UserDAO(IUserDAO):

    def __init__(self, database: Database):
        self.database = database

    def _user_orm_to_entity_converter(self, user_orm: User) -> UserEntity:
        return UserEntity(
            id=user_orm.id,
            user_id=user_orm.user_id,
            chat_id=user_orm.chat_id,
            username=user_orm.username,
            rank=user_orm.rank,
            rate=user_orm.rate,
            wins=user_orm.wins,
            looses=user_orm.looses,
            admin=user_orm.admin,
        )

    def try_to_get_user_entity_by_user_id(self, user_id: int) -> Optional[UserEntity]:
        query = select(User).filter_by(user_id=user_id)
        user = self.database.session.execute(query).first()
        return user and self._user_orm_to_entity_converter(user[0])

    def try_to_get_user_entity_by_username(self, username: str) -> Optional[UserEntity]:
        query = select(User).filter_by(username=username)
        user = self.database.session.execute(query).first()
        return user and self._user_orm_to_entity_converter(user[0])

    def create_user(
            self,
            user_id: int,
            chat_id: int,
            username: str,
    ) -> UserEntity:
        user = User(
            user_id=user_id,
            chat_id=chat_id,
            username=username,
        )
        self.database.session.add(user)
        self.database.session.commit()
        return self._user_orm_to_entity_converter(user)

    def update_rate_rank(
            self,
            user_id: int,
            rate: int,
            rank: str,
            wins: int,
            looses: int,
    ):
        query = update(User).where(
            User.id == user_id,
        ).values(
            rate=rate,
            rank=rank,
            wins=wins,
            looses=looses,
        )
        self.database.session.execute(query)
        self.database.session.commit()

    def fetch_users_usernames(self) -> list[UserEntity]:
        query = select(User).order_by(User.rate.desc())
        users = self.database.session.execute(query)
        return list(map(lambda x: self._user_orm_to_entity_converter(x[0]), users))
