import random
from modules.const import (
    BREAKING_BALL_AVG,
    MEET_AVG,
    POWER_AVG,
    SPEED_BATTER_AVG,
    SPEED_PITCHER_AVG,
    TRAJECTORY_AVG,
)
from modules.logic import physics

TRAJECTORY_MAP = {
    1: (650, 50, 125, 175),
    2: (550, 100, 125, 225),
    3: (450, 150, 125, 275),
    4: (350, 100, 225, 325),
}

BATTING_RESULT_MAP = {
    "PULL": {
        "GB": {"1B": 180, "2B": 20, "3B": 0, "HR": 0},
        "LD": {"1B": 385, "2B": 165, "3B": 0, "HR": 30},
        "IFFB": {"1B": 10, "2B": 0, "3B": 0, "HR": 0},  # 内野フライ
        "OFFB": {"1B": 185, "2B": 65, "3B": 0, "HR": 30},  # 外野フライ
    },
    "CENT": {
        "GB": {"1B": 140, "2B": 10, "3B": 0, "HR": 0},
        "LD": {"1B": 355, "2B": 155, "3B": 0, "HR": 20},
        "IFFB": {"1B": 10, "2B": 0, "3B": 0, "HR": 0},  # 内野フライ
        "OFFB": {"1B": 165, "2B": 45, "3B": 0, "HR": 20},  # 外野フライ
    },
    "OPPO": {
        "GB": {"1B": 100, "2B": 10, "3B": 0, "HR": 0},
        "LD": {"1B": 325, "2B": 145, "3B": 0, "HR": 10},
        "IFFB": {"1B": 10, "2B": 0, "3B": 0, "HR": 0},  # 内野フライ
        "OFFB": {"1B": 145, "2B": 25, "3B": 0, "HR": 10},  # 外野フライ
    },
}


def strikeout_logic(speed_p: int, breaking_ball: int, meet: int) -> str:
    """
        投手と打者の能力に基づき、三振(SO)か凡退(OUT)かを判定する

    Args:
        - speed_p : 球速
        - breaking_ball : 変化量
        - meet : ミート

    Returns:
        - str : 打席の結果
    """

    # 三振率の計算
    swing_out_chance = (
        25
        + (speed_p - SPEED_PITCHER_AVG) * 0.25
        + (breaking_ball - BREAKING_BALL_AVG)
        + (meet - MEET_AVG) * (-0.5)
    )

    if random.randrange(100) < swing_out_chance:
        return "SO"
    else:
        return "OUT"


