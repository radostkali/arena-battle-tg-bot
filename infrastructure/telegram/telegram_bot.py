from millet import Agent
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

import constants
from infrastructure.telegram.telegram_agent_handler import TelegramAgentHandler


class TelegramBot:
    updater: Updater
    agent: Agent

    def __init__(self, telegram_bot_token: str, agent: Agent) -> None:
        self.updater = Updater(token=telegram_bot_token)
        self.agent = agent
        self._add_handlers()

    def _add_handlers(self) -> None:
        message_handler = MessageHandler(
            filters=Filters.text,
            callback=TelegramAgentHandler(agent=self.agent).callback,
        )
        self.updater.dispatcher.add_handler(message_handler)
        for command, _ in constants.TELEGRAM_COMMANDS:
            command_handler = CommandHandler(
                command=command,
                callback=TelegramAgentHandler(agent=self.agent).callback,
            )
            self.updater.dispatcher.add_handler(command_handler)

    def start(self):
        self.updater.start_polling()
