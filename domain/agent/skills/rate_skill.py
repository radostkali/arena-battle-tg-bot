from millet import Skill

from domain.entities import TelegramRequestEntity
from domain.interfaces import IUserDAO
from domain.agent.skills.common import (
    make_html_response,
)


class RateSkill(Skill):
    """
    Отображает ранг и рейтинг пользователя, а также количество побед и поражений на арене.
    """

    def __init__(self, user_dao: IUserDAO):
        super().__init__()
        self.user_dao = user_dao

    def start(self, initial_message: TelegramRequestEntity):
        user_entity = self.user_dao.try_to_get_user_entity_by_user_id(user_id=initial_message.user_id)
        telegram_response_entity = make_html_response(
            telegram_request_entity=initial_message,
            message=(
                f'Приветствую, <b>{user_entity.username}</b>. Ты - <i>{user_entity.rank.value}</i>.\n'
                f'У тебя <b>{user_entity.wins}</b> побед и <b>{user_entity.looses}</b> поражений.\n'
            ),
        )
        self.finish(telegram_response_entity)
