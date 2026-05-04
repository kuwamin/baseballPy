from modules import database, core_game, display


def main() -> None:
    """
    1年間のペナントレースを実行する

    Args:
        -

    Returns:
        -
    """

    file_path: str = "test.xlsx"
    team_list: list[str] = [
        "Hawks",
        "Fighters",
        "Buffaloes",
        "Eagles",
        "Lions",
        "Marines",
    ]
    total_games_team: int = 72
    total_games: int = total_games_team * len(team_list)

    # 成績リセット
    database.reset_result(file_path)

    # 試合実行
    for game_number in range(1, total_games + 1):
        core_game.game(file_path, game_number, team_list, total_games_team)

    # シーズン結果表示
    is_fatigue_considered = False
    display.display_season_result_b(file_path, team_list, is_fatigue_considered)
    display.display_season_result_p(file_path, team_list)


if __name__ == "__main__":
    main()
