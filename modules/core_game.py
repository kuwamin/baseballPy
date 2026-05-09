import random
from modules import stats
from modules import selectors
from modules import database
from modules import display
from modules.logic import physics, game_rules, special
from modules.models import Batter, Pitcher


def logic(
    pitcher: Pitcher, batter: Batter, game_condition: list[int], is_risp: bool
) -> list[int]:
    """
        打席の結果判定と成績更新処理

    Args:
        - pitcher : Pitcher インスタンス
        - batter : Batter インスタンス
        - game_condition : 試合状況のリスト
        - is_risp : 得点圏 True、非得点圏 False

    Returns:
        - list[int] : 更新された試合状況のリスト
    """
    # 投手の特殊能力による補正
    (
        speed_special_corr,
        control_special_corr,
        breaking_special_corr,
    ) = special.special_ability_pitcher(pitcher, batter, is_risp)

    # 投手の調子による補正
    speed_condition_corr, control_condition_corr, breaking_ball_condition_corr = (
        physics.pitcher_condition_correction(pitcher.condition)
    )

    # 投手の疲労による補正
    # TODO:責務を分けるようにリファクタリング
    fatigue_debuff_pitcher = pitcher.accumulated_fatigue / 100.0
    speed_p = (
        pitcher.speed
        + speed_special_corr
        + speed_condition_corr
        + (-3 * fatigue_debuff_pitcher)
    )
    control = (
        pitcher.control
        + control_special_corr
        + control_condition_corr
        + (-10 * fatigue_debuff_pitcher)
    )
    breaking_ball = (
        pitcher.breaking_ball
        + breaking_special_corr
        + breaking_ball_condition_corr
        + (-1.5 * fatigue_debuff_pitcher)
    )

    # 野手の特殊能力による補正
    meet_special_corr, power_special_corr = special.special_ability_batter(
        pitcher, batter, is_risp
    )

    # 野手の調子による補正
    meet_condition_corr, power_condition_corr = physics.batter_condition_correction(
        batter.condition
    )

    # 投手の基礎能力による補正
    meet_pitcher_corr, power_pitcher_corr = physics.pitcher_ability_correction(
        speed_p, control, breaking_ball
    )

    # 野手の疲労による補正
    # TODO:責務を分けるようにリファクタリング
    fatigue_debuff_batter = batter.accumulated_fatigue / 100.0
    trajectory = batter.trajectory
    meet = (
        batter.meet
        + meet_pitcher_corr
        + meet_condition_corr
        + meet_special_corr
        + (-5 * fatigue_debuff_batter)
    )
    power = (
        batter.power
        + power_pitcher_corr
        + power_condition_corr
        + power_special_corr
        + (-5 * fatigue_debuff_batter)
    )
    speed_b = batter.speed + (-5 * fatigue_debuff_batter)
    eye = batter.eye

    result = game_rules.result_logic(
        trajectory, meet, power, speed_b, eye, speed_p, control, breaking_ball
    )

    old_score = game_condition[4]
    game_condition = game_rules.base_advancement_logic(result, game_condition)
    rbi = game_condition[4] - old_score

    stats.update_stats_batter(pitcher, batter, result, is_risp, rbi)
    stats.update_stats_pitcher(pitcher, batter, result, is_risp, rbi)

    return game_condition


def run_at_bat(
    pitcher: Pitcher, batter: Batter, game_condition: list[int]
) -> list[int]:
    """
        1打席の実行処理

    Args:
        - pitcher : Pitcher インスタンス
        - batter : Batter インスタンス
        - game_condition : 試合状況のリスト

    Returns:
        - list[int] : 更新された試合状況のリスト
    """
    is_risp = stats.judge_risp(game_condition)
    game_condition = logic(pitcher, batter, game_condition, is_risp)
    return game_condition


