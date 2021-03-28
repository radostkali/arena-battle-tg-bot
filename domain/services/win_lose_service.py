from domain.interfaces import IUserDAO
from domain.entities import RankChoices
from domain.entities.rank_choices import RATE_RANK_MAP


class WinLoseService:

    def __init__(self, user_dao: IUserDAO):
        self.user_dao = user_dao

    def _calc_rank_by_rate(self, target_rate: int) -> RankChoices:
        target_rank = RankChoices[RATE_RANK_MAP[0][1]]
        for rate, rank in RATE_RANK_MAP:
            if target_rate >= rate:
                target_rank = RankChoices[rank]

        return target_rank

    def win(self, username: str):
        user_entity = self.user_dao.try_to_get_user_entity_by_username(username=username)
        rate = min(user_entity.rate + 2, RATE_RANK_MAP[-1][0] + 1)
        rank = self._calc_rank_by_rate(target_rate=rate)
        self.user_dao.update_rate_rank(
            user_id=user_entity.id,
            rate=rate,
            rank=rank,
            wins=user_entity.wins + 1,
            looses=user_entity.looses,
        )

    def loose(self, username: str):
        user_entity = self.user_dao.try_to_get_user_entity_by_username(username=username)
        rate = max(user_entity.rate - 1, RATE_RANK_MAP[0][0] + 1)
        rank = self._calc_rank_by_rate(target_rate=rate)
        self.user_dao.update_rate_rank(
            user_id=user_entity.id,
            rate=rate,
            rank=rank,
            wins=user_entity.wins,
            looses=user_entity.looses + 1,
        )
