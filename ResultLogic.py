import random


def result_logic(trajectory, meet, power, speed):

    # --- 1. 各結果の基本値計算 ---
    singlePer = (100 + (trajectory * -30) // 4 + (meet * 140 + power * -60 + speed * 15) // 50 - random.randrange(40) + random.randrange(30))
    doublePer = (-25 + (trajectory * 10) // 4 + (meet * 0 + power * 25 + speed * 20) // 50 - random.randrange(10) + random.randrange(8))
    triplePer = (-12 + (trajectory * 0) // 4 + (meet * 0 + power * 0 + speed * 15) // 50 - random.randrange(5) + random.randrange(4))
    homeRunPer = (-40 + (trajectory * 20) // 4 + (meet * -10 + power * 60 + speed * -10) // 50 - random.randrange(16) + random.randrange(12))
    walkPer = (-40 + (trajectory * 30) // 4 + (meet * 0 + power * 80 + speed * -10) // 50 - random.randrange(16) + random.randrange(12))
    hitByPitchPer = (10 + (trajectory * 0) // 4 + (meet * 0 + power * 0 + speed * 0) // 50 - random.randrange(4) + random.randrange(3))

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

    return result