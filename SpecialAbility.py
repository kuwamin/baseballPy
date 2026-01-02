def test(pitcher, batter, is_risp):

    # グローバル変数化
    meet_corr = 0
    power_corr = 0

    # 得点圏チェック
    if is_risp == True:
        if batter.clutch_b == "A":
            meet_corr += 15
            power_corr += 10
        elif batter.clutch_b == "B":
            meet_corr += 8
            power_corr += 5
        elif batter.clutch_b == "C":
            meet_corr += 5
            power_corr += 2
        elif batter.clutch_b == "D":
            meet_corr += 0
            power_corr += 0
        elif batter.clutch_b == "E":
            meet_corr -= 5
            power_corr -= 2
        elif batter.clutch_b == "F":
            meet_corr -= 8
            power_corr -= 5
        elif batter.clutch_b == "G":
            meet_corr -= 15
            power_corr -= 10

    # 対左投手チェック
    if pitcher.throwing == "左":
        if batter.vs_left_b == "A":
            meet_corr += 15
            power_corr += 10
        elif batter.vs_left_b == "B":
            meet_corr += 8
            power_corr += 5
        elif batter.vs_left_b == "C":
            meet_corr += 5
            power_corr += 2
        elif batter.vs_left_b == "D":
            meet_corr += 0
            power_corr += 0
        elif batter.vs_left_b == "E":
            meet_corr -= 5
            power_corr -= 2
        elif batter.vs_left_b == "F":
            meet_corr -= 8
            power_corr -= 5
        elif batter.vs_left_b == "G":
            meet_corr -= 15
            power_corr -= 10


    return meet_corr, power_corr