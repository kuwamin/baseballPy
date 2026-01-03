def pitcher_ability(pitcher):

    # 基準値（平均値）
    speed_avg = 145
    control_avg = 50
    breaking_ball_avg = 6

    # 初期値
    meet_corr = 0
    power_corr = 0

    # 球速による補正
    meet_corr += (pitcher.speed - speed_avg) * (-8)/15
    power_corr += (pitcher.speed - speed_avg) * (-4)/15

    # コントロールによる補正
    meet_corr += (pitcher.control - control_avg) * (-4)/30
    power_corr += (pitcher.control - control_avg) * (-12)/30

    # 変化球による補正
    meet_corr += (pitcher.breaking_ball - breaking_ball_avg) * (-8)/4
    power_corr += (pitcher.breaking_ball - breaking_ball_avg) * (-4)/4

    return meet_corr, power_corr