from modules.const import BREAKING_BALL_AVG, CONTROL_AVG, SPEED_AVG


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


def pitcher_ability_correction(speed_p: int, control: int, breaking_ball: int):
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
    meet_corr += (speed_p - SPEED_AVG) * (-9) / 8
    power_corr += (speed_p - SPEED_AVG) * (-6) / 8

    # コントロールによる補正 (ミートへの影響は0, パワーのみ影響)
    meet_corr += (control - CONTROL_AVG) * (-0) / 30
    power_corr += (control - CONTROL_AVG) * (-6) / 30

    # 変化球による補正
    meet_corr += (breaking_ball - BREAKING_BALL_AVG) * (-6) / 4
    power_corr += (breaking_ball - BREAKING_BALL_AVG) * (-3) / 4

    return meet_corr, power_corr
