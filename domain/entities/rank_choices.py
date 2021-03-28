import enum

import constants


class RankChoices(enum.Enum):
    salaga = constants.RANK_SALAGA
    novicheck = constants.RANK_NOVICHOK
    mestniy = constants.RANK_MESTNIY
    byivaliy = constants.RANK_BYIVALIY
    boec = constants.RANK_BOEC
    veteran = constants.RANK_VETERAN
    monstr = constants.RANK_MONSTR
    king = constants.RANK_KING
    imperor = constants.RANK_IMPEROR
    legend = constants.RANK_LEGEND
    god = constants.RANK_GOD


RATE_RANK_MAP = (
    (0, RankChoices.salaga),
    (2, RankChoices.novicheck),
    (4, RankChoices.mestniy),
    (6, RankChoices.byivaliy),
    (8, RankChoices.boec),
    (10, RankChoices.veteran),
    (12, RankChoices.monstr),
    (14, RankChoices.king),
    (16, RankChoices.imperor),
    (18, RankChoices.legend),
    (20, RankChoices.god),
)
