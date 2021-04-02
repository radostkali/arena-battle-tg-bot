from millet import Skill

from domain.entities import RequestEntity, UserEntity
from domain.interfaces import IUserDAO
from domain.agent.skills.common import (
    make_html_response,
)


class TableSkill(Skill):
    """
    Показывает список пользователей с их рейтингами, рангами и т.д.
    Короче, турнирная таблица.
    """

    def __init__(self, user_dao: IUserDAO):
        super().__init__()
        self.user_dao = user_dao

    def _get_users_info_list_message(self, users_entities: list[UserEntity]) -> str:
        user_info_line_list = []
        for i, user_entity in enumerate(users_entities, start=1):
            user_info_line_list.append(
                f'{i}. <b>{user_entity.username}</b> - {user_entity.rank.value} '
                f'(побед: {user_entity.wins}, поражений: {user_entity.looses})'
            )
        return '\n'.join(user_info_line_list)

    def start(self, initial_message: RequestEntity):
        users_entities = self.user_dao.fetch_users_usernames()
        users_info = self._get_users_info_list_message(users_entities=users_entities)
        response_entity = make_html_response(
            request_entity=initial_message,
            message=(
                f'Вот последние списки мясников с арены:\n'
                f'{users_info}'
            ),
        )
        self.finish(response_entity)
