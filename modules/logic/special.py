"""
特殊能力による能力補正、および疲労度の蓄積・回復を担当するモジュール
"""

# --- 1. 補正値マッピングの定義 ---

# 野手用ランク補正 (ランク: (ミート補正, パワー補正))
BATTER_RANK_MAP = {
    "A": (15, 10),
    "B": (8, 5),
    "C": (5, 2),
    "D": (0, 0),
    "E": (-5, -2),
    "F": (-8, -5),
    "G": (-15, -10),
}

# 投手用ランク補正 (ランク: (球速, 制球, 変化球))
PITCHER_RANK_MAP = {
    "A": (2, 4, 4),
    "B": (1, 2, 2),
    "C": (1, 1, 0),
    "D": (0, 0, 0),
    "E": (-1, -1, 0),
    "F": (-1, -2, -2),
    "G": (-2, -4, -4),
}

# ノビ(fastball_life)補正
NOBI_MAP = {"A": 8, "B": 4, "C": 2, "D": 0, "E": -2, "F": -4, "G": -8}

# 回復・疲労用定数
RECOVERY_MAP = {"A": 40, "B": 35, "C": 30, "D": 25, "E": 20, "F": 15, "G": 10}
POS_FATIGUE_MAP = {
    "捕": 2.0,
    "遊": 1.7,
    "二": 1.5,
    "中": 1.2,
    "三": 1.1,
    "右": 1.0,
    "一": 1.0,
    "左": 0.8,
    "指": 0.6,
}


# --- 2. 特殊能力補正ロジック ---


def special_ability_b(pitcher, batter, is_risp):
    """
    打者の特殊能力（チャンス、対左）による能力補正値を計算する
    """
    meet_corr = 0
    power_corr = 0

    # 得点圏（チャンス）チェック
    if is_risp:
        m, p = BATTER_RANK_MAP.get(batter.clutch_b, (0, 0))
        meet_corr += m
        power_corr += p

    # 対左投手チェック
    if pitcher.throwing == "左":
        m, p = BATTER_RANK_MAP.get(batter.vs_left_b, (0, 0))
        meet_corr += m
        power_corr += p

    return meet_corr, power_corr


def special_ability_p(pitcher, batter, is_risp):
    """
    投手の特殊能力（ピンチ、対左、ノビ）による能力補正値を計算する
    """
    speed_corr = 0
    control_corr = 0
    breaking_ball_corr = 0

    # 得点圏（ピンチ）チェック
    if is_risp:
        s, c, b = PITCHER_RANK_MAP.get(pitcher.clutch_p, (0, 0, 0))
        speed_corr += s
        # control_corr += c # 元ロジックに合わせて微調整可
        breaking_ball_corr += b

    # 対左打者チェック
    if batter.batting == "左":
        # 対左ランク補正（投手専用）
        # 元コードは個別の値だったので、ここではマッピングから取得
        # ※必要に応じてPITCHER_RANK_MAPとは別の専用MAPを作ってもOK
        if pitcher.vs_left_p == "A":
            speed_corr += 3
            control_corr += 6
        elif pitcher.vs_left_p == "B":
            speed_corr += 2
            control_corr += 5
        elif pitcher.vs_left_p == "C":
            speed_corr += 1
            control_corr += 2
        elif pitcher.vs_left_p == "E":
            speed_corr -= 1
            control_corr -= 2
        elif pitcher.vs_left_p == "F":
            speed_corr -= 2
            control_corr -= 5
        elif pitcher.vs_left_p == "G":
            speed_corr -= 3
            control_corr -= 6

    # ノビチェック
    speed_corr += NOBI_MAP.get(pitcher.fastball_life, 0)

    return speed_corr, control_corr, breaking_ball_corr


# --- 3. 疲労度更新ロジック ---


def update_player_fatigue_p(
    pitchers_1, pitcher_records_1, pitchers_2, pitcher_records_2
):
    """
    試合終了後の投手疲労度（スタミナ減少・蓄積疲労）を更新する
    """
    for team_pitchers, records in [
        (pitchers_1, pitcher_records_1),
        (pitchers_2, pitcher_records_2),
    ]:
        # 実際に投げた投手のリスト
        played_pitchers = [r[0] for r in records]

        for p in team_pitchers:
            base_recover = RECOVERY_MAP.get(p.recovery, 15)

            if p in played_pitchers:
                # 試合に出た投手：打者数に応じて疲労
                pitch_load = p.stats.get("bf", 0) * 4
                p.fatigue_stamina += pitch_load
                p.accumulated_fatigue += (pitch_load * 0.2) - (base_recover * 0.01)
            else:
                # 試合に出ていない投手：回復
                p.fatigue_stamina = max(0, p.fatigue_stamina - base_recover)
                # 先発とリリーフで回復量に差
                recovery_weight = 0.2 if p.role == "先" else 0.02
                p.accumulated_fatigue -= base_recover * recovery_weight

            p.accumulated_fatigue = max(0, p.accumulated_fatigue)


def update_player_fatigue_b(batters_1, starters_batter_1, batters_2, starters_batter_2):
    """
    試合終了後の野手疲労度（蓄積疲労）を更新する
    """
    for team_batters, starters in [
        (batters_1, starters_batter_1),
        (batters_2, starters_batter_2),
    ]:
        # スタメンの選手とポジションの対応
        active_pos_map = {s[1]: s[0] for s in starters}  # {player_obj: position_str}

        for b in team_batters:
            base_recover = RECOVERY_MAP.get(b.recovery, 15)

            if b in active_pos_map:
                # 試合に出た野手：ポジションごとの負荷
                pos = active_pos_map[b]
                fatigue_weight = POS_FATIGUE_MAP.get(pos, 1.0)
                b.accumulated_fatigue += fatigue_weight - (base_recover * 0.01)
            else:
                # 試合に出なかった野手：回復
                b.accumulated_fatigue -= base_recover * 0.05

            b.accumulated_fatigue = max(0, b.accumulated_fatigue)
