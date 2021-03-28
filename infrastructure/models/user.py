from sqlalchemy import Boolean, Column, Enum, Integer, String

from infrastructure.models.base import Base

from domain.entities import RankChoices


DB_TABLE_NAME_USER = 'user'


class User(Base):
    __tablename__ = DB_TABLE_NAME_USER

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    chat_id = Column(Integer)
    username = Column(String)
    rate = Column(Integer, default=1)
    rank = Column(Enum(RankChoices), default=RankChoices.salaga)
    wins = Column(Integer, default=0)
    looses = Column(Integer, default=0)
    admin = Column(Boolean, default=False)

    def __repr__(self):
        return '<User(id={}, username={})>'.format(
            self.id,
            self.username,
        )
