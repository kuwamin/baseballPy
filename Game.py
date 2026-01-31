# ライブラリインポート
import random
import AquireData
import AssignWinLoss
import DecideBatter
import DecideOrder
import DecidePitcher
import DecideRelief
import DecideTeam
import DisplayStarter
import GetSeasonStats
import OutputExam
import RunAtBat

def game(file_path, game_number, teams, total_games_team):
    """
    1試合実行
    """
    # 変数
    inning_number = 1    
    top_bottom = 0       
    batter_number_1 = 1  
    batter_number_2 = 1
    
    score_1 = [] # 後攻(Team1)の各回の得点
    score_2 = [] # 先行(Team2)の各回の得点
    game_condition = [0,0,0,0,0]

    # 対戦チーム決定・データ取得
    team_name_1, team_name_2 = DecideTeam.decide_team(game_number, teams, total_games_team)
    pitchers_1, batters_1 = AquireData.Aquire_data(file_path, team_name_1)
    pitchers_2, batters_2 = AquireData.Aquire_data(file_path, team_name_2)

    # スタメン・先発決定
    starters_batter_1 = DecideOrder.decide_order(DecideBatter.decide_batter(batters_1))
    starters_batter_2 = DecideOrder.decide_order(DecideBatter.decide_batter(batters_2))
    # 先発投手決定
    starters_pitcher_1 = DecidePitcher.decide_pitcher(pitchers_1, game_number)
    starters_pitcher_2 = DecidePitcher.decide_pitcher(pitchers_2, game_number)

    active_pitcher_1 = starters_pitcher_1[1]
    active_pitcher_2 = starters_pitcher_2[1]
    
    # 勝利投手判定用：リード時の投手を保持
    # [投手のオブジェクト, 投球開始時の味方スコア, 投球開始時の相手スコア]
    pitcher_records_1 = [[active_pitcher_1, 0, 0]] 
    pitcher_records_2 = [[active_pitcher_2, 0, 0]]

    # スタミナ初期化
    current_stamina_1 = active_pitcher_1.stamina * 1.5
    current_stamina_2 = active_pitcher_2.stamina * 1.5

    # スタメン表示 (※消さずに維持)
    DisplayStarter.desplay_starter_b(starters_batter_1, [GetSeasonStats.get_batter_stats(s[1]) for s in starters_batter_1])
    DisplayStarter.desplay_starter_p(starters_pitcher_1, GetSeasonStats.get_pitcher_stats(active_pitcher_1))
    DisplayStarter.desplay_starter_b(starters_batter_2, [GetSeasonStats.get_batter_stats(s[1]) for s in starters_batter_2])
    DisplayStarter.desplay_starter_p(starters_pitcher_2, GetSeasonStats.get_pitcher_stats(active_pitcher_2))

    # 成績リセット
    all_starters = [s[1] for s in starters_batter_1 + starters_batter_2] + [active_pitcher_1, active_pitcher_2]
    for p in all_starters: p.stats = {key: 0 for key in p.stats}

    # 試合数カウント
    for b in [s[1] for s in starters_batter_1 + starters_batter_2]: b.stats['games'] += 1
    active_pitcher_1.stats['games'] += 1; active_pitcher_1.stats['starts'] += 1
    active_pitcher_2.stats['games'] += 1; active_pitcher_2.stats['starts'] += 1

    # 打席実行
    while inning_number <= 9:
        current_diff = sum(score_1) - sum(score_2) # 正ならTeam1リード

        # --- 表 (攻撃:Team2 / 守備:Team1) ---
        if top_bottom == 0:
            if current_stamina_1 <= 0:
                # 状況に応じたリリーフ選出
                active_pitcher_1 = DecideRelief.decide_relief(pitchers_1, pitcher_records_1, inning_number, current_diff)
                active_pitcher_1.stats = {key: 0 for key in active_pitcher_1.stats}
                active_pitcher_1.stats['games'] += 1
                current_stamina_1 = active_pitcher_1.stamina * 0.2
                pitcher_records_1.append([active_pitcher_1, sum(score_1), sum(score_2)])

            while True:
                batter = starters_batter_2[batter_number_2 % 9 - 1][1]
                game_condition = RunAtBat.run_at_bat(active_pitcher_1, batter, game_condition)
                current_stamina_1 -= random.randint(1, 7)
                batter_number_2 += 1
                if game_condition[3] == 3:
                    score_2.append(game_condition[4])
                    top_bottom = 1; game_condition = [0,0,0,0,0]
                    break

        # --- 裏 (攻撃:Team1 / 守備:Team2) ---
        else:
            if current_stamina_2 <= 0:
                active_pitcher_2 = DecideRelief.decide_relief(pitchers_2, pitcher_records_2, inning_number, -current_diff)
                active_pitcher_2.stats = {key: 0 for key in active_pitcher_2.stats}
                active_pitcher_2.stats['games'] += 1
                current_stamina_2 = active_pitcher_2.stamina * 0.2
                pitcher_records_2.append([active_pitcher_2, sum(score_2), sum(score_1)])

            while True:
                batter = starters_batter_1[batter_number_1 % 9 - 1][1]
                game_condition = RunAtBat.run_at_bat(active_pitcher_2, batter, game_condition)
                current_stamina_2 -= random.randint(1, 7)
                batter_number_1 += 1
                if game_condition[3] == 3:
                    score_1.append(game_condition[4])
                    top_bottom = 0; game_condition = [0,0,0,0,0]
                    inning_number += 1
                    break     

    # --- 試合終了後の判定ロジック ---
    total_1, total_2 = sum(score_1), sum(score_2)
    print(f"試合終了: {total_1} - {total_2}\n")

    # 勝利・敗戦・セーブ・ホールドの決定
    AssignWinLoss.assign_win_loss(pitcher_records_1, pitcher_records_2, total_1, total_2)

    # QS判定 (先発のみ)
    for rec in [pitcher_records_1[0], pitcher_records_2[0]]:
        p = rec[0]; outs = p.stats.get('outs_pitched', 0); er = p.stats.get('自責点', 0)
        if outs >= 18 and er <= 3: p.stats['qs'] += 1
        if outs >= 27: p.stats['complete_games'] += 1

    # 保存用リスト作成
    all_active_players = [s[1] for s in starters_batter_1 + starters_batter_2]
    all_active_players.extend([r[0] for r in pitcher_records_1])
    all_active_players.extend([r[0] for r in pitcher_records_2])

    OutputExam.output_exam(file_path, team_name_1, team_name_2, all_active_players)