from millet import Skill

from domain.entities import RequestEntity
from domain.interfaces import IUserDAO
from domain.agent.skills.common import (
    make_html_response,
)


class OtherUserRateSkill(Skill):
    """
    Отображает ранг и рейтинг указанного пользователя, а также количество побед и поражений на арене.
    """

    def __init__(self, user_dao: IUserDAO):
        super().__init__()
        self.user_dao = user_dao

    def start(self, initial_message: RequestEntity):
        user_entity = self.user_dao.try_to_get_user_entity_by_user_id(user_id=initial_message.user_id_reply_to)
        if not user_entity:
            response_entity = make_html_response(
                request_entity=initial_message,
                message=(
                    f'Я таких не знаю, сначала пусть придет и запишется на арену.'
                ),
            )
            self.finish(response_entity)

        response_entity = make_html_response(
            request_entity=initial_message,
            message=(
                f'<b>{user_entity.username}</b> - <i>{user_entity.rank.value}</i>.\n'
                f'Побед: <b>{user_entity.wins}</b>, поражений: <b>{user_entity.looses}</b>.\n'
            ),
        )
        self.finish(response_entity)