def result_logic(
    trajectory: int,
    meet: int,
    power: int,
    speed_b: int,
    eye: str,
    speed_p: int,
    control: int,
    breaking_ball: int,
) -> str:
    """
        打撃結果（単打、本塁打、四球など）を確率に基づき判定する

    Args:
        - trajectory : 弾道
        - meet : ミート
        - power : パワー
        - speed_b : 走力
        - eye : 選球眼
        - speed_p : 球速
        - control : コントロール
        - breaking_ball : 変化量

    Returns:
        - str : 打席の結果
    """

    # 三振、四球、死球のロジック（打球発生なし）
    # 三振
    swing_out_per = (
        125
        + (speed_p - SPEED_PITCHER_AVG)
        + (breaking_ball - BREAKING_BALL_AVG) * 3
        + (meet - MEET_AVG) * (-5)
    )
    # 四球
    walk_per = (
        -15
        + (trajectory * 30) // 4
        + (meet * 0 + power * 80 + speed_b * -10) // 50
        - random.randrange(24)
        + random.randrange(32)
    )
    # 選球眼補正
    walk_per_corr = physics.eye_logic(eye)
    walk_per += (walk_per_corr - control) * 1.5
    # 死球
    hpb_per = 10

    # 判定実行
    num = random.randrange(1000)
    result = ""
    soP = swing_out_per
    wP = soP + walk_per
    hpbP = wP + hpb_per

    if num <= soP:
        result = "SO"
    elif num <= wP:
        result = "BB"
    elif num <= hpbP:
        result = "HBP"

    # 三振、四球、死球の場合、処理終了
    if result:
        return result

    # 三振、四球、死球以外のロジック（打球発生あり）
    # 打球角度
    ground_ball_per, line_drive_per, infield_fly_ball_per, outfield_fly_ball_per = (
        TRAJECTORY_MAP.get(trajectory)
    )
    # 判定実行
    num = random.randrange(1000)
    gbP = ground_ball_per
    ldP = gbP + line_drive_per
    iffbP = ldP + infield_fly_ball_per
    offbP = iffbP + outfield_fly_ball_per
    if num <= gbP:
        trajectory_result = "GB"
    elif num <= ldP:
        trajectory_result = "LD"
    elif num <= iffbP:
        trajectory_result = "IFFB"
    elif num <= offbP:
        trajectory_result = "OFFB"

    # 打球方向
    batting_power = meet * 0.5 + power
    pull_per = ((1 / 450) * batting_power + (7 / 30)) * 1000
    center_per = (-(1 / 900) * batting_power + (13 / 30)) * 1000
    opposite_per = (-(1 / 900) * batting_power + (1 / 3)) * 1000

    # 判定実行
    num = random.randrange(1000)
    pP = pull_per
    cP = pP + center_per
    if num <= pP:
        direction_result = "PULL"
    elif num <= cP:
        direction_result = "CENT"
    else:
        direction_result = "OPPO"

    # 辞書を一度取得
    probs = BATTING_RESULT_MAP[direction_result][trajectory_result]

    # 各キーの値を個別に代入
    single_per = probs["1B"] / 0.72  # 三振、四球、死球の確率（28％）を考慮
    double_per = probs["2B"] / 0.72
    triple_per = probs["3B"] / 0.72
    homeRun_per = probs["HR"] / 0.72

    # 確率の計算
    sP = single_per
    dP = double_per + sP
    tP = triple_per + dP
    hrP = homeRun_per + tP

    # 判定実行
    num = random.randrange(1000)
    result = ""

    if num <= sP:
        result = "1B"
    elif num <= dP:
        result = "2B"
    elif num <= tP:
        result = "3B"
    elif num <= hrP:
        result = "HR"
    else:
        result = "OUT"

    # 成績補正
    if result == "OUT":
        single_change_per = (meet - MEET_AVG) * 2 + (speed_b - SPEED_BATTER_AVG)
        double_change_per = (power - POWER_AVG) * 0.25
        homeRun_change_per = (power - POWER_AVG) * 2 + (
            trajectory - TRAJECTORY_AVG
        ) * 10

        # マイナス値を0に補正
        single_change_per = max(0, single_change_per)
        double_change_per = max(0, double_change_per)
        homeRun_change_per = max(0, homeRun_change_per)

        num = random.randrange(1000)
        scP = single_change_per
        dcP = scP + double_change_per
        hrP = dcP + homeRun_change_per

        if num <= scP:
            result = "1B"
        elif num <= dcP:
            result = "2B"
        elif num <= hrP:
            result = "HR"

    elif result == "1B":
        double_change_per = (power - POWER_AVG) * 0.25 + (
            speed_b - SPEED_BATTER_AVG
        ) * 2
        homeRun_change_per = (power - POWER_AVG) * 3

        # マイナス値を0に補正
        double_change_per = max(0, double_change_per)
        homeRun_change_per = max(0, homeRun_change_per)

        num = random.randrange(1000)
        dcP = double_change_per
        hrP = dcP + homeRun_change_per

        if num <= dcP:
            result = "2B"
        elif num <= hrP:
            result = "HR"

    elif result == "2B":
        triple_change_per = (speed_b - SPEED_BATTER_AVG) * 8
        homeRun_change_per = (power - POWER_AVG) * 4 + (
            trajectory - TRAJECTORY_AVG
        ) * 15

        # マイナス値を0に補正
        triple_change_per = max(0, triple_change_per)
        homeRun_change_per = max(0, homeRun_change_per)

        num = random.randrange(1000)
        tcP = triple_change_per
        hrP = tcP + homeRun_change_per
        if num <= tcP:
            result = "3B"
        elif num <= hrP:
            result = "HR"

    return result


