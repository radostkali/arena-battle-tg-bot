from millet import Agent
from telegram.update import Update
from telegram.ext import CallbackContext

from domain.entities import TelegramRequestEntity, TelegramResponseEntity


class TelegramAgentHandler:

    def __init__(self, agent: Agent):
        self.agent = agent

    def _parse_telegram_request(self, update: Update) -> TelegramRequestEntity:
        try:
            user_id_reply_to = update.message.reply_to_message.from_user.id
        except AttributeError:
            user_id_reply_to = None

        telegram_request_entity = TelegramRequestEntity(
            chat_id=update.effective_chat.id,
            user_id=update.effective_user.id,
            message=update.message.text,
            user_id_reply_to=user_id_reply_to,
        )
        return telegram_request_entity

    def _send_telegram_response(self, update: Update, telegram_response_entity: TelegramResponseEntity):
        update.message.reply_text(
            text=telegram_response_entity.text,
            parse_mode=telegram_response_entity.parse_mode,
            disable_web_page_preview=telegram_response_entity.disable_web_page_preview,
        )

    def callback(self, update: Update, context: CallbackContext):
        telegram_request_entity = self._parse_telegram_request(update)
        telegram_response_entities: list[TelegramResponseEntity] = self.agent.query(
            message=telegram_request_entity,
            user_id=str(telegram_request_entity.user_id),
        )
        for telegram_response_entity in telegram_response_entities:
            self._send_telegram_response(
                update=update,
                telegram_response_entity=telegram_response_entity,
            )
