import random

from modules.models import Batter, Pitcher

# --- 1. 並べ替え・計算用の補助関数 ---


def get_power(item):
    """並べ替え用の補助関数：パワーを返す"""
    return item[1].power


def get_speed(item):
    """並べ替え用の補助関数：走力を返す"""
    return item[1].speed


def get_total_hit_skill(item):
    """並べ替え用の補助関数：総合打力（ミート+パワー）を返す"""
    return item[1].meet + item[1].power


def get_meet(item):
    """並べ替え用の補助関数：ミートを返す"""
    return item[1].meet


def calculate_score(player: Batter, weight: int, is_fatigue_considered: bool) -> int:
    """
        選手の評価スコアを計算する

    Args:
        - player: 評価する選手のインスタンス
        - weight : ポジションの守備の重み
        - is_fatigue_considered : 疲労を考慮する True、考慮しない False

    Returns:
        - int: 選手の評価スコア
    """
    # 疲労によるデバフ係数の計算
    fatigue_debuff = player.accumulated_fatigue / 100.0

    if is_fatigue_considered == 1:
        # 疲労による能力低下の計算
        meet_corr = -(10 * fatigue_debuff)
        power_corr = -(10 * fatigue_debuff)
        speed_corr = -(10 * fatigue_debuff)
        fielding_corr = -(5 * fatigue_debuff)
    else:
        meet_corr = 0
        power_corr = 0
        speed_corr = 0
        fielding_corr = 0

    # デバフ後の能力でスコアを計算
    batting_score = (
        player.trajectory * 10
        + (player.meet + meet_corr + player.power + power_corr) * 2
        + (player.speed + speed_corr)
    )
    fielding_score = (player.arm + player.catching + fielding_corr) * weight

    return batting_score + fielding_score


