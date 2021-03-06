from millet import Skill

import constants

from domain.entities import RequestEntity
from domain.interfaces import IUserDAO
from domain.agent.skills.common import (
    make_html_response,
    make_text_response,
)


class StartSkill(Skill):
    """
    Регистрация нового участника арены.
    """

    def __init__(self, user_dao: IUserDAO):
        super().__init__()
        self.user_dao = user_dao

    def start(self, initial_message: RequestEntity):
        response_entity = make_text_response(
            request_entity=initial_message,
            message=(
                'Короче, беженец, я тебя спас и в благородство играть не буду. '
                'Ты на арене горячее мясо и должен принести мне деньжат, '
                'рыпаться не советую, постараешься - живым уйдешь, еще и хабар нехилый прихватишь.'
            ),
        )
        self.say(response_entity)

        response_entity = make_text_response(
            request_entity=initial_message,
            message=(
                'Это твоя новая жизнь и имя тоже будет новое. Как звать тебя будем новичок?'
            ),
        )
        username_telegram_request: RequestEntity = self.ask(response_entity)
        while True:
            username = username_telegram_request.message
            user_entity = self.user_dao.try_to_get_user_entity_by_username(username=username)
            if user_entity:
                response_entity = make_html_response(
                    request_entity=initial_message,
                    message=(
                        f'Придумай что-нибудь пооригинальней, чем <b>{username}</b>. У нас таки пол арены ходит.'
                    ),
                )
                username_telegram_request: RequestEntity = self.ask(response_entity)
            else:
                user_entity = self.user_dao.create_user(
                    user_id=response_entity.user_id,
                    chat_id=response_entity.chat_id,
                    username=username,
                )
                response_entity = make_html_response(
                    request_entity=initial_message,
                    message=(
                        f'Хорошо, <b>{user_entity.username}</b>. Посмотрим на что ты способен, <i>салага</i>.\n'
                        f'Сейчас твой рейтинг <b>{user_entity.rate}</b>\n'
                        f'Если что-то понадобиться, обращайся: <b>/{constants.TELEGRAM_COMMAND_HELP}</b>'
                    ),
                )
                self.finish(response_entity)
