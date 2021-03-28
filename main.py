#!/usr/bin/env python3
import logging

from millet import Agent

import settings

from infrastructure.daos import UserDAO
from infrastructure.database import Database
from infrastructure.models.base import Base
from infrastructure.telegram.telegram_bot import TelegramBot

from domain.agent.skills_classifier import SkillClassifier
from domain.services import WinLoseService


logging.basicConfig(
    format='[%(name)s %(levelname)s] %(asctime)s: %(message)s',
    level=logging.INFO,
)

database = Database(
    database_url=settings.DATABASE_URL,
    base=Base,
)
database.create_tables()

user_dao = UserDAO(database)
win_lose_service = WinLoseService(user_dao=user_dao)
skill_classifier = SkillClassifier(
    win_lose_service=win_lose_service,
    user_dao=user_dao,
)
agent = Agent(skill_classifier=skill_classifier)

telegram_bot = TelegramBot(
    telegram_bot_token=settings.TELEGRAM_BOT_TOKEN,
    agent=agent,
)

if __name__ == "__main__":
    telegram_bot.start()
