import random

def decide_relief(pitchers, already_played_records, inning, score_diff):
    """
    役割に応じたリリーフ選出
    """
    already_played = [r[0] for r in already_played_records]
    
    if inning >= 9 and 0 < score_diff <= 3:
        role_target = ["抑"] 
    elif inning >= 7 and 0 < score_diff <= 3:
        role_target = ["セ", "継"] 
    elif score_diff >= 0:
        role_target = ["継", "セ"] 
    else:
        role_target = ["継"] 

    # フィルタリング条件：減少体力が一定以下（例: 最大スタミナの半分以下）
    candidates = [
        p for p in pitchers 
        if p not in already_played 
        and p.role in role_target
        and p.fatigue_stamina < (p.stamina * 0.5)
    ]
    
    # もし条件に合う選手が誰もいない場合は、全リリーフから選出
    if not candidates:
        candidates = [p for p in pitchers if p not in already_played and p.role != "先"]

    # 疲労が少ない（fatigue_staminaが低い）順にソートして上位から選ぶ
    pool = sorted(candidates, key=lambda x: x.fatigue_stamina)[:3]
    return random.choice(pool)