def result_logic_old(
    trajectory: int,
    meet: int,
    power: int,
    speed_b: int,
    eye: str,
    speed_p: int,
    control: int,
    breaking_ball: int,
) -> str:
    """
        打撃結果（単打、本塁打、四球など）を確率に基づき判定する

    Args:
        - trajectory : 弾道
        - meet : ミート
        - power : パワー
        - speed_b : 走力
        - eye : 選球眼
        - speed_p : 球速
        - control : コントロール
        - breaking_ball : 変化量

    Returns:
        - str : 打席の結果
    """
    # 各結果の基本値計算
    single_per = (
        120
        + (trajectory * -30) // 4
        + (meet * 140 + power * -60 + speed_b * 15) // 50
        - random.randrange(30)
        + random.randrange(40)
    )
    double_per = (
        -25
        + (trajectory * 10) // 4
        + (meet * 0 + power * 25 + speed_b * 20) // 50
        - random.randrange(8)
        + random.randrange(10)
    )
    triple_per = (
        -15
        + (trajectory * 0) // 4
        + (meet * 0 + power * 0 + speed_b * 15) // 50
        - random.randrange(4)
        + random.randrange(5)
    )
    homeRun_per = (
        -40
        + (trajectory * 20) // 4
        + (meet * -10 + power * 60 + speed_b * -10) // 50
        - random.randrange(12)
        + random.randrange(16)
    )
    walk_per = (
        -15
        + (trajectory * 30) // 4
        + (meet * 0 + power * 80 + speed_b * -10) // 50
        - random.randrange(24)
        + random.randrange(32)
    )
    HBP_per = (
        10
        + (trajectory * 0) // 4
        + (meet * 0 + power * 0 + speed_b * 0) // 50
        - random.randrange(3)
        + random.randrange(4)
    )

    # 選球眼のランクを数値に変換
    walk_per_corr = physics.eye_logic(eye)

    # 投手・野手能力に応じて確率変動
    walk_per += (walk_per_corr - control) * 1.5

    # マイナス値を0に補正
    single_per = max(0, single_per)
    double_per = max(0, double_per)
    triple_per = max(0, triple_per)
    homeRun_per = max(0, homeRun_per)
    walk_per = max(0, walk_per)
    HBP_per = max(0, HBP_per)

    # 確率の計算
    sP = single_per
    dP = double_per + sP
    tP = triple_per + dP
    hrP = homeRun_per + tP
    wP = walk_per + hrP
    hbpP = HBP_per + wP

    # 判定実行
    num = random.randrange(1000)
    result = ""

    if num <= sP:
        result = "1B"
    elif num <= dP:
        result = "2B"
    elif num <= tP:
        result = "3B"
    elif num <= hrP:
        result = "HR"
    elif num <= wP:
        result = "BB"
    elif num <= hbpP:
        result = "HBP"
    else:
        # 凡退の中で三振かどうかを判定
        result = strikeout_logic(speed_p, breaking_ball, meet)

    return result


def base_advancement_logic(result: str, game_condition: list[int]) -> list[int]:
    """
        打撃結果に基づき、ランナーの進塁とスコア、アウトカウントを更新する

    Args:
        - result : 打席結果
        - game_condition : 試合状況のリスト

    Returns:
        - list[int] : 更新された試合状況のリスト
    """
    # game_condition: [b1, b2, b3, outs, score]
    b1, b2, b3 = game_condition[0], game_condition[1], game_condition[2]
    outs = game_condition[3]
    score = game_condition[4]

    if result == "1B":
        score += b3
        b3, b2, b1 = b2, b1, 1

    elif result == "2B":
        score += b3 + b2
        b3, b2, b1 = b1, 1, 0

    elif result == "3B":
        score += b3 + b2 + b1
        b3, b2, b1 = 1, 0, 0

    elif result == "HR":
        score += b3 + b2 + b1 + 1
        b3, b2, b1 = 0, 0, 0

    elif result in ["BB", "HBP"]:
        if b1 == 1 and b2 == 1 and b3 == 1:
            score += 1
        elif b1 == 1 and b2 == 1:
            b3 = 1
        elif b1 == 1:
            b2 = 1
        b1 = 1

    elif result in ["OUT", "SO"]:
        outs += 1

    # game_conditionリストを直接書き換え
    game_condition[0], game_condition[1], game_condition[2] = b1, b2, b3
    game_condition[3] = outs
    game_condition[4] = score

    return game_condition
