# ライブラリインポート
import Game
import ResetResult
import SummaryResult

def main():

    # 変数
    gameNumber = 10    #試合数


    # 事前処理
    ResetResult.test()


    # 年単位（143試合）実行
    for i in range(gameNumber):
        Game.game()

    # 事後処理
    SummaryResult.test()

# 処理実行
if __name__ == "__main__":
    main()