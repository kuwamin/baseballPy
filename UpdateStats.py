def update_stats(pitcher, batter, result, risp, rbi):
    """判定結果に基づいて野手(batter)のstats辞書のみを更新する"""
    
    # --- 打者の更新（ここだけを実行） ---
    # 打席数
    batter.stats['pa'] += 1
    
    # 打点
    if 'rbi' not in batter.stats:
        batter.stats['rbi'] = 0
    batter.stats['rbi'] += rbi
    
    # 得点圏打席
    if risp:
        batter.stats['risp_pa'] += 1

    # 安打・四死球・三振の判定
    if result in ["1B", "2B", "3B", "HR"]:
        batter.stats['hits'] += 1
        if result == "1B": batter.stats['singles'] += 1
        elif result == "2B": batter.stats['doubles'] += 1
        elif result == "3B": batter.stats['triples'] += 1
        elif result == "HR": batter.stats['hr'] += 1
        
        if risp:
            batter.stats['risp_hits'] += 1

    elif result == "BB":
        batter.stats['walks'] += 1
    elif result == "HBP":
        batter.stats['hbp'] += 1
    elif result == "SO":
        batter.stats['so'] += 1

    # 打数(ab)の計算: 打席数 - (四球 + 死球)
    batter.stats['ab'] = batter.stats['pa'] - (batter.stats['walks'] + batter.stats['hbp'])
    
    # ※投手の更新（pitcher.stats...）は行わない