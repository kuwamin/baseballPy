# ライブラリインポート
import AquireData
import DecideBatter
import DecidePitcher
import DisplayStarter
import OutputExam
import RunAtBat

def game():
    
    # 変数
    inningNumber = 1    #イニング
    TopBottom = 0   #表裏
    batterNumber_1 = 1  #打順(1番から)
    batterNumber_2 = 1
    score_1 = []
    score_2 = []
    game_condition = [0,0,0,0,0]    # 一塁、二塁、三塁、アウトカウント、イニングでの得点


    # 事前処理
    # エクセルからデータ取得
    pitchers_1, batters_1= AquireData.test('test1')
    pitchers_2, batters_2= AquireData.test('test2')

    # スタメン決定
    starters_batter_1 = DecideBatter.test(batters_1)
    starters_pitcher_1 = DecidePitcher.test(pitchers_1)
    starters_batter_2 = DecideBatter.test(batters_2)
    starters_pitcher_2 = DecidePitcher.test(pitchers_2)

    # 全スタメンの成績をリセット（これを忘れると前試合の成績が残る）
    all_starters = [s[1] for s in starters_batter_1 + starters_batter_2] + [starters_pitcher_1[1], starters_pitcher_2[1]]
    for p in all_starters:
        # すべての項目を0で初期化
        p.stats = {key: 0 for key in p.stats}

    # スタメン表示
    DisplayStarter.test(starters_batter_1,starters_pitcher_1,  starters_batter_2,starters_pitcher_2)
    
    # 打席実行
    while inningNumber <= 9:
        print(f"--- {inningNumber}回{'表' if TopBottom == 0 else '裏'}の攻撃 ---")
        
        if TopBottom == 0:  # 表
            while True:
                pitcher = starters_pitcher_1[1]
                batter = starters_batter_2[batterNumber_2 % 9 - 1][1]
                
                game_condition = RunAtBat.runAtBat(pitcher, batter, game_condition)
                
                batterNumber_2 += 1
                if game_condition[3] == 3:  
                    score_2.append(game_condition[4])
                    print(f"{game_condition[4]} 点")

                    TopBottom = 1  
                    game_condition = [0,0,0,0,0]   
                    break
        else:   # 裏
            while True:
                
                pitcher = starters_pitcher_2[1]
                batter = starters_batter_1[batterNumber_1 % 9 - 1][1]
                
                game_condition = RunAtBat.runAtBat(pitcher, batter, game_condition)
                
                batterNumber_1 += 1
                if game_condition[3] == 3:
                    score_1.append(game_condition[4])
                    print(f"{game_condition[4]} 点")

                    TopBottom = 0
                    game_condition = [0,0,0,0,0]   
                    inningNumber += 1
                    
                    break     
        

    # 事後処理
    print(f"{sum(score_2)} - {sum(score_1)}")
    print(starters_batter_1[0][1].stats['pa'])


    # 全選手をひとまとめにする（投手と野手両方）
    all_active_players = []
    for item in starters_batter_1 + starters_batter_2:
        all_active_players.append(item[1])
    all_active_players.append(starters_pitcher_1[1])
    all_active_players.append(starters_pitcher_2[1])

    # エクセル更新実行
    OutputExam.test('test.xlsx', all_active_players)
