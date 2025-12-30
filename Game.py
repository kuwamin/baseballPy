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
    batterNumber_1 = 1
    batterNumber_2 = 1
    game_condition = [0,0,0,0,0]    # 一塁、二塁、三塁、アウトカウント、得点


    # 事前処理
    # エクセルからデータ取得
    pitchers_1, batters_1= AquireData.test('test1')
    pitchers_2, batters_2= AquireData.test('test2')

    # スタメン決定
    starters_batter_1 = DecideBatter.test(batters_1)
    starters_pitcher_1 = DecidePitcher.test(pitchers_1)
    starters_batter_2 = DecideBatter.test(batters_2)
    starters_pitcher_2 = DecidePitcher.test(pitchers_2)

    # スタメン表示
    DisplayStarter.test(starters_batter_1,starters_pitcher_1,  starters_batter_2,starters_pitcher_2)
    
    # 打席実行
    while inningNumber <= 9:
        print(f"--- {inningNumber}回{'表' if TopBottom == 0 else '裏'}の攻撃 ---")
        
        if TopBottom == 0:
            while True:
                pitcher = starters_pitcher_1[1]
                batter = starters_batter_2[batterNumber_2 % 9 - 1][1]
                print(batter.name) 
                
                game_condition = RunAtBat.runAtBat(pitcher, batter, game_condition)
                
                batterNumber_2 += 1
                if game_condition[3] == 3:
                    TopBottom = 1  
                    game_condition[3] = 0   
                    break
        else:
            while True:
                
                pitcher = starters_pitcher_2[1]
                batter = starters_batter_1[batterNumber_1 % 9 - 1][1]
                print(batter.name)
                
                game_condition = RunAtBat.runAtBat(pitcher, batter, game_condition)
                
                batterNumber_1 += 1
                if game_condition[3] == 3:
                    TopBottom = 0
                    game_condition[3] = 0
                    inningNumber += 1
                    break     
        

    # 事後処理
    OutputExam.test()
