def pitcher_ability(speed_p, control, breaking_ball):

    # 基準値（平均値）
    speed_avg = 147
    control_avg = 50
    breaking_ball_avg = 6

    # 野手側補正値初期値
    meet_corr = 0
    power_corr = 0

    # 球速による補正
    meet_corr += (speed_p - speed_avg) * (-9)/8
    power_corr += (speed_p - speed_avg) * (-6)/8

    # コントロールによる補正
    meet_corr += (control - control_avg) * (-0)/30
    power_corr += (control - control_avg) * (-6)/30

    # 変化球による補正
    meet_corr += (breaking_ball - breaking_ball_avg) * (-6)/4
    power_corr += (breaking_ball - breaking_ball_avg) * (-3)/4

    return meet_corr, power_corr