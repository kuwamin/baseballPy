# ライブラリインポート
import Game
import ResetResult
import SummaryResult

def main():
    """
    ペナントレースを実行
    """

    # 変数
    game_number = 143    #試合数
    file_path = 'test.xlsx'

    # 事前処理
    ResetResult.reset_result(file_path)

    # 年単位（143試合）実行
    for i in range(game_number):
        Game.game(file_path)

    # 事後処理
    SummaryResult.test()


# 処理実行
if __name__ == "__main__":
    main()