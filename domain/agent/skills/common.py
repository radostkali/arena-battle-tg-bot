import constants
from domain.entities import TelegramRequestEntity, TelegramResponseEntity


def get_html_commands_description() -> str:
    command_html_raw_list = []
    for command, description in constants.TELEGRAM_COMMANDS:
        command_html_raw_list.append(
            f'<b>/{command}</b> - {description}'
        )
    commands_html_list = '\n'.join(command_html_raw_list)
    return commands_html_list


def make_text_response(
        telegram_request_entity: TelegramRequestEntity,
        message: str,
) -> TelegramResponseEntity:
    return TelegramResponseEntity(
        chat_id=telegram_request_entity.chat_id,
        user_id=telegram_request_entity.user_id,
        text=message,
    )


def make_html_response(
        telegram_request_entity: TelegramRequestEntity,
        message: str,
) -> TelegramResponseEntity:
    return TelegramResponseEntity(
        chat_id=telegram_request_entity.chat_id,
        user_id=telegram_request_entity.user_id,
        text=message,
        parse_mode='HTML',
    )
