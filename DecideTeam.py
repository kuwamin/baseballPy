def decide_team(game_number):
    teams = ['Hawks', 'Fighters', 'Buffaloes', 'Eagles', 'Lions', 'Marines']
    
    # 1. リーグ全体の試合数は 420試合 (6チーム × 140試合 / 2)
    idx = (game_number - 1)
    
    # 2. team_1 を決定
    team_1_idx = (idx // 70) % 6
    team_name_1 = teams[team_1_idx]

    # 3. team_1 以外のチームリストを作成
    other_teams = []
    for t in teams:
        if t != team_name_1:
            other_teams.append(t)

    # 4. 残った 5 チームから対戦相手を決定
    team_2_idx = (idx // 14) % 5
    team_name_2 = other_teams[team_2_idx]

    return team_name_1, team_name_2