from millet import Skill

from domain.entities import TelegramRequestEntity
from domain.agent.skills.common import (
    get_html_commands_description,
    make_html_response,
)


class HelpSkill(Skill):
    """
    Выводит список доступных команд Агента.
    """

    def start(self, initial_message: TelegramRequestEntity):
        telegram_response_entity = make_html_response(
            telegram_request_entity=initial_message,
            message=(
                f'Вот список команд. Ознакомься и говори, чего хочешь.\n'
                f'{get_html_commands_description()}'
            ),
        )
        self.finish(telegram_response_entity)
