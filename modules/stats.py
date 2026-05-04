from modules.models import Batter, Pitcher


def get_batter_stats(player: Batter) -> str:
    """
    打率、本塁打、打点、出塁率、OPSを計算して文字列で返す

    Args:
        - player : Batter のインスタンス

    Returns:
        - str : 表示する文字列
    """
    stats = player.stats
    games = stats.get("games", 0)
    hits = stats.get("hits", 0)
    ab = stats.get("ab", 0)
    hr = stats.get("hr", 0)
    rbi = stats.get("rbi", 0)

    single = stats.get("singles", 0)
    double = stats.get("doubles", 0)
    triple = stats.get("triples", 0)
    bb = stats.get("walks", 0)
    hbp = stats.get("hbp", 0)
    sf = stats.get("sf", 0)

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


def get_pitcher_stats(pitcher: Pitcher):
    """
    防御率などを計算して文字列で返す

    Args:
        - pitcher : Pitcher のインスタンス

    Returns:
        - str : 表示する文字列
    """
    stats = pitcher.stats
    games = stats.get("games", 0)
    wins = stats.get("wins", 0)
    losses = stats.get("losses", 0)
    saves = stats.get("saves", 0)
    holds = stats.get("holds", 0)
    er = stats.get("自責点", 0)

    # アウト数の計算 (bf - 被安打 - 与四死球)
    bf = stats.get("bf", 0)
    h = stats.get("hits_allowed", 0)
    bb = stats.get("walks_allowed", 0)
    hbp = stats.get("hbp_allowed", 0)

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


def judge_risp(game_condition: list[int]) -> bool:
    """
    得点圏（2塁または3塁）にランナーがいるか判定
    game_condition: [b1, b2, b3, outs, score]
    """
    return game_condition[1] == 1 or game_condition[2] == 1


def update_stats_batter(
    pitcher: Pitcher, batter: Batter, result: str, risp: bool, rbi: int
) -> None:
    """
    判定結果に基づいて野手のstats辞書を更新する

    Args:
        - pitcher : Pitcher のインスタンス
        - batter : Batter のインスタンス
        - result : 打席結果
        - risp : 得点圏 True、非得点圏 False
        - rbi : 打点

    Returns:
        - None
    """
    stats = batter.stats

    stats["pa"] += 1
    stats["rbi"] += rbi

    # 得点圏打数の判定
    if risp and result not in ["BB", "HBP"]:
        stats["risp_ab"] += 1

    # 結果別の分岐
    if result in ["1B", "2B", "3B", "HR"]:
        stats["hits"] += 1
        if result == "1B":
            stats["singles"] += 1
        elif result == "2B":
            stats["doubles"] += 1
        elif result == "3B":
            stats["triples"] += 1
        elif result == "HR":
            stats["hr"] += 1

        if risp:
            stats["risp_hits"] += 1

    elif result == "BB":
        stats["walks"] += 1
    elif result == "HBP":
        stats["hbp"] += 1
    elif result == "SO":
        stats["so"] += 1

    # 打数(ab) = 打席(pa) - (四球 + 死球 + 犠飛)
    stats["ab"] = stats["pa"] - (stats["walks"] + stats["hbp"] + stats.get("sf", 0))


def update_stats_pitcher(
    pitcher: Pitcher, batter: Batter, result: str, risp: bool, rbi: int
) -> None:
    """
    判定結果に基づいて投手のstats辞書を更新する

    Args:
        - pitcher : Pitcher のインスタンス
        - batter : Batter のインスタンス
        - result : 打席結果
        - risp : 得点圏 True、非得点圏 False
        - rbi : 打点

    Returns:
        - None
    """
    stats = pitcher.stats

    stats["bf"] += 1
    stats["失点"] += rbi
    stats["自責点"] += rbi

    if risp:
        stats["risp_bf"] += 1

    if result in ["1B", "2B", "3B", "HR"]:
        stats["hits_allowed"] += 1
        if result == "HR":
            stats["hr_allowed"] += 1
        if risp:
            stats["risp_hits_allowed"] += 1

    elif result == "BB":
        stats["walks_allowed"] += 1
    elif result == "HBP":
        stats["hbp_allowed"] += 1
    elif result == "SO":
        stats["strikeouts"] += 1
        stats["outs_pitched"] += 1
    elif result == "OUT":
        stats["outs_pitched"] += 1


