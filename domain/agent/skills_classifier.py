from millet import Skill
from millet.agent import BaseSkillClassifier

import constants

from domain.entities import TelegramRequestEntity
from domain.interfaces import IUserDAO
from domain.agent.skills import (
    HelpSkill,
    OtherUserRateSkill,
    RateSkill,
    StartSkill,
    TableSkill,
    WinLoseSkill,
)
from domain.services import WinLoseService


class SkillClassifier(BaseSkillClassifier):

    def __init__(
            self,
            win_lose_service: WinLoseService,
            user_dao: IUserDAO,
    ):
        self.win_lose_service = win_lose_service
        self.user_dao = user_dao

    def _has_admin_permissions(self, message: TelegramRequestEntity) -> bool:
        user_entity = self.user_dao.try_to_get_user_entity_by_user_id(user_id=message.user_id)
        return user_entity.admin

    def classify(self, message: TelegramRequestEntity) -> list[Skill]:
        skills = []

        if message.message == f'/{constants.TELEGRAM_COMMAND_START}':
            user_entity = self.user_dao.try_to_get_user_entity_by_user_id(user_id=message.user_id)
            if user_entity:
                skill = HelpSkill()
            else:
                skill = StartSkill(user_dao=self.user_dao)
            skills.append(skill)

        elif (
                message.message == f'/{constants.TELEGRAM_COMMAND_RATE}' or
                message.message == f'/{constants.TELEGRAM_COMMAND_RATE}@sidorovich_battle_bot'
        ):
            if message.user_id_reply_to:
                skill = OtherUserRateSkill(user_dao=self.user_dao)
            else:
                skill = RateSkill(user_dao=self.user_dao)
            skills.append(skill)

        elif (
                message.message == f'/{constants.TELEGRAM_COMMAND_TABLE}' or
                message.message == f'/{constants.TELEGRAM_COMMAND_TABLE}@sidorovich_battle_bot'
        ):
            skill = TableSkill(user_dao=self.user_dao)
            skills.append(skill)

        elif (
                message.message == f'/{constants.TELEGRAM_COMMAND_HELP}' or
                message.message == f'/{constants.TELEGRAM_COMMAND_HELP}@sidorovich_battle_bot'
        ):
            skill = HelpSkill()
            skills.append(skill)

        elif message.message == f'/{constants.TELEGRAM_COMMAND_WINLOSE}':
            if self._has_admin_permissions(message=message):
                skill = WinLoseSkill(
                    win_lose_service=self.win_lose_service,
                    user_dao=self.user_dao,
                )
            else:
                skill = HelpSkill()
            skills.append(skill)

        return skills
