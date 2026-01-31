def assign_win_loss(records_1, records_2, score_1, score_2):
    """
    勝利・敗戦・セーブ・ホールドの割り当て
    """
    if score_1 == score_2: return # 引き分けは処理しない

    win_records = records_1 if score_1 > score_2 else records_2
    loss_records = records_2 if score_1 > score_2 else records_1
    win_score = score_1 if score_1 > score_2 else score_2
    loss_score = score_2 if score_1 > score_2 else score_1
    
    # 1. 敗戦投手の決定
    loser = loss_records[0][0]
    for p, s_own, s_opp in loss_records:
        if s_own < s_opp: break
        loser = p
    loser.stats['losses'] += 1

    # 2. 勝利投手の決定
    winner = None
    starter = win_records[0][0]
    # 先発が5回(15アウト)以上投げ、降板時も試合終了時もリードを保っていた場合
    if starter.stats.get('outs_pitched', 0) >= 15:
        # 簡易的に、先発が降板した時にリードしていれば権利ありとする
        winner = starter
    else:
        # 先発に権利がない場合、2番手以降で勝利に貢献した投手に
        if len(win_records) > 1:
            winner = win_records[1][0]
        else:
            winner = starter
    
    winner.stats['wins'] += 1

    # 3. セーブ・ホールドの判定 (勝利チームのリリーフが対象)
    if len(win_records) > 1:
        last_pitcher = win_records[-1][0]
        for i, (p, s_own, s_opp) in enumerate(win_records):
            if p == winner: continue # 勝利投手には付かない
            
            # 登板時の点差
            lead_margin = s_own - s_opp
            if lead_margin <= 0: continue # 同点・ビハインド登板は対象外

            # 共通条件：リードを守って降板（または試合終了）すること
            # 簡易判定：現在の投手成績から失点をチェック（本来は降板時判定が必要だが簡易化）
            er_allowed = p.stats.get('自責点', 0)
            
            if p == last_pitcher:
                # セーブ判定：3点以内リードで1イニング以上投げ切るなど
                if lead_margin <= 3:
                    p.stats['saves'] += 1
            else:
                # ホールド判定：リード場面で登板し、リードを保って次へ繋ぐ
                if lead_margin <= 3:
                    p.stats['holds'] += 1