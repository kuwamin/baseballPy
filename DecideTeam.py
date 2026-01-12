def decide_team(game_number, teams, total_games_team):
    """
    試合数に応じて対戦カードを決定。
    team_2を剰余(%)で計算することで、毎試合相手が切り替わるように設定。
    """
    num_teams = len(teams)
    num_opponents = num_teams - 1

    idx = (game_number - 1)
    
    # 1チームあたりの消化試合数(total_games_team)ごとに主役チーム(team_1)を固定
    team_1_idx = (idx // total_games_team) % num_teams
    team_name_1 = teams[team_1_idx]

    # team_1以外の5チームから対戦相手を選択
    other_teams = [t for t in teams if t != team_name_1]

    # 剰余を用いることで 0,1,2,3,4,0,1... と毎試合インデックスを変化させる
    team_2_idx = idx % num_opponents
    team_name_2 = other_teams[team_2_idx]

    return team_name_1, team_name_2