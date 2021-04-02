from millet import Skill

import constants

from domain.entities import RequestEntity, UserEntity
from domain.interfaces import IUserDAO
from domain.services import WinLoseService
from domain.agent.skills.common import (
    make_html_response,
)


class WinLoseSkill(Skill):
    """
    [Команда для админов] Начисляет указанному юзеру победу или поражение.
    """

    def __init__(self, win_lose_service: WinLoseService, user_dao: IUserDAO):
        super().__init__()
        self.win_lose_service = win_lose_service
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
                f'Введи имя бойца, которому хочешь начислить победу или поражение:\n'
                f'{users_info}'
            ),
        )
        username_telegram_request: RequestEntity = self.ask(response_entity)

        username = username_telegram_request.message
        user_entity = self.user_dao.try_to_get_user_entity_by_username(username=username)
        if not user_entity:
            response_entity = make_html_response(
                request_entity=initial_message,
                message=(
                    f'Браток, тебя что контроллер оприходовал? Бойца с именем <i>{username}</i> в наших краях нету.\n'
                    f'Возвращайся, когда вспомнишь как его зовут: <b>/{constants.TELEGRAM_COMMAND_WINLOSE}</b>'
                ),
            )
            self.finish(response_entity)

        response_entity = make_html_response(
            request_entity=initial_message,
            message=(
                f'Напиши <b>1</b>, если {username} одержал победу на арене.\n'
                f'Напиши <b>2</b>, если он пал в честном бою.'
            ),
        )
        win_or_lose: RequestEntity = self.ask(response_entity)
        if win_or_lose.message not in ('1', '2'):
            response_entity = make_html_response(
                request_entity=initial_message,
                message=(
                    f'Тебя видно кровосос подсосал.\n'
                    f'Отдохни и приходи еще: <b>/{constants.TELEGRAM_COMMAND_WINLOSE}</b>'
                ),
            )
            self.finish(response_entity)

        if win_or_lose.message == '1':
            self.win_lose_service.win(username=username)
        else:
            self.win_lose_service.loose(username=username)

        users_entities = self.user_dao.fetch_users_usernames()
        users_info = self._get_users_info_list_message(users_entities=users_entities)
        response_entity = make_html_response(
            request_entity=initial_message,
            message=(
                f'Учтено. Актуальный рейтинг сталкеров:\n'
                f'{users_info}'
            ),
        )
        self.finish(response_entity)
