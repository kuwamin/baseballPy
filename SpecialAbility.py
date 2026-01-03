def special_ability_b(pitcher, batter, is_risp):

    # グローバル変数化
    meet_corr = 0
    power_corr = 0

    # 得点圏チェック
    if is_risp == True:
        # 野手側（チャンス）チェック
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


def special_ability_p(pitcher, batter, is_risp):

    # グローバル変数化
    speed_corr = 0
    control_corr = 0
    breaking_ball_corr = 0

    # 得点圏チェック
    if is_risp == True:
        #投手側（ピンチ）チェック
        if pitcher.clutch_p == "A":
            speed_corr += 2
            breaking_ball_corr += 4
        elif pitcher.clutch_p == "B":
            speed_corr += 1
            breaking_ball_corr += 2
        elif pitcher.clutch_p == "C":
            speed_corr += 1
        elif pitcher.clutch_p == "D":
            speed_corr += 0
            breaking_ball_corr += 0
        elif pitcher.clutch_p == "E":
            speed_corr -= 1
        elif pitcher.clutch_p == "F":
            speed_corr -= 1
            breaking_ball_corr -= 2
        elif pitcher.clutch_p == "G":
            speed_corr -= 2
            breaking_ball_corr -= 4

    # 対左投手チェック
    if batter.batting == "左":
        if pitcher.vs_left_p == "A":
            speed_corr += 3
            control_corr += 6
            # スタミナ消費量ロジック実装予定
        elif pitcher.vs_left_p == "B":
            speed_corr += 2
            control_corr += 5
        elif pitcher.vs_left_p == "C":
            speed_corr += 1
            control_corr += 2
        elif pitcher.vs_left_p == "D":
            speed_corr += 0
            breaking_ball_corr += 0
        elif pitcher.vs_left_p == "E":
            speed_corr -= 1
            control_corr -= 2
        elif pitcher.vs_left_p == "F":
            speed_corr -= 2
            control_corr -= 5
        elif pitcher.vs_left_p == "G":
            speed_corr -= 3
            control_corr -= 6

    # ノビチェック
    if pitcher.fastball_life == "A":
        speed_corr += 8
    elif pitcher.fastball_life == "B":
        speed_corr += 4
    elif pitcher.fastball_life == "C":
        speed_corr += 2
    elif pitcher.fastball_life == "D":
        speed_corr += 0
    elif pitcher.fastball_life == "E":
        speed_corr -= 2
    elif pitcher.fastball_life == "F":
        speed_corr -= 4
    elif pitcher.fastball_life == "G":
        speed_corr += 8
        
    return speed_corr, control_corr, breaking_ball_corr
