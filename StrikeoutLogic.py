import random

def strikeout_logic(speed_p, breaking_ball, meet):
    # 計算用平均値
    meet_avg = 50
    speed_p_avg = 145
    breaking_ball_avg = 6

    if random.randrange(100) < 10 + (speed_p - speed_p_avg)*1.5 + (breaking_ball - breaking_ball_avg)*2 + (meet - meet_avg)*(-0.25):
        return "SO"
    else:
        return "OUT"