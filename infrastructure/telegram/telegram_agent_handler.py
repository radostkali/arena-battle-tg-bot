from millet import Agent
from telegram.update import Update
from telegram.ext import CallbackContext

from domain.entities import RequestEntity, ResponseEntity


class TelegramAgentHandler:

    def __init__(self, agent: Agent):
        self.agent = agent

    def _parse_telegram_request(self, update: Update) -> RequestEntity:
        try:
            user_id_reply_to = update.message.reply_to_message.from_user.id
        except AttributeError:
            user_id_reply_to = None

        request_entity = RequestEntity(
            chat_id=update.effective_chat.id,
            user_id=update.effective_user.id,
            message=update.message.text,
            user_id_reply_to=user_id_reply_to,
        )
        return request_entity

    def _send_telegram_response(self, update: Update, response_entity: ResponseEntity):
        update.message.reply_text(
            text=response_entity.text,
            parse_mode=response_entity.parse_mode,
            disable_web_page_preview=response_entity.disable_web_page_preview,
        )

    def callback(self, update: Update, context: CallbackContext):
        request_entity = self._parse_telegram_request(update)
        response_entities: list[ResponseEntity] = self.agent.query(
            message=request_entity,
            user_id=str(request_entity.user_id),
        )
        for response_entity in response_entities:
            self._send_telegram_response(
                update=update,
                response_entity=response_entity,
            )
