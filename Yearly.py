# ライブラリインポート
import Game
import ResetResult
import SummaryResult

def main():
    """
    ペナントレースを実行
    """

    # 変数
    total_games = 143    #試合数
    file_path = 'test.xlsx'

    # 事前処理
    ResetResult.reset_result(file_path)

    # 年単位（143試合）実行
    for game_number in range(1, total_games + 1):
        Game.game(file_path, game_number)

    # 事後処理
    SummaryResult.test()


# 処理実行
if __name__ == "__main__":
    main()