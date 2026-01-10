import random

import EyeLogic
import StrikeoutLogic


def result_logic(trajectory, meet, power, speed_b, eye, speed_p, control, breaking_ball):

    # --- 1. 各結果の基本値計算 ---
    single_per = (110 + (trajectory * -30) // 4 + (meet * 140 + power * -60 + speed_b * 15) // 50 - random.randrange(30) + random.randrange(40))
    double_per = (-25 + (trajectory * 10) // 4 + (meet * 0 + power * 25 + speed_b * 20) // 50 - random.randrange(8) + random.randrange(10))
    triple_per = (-15 + (trajectory * 0) // 4 + (meet * 0 + power * 0 + speed_b * 15) // 50 - random.randrange(4) + random.randrange(5))
    homeRun_per = (-40 + (trajectory * 20) // 4 + (meet * -10 + power * 60 + speed_b * -10) // 50 - random.randrange(12) + random.randrange(16))
    walk_per = (-15 + (trajectory * 30) // 4 + (meet * 0 + power * 80 + speed_b * -10) // 50 - random.randrange(24) + random.randrange(32))
    HBP_per = (10 + (trajectory * 0) // 4 + (meet * 0 + power * 0 + speed_b * 0) // 50 - random.randrange(3) + random.randrange(4))


    # 選球眼のランクを数値に変換
    walk_per_corr = EyeLogic.eye_logic(eye)

    # 投手・野手能力に応じて確率変動
    walk_per += (walk_per_corr - control) * 1.5

    # マイナス値を0に補正
    single_per = max(0, single_per) 
    double_per = max(0, double_per)
    triple_per = max(0, triple_per)
    homeRun_per = max(0, homeRun_per)
    walk_per = max(0, walk_per)
    HBP_per = max(0, HBP_per)

    # --- 2. 累積確率の計算 ---
    sP = single_per
    dP = double_per + sP
    tP = triple_per + dP
    hrP = homeRun_per + tP
    wP = walk_per + hrP
    hbpP = HBP_per + wP

    # --- 3. 判定実行 ---
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
        result = StrikeoutLogic.strikeout_logic(speed_p, breaking_ball, meet)

    return result