"""
成績の集計・更新・文字列化を担当するモジュール
"""

# --- 1. 成績表示用（文字列変換） ---


def get_batter_stats(player):
    """
    打率、本塁打、打点、出塁率、OPSを計算して文字列で返す
    """
    s = player.stats
    games = s.get("games", 0)
    hits = s.get("hits", 0)
    ab = s.get("ab", 0)
    hr = s.get("hr", 0)
    rbi = s.get("rbi", 0)

    single = s.get("singles", 0)
    double = s.get("doubles", 0)
    triple = s.get("triples", 0)
    bb = s.get("walks", 0)
    hbp = s.get("hbp", 0)
    sf = s.get("sf", 0)

    # 1. 打率 (AVG)
    avg = hits / ab if ab > 0 else 0.0

    # 2. 出塁率 (OBP)
    obp_denom = ab + bb + hbp + sf
    obp = (hits + bb + hbp) / obp_denom if obp_denom > 0 else 0.0

    # 3. 長打率 (SLG)
    total_bases = (single * 1) + (double * 2) + (triple * 3) + (hr * 4)
    slg = total_bases / ab if ab > 0 else 0.0

    # 4. OPS
    ops = obp + slg

    return f"{games}試合 {avg:.3f} {hr}本 {rbi}打点 OBP{obp:.3f} OPS{ops:.3f}"


def get_pitcher_stats(pitcher):
    """
    累積データから防御率などを計算して文字列で返す
    """
    s = pitcher.stats
    games = s.get("games", 0)
    wins = s.get("wins", 0)
    losses = s.get("losses", 0)
    saves = s.get("saves", 0)
    holds = s.get("holds", 0)
    er = s.get("自責点", 0)

    # アウト数の計算 (bf - 被安打 - 与四死球)
    bf = s.get("bf", 0)
    h = s.get("hits_allowed", 0)
    bb = s.get("walks_allowed", 0)
    hbp = s.get("hbp_allowed", 0)

    total_outs = bf - (h + bb + hbp)

    # 防御率 (ERA)
    # 公式: (自責点 * 9) / (投球回)  ※投球回 = アウト数 / 3
    if total_outs > 0:
        era = (er * 27) / total_outs
    else:
        era = 0.00

    # 投球回を「回 1/3」形式にするための計算
    innings = total_outs // 3
    remaining_outs = total_outs % 3
    innings_str = f"{innings}.{remaining_outs}"

    return (
        f"{games}登板 {innings_str}回 {era:.2f} {wins}勝 {losses}敗 {saves}S {holds}H"
    )


# --- 2. 試合中のリアルタイム更新 ---


def judge_risp(game_condition):
    """
    得点圏（2塁または3塁）にランナーがいるか判定
    game_condition: [b1, b2, b3, outs, score]
    """
    return game_condition[1] == 1 or game_condition[2] == 1


def update_stats_b(pitcher, batter, result, risp, rbi):
    """判定結果に基づいて野手のstats辞書を更新する"""
    s = batter.stats

    s["pa"] += 1
    s["rbi"] += rbi

    # 得点圏打数の判定
    if risp and result not in ["BB", "HBP"]:
        s["risp_ab"] += 1

    # 結果別の分岐
    if result in ["1B", "2B", "3B", "HR"]:
        s["hits"] += 1
        if result == "1B":
            s["singles"] += 1
        elif result == "2B":
            s["doubles"] += 1
        elif result == "3B":
            s["triples"] += 1
        elif result == "HR":
            s["hr"] += 1

        if risp:
            s["risp_hits"] += 1

    elif result == "BB":
        s["walks"] += 1
    elif result == "HBP":
        s["hbp"] += 1
    elif result == "SO":
        s["so"] += 1

    # 打数(ab) = 打席(pa) - (四球 + 死球 + 犠飛)
    # ※sf(犠飛)も辞書にあることを想定
    s["ab"] = s["pa"] - (s["walks"] + s["hbp"] + s.get("sf", 0))


def update_stats_p(pitcher, batter, result, risp, rbi):
    """判定結果に基づいて投手のstats辞書を更新する"""
    s = pitcher.stats

    s["bf"] += 1
    s["失点"] += rbi
    s["自責点"] += rbi

    if risp:
        s["risp_bf"] += 1

    if result in ["1B", "2B", "3B", "HR"]:
        s["hits_allowed"] += 1
        if result == "HR":
            s["hr_allowed"] += 1
        if risp:
            s["risp_hits_allowed"] += 1

    elif result == "BB":
        s["walks_allowed"] += 1
    elif result == "HBP":
        s["hbp_allowed"] += 1
    elif result == "SO":
        s["strikeouts"] += 1
        s["outs_pitched"] += 1
    elif result == "OUT":
        s["outs_pitched"] += 1


# --- 3. 試合終了時の称号割り当て ---


def assign_win_loss(records_1, records_2, score_1, score_2):
    """
    勝利・敗戦・セーブ・ホールドの割り当て
    records: [(pitcher_obj, score_own, score_opp), ...] 登板順のリスト
    """
    if score_1 == score_2:
        return

    is_team1_win = score_1 > score_2
    win_records = records_1 if is_team1_win else records_2
    loss_records = records_2 if is_team1_win else records_1

    # 1. 敗戦投手の決定
    # リードを許した時点の投手を簡易的に敗戦投手とする
    loser = loss_records[0][0]
    for p, s_own, s_opp in loss_records:
        if s_own < s_opp:
            loser = p
            break
    loser.stats["losses"] += 1

    # 2. 勝利投手の決定
    winner = None
    starter, s_start_own, s_start_opp = win_records[0]

    # 先発が5回(15アウト)以上投げ、降板時にリードしている場合
    if starter.stats.get("outs_pitched", 0) >= 15 and s_start_own > s_start_opp:
        winner = starter
    else:
        # 先発に権利がない場合、2番手以降を暫定勝利投手に
        winner = win_records[1][0] if len(win_records) > 1 else starter

    winner.stats["wins"] += 1

    # 3. セーブ・ホールドの判定
    if len(win_records) > 1:
        last_pitcher = win_records[-1][0]
        for p, s_in_own, s_in_opp in win_records:
            if p == winner:
                continue

            lead_margin = s_in_own - s_in_opp
            if lead_margin <= 0:
                continue

            if p == last_pitcher:
                if lead_margin <= 3:
                    p.stats["saves"] += 1
            else:
                if lead_margin <= 3:
                    p.stats["holds"] += 1
