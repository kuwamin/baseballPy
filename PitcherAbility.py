import SpecialAbility


def pitcher_ability(pitcher, batter, is_risp):

    # 基準値（平均値）
    speed_avg = 147
    control_avg = 50
    breaking_ball_avg = 6

    # 野手側補正値初期値
    meet_corr = 0
    power_corr = 0

    # 球速による補正
    meet_corr += (pitcher.speed - speed_avg) * (-6)/8
    power_corr += (pitcher.speed - speed_avg) * (-3)/8

    # コントロールによる補正
    meet_corr += (pitcher.control - control_avg) * (-0)/30
    power_corr += (pitcher.control - control_avg) * (-9)/30

    # 変化球による補正
    meet_corr += (pitcher.breaking_ball - breaking_ball_avg) * (-6)/3
    power_corr += (pitcher.breaking_ball - breaking_ball_avg) * (-3)/3

    return meet_corr, power_corr