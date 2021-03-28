from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import MetaData
from typing import Type


class Database:
    engine: Engine
    session: Session
    metadata: MetaData
    base: Type[declarative_base]

    def __init__(self, database_url: str, base: Type[declarative_base]):
        self.engine = create_engine(url=database_url)
        self.session = Session(bind=self.engine)
        self.base = base

    def create_tables(self) -> None:
        self.base.metadata.create_all(self.engine)

    def drop_tables(self) -> None:
        self.base.metadata.drop_all(self.engine)
