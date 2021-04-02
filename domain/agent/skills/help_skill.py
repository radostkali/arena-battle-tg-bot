from millet import Skill

from domain.entities import RequestEntity
from domain.agent.skills.common import (
    get_html_commands_description,
    make_html_response,
)


class HelpSkill(Skill):
    """
    Выводит список доступных команд Агента.
    """

    def start(self, initial_message: RequestEntity):
        response_entity = make_html_response(
            request_entity=initial_message,
            message=(
                f'Вот список команд. Ознакомься и говори, чего хочешь.\n'
                f'{get_html_commands_description()}'
            ),
        )
        self.finish(response_entity)
