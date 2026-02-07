# ライブラリインポート
import display_season_result
import game
import reset_result


def main():
    """
    ペナントレースを実行
    """

    # 変数
    file_path = "test.xlsx"
    teams = ["Hawks", "Fighters", "Buffaloes", "Eagles", "Lions", "Marines"]
    total_games_team = 7  # ホームゲームの試合数
    total_games = total_games_team * len(teams)

    # 事前処理
    reset_result.reset_result(file_path)

    # 年単位（143試合）実行
    for game_number in range(1, total_games + 1):
        game.game(file_path, game_number, teams, total_games_team)

    # 事後処理
    is_fatigue_considered = (
        False  # ベストオーダーを出力（疲労による能力ダウンを考慮しない）
    )
    display_season_result.display_season_result_b(
        file_path, teams, is_fatigue_considered
    )  # スタメンの最終打撃成績を表示
    display_season_result.display_season_result_p(
        file_path, teams
    )  # 先発投手全員の結果を表示


# 処理実行
if __name__ == "__main__":
    main()
