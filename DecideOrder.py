def get_power(item):
    """並べ替え用の補助関数：パワーを返す"""
    return item[1].power

def get_speed(item):
    """並べ替え用の補助関数：走力を返す"""
    return item[1].speed

def get_total_hit_skill(item):
    """並べ替え用の補助関数：総合打力（ミート+パワー）を返す"""
    return item[1].meet + item[1].power

def get_meet(item):
    """並べ替え用の補助関数：ミートを返す"""
    return item[1].meet

def decide_order(starters):
    """
    上位7人を「打力のある選手」として選抜し、その中で1〜4番を決定する
    """
    # starters は [(pos, player), ...] のリスト
    working_list = starters[:]
    lineup = [None] * 9

    # 1. まず、総合打力が高い「上位打線候補」7人を選び出す
    # 総合打力（ミート+パワー）で降順（大きい順）に並べ替え
    working_list.sort(key=get_total_hit_skill, reverse=True)
    
    # 上位7人と、それ以外（下位候補2人）に分ける
    top_candidates = working_list[:6]
    bottom_candidates = working_list[6:]

    # --- 上位打線(1~4番)を top_candidates から決める ---

    # 4番：上位候補の中で最強のパワー
    top_candidates.sort(key=get_power, reverse=True)
    lineup[3] = top_candidates.pop(0)

    # 1番：上位候補の中で最強の走力
    top_candidates.sort(key=get_speed, reverse=True)
    lineup[0] = top_candidates.pop(0)

    # 3番：上位候補の中で総合打力が高い人
    top_candidates.sort(key=get_total_hit_skill, reverse=True)
    lineup[2] = top_candidates.pop(0)

    # 2番：上位候補の中でミートが高い人
    top_candidates.sort(key=get_meet, reverse=True)
    lineup[1] = top_candidates.pop(0)

    # --- 残りの打順(5~9番)を決める ---

    # 5, 6：top_candidates の残りと bottom_candidates を合流させてパワー順
    remaining_players = top_candidates + bottom_candidates
    remaining_players.sort(key=get_power, reverse=True)
    
    lineup[4] = remaining_players.pop(0)
    lineup[5] = remaining_players.pop(0)
    

    # 7, 8, 9番：残りをミート順
    remaining_players.sort(key=get_meet, reverse=True)
    lineup[8] = remaining_players.pop(0)
    lineup[6] = remaining_players.pop(0)
    lineup[7] = remaining_players.pop(0)

    return lineup