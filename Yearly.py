# ライブラリインポート
import Game
import ResetResult
import SummaryResult

# 事前処理
ResetResult.test()


# 年単位（143試合）実行
for i in range(143):
    Game.test()

# 事後処理
SummaryResult.test()
