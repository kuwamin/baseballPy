# ライブラリインポート
import AquireData
import DecideBatter
import DecidePitcher
import DisplayStarter
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
    starters_batter_1 = DecideBatter.decide_batter(batters_1)
    starters_pitcher_1 = DecidePitcher.decide_pitcher(pitchers_1, game_number)
    starters_batter_2 = DecideBatter.decide_batter(batters_2)
    starters_pitcher_2 = DecidePitcher.decide_pitcher(pitchers_2, game_number)

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

    # スタメン表示
    DisplayStarter.desplay_starter(starters_batter_1,starters_pitcher_1,  starters_batter_2,starters_pitcher_2)
    
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

    # QS / HQS の判定
    for p in [starters_pitcher_1[1], starters_pitcher_2[1]]:
        outs = p.stats.get('outs_pitched', 0)
        er = p.stats.get('自責点', 0)

        # HQS判定（7回2自責点以下）
        if outs >= 21 and er <= 2:
            p.stats['hqs'] += 1
            p.stats['qs'] += 1  # HQSなら当然QSも達成
        # QS判定（6回3自責点以下）
        elif outs >= 18 and er <= 3:
            p.stats['qs'] += 1


    # 全選手をひとまとめにする（投手と野手両方）
    all_active_players = []
    for item in starters_batter_1 + starters_batter_2:
        all_active_players.append(item[1])
    all_active_players.append(starters_pitcher_1[1])
    all_active_players.append(starters_pitcher_2[1])

    # エクセル更新実行
    OutputExam.output_exam('test.xlsx', all_active_players)
