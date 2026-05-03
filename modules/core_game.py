import random
from modules import stats
from modules import selectors
from modules import database
from modules import display
from modules.logic import physics, game_rules, special


def logic(pitcher, batter, game_condition, is_risp):
    """打席の結果判定と成績更新"""
    speed_sa, control_sa, breaking_sa = special.special_ability_p(
        pitcher, batter, is_risp
    )

    k_p = pitcher.accumulated_fatigue / 100.0
    speed_p = pitcher.speed + speed_sa + (-3 * k_p)
    control = pitcher.control + control_sa + (-10 * k_p)
    breaking_ball = pitcher.breaking_ball + breaking_sa + (-1.5 * k_p)

    meet_sa, power_sa = special.special_ability_b(pitcher, batter, is_risp)
    meet_p, power_p = physics.pitcher_ability(speed_p, control, breaking_ball)

    k_b = batter.accumulated_fatigue / 100.0
    trajectory = batter.trajectory
    meet = batter.meet + meet_p + meet_sa + (-5 * k_b)
    power = batter.power + power_p + power_sa + (-5 * k_b)
    speed_b = batter.speed + (-5 * k_b)
    eye = batter.eye

    result = game_rules.result_logic(
        trajectory, meet, power, speed_b, eye, speed_p, control, breaking_ball
    )

    old_score = game_condition[4]
    game_condition = game_rules.base_advancement_logic(result, game_condition)
    rbi = game_condition[4] - old_score

    stats.update_stats_b(pitcher, batter, result, is_risp, rbi)
    stats.update_stats_p(pitcher, batter, result, is_risp, rbi)

    return game_condition


def run_at_bat(pitcher, batter, game_condition):
    """1打席の実行フロー"""
    risp = stats.judge_risp(game_condition)
    game_condition = logic(pitcher, batter, game_condition, risp)
    return game_condition


