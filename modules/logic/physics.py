import random

from modules.const import BREAKING_BALL_AVG, CONTROL_AVG, SPEED_PITCHER_AVG
from modules.models import Batter, Player

# 野手用ランク補正 (ランク: (ミート補正, パワー補正))
PITCHER_CONDITION_MAP = {
    5: (4, 24, 2),
    4: (2, 12, 1),
    3: (0, 0, 0),
    2: (-2, -12, -1),
    1: (-4, -24, -2),
}

BATTER_CONDITION_MAP = {
    5: (15, 15),
    4: (10, 10),
    3: (0, 0),
    2: (-10, -10),
    1: (-15, -15),
}


def eye_logic(eye: str) -> int:
    """
        選球眼ランクに基づいた四球発生率の補正値を返す

    Args:
        - eye : 選球眼のランク

    Returns:
        - int : 選球眼の補正値
    """
    # ランクと補正値の対応表
    if eye == "A":
        walk_per_corr = 80
    elif eye == "B":
        walk_per_corr = 70
    elif eye == "C":
        walk_per_corr = 60
    elif eye == "D":
        walk_per_corr = 50
    elif eye == "E":
        walk_per_corr = 40
    elif eye == "F":
        walk_per_corr = 30
    elif eye == "G":
        walk_per_corr = 20

    return walk_per_corr


def pitcher_ability_correction(
    speed_p: int, control: int, breaking_ball: int
) -> tuple[int, int]:
    """
        投手の能力（球速・制御・変化球）から、野手のミート・パワーへの補正値を算出する

    Args:
        - speed_p : 球速
        - control : コントロール
        - breaking_ball : 変化量

    Returns:
        - tuple[int, int]: 以下の順に格納された補正値のタプル
            - meet_corr : ミート補正
            - power_corr : パワー補正
    """

    # 野手側補正値初期値
    meet_corr = 0
    power_corr = 0

    # 球速による補正 (1kmの差でミート約-1.125, パワー約-0.75)
    meet_corr += (speed_p - SPEED_PITCHER_AVG) * (-9) / 8
    power_corr += (speed_p - SPEED_PITCHER_AVG) * (-6) / 8

    # コントロールによる補正 (ミートへの影響は0, パワーのみ影響)
    meet_corr += (control - CONTROL_AVG) * (-0) / 30
    power_corr += (control - CONTROL_AVG) * (-6) / 30

    # 変化球による補正
    meet_corr += (breaking_ball - BREAKING_BALL_AVG) * (-6) / 4
    power_corr += (breaking_ball - BREAKING_BALL_AVG) * (-3) / 4

    return meet_corr, power_corr


def pitcher_condition_correction(condition: int) -> tuple[int, int, int]:
    """
        投手の調子から投手能力への補正値を決める

    Args:
        - condition : 調子（1~5）

    Returns:
        - tuple[int, int, int]: 以下の順に格納された補正値のタプル
            - speed_corr : 球速補正
            - control_corr : コントロール補正
            - breaking_ball_corr : 変化量補正
    """
    speed_corr, control_corr, breaking_ball_corr = PITCHER_CONDITION_MAP.get(
        condition, (0, 0, 0)
    )

    return speed_corr, control_corr, breaking_ball_corr


def batter_condition_correction(condition: int) -> tuple[int, int]:
    """
        野手の調子から野手能力への補正値を決める

    Args:
        - condition : 調子（1~5）

    Returns:
        - tuple[int, int]: 以下の順に格納された補正値のタプル
            - meet_corr : ミート補正
            - power_corr : パワー補正
    """
    meet_corr, power_corr = BATTER_CONDITION_MAP.get(condition, (0, 0))

    return meet_corr, power_corr


def update_player_condition(players: list[Player]) -> None:
    """
        選手の調子を変動させる

    Args:
        - players : チームの全選手

    Returns:
        -
    """
    for player in players:
        r = random.random()

        new_condition = player.condition

        if player.condition == 1:
            if r < 0.25:
                new_condition = 2

        elif player.condition == 2:
            if r < 0.10:
                new_condition = 1
            elif r < 0.35:
                new_condition = 3

        elif player.condition == 3:
            if r < 0.01:
                new_condition = 2
            elif r < 0.02:
                new_condition = 4

        elif player.condition == 4:
            if r < 0.25:
                new_condition = 3
            elif r < 0.35:
                new_condition = 5

        elif player.condition == 5:
            if r < 0.25:
                new_condition = 4

        # 値を更新
        player.condition = new_condition
