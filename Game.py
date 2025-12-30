# ライブラリインポート
import AquireData
import DecideMember
import OutputExam
import RunAtBat

def game():
    
    # 変数
    inningNumber = 1    #イニング
    outCount = 0    #アウト


    # 事前処理
    pichers, batters= AquireData.test()

    # --- 表示処理 ---
    starters = DecideMember.test(batters)

    print("--- 本日のスタメン ---")
    # タプルをアンパックして受け取る
    for i, (game_pos, player) in enumerate(starters, 1):
        # player.position（本来の位置）ではなく、game_pos（今日の位置）を表示
        print(f"{i}番 ({game_pos}) {player.name} {player.trajectory} {player.meet} {player.power} {player.speed} {player.arm} {player.fielding} {player.catching}")


    # 打席実行
    while inningNumber <= 9:
        RunAtBat.runAtBat()
        inningNumber += 1

    # 事後処理
    OutputExam.test()
