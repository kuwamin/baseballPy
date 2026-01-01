def test(pitcher, batter, is_risp):

    # グローバル変数化
    meet = batter.meet
    power = batter.power

    # 得点圏チェック
    if is_risp == True:
        if batter.clutch_b == "A":
            meet += 15
            power += 10
        elif batter.clutch_b == "B":
            meet += 8
            power += 5
        elif batter.clutch_b == "C":
            meet += 5
            power += 2
        elif batter.clutch_b == "D":
            meet += 0
            power += 0
        elif batter.clutch_b == "E":
            meet -= 5
            power -= 2
        elif batter.clutch_b == "F":
            meet -= 8
            power -= 5
        elif batter.clutch_b == "G":
            meet -= 15
            power -= 10

    # 対左投手チェック
    if pitcher.throwing == "左":
        if batter.vs_left_b == "A":
            meet += 15
            power += 10
        elif batter.vs_left_b == "B":
            meet += 8
            power += 5
        elif batter.vs_left_b == "C":
            meet += 5
            power += 2
        elif batter.vs_left_b == "D":
            meet += 0
            power += 0
        elif batter.vs_left_b == "E":
            meet -= 5
            power -= 2
        elif batter.vs_left_b == "F":
            meet -= 8
            power -= 5
        elif batter.vs_left_b == "G":
            meet -= 15
            power -= 10


    return meet, power