# ライブラリインポート
import Game
import ResetResult
import SummaryResult

def yearly():

    # 変数
    gameNumber = 3    #試合数


    # 事前処理
    ResetResult.test()


    # 年単位（143試合）実行
    for i in range(gameNumber):
        Game.game()

    # 事後処理
    SummaryResult.test()
