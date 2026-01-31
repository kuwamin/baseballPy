import random


def decide_relief(pitchers, already_played_records, inning, score_diff):
    """
    役割に応じたリリーフ選出
    """
    already_played = [r[0] for r in already_played_records]
    
    # 接戦（3点差以内）の終盤判断
    if inning >= 9 and 0 < score_diff <= 3:
        role_target = ["抑"] 
    elif inning >= 7 and 0 < score_diff <= 3:
        role_target = ["セ", "継"] 
    elif score_diff >= 0:
        role_target = ["継", "セ"] 
    else:
        role_target = ["継"] 

    candidates = [p for p in pitchers if p not in already_played and p.role in role_target]
    if not candidates:
        candidates = [p for p in pitchers if p not in already_played]

    # 登板過多を防ぐため、ゲーム数の少ない順にソートして上位3名から抽選
    pool = sorted(candidates, key=lambda x: x.stats.get('games', 0))[:3]
    return random.choice(pool)