def game(
    file_path: str, game_number: int, team_list: list[str], total_games_team: int
) -> None:
    """
        1試合の実行（イニング進行・選手交代・事後処理）

    Args:
        - file_path : 読み込み対象となるExcelファイルのパス
        - game_number : 試合数
        - team_list : チームのリスト
        - total_games_team : 全試合数

    Returns:
        - None
    """
    # 前準備（チーム決定・データ取得）
    team_name_1, team_name_2 = selectors.decide_team(
        game_number, team_list, total_games_team
    )
    pitchers_1, batters_1 = database.Aquire_data(file_path, team_name_1)
    pitchers_2, batters_2 = database.Aquire_data(file_path, team_name_2)

    is_fatigue_considered = True
    selected_batters_1 = selectors.decide_batter(batters_1, is_fatigue_considered)
    starters_batters_1 = selectors.decide_order(selected_batters_1)
    selected_batters_2 = selectors.decide_batter(batters_2, is_fatigue_considered)
    starters_batters_2 = selectors.decide_order(selected_batters_2)

    active_pitcher_1 = selectors.decide_pitcher(pitchers_1, game_number)
    active_pitcher_2 = selectors.decide_pitcher(pitchers_2, game_number)

    # スタメン表示
    display.display_starter_batter(starters_batters_1)
    display.display_starter_pitcher(("先発", active_pitcher_1))

    display.display_starter_batter(starters_batters_2)
    display.display_starter_pitcher(("先発", active_pitcher_2))

    # 今日の試合の集計準備（成績リセット）
    for player in pitchers_1 + pitchers_2 + batters_1 + batters_2:
        player.stats = {key: 0 for key in player.stats}

    # 今日の試合の出場選手の試合数を更新
    # 両チームを1つのタプル（またはリスト）にまとめてループ
    for team_starters in [starters_batters_1, starters_batters_2]:
        for _, player in team_starters:
            player.stats["games"] += 1
    for p in [active_pitcher_1, active_pitcher_2]:
        p.stats["games"] += 1
        p.stats["starts"] += 1

    # 試合変数初期化
    current_stamina_1 = (
        active_pitcher_1.stamina - active_pitcher_1.fatigue_stamina
    ) * 1.5
    current_stamina_2 = (
        active_pitcher_2.stamina - active_pitcher_2.fatigue_stamina
    ) * 1.5
    # [投手のインスタンス, 登板時のTeam1の得点, Team2の得点]
    pitcher_records_1 = [[active_pitcher_1, 0, 0]]
    pitcher_records_2 = [[active_pitcher_2, 0, 0]]

    # 試合本編
    inning = 1
    top_bottom = 0  # 0:表, 1:裏
    b_num_1, b_num_2 = 1, 1
    scores_1, scores_2 = [], []
    game_condition = [0, 0, 0, 0, 0]  # [b1, b2, b3, outs, score]

    while inning <= 9:

        if top_bottom == 0:  # 表（攻撃：Team 2 / 守備：Team 1）
            diff = sum(scores_1) - sum(scores_2)
            # イニングの先頭で投手交代するか決める
            if current_stamina_1 <= 0:
                active_pitcher_1 = selectors.decide_relief(
                    pitchers_1, pitcher_records_1, inning, diff
                )
                active_pitcher_1.stats = {k: 0 for k in active_pitcher_1.stats}
                active_pitcher_1.stats["games"] += 1
                current_stamina_1 = (
                    active_pitcher_1.stamina - active_pitcher_1.fatigue_stamina
                ) * 0.2
                pitcher_records_1.append(
                    [active_pitcher_1, sum(scores_1), sum(scores_2)]
                )

            while True:
                batter = starters_batters_2[(b_num_2 - 1) % 9][1]
                game_condition = run_at_bat(active_pitcher_1, batter, game_condition)
                current_stamina_1 -= random.randint(1, 7)
                b_num_2 += 1
                if game_condition[3] == 3:
                    scores_2.append(game_condition[4])
                    top_bottom = 1
                    game_condition = [0, 0, 0, 0, 0]
                    break
        else:  # 裏（攻撃：Team 1 / 守備：Team 2）
            diff = sum(scores_1) - sum(scores_2)
            if current_stamina_2 <= 0:
                active_pitcher_2 = selectors.decide_relief(
                    pitchers_2, pitcher_records_2, inning, -diff
                )
                active_pitcher_2.stats = {k: 0 for k in active_pitcher_2.stats}
                active_pitcher_2.stats["games"] += 1
                current_stamina_2 = (
                    active_pitcher_2.stamina - active_pitcher_2.fatigue_stamina
                ) * 0.2
                pitcher_records_2.append(
                    [active_pitcher_2, sum(scores_2), sum(scores_1)]
                )

            while True:
                batter = starters_batters_1[(b_num_1 - 1) % 9][1]
                game_condition = run_at_bat(active_pitcher_2, batter, game_condition)
                current_stamina_2 -= random.randint(1, 7)
                b_num_1 += 1
                if game_condition[3] == 3:
                    scores_1.append(game_condition[4])
                    top_bottom = 0
                    game_condition = [0, 0, 0, 0, 0]
                    inning += 1
                    break

    # 6. 事後処理
    total_1, total_2 = sum(scores_1), sum(scores_2)
    print(f"試合終了: {team_name_1} {total_1} - {total_2} {team_name_2}\n")

    stats.assign_win_loss(pitcher_records_1, pitcher_records_2, total_1, total_2)

    # QS/完投判定
    for rec in [pitcher_records_1[0], pitcher_records_2[0]]:
        p = rec[0]
        outs = p.stats.get("outs_pitched", 0)
        er = p.stats.get("自責点", 0)
        if outs >= 18 and er <= 3:
            p.stats["qs"] += 1
        if outs >= 27:
            p.stats["complete_games"] += 1

    # 疲労度更新
    special.update_player_fatigue_pitcher(
        pitchers_1, pitcher_records_1, pitchers_2, pitcher_records_2
    )
    special.update_player_fatigue_batter(
        batters_1, starters_batters_1, batters_2, starters_batters_2
    )

    # 調子更新
    physics.update_player_condition(pitchers_1)
    physics.update_player_condition(pitchers_2)
    physics.update_player_condition(batters_1)
    physics.update_player_condition(batters_2)

    # 保存処理（今日の成績 all_players 分を Excel に加算）
    all_players = list(
        set(
            [s[1] for s in starters_batters_1 + starters_batters_2]
            + pitchers_1
            + pitchers_2
        )
    )
    database.output_exam(file_path, team_name_1, team_name_2, all_players)