def assign_win_loss(
    records_1: list[list], records_2: list[list], score_1: int, score_2: int
) -> None:
    """

    勝利・敗戦・セーブ・ホールドの割り当て、成績更新処理

    Args:
        - records_1 : Team1 の登板投手の記録リスト
        - records_2 : Team2 の登板投手の記録リスト
        - score_1 : Team1 の得点
        - score_2 : Team2 の得点

    Returns:
        - None
    """
    if score_1 == score_2:
        return

    is_team1_win = score_1 > score_2
    win_recs = records_1 if is_team1_win else records_2
    loss_recs = records_2 if is_team1_win else records_1
    final_win_score = score_1 if is_team1_win else score_2
    final_loss_score = score_2 if is_team1_win else score_1

    # 敗戦投手の決定 (責任消滅ロジックを追加)
    loser = None
    for i, rec in enumerate(loss_recs):
        p, s_in, s_opp_in = rec
        s_out = loss_recs[i + 1][1] if i + 1 < len(loss_recs) else final_loss_score
        s_opp_out = loss_recs[i + 1][2] if i + 1 < len(loss_recs) else final_win_score

        # もし自分のイニング終了時に「同点以上」なら、これまでの負け責任はリセット
        if s_out >= s_opp_out:
            loser = None
        # もし負けている状態でマウンドを降り、かつ既に loser が決まっていないなら責任を負う
        elif s_out < s_opp_out and loser is None:
            loser = p

    loser.stats["losses"] += 1

    # 勝利投手の決定
    winner = None
    starter_rec = win_recs[0]
    starter_p = starter_rec[0]

    # 先発の降板時スコアを取得
    st_out = win_recs[1][1] if len(win_recs) > 1 else final_win_score
    st_opp_out = win_recs[1][2] if len(win_recs) > 1 else final_loss_score

    # 先発勝利の条件: 5回(15個のアウト)以上投げ、降板時にリード、そのまま逆転されずに勝利
    if starter_p.stats.get("outs_pitched", 0) >= 15 and st_out > st_opp_out:
        winner = starter_p
    else:
        # 先発に権利がない場合、勝ち越した瞬間に投げていた投手を勝者とする
        for i, rec in enumerate(win_recs):
            p, s_in, s_opp_in = rec
            s_out = win_recs[i + 1][1] if i + 1 < len(win_recs) else final_win_score
            s_opp_out = (
                win_recs[i + 1][2] if i + 1 < len(win_recs) else final_loss_score
            )

            if s_out > s_opp_out:
                winner = p
                break

    # 万が一 winner が特定できない（ずっとリードしていたが先発が5回未満など）場合は2番手
    if not winner:
        winner = win_recs[1][0] if len(win_recs) > 1 else starter_p

    winner.stats["wins"] += 1

    # セーブ・ホールドの決定
    if len(win_recs) > 1:
        last_pitcher = win_recs[-1][0]

        for i, rec in enumerate(win_recs):
            p, s_in, s_opp_in = rec
            if p == winner:
                continue

            # 降板時スコア
            s_out = win_recs[i + 1][1] if i + 1 < len(win_recs) else final_win_score
            s_opp_out = (
                win_recs[i + 1][2] if i + 1 < len(win_recs) else final_loss_score
            )

            # 条件A: リードした場面で登板したか（3点差以内、あるいはランナー状況によるが簡易的に3点差）
            lead_at_in = s_in - s_opp_in
            # 条件B: リードを保って降りたか
            is_lead_maintained = s_out > s_opp_out

            if is_lead_maintained and 0 < lead_at_in <= 3:
                if p == last_pitcher:
                    # 最後の投手がリードを守ればセーブ
                    p.stats["saves"] += 1
                else:
                    # 途中の投手がリードを守ればホールド
                    p.stats["holds"] += 1