def decide_team(
    game_number: int, team_list: list[str], total_games_team: int
) -> tuple[str, str]:
    """
        対戦カードを決定

    Args:
        - game_number : 試合数
        - team_list : チームのリスト
        - total_games_team : 全試合数

    Returns:
        - tuple[str, str]: 対戦する2つのチーム名のタプル
            - team_name_1: 基準となるチーム名
            - team_name_2: 対戦相手として選択されたチーム名
    """
    team_number = len(team_list)
    num_opponents = team_number - 1

    idx = game_number - 1

    # 1チームあたりの消化試合数(total_games_team)ごとteam_1を固定
    team_1_idx = (idx // total_games_team) % team_number
    team_name_1 = team_list[team_1_idx]

    # team_1以外の5チームから対戦相手を選択
    other_team_list = [team for team in team_list if team != team_name_1]

    # team_2を決定
    team_2_idx = idx % num_opponents
    team_name_2 = other_team_list[team_2_idx]

    return team_name_1, team_name_2


def decide_batter(batters: list[Batter], is_fatigue_considered: bool) -> list[Batter]:
    """
        攻守の総合力に基づいて各ポジションのレギュラーを選出する

    Args:
        - batters : チームに所属する Batter のリスト
        - is_fatigue_considered : 疲労を考慮する True、考慮しない False

    Returns:
        - list[Batter]: スタメンに選ばれた Batter のリスト
    """
    # 守備を重視する重み
    position_weights = {
        "捕": 1.0,
        "遊": 0.9,
        "二": 0.9,
        "中": 0.6,
        "三": 0.4,
        "右": 0.3,
        "左": 0.1,
        "一": 0.1,
    }

    selected_players = []
    candidates = batters[:]

    # 各ポジションの選出
    for position in position_weights.keys():
        position_weight = position_weights[position]
        position_candidates = []

        # そのポジションの選手をリストアップ
        for player in candidates:
            if player.position == position:
                position_candidates.append(player)

        # 一番スコアが高い選手を探す
        max_score = 0
        for player in position_candidates:
            current_score = calculate_score(
                player, position_weight, is_fatigue_considered
            )
            if current_score > max_score:
                max_score = current_score
                best_player = player

        selected_players.append((position, best_player))
        candidates.remove(best_player)

    # 指名打者(指)の選出
    # DHは守備関係ないので position_weight=0 で計算
    max_dh_score = 0
    for player in candidates:
        current_dh_score = calculate_score(player, 0, is_fatigue_considered)
        if current_dh_score > max_dh_score:
            max_dh_score = current_dh_score
            dh_player = player

    selected_players.append(("指", dh_player))

    return selected_players


def decide_order(starters: list[Batter]) -> list[Batter]:
    """
        スタメン Batter のリストをもとに打順を決める

    Args:
        - starters : スタメン Batter のリスト

    Returns:
        - list[Batter] : 打順組み換え後の Batter のリスト
    """
    working_list = starters[:]
    lineup = [None] * 9

    # 総合打力が高い「上位打線候補」7人を選び出す
    working_list.sort(key=get_total_hit_skill, reverse=True)
    top_candidates = working_list[:6]
    bottom_candidates = working_list[6:]

    # 上位打線(1~4番)を top_candidates から決める
    # 4番：上位候補の中で最強のパワー
    top_candidates.sort(key=get_power, reverse=True)
    lineup[3] = top_candidates.pop(0)

    # 1番：上位候補の中で最強の走力
    top_candidates.sort(key=get_speed, reverse=True)
    lineup[0] = top_candidates.pop(0)

    # 3番：上位候補の中で総合打力が高い人
    top_candidates.sort(key=get_total_hit_skill, reverse=True)
    lineup[2] = top_candidates.pop(0)

    # 2番：上位候補の中でミートが高い人
    top_candidates.sort(key=get_meet, reverse=True)
    lineup[1] = top_candidates.pop(0)

    # 残りの打順(5~9番)を決める
    # 5, 6：top_candidates の残りと bottom_candidates を合流させてパワー順
    remaining_players = top_candidates + bottom_candidates
    remaining_players.sort(key=get_power, reverse=True)
    lineup[4] = remaining_players.pop(0)
    lineup[5] = remaining_players.pop(0)

    # 7, 8, 9番：残りをミート順
    remaining_players.sort(key=get_meet, reverse=True)
    lineup[8] = remaining_players.pop(0)
    lineup[6] = remaining_players.pop(0)
    lineup[7] = remaining_players.pop(0)

    return lineup


def decide_pitcher(pitchers: list[Pitcher], game_number: int) -> Pitcher:
    """
    試合番号と投手の状態に基づいて、その試合の先発投手を決定する。

    Args:
        - pitchers : チームに所属する全投手のリスト。
        - game_number : シーズン内の通算試合番号（1から開始）。

    Returns:
        - Pitcher : 決定した投手オブジェクト
    """
    # 先発適性を持つ投手を抽出
    starters = [pitcher for pitcher in pitchers if pitcher.role == "先"]
    num_starters = len(starters)

    # 本来のローテーション開始位置
    start_idx = (game_number - 1) % num_starters

    # スタミナチェック（本来の番から順に最大1周分確認）
    for i in range(num_starters):
        current_idx = (start_idx + i) % num_starters
        candidate = starters[current_idx]

        # スタミナが70%より多ければ採用
        if candidate.fatigue_stamina < (candidate.stamina * 0.70):
            return candidate

    # 全員疲れていた場合の予備（本来の番の人を返す）
    return starters[start_idx]


def decide_relief(
    pitchers: list[Pitcher],
    already_played_records: list[list],
    inning: int,
    score_diff: int,
) -> Pitcher:
    """
    役割に応じたリリーフを選出する。

    Args:
        - pitchers : チームに所属する全投手のリスト。
        - already_played_records : すでに登板済みの投手の記録リスト
        - inning : イニング
        - score_diff : 点差

    Returns:
        - Pitcher : 決定した投手オブジェクト
    """
    already_played_list = [
        played_pitcher[0] for played_pitcher in already_played_records
    ]

    if inning >= 9 and 0 < score_diff <= 3:
        role_target = ["抑"]
    elif inning >= 7 and 0 < score_diff <= 3:
        role_target = ["セ", "継"]
    elif score_diff >= 0:
        role_target = ["継", "セ"]
    else:
        role_target = ["継"]

    # フィルタリング条件：減少体力が一定以下
    candidates = [
        pitcher
        for pitcher in pitchers
        if pitcher not in already_played_list
        and pitcher.role in role_target
        and pitcher.fatigue_stamina < (pitcher.stamina * 0.25)
    ]

    # もし条件に合う選手が誰もいない場合は、全リリーフから選出
    if not candidates:
        candidates = [
            pitcher
            for pitcher in pitchers
            if pitcher not in already_played_list and pitcher.role != "先"
        ]

    # 疲労（fatigue_stamina）が最も小さい選手を1人選出
    return min(candidates, key=lambda x: x.fatigue_stamina)
