from modules import database
from modules import core_game
from modules import display


def main() -> None:
    """1年間のペナントレースを実行する"""

    file_path = "test.xlsx"
    teams = ["Hawks", "Fighters", "Buffaloes", "Eagles", "Lions", "Marines"]
    total_games_team = 4
    total_games = total_games_team * len(teams)

    # 1. 成績リセット (database.py)
    database.reset_result(file_path)

    # 2. 試合実行 (core_game.py)
    for game_number in range(1, total_games + 1):
        core_game.game(file_path, game_number, teams, total_games_team)

    # 3. シーズン結果表示 (display.py)
    is_fatigue_considered = False
    display.display_season_result_b(file_path, teams, is_fatigue_considered)
    display.display_season_result_p(file_path, teams)


if __name__ == "__main__":
    main()
