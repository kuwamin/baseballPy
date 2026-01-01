def update_stats(pitcher, batter, result, risp):
    """判定結果に基づいてstats辞書を更新する"""
    # 共通加算項目
    batter.stats['pa'] += 1
    pitcher.stats['batters_faced'] += 1
    
    if risp:
        batter.stats['risp_pa'] += 1
        pitcher.stats['risp_batters'] += 1

    # 結果別加算項目
    if result == "1B":
        batter.stats['hits'] += 1
        batter.stats['singles'] += 1
        pitcher.stats['hits_allowed'] += 1
        if risp:
            batter.stats['risp_hits'] += 1
            pitcher.stats['risp_hits'] += 1
            
    elif result == "2B":
        batter.stats['hits'] += 1
        batter.stats['doubles'] += 1
        pitcher.stats['hits_allowed'] += 1
        if risp:
            batter.stats['risp_hits'] += 1
            pitcher.stats['risp_hits'] += 1

    elif result == "3B":
        batter.stats['hits'] += 1
        batter.stats['triples'] += 1
        pitcher.stats['hits_allowed'] += 1
        if risp:
            batter.stats['risp_hits'] += 1
            pitcher.stats['risp_hits'] += 1

    elif result == "HR":
        batter.stats['hits'] += 1
        batter.stats['hr'] += 1
        pitcher.stats['hits_allowed'] += 1
        pitcher.stats['hr_allowed'] += 1
        if risp:
            batter.stats['risp_hits'] += 1
            pitcher.stats['risp_hits'] += 1

    elif result == "BB":
        batter.stats['walks'] += 1
        pitcher.stats['walks'] += 1

    elif result == "HBP":
        batter.stats['hbp'] += 1
        pitcher.stats['hit_by_pitch'] += 1

    elif result == "SO":
        batter.stats['so'] += 1
        pitcher.stats['strikeouts'] += 1
        pitcher.stats['outs_pitched'] += 1

    elif result == "OUT":
        pitcher.stats['outs_pitched'] += 1

    # 打数(ab)の計算: 打席数 - (四球 + 死球)
    batter.stats['ab'] = batter.stats['pa'] - (batter.stats['walks'] + batter.stats['hbp'])