import random
import SpecialAbility
import UpdateStats

def logic(pitcher, batter, game_condition, is_risp):
    """
    打席の結果を判定し、進塁処理を行い、成績を更新する
    """

    # 0. 特殊能力による能力変動
    meet, power = SpecialAbility.test(pitcher, batter, is_risp)



    # --- 1. 各結果の基本値計算 ---
    singlePer = (100 + (batter.trajectory * -30) // 4 + (meet * 140 + power * -60 + batter.speed * 15) // 50 - random.randrange(40) + random.randrange(30))
    doublePer = (-25 + (batter.trajectory * 10) // 4 + (meet * 0 + power * 25 + batter.speed * 20) // 50 - random.randrange(10) + random.randrange(8))
    triplePer = (-12 + (batter.trajectory * 0) // 4 + (meet * 0 + power * 0 + batter.speed * 15) // 50 - random.randrange(5) + random.randrange(4))
    homeRunPer = (-40 + (batter.trajectory * 20) // 4 + (meet * -10 + power * 60 + batter.speed * -10) // 50 - random.randrange(16) + random.randrange(12))
    walkPer = (-40 + (batter.trajectory * 30) // 4 + (meet * 0 + power * 80 + batter.speed * -10) // 50 - random.randrange(16) + random.randrange(12))
    hitByPitchPer = (10 + (batter.trajectory * 0) // 4 + (meet * 0 + power * 0 + batter.speed * 0) // 50 - random.randrange(4) + random.randrange(3))

    # マイナス値を0に補正
    singlePer = max(0, singlePer) 
    doublePer = max(0, doublePer)
    triplePer = max(0, triplePer)
    homeRunPer = max(0, homeRunPer)
    walkPer = max(0, walkPer)
    hitByPitchPer = max(0, hitByPitchPer)

    # --- 2. 累積確率の計算 ---
    sP = singlePer
    dP = doublePer + sP
    tP = triplePer + dP
    hrP = homeRunPer + tP
    wP = walkPer + hrP
    hbpP = hitByPitchPer + wP

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
        if random.randrange(100) < 20:
            result = "SO"
        else:
            result = "OUT"

    # --- 4. 進塁処理 ---
    b1, b2, b3 = game_condition[0], game_condition[1], game_condition[2]
    outs = game_condition[3]
    old_score = game_condition[4] # 更新前のスコアを保持
    score = old_score

    if result == "1B":
        score += b3
        b3, b2, b1 = b2, b1, 1

    elif result == "2B":
        score += (b3 + b2)
        b3, b2, b1 = b1, 1, 0

    elif result == "3B":
        score += (b3 + b2 + b1)
        b3, b2, b1 = 1, 0, 0

    elif result == "HR":
        score += (b3 + b2 + b1 + 1)
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

    # 今回の打席で発生した得点（＝打点）を計算
    rbi = score - old_score

    # game_conditionリストを更新
    game_condition[0], game_condition[1], game_condition[2] = b1, b2, b3
    game_condition[3] = outs
    game_condition[4] = score

    # --- 5. 成績(stats)の更新 ---
    UpdateStats.update_stats(pitcher, batter, result, is_risp, rbi)
    print(f"{batter.name} : {result}")
    
    return game_condition