def decide_pitcher(pitchers, game_number):
    """
    先発投手を選出する
    """
    # 1. 先発適性（"先"）を持つ投手だけを抽出
    starters_list = [p for p in pitchers if p.role == "先"]

    # 2. ローテーションのインデックスを計算
    rotation_index = (game_number - 1) % len(starters_list)

    # 3. 該当する投手を選出
    p = starters_list[rotation_index]
    
    return ("先発", p)