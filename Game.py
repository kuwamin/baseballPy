# ライブラリインポート
import AquireData
import DecideBatter
import DecidePitcher
import OutputExam
import RunAtBat

def game():
    
    # 変数
    inningNumber = 1    #イニング
    TopBottom = 0   #表裏
    outCount = 0    #アウトカウント
    batterNumber_1 = 1
    batterNumber_2 = 1


    # 事前処理
    pitchers_1, batters_1= AquireData.test('test1')
    pitchers_2, batters_2= AquireData.test('test2')

    # --- 表示処理 ---
    starters_batter_1 = DecideBatter.test(batters_1)
    starters_pitcher_1 = DecidePitcher.test(pitchers_1)


    starters_batter_2 = DecideBatter.test(batters_2)
    starters_pitcher_2 = DecidePitcher.test(pitchers_2)

    
    print("--- 本日のスタメン ---")
    # タプルをアンパックして受け取る
    for i, (game_pos, batter1) in enumerate(starters_batter_1, 1):
        print(f"{i}番 ({game_pos}) {batter1.name} {batter1.trajectory} {batter1.meet} {batter1.power} {batter1.speed} {batter1.arm} {batter1.fielding} {batter1.catching}")
    p_role1, pitcher = starters_pitcher_1
    print(f"({p_role1}) {pitcher.name} {pitcher.speed}km {pitcher.control} {pitcher.stamina}")

    print("\n--- 本日のスタメン ---")
    for i, (game_pos, batter2) in enumerate(starters_batter_2, 1):
        print(f"{i}番 ({game_pos}) {batter2.name} {batter2.trajectory} {batter2.meet} {batter2.power} {batter2.speed} {batter2.arm} {batter2.fielding} {batter2.catching}")
    p_role2, pitcher2 = starters_pitcher_2
    print(f"({p_role2}) {pitcher2.name} {pitcher2.speed}km {pitcher2.control} {pitcher2.stamina}")
    

    # 打席実行
    while inningNumber <= 9:
        print(f"--- {inningNumber}回{'表' if TopBottom == 0 else '裏'}の攻撃 ---")
        
        if TopBottom == 0:
            while True:
                pitcher = starters_pitcher_1
                batter = starters_batter_2[batterNumber_2 % 9 - 1]
                print(batter[1].name) 
                
                RunAtBat.runAtBat(pitcher, batter)
                
                batterNumber_2 += 1
                outCount += 1
                if outCount == 3:
                    TopBottom = 1  
                    outCount = 0   
                    break
        else:
            while True:
                
                pitcher = starters_pitcher_2
                batter = starters_batter_1[batterNumber_1 % 9 - 1]
                print(batter[1].name)
                
                RunAtBat.runAtBat(pitcher, batter)
                
                batterNumber_1 += 1
                outCount += 1
                if outCount == 3:
                    TopBottom = 0
                    outCount = 0
                    inningNumber += 1
                    break     
        

    # 事後処理
    OutputExam.test()
