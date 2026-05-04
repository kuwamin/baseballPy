import random
from modules.const import BREAKING_BALL_AVG, MEET_AVG, SPEED_AVG
from modules.logic import physics


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
        + (speed_p - SPEED_AVG) * 0.25
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
