def update_stats_b(pitcher, batter, result, risp, rbi):
    """判定結果に基づいて野手のstats辞書を更新する"""
    
    # 全打席共通の加算
    batter.stats['pa'] += 1
    batter.stats['rbi'] += rbi
    
    # 得点圏打数の判定（四死球以外かつ得点圏）
    if risp and result not in ["BB", "HBP"]:
        batter.stats['risp_ab'] += 1

    # 結果別の分岐
    if result in ["1B", "2B", "3B", "HR"]:
        batter.stats['hits'] += 1
        if result == "1B":   batter.stats['singles'] += 1
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

    # 打数(ab)の再計算
    batter.stats['ab'] = batter.stats['pa'] - (batter.stats['walks'] + batter.stats['hbp'])


def update_stats_p(pitcher, batter, result, risp, rbi):
    """判定結果に基づいて投手のstats辞書を更新する"""

    # 全打席共通の加算
    pitcher.stats['bf'] += 1
    pitcher.stats['失点'] += rbi
    pitcher.stats['自責点'] += rbi

    # 得点圏打者数の加算
    if risp:
        pitcher.stats['risp_bf'] += 1

    # 結果別の分岐
    if result in ["1B", "2B", "3B", "HR"]:
        pitcher.stats['hits_allowed'] += 1
        if result == "HR":
            pitcher.stats['hr_allowed'] += 1
        
        if risp:
            pitcher.stats['risp_hits_allowed'] += 1

    elif result == "BB":
        pitcher.stats['walks_allowed'] += 1
    elif result == "HBP":
        pitcher.stats['hbp_allowed'] += 1
    elif result == "SO":
        pitcher.stats['strikeouts'] += 1
        pitcher.stats['outs_pitched'] += 1

    elif result == "OUT":
        pitcher.stats['outs_pitched'] += 1