def game(file_path, game_number, teams, total_games_team):
    """1試合の実行（イニング進行・選手交代・事後処理）"""

    # 1. 前準備（チーム決定・データ取得）
    team_name_1, team_name_2 = selectors.decide_team(
        game_number, teams, total_games_team
    )
    pitchers_1, batters_1 = database.Aquire_data(file_path, team_name_1)
    pitchers_2, batters_2 = database.Aquire_data(file_path, team_name_2)

    is_fatigue_considered = True
    starters_batter_1 = selectors.decide_order(
        selectors.decide_batter(batters_1, is_fatigue_considered)
    )
    starters_batter_2 = selectors.decide_order(
        selectors.decide_batter(batters_2, is_fatigue_considered)
    )

    active_p1 = selectors.decide_pitcher(pitchers_1, game_number)[1]
    active_p2 = selectors.decide_pitcher(pitchers_2, game_number)[1]

    # --- 2. スタメン表示（成績リセット前に行う） ---
    # ここで stats.get_..._stats を使い、辞書を適切な表示文字列に変換してから display に渡します
    display.display_starter_b(
        starters_batter_1, [stats.get_batter_stats(s[1]) for s in starters_batter_1]
    )
    display.display_starter_p(("先発", active_p1), stats.get_pitcher_stats(active_p1))

    display.display_starter_b(
        starters_batter_2, [stats.get_batter_stats(s[1]) for s in starters_batter_2]
    )
    display.display_starter_p(("先発", active_p2), stats.get_pitcher_stats(active_p2))

    # --- 3. 今日の試合の集計準備（成績リセット） ---
    # 表示が終わったので、全選手の stats を 0 にして今日の分だけをカウントするようにします
    for player in pitchers_1 + pitchers_2 + batters_1 + batters_2:
        player.stats = {key: 0 for key in player.stats}

    # 今日の試合の出場登録
    for b in [s[1] for s in starters_batter_1 + starters_batter_2]:
        b.stats["games"] += 1
    for p in [active_p1, active_p2]:
        p.stats["games"] += 1
        p.stats["starts"] += 1

    # 4. 試合変数初期化
    current_stamina_1 = (active_p1.stamina - active_p1.fatigue_stamina) * 1.5
    current_stamina_2 = (active_p2.stamina - active_p2.fatigue_stamina) * 1.5
    p_records_1 = [[active_p1, 0, 0]]
    p_records_2 = [[active_p2, 0, 0]]

    # 5. 試合本編
    inning = 1
    top_bottom = 0  # 0:表, 1:裏
    b_num_1, b_num_2 = 1, 1
    scores_1, scores_2 = [], []
    game_cond = [0, 0, 0, 0, 0]  # [b1, b2, b3, outs, score]

    while inning <= 9:
        diff = sum(scores_1) - sum(scores_2)

        if top_bottom == 0:  # 表（攻撃：Team 2 / 守備：Team 1）
            if current_stamina_1 <= 0:
                active_p1 = selectors.decide_relief(
                    pitchers_1, p_records_1, inning, diff
                )
                active_p1.stats = {
                    k: 0 for k in active_p1.stats
                }  # リリーフの当日成績をリセット
                active_p1.stats["games"] += 1
                current_stamina_1 = (
                    active_p1.stamina - active_p1.fatigue_stamina
                ) * 0.2
                p_records_1.append([active_p1, sum(scores_1), sum(scores_2)])

            while True:
                batter = starters_batter_2[(b_num_2 - 1) % 9][1]
                game_cond = run_at_bat(active_p1, batter, game_cond)
                current_stamina_1 -= random.randint(1, 7)
                b_num_2 += 1
                if game_cond[3] == 3:
                    scores_2.append(game_cond[4])
                    top_bottom = 1
                    game_cond = [0, 0, 0, 0, 0]
                    break
        else:  # 裏（攻撃：Team 1 / 守備：Team 2）
            if current_stamina_2 <= 0:
                active_p2 = selectors.decide_relief(
                    pitchers_2, p_records_2, inning, -diff
                )
                active_p2.stats = {k: 0 for k in active_p2.stats}
                active_p2.stats["games"] += 1
                current_stamina_2 = (
                    active_p2.stamina - active_p2.fatigue_stamina
                ) * 0.2
                p_records_2.append([active_p2, sum(scores_2), sum(scores_1)])

            while True:
                batter = starters_batter_1[(b_num_1 - 1) % 9][1]
                game_cond = run_at_bat(active_p2, batter, game_cond)
                current_stamina_2 -= random.randint(1, 7)
                b_num_1 += 1
                if game_cond[3] == 3:
                    scores_1.append(game_cond[4])
                    top_bottom = 0
                    game_cond = [0, 0, 0, 0, 0]
                    inning += 1
                    break

    # 6. 事後処理
    total_1, total_2 = sum(scores_1), sum(scores_2)
    print(f"試合終了: {team_name_1} {total_1} - {total_2} {team_name_2}\n")

    stats.assign_win_loss(p_records_1, p_records_2, total_1, total_2)

    # QS/完投判定
    for rec in [p_records_1[0], p_records_2[0]]:
        p = rec[0]
        outs = p.stats.get("outs_pitched", 0)
        er = p.stats.get("自責点", 0)
        if outs >= 18 and er <= 3:
            p.stats["qs"] += 1
        if outs >= 27:
            p.stats["complete_games"] += 1

    # 疲労度更新
    special.update_player_fatigue_p(pitchers_1, p_records_1, pitchers_2, p_records_2)
    special.update_player_fatigue_b(
        batters_1, starters_batter_1, batters_2, starters_batter_2
    )

    # 保存処理（今日の成績 all_players 分を Excel に加算）
    all_players = list(
        set(
            [s[1] for s in starters_batter_1 + starters_batter_2]
            + pitchers_1
            + pitchers_2
        )
    )
    database.output_exam(file_path, team_name_1, team_name_2, all_players)
