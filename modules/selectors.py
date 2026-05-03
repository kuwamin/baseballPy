import random

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


def calculate_score(player, weight, is_fatigue_considered):
    """
    選手の蓄積疲労を考慮した実効評価スコアを計算する
    """
    # デバフ係数の計算 (RunAtBatと同様の基準)
    k = player.accumulated_fatigue / 100.0

    if is_fatigue_considered == 1:
        # 疲労による能力低下の計算
        meet_corr = -(10 * k)
        power_corr = -(10 * k)
        speed_corr = -(10 * k)
        fielding_corr = -(5 * k)
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


# --- 2. チーム・選手選出メイン関数 ---


def decide_team(game_number, teams, total_games_team):
    """
    対戦カードを決定
    """
    num_teams = len(teams)
    num_opponents = num_teams - 1

    idx = game_number - 1

    # 1チームあたりの消化試合数(total_games_team)ごとteam_1を固定
    team_1_idx = (idx // total_games_team) % num_teams
    team_name_1 = teams[team_1_idx]

    # team_1以外の5チームから対戦相手を選択
    other_teams = [t for t in teams if t != team_name_1]

    # team_2を決定
    team_2_idx = idx % num_opponents
    team_name_2 = other_teams[team_2_idx]

    return team_name_1, team_name_2


def decide_batter(batters, is_fatigue_considered):
    """
    攻守の総合力に基づいて各ポジションのレギュラーを選出する
    """
    # 守備を重視する重み
    pos_weights = {
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
        max_score = calculate_score(best_player, weight, is_fatigue_considered)

        for p in pos_candidates:
            current_score = calculate_score(p, weight, is_fatigue_considered)
            if current_score > max_score:
                max_score = current_score
                best_player = p

        selected_players.append((pos, best_player))
        candidates.remove(best_player)

    # 2. 指名打者(指)の選出
    if candidates:
        dh_player = candidates[0]
        # DHは守備関係ないので weight=0 で計算
        max_dh_score = calculate_score(dh_player, 0, is_fatigue_considered)

        for p in candidates:
            current_dh_score = calculate_score(p, 0, is_fatigue_considered)
            if current_dh_score > max_dh_score:
                max_dh_score = current_dh_score
                dh_player = p

        selected_players.append(("指", dh_player))

    return selected_players


def decide_order(starters):
    """
    上位7人を「打力のある選手」として選抜し、その中で1〜4番を決定する
    """
    # starters は [(pos, player), ...] のリスト
    working_list = starters[:]
    lineup = [None] * 9

    # 1. まず、総合打力が高い「上位打線候補」7人を選び出す
    # 総合打力（ミート+パワー）で降順（大きい順）に並べ替え
    working_list.sort(key=get_total_hit_skill, reverse=True)

    # 上位7人と、それ以外（下位候補2人）に分ける
    top_candidates = working_list[:6]
    bottom_candidates = working_list[6:]

    # --- 上位打線(1~4番)を top_candidates から決める ---

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

    # --- 残りの打順(5~9番)を決める ---

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


def decide_pitcher(pitchers, game_number):
    """
    先発投手を選出する
    """
    # 1. 先発適性を持つ投手を抽出
    starters_list = [p for p in pitchers if p.role == "先"]

    # 2. 本来のローテーション順を特定
    rotation_index = (game_number - 1) % len(starters_list)
    p = starters_list[rotation_index]

    # 減少体力のチェック
    check_count = 0
    while p.fatigue_stamina > (p.stamina * 0.3) and check_count < len(starters_list):
        rotation_index = (rotation_index + 1) % len(starters_list)
        p = starters_list[rotation_index]
        check_count += 1

    return ("先発", p)


def decide_relief(pitchers, already_played_records, inning, score_diff):
    """
    役割に応じたリリーフ選出
    """
    already_played = [r[0] for r in already_played_records]

    if inning >= 9 and 0 < score_diff <= 3:
        role_target = ["抑"]
    elif inning >= 7 and 0 < score_diff <= 3:
        role_target = ["セ", "継"]
    elif score_diff >= 0:
        role_target = ["継", "セ"]
    else:
        role_target = ["継"]

    # フィルタリング条件：減少体力が一定以下（例: 最大スタミナの半分以下）
    candidates = [
        p
        for p in pitchers
        if p not in already_played
        and p.role in role_target
        and p.fatigue_stamina < (p.stamina * 0.5)
    ]

    # もし条件に合う選手が誰もいない場合は、全リリーフから選出
    if not candidates:
        candidates = [p for p in pitchers if p not in already_played and p.role != "先"]

    # 疲労が少ない（fatigue_staminaが低い）順にソートして上位から選ぶ
    pool = sorted(candidates, key=lambda x: x.fatigue_stamina)[:3]
    return random.choice(pool)
