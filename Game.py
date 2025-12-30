# ライブラリインポート
import AquireData
import DecideBatter
import DecidePitcher
import OutputExam
import RunAtBat

def game():
    
    # 変数
    inningNumber = 1    #イニング
    outCount = 0    #アウト


    # 事前処理
    pichers_1, batters_1= AquireData.test('test1')
    pichers_2, batters_2= AquireData.test('test2')

    # --- 表示処理 ---
    starters_batter_1 = DecideBatter.test(batters_1)
    starters_pitcher_1 = DecidePitcher.test(pichers_1)


    starters_batter_2 = DecideBatter.test(batters_2)
    starters_pitcher_2 = DecidePitcher.test(pichers_2)

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
        RunAtBat.runAtBat()
        inningNumber += 1

    # 事後処理
    OutputExam.test()
