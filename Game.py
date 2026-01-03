# ライブラリインポート
import AquireData
import DecideBatter
import DecideOrder
import DecidePitcher
import DisplayStarter
import GetSeasonStats
import OutputExam
import RunAtBat

def game(file_path, game_number):
    
    # 変数
    inning_number = 1    #イニング
    top_bottom = 0   #表裏
    batter_number_1 = 1  #打順(1番から)
    batter_number_2 = 1
    score_1 = []
    score_2 = []
    game_condition = [0,0,0,0,0]    # 一塁、二塁、三塁、アウトカウント、イニングでの得点
    team_name_1 = 'test1'
    team_name_2 = 'test2'


    # 事前処理
    # エクセルからデータ取得
    pitchers_1, batters_1= AquireData.Aquire_data(file_path, team_name_1)
    pitchers_2, batters_2= AquireData.Aquire_data(file_path, team_name_2)

    # スタメン決定
    starters_list_1 = DecideBatter.decide_batter(batters_1)
    starters_batter_1 = DecideOrder.decide_order(starters_list_1)
    starters_list_2 = DecideBatter.decide_batter(batters_2)
    starters_batter_2 = DecideOrder.decide_order(starters_list_2)

    starters_pitcher_1 = DecidePitcher.decide_pitcher(pitchers_1, game_number)
    starters_pitcher_2 = DecidePitcher.decide_pitcher(pitchers_2, game_number)


    b_stats_1 = [GetSeasonStats.get_batter_stats(s[1]) for s in starters_batter_1]
    b_stats_2 = [GetSeasonStats.get_batter_stats(s[1]) for s in starters_batter_2]

    p_stats_1 = GetSeasonStats.get_pitcher_stats(starters_pitcher_1[1])
    p_stats_2 = GetSeasonStats.get_pitcher_stats(starters_pitcher_2[1])

    # 全スタメンの成績（前の試合のstats）をリセット
    all_starters = [s[1] for s in starters_batter_1 + starters_batter_2] + [starters_pitcher_1[1], starters_pitcher_2[1]]
    for p in all_starters:
        # すべての項目を0で初期化
        p.stats = {key: 0 for key in p.stats}

    # 1. 野手の試合数をカウント
    for b in [s[1] for s in starters_batter_1 + starters_batter_2]:
        b.stats['games'] += 1

    # 2. 投手の登板数・先発数をカウント
    p1 = starters_pitcher_1[1]
    p2 = starters_pitcher_2[1]

    p1.stats['games'] += 1
    p1.stats['starts'] += 1
    p2.stats['games'] += 1
    p2.stats['starts'] += 1

    # スタメン表示 (引数に成績リストを追加)
    DisplayStarter.desplay_starter(starters_batter_1, starters_pitcher_1, b_stats_1, p_stats_1)
    DisplayStarter.desplay_starter(starters_batter_2, starters_pitcher_2, b_stats_2, p_stats_2)

    # 打席実行
    while inning_number <= 9:
        print(f"--- {inning_number}回{'表' if top_bottom == 0 else '裏'}の攻撃 ---")
        
        if top_bottom == 0:  # 表
            while True:
                pitcher = starters_pitcher_1[1]
                batter = starters_batter_2[batter_number_2 % 9 - 1][1]
                
                game_condition = RunAtBat.run_at_bat(pitcher, batter, game_condition)
                
                batter_number_2 += 1
                if game_condition[3] == 3:  # 3アウト
                    score_2.append(game_condition[4])
                    print(f"{game_condition[4]} 点")

                    top_bottom = 1  
                    game_condition = [0,0,0,0,0]   
                    break

        else:   # 裏
            while True:
                
                pitcher = starters_pitcher_2[1]
                batter = starters_batter_1[batter_number_1 % 9 - 1][1]
                
                game_condition = RunAtBat.run_at_bat(pitcher, batter, game_condition)
                
                batter_number_1 += 1
                if game_condition[3] == 3:
                    score_1.append(game_condition[4])
                    print(f"{game_condition[4]} 点")

                    top_bottom = 0
                    game_condition = [0,0,0,0,0]   
                    inning_number += 1
                    break     
        

    # 事後処理
    print(f"{sum(score_2)} - {sum(score_1)}")

    total_score_1 = sum(score_1) 
    total_score_2 = sum(score_2)  

    p1 = starters_pitcher_1[1] 
    p2 = starters_pitcher_2[1]

    # 勝利・敗戦の判定
    if total_score_1 > total_score_2:
        # 後攻側が勝利
        p1.stats['wins'] += 1
        p2.stats['losses'] += 1
    elif total_score_2 > total_score_1:
        # 先行側が勝利
        p2.stats['wins'] += 1
        p1.stats['losses'] += 1


    # QS / HQS / 完投 / 完封 の判定
    # 投手と、その投力が許した得点（＝相手チームの得点）をペアにする
    pitcher_evals = [
        (p1, total_score_2),
        (p2, total_score_1) 
    ]

    for p, score_allowed in pitcher_evals:
        outs = p.stats.get('outs_pitched', 0)
        er = p.stats.get('自責点', 0)

        # QS/HQS 判定
        if outs >= 21 and er <= 2:
            p.stats['hqs'] += 1
            p.stats['qs'] += 1
        elif outs >= 18 and er <= 3:
            p.stats['qs'] += 1
        
        # 完投判定 (9イニング = 27アウト)
        if outs >= 27:
            p.stats['complete_games'] += 1
            # 完封判定 (完投かつ失点0)
            if score_allowed == 0:
                p.stats['shutouts'] += 1


    # 全選手をひとまとめにする（投手と野手両方）
    all_active_players = []
    for item in starters_batter_1 + starters_batter_2:
        all_active_players.append(item[1])
    all_active_players.append(starters_pitcher_1[1])
    all_active_players.append(starters_pitcher_2[1])

    # エクセル更新実行
    OutputExam.output_exam('test.xlsx', all_active_players)