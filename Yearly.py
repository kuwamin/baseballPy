# ライブラリインポート
import DisplaySeasonResult
import Game
import ResetResult
import SummaryResult

def main():
    """
    ペナントレースを実行
    """

    # 変数
    total_games_team = 1   #ホームゲームの試合数
    total_games = total_games_team * 6
    file_path = 'test.xlsx'

    # 事前処理
    ResetResult.reset_result(file_path)

    # 年単位（143試合）実行
    for game_number in range(1, total_games + 1):
        Game.game(file_path, game_number)

    # 事後処理
    DisplaySeasonResult.display_season_result_b(file_path)   # スタメンの最終打撃成績を表示
    DisplaySeasonResult.display_season_result_p(file_path)   # 先発投手全員の結果を表示
    SummaryResult.test()


# 処理実行
if __name__ == "__main__":
    main()