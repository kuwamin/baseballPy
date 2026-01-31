def get_batter_stats(player):
    """
    打率、本塁打、打点、出塁率、OPSを計算して文字列で返す
    """
    # 累積データの取得
    hits = player.stats.get('hits', 0)
    ab = player.stats.get('ab', 0)
    hr = player.stats.get('hr', 0)
    rbi = player.stats.get('rbi', 0)
    

    single = player.stats.get('singles', 0)  
    double = player.stats.get('doubles', 0)  
    triple = player.stats.get('triples', 0)  
    bb = player.stats.get('walks', 0)        
    hbp = player.stats.get('hbp', 0)
    sf = player.stats.get('sf', 0) 

    # 1. 打率 (AVG)
    if ab > 0:
        avg = hits / ab
    else:
        avg = 0.0

    # 2. 出塁率 (OBP)
    obp_denominator = ab + bb + hbp + sf
    if obp_denominator > 0:
        obp = (hits + bb + hbp) / obp_denominator  
    else:
        obp = 0.0

    # 3. 長打率 (SLG)
    total_bases = (single * 1) + (double * 2) + (triple * 3) + (hr * 4)
    if ab > 0:
        slg = total_bases / ab  
    else:
        slg = 0.0

    # 4. OPS
    ops = obp + slg

    return f"{avg:.3f} {hr}本 {rbi}打点 OBP{obp:.3f} OPS{ops:.3f}"


def get_pitcher_stats(pitcher):
    """
    辞書にある対戦打者数などのデータからアウト数を逆算して防御率を計算する
    """
    games = pitcher.stats.get('games', 0)
    wins = pitcher.stats.get('wins', 0)
    losses = pitcher.stats.get('losses', 0)
    saves = pitcher.stats.get('saves', 0)
    holds = pitcher.stats.get('holds', 0)
    er = pitcher.stats.get('自責点', 0)
    
    # 辞書の中にあるデータからアウト数を逆算
    # bf(打者数) - (hits_allowed(被安打) + walks_allowed(四球) + hbp_allowed(死球))
    bf = pitcher.stats.get('bf', 0)
    h = pitcher.stats.get('hits_allowed', 0)
    bb = pitcher.stats.get('walks_allowed', 0)
    hbp = pitcher.stats.get('hbp_allowed', 0)
    
    total_outs = bf - (h + bb + hbp)

    # 防御率 (ERA) の計算
    if total_outs > 0:
        # 公式: (自責点 * 9) / (アウト数 / 3)
        era = (er * 9) / (total_outs / 3)
    else:
        era = 0.00

    return f"{games}登板 {(total_outs / 3)}回 {era:.2f} {wins}勝 {losses}敗 {saves}S {holds}H"