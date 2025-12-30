# ライブラリインポート
import AquireData
import DecideMember
import RunAtBat
import SummaryResult


def game():
    
    # 変数
    inningNumber = 1    #イニング
    outCount = 0    #アウト


    # 事前処理
    AquireData.test()

    DecideMember.test()


    # 打席実行
    while inningNumber <= 9:
        RunAtBat.runAtBat()
        inningNumber += 1

    # 事後処理
    SummaryResult.test()
