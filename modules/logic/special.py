from modules.models import Batter, Pitcher

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

# 対ピンチ補正 (ランク: (球速, 制球, 変化球))
PITCHER_RISP_MAP = {
    "A": (2, 0, 4),
    "B": (1, 0, 2),
    "C": (1, 0, 0),
    "D": (0, 0, 0),
    "E": (-1, 0, 0),
    "F": (-1, 0, -2),
    "G": (-2, 0, -4),
}

# 対左打者補正 (ランク: (球速, 制球, 変化球))
PITCHER_LEFT_MAP = {
    "A": (6, 12, 0),
    "B": (4, 10, 0),
    "C": (2, 4, 0),
    "D": (0, 0, 0),
    "E": (-2, 4, 0),
    "F": (-4, -10, -2),
    "G": (-6, -12, -4),
}

# ノビ(fastball_life)補正
PITCHER_NOBI_MAP = {"A": 8, "B": 4, "C": 2, "D": 0, "E": -2, "F": -4, "G": -8}

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


def special_ability_batter(
    pitcher: Pitcher, batter: Batter, is_risp: bool
) -> tuple[int, int]:
    """
        打者の特殊能力（チャンス、対左）による能力補正値を計算する

    Args:
        - pitcher : Pitcher インスタンス
        - batter : Batter インスタンス
        - is_risp : 得点圏 True、非得点圏 False

    Returns:
        - tuple[int, int]: 以下の順に格納された補正値のタプル
            - meet_corr : ミート補正
            - power_corr : パワー補正
    """
    meet_corr = 0
    power_corr = 0

    # 得点圏チェック
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


def special_ability_pitcher(
    pitcher: Pitcher, batter: Batter, is_risp: bool
) -> tuple[int, int, int]:
    """
        投手の特殊能力（ピンチ、対左、ノビ）による能力補正値を計算する

    Args:
        - pitcher : Pitcher インスタンス
        - batter : Batter インスタンス
        - is_risp : 得点圏 True、非得点圏 False

    Returns:
        - tuple[int, int, int]: 以下の順に格納された補正値のタプル
            - speed_corr (int): 球速補正
            - control_corr (int): コントロール補正
            - breaking_ball_corr (int): 変化球変化量補正
    """
    speed_corr = 0
    control_corr = 0
    breaking_ball_corr = 0

    # 得点圏チェック
    if is_risp:
        s, c, b = PITCHER_RISP_MAP.get(pitcher.clutch_p)
        speed_corr += s
        control_corr += c
        breaking_ball_corr += b

    # 対左打者チェック
    if batter.batting == "左":
        s, c, b = PITCHER_LEFT_MAP.get(pitcher.clutch_p)
        speed_corr += s
        control_corr += c
        breaking_ball_corr += b

    # ノビチェック
    speed_corr += PITCHER_NOBI_MAP.get(pitcher.fastball_life)

    return speed_corr, control_corr, breaking_ball_corr


def update_player_fatigue_pitcher(
    pitchers_1: list[Pitcher],
    pitcher_records_1: list[list],
    pitchers_2: list[Pitcher],
    pitcher_records_2: list[list],
) -> None:
    """

    試合終了後の投手疲労度（スタミナ減少・蓄積疲労）を更新する

    Args:
        - pitchers_1 : Team1 の Pitcher インスタンスリスト
        - pitcher_records_1 : Team1 の登板投手の記録リスト
        - pitchers_2 : Team2 の Pitcher インスタンスリスト
        - pitcher_records_2 : Team2 の登板投手の記録リスト

    Returns:
        - None
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


def update_player_fatigue_batter(
    batters_1: list[Batter],
    starters_batter_1: list[Batter],
    batters_2: list[Batter],
    starters_batter_2: list[Batter],
) -> None:
    """

    試合終了後の野手疲労度（蓄積疲労）を更新する

    Args:
        - batters_1 : Team1 の Batter インスタンスリスト
        - starters_batter_1 : Team1 の スタメンの Batter インスタンスリスト
        - batters_2 : Team2 の Batter インスタンスリスト
        - starters_batter_2 : Team2 の スタメンの Batter インスタンスリスト

    Returns:
        - None
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
