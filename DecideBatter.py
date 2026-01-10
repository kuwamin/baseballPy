def calculate_score(player, weight):
    """
    選手の総合評価スコアを計算する
    """
    batting_score = player.trajectory * 10 + (player.meet + player.power) * 2 + player.speed
    fielding_score = (player.arm + player.fielding + player.catching) * weight
    
    return batting_score + fielding_score


def decide_batter(batters):
    """
    攻守の総合力に基づいて各ポジションのレギュラーを選出する
    """
    # 守備を重視する重み
    pos_weights = {
        '捕': 1.0, '遊': 0.9, '二': 0.8, '中': 0.7,
        '三': 0.4, '右': 0.3, '左': 0.2, '一': 0.1
    }
    
    selected_players = []
    candidates = batters[:]

    # 1. 各ポジションの選出
    for pos in pos_weights.keys():
        weight = pos_weights[pos]
        pos_candidates = []
        
        # そのポジションの選手をリストアップ
        for p in candidates:
            if p.position == pos:
                pos_candidates.append(p)
        
        if not pos_candidates:
            continue

        # 一番スコアが高い選手を探す
        best_player = pos_candidates[0]
        max_score = calculate_score(best_player, weight)
        
        for p in pos_candidates:
            current_score = calculate_score(p, weight)
            if current_score > max_score:
                max_score = current_score
                best_player = p
        
        selected_players.append((pos, best_player))
        candidates.remove(best_player)

    # 2. 指名打者(指)の選出
    if candidates:
        dh_player = candidates[0]
        # DHは守備関係ないので weight=0 で計算
        max_dh_score = calculate_score(dh_player, 0)
        
        for p in candidates:
            current_dh_score = calculate_score(p, 0)
            if current_dh_score > max_dh_score:
                max_dh_score = current_dh_score
                dh_player = p
                
        selected_players.append(('指', dh_player))

    return selected_players