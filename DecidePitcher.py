def decide_pitcher(pitchers, game_number):
    """
    先発投手を選出する
    """
    # 1. 先発適性を持つ投手を抽出
    starters_list = [p for p in pitchers if p.role == "先"]

    # 2. 本来のローテーション順を特定
    rotation_index = (game_number - 1) % len(starters_list)
    p = starters_list[rotation_index]

    # 減少体力のチェック
    check_count = 0
    while p.fatigue_stamina > (p.stamina * 0.3) and check_count < len(starters_list):
        rotation_index = (rotation_index + 1) % len(starters_list)
        p = starters_list[rotation_index]
        check_count += 1
    
    return ("先発", p)