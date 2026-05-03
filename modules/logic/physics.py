def eye_logic(eye):
    """
    選球眼ランクに基づいた四球発生率の補正値を返す
    """
    # ランクと補正値の対応表（辞書形式に整理しても良いですが、元のロジックを維持します）
    if eye == "A":
        walk_per_corr = 80
    elif eye == "B":
        walk_per_corr = 70
    elif eye == "C":
        walk_per_corr = 60
    elif eye == "D":
        walk_per_corr = 50
    elif eye == "E":
        walk_per_corr = 40
    elif eye == "F":
        walk_per_corr = 30
    elif eye == "G":
        walk_per_corr = 20
    else:
        walk_per_corr = 0  # 定義外の入力に対する安全策

    return walk_per_corr


def pitcher_ability(speed_p, control, breaking_ball):
    """
    投手の能力（球速・制御・変化球）から、野手のミート・パワーへのデバフ値を算出する
    """
    # 基準値（平均値）
    speed_avg = 147
    control_avg = 50
    breaking_ball_avg = 6

    # 野手側補正値初期値
    meet_corr = 0
    power_corr = 0

    # 1. 球速による補正 (1kmの差でミート約-1.125, パワー約-0.75)
    meet_corr += (speed_p - speed_avg) * (-9) / 8
    power_corr += (speed_p - speed_avg) * (-6) / 8

    # 2. コントロールによる補正 (ミートへの影響は0, パワーのみ影響)
    meet_corr += (control - control_avg) * (-0) / 30
    power_corr += (control - control_avg) * (-6) / 30

    # 3. 変化球による補正
    meet_corr += (breaking_ball - breaking_ball_avg) * (-6) / 4
    power_corr += (breaking_ball - breaking_ball_avg) * (-3) / 4

    return meet_corr, power_corr
