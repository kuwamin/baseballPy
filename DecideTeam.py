def decide_team(game_number, teams, total_games_team):
    """
    対戦カードを決定
    """
    num_teams = len(teams)
    num_opponents = num_teams - 1

    idx = (game_number - 1)
    
    # 1チームあたりの消化試合数(total_games_team)ごとteam_1を固定
    team_1_idx = (idx // total_games_team) % num_teams
    team_name_1 = teams[team_1_idx]

    # team_1以外の5チームから対戦相手を選択
    other_teams = [t for t in teams if t != team_name_1]

    # team_2を決定
    team_2_idx = idx % num_opponents
    team_name_2 = other_teams[team_2_idx]

    return team_name_1, team_name_2