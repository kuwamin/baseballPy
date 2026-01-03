def decide_order(starters):
    """
    スタメン9人を能力値に基づいて最適な打順（1番～9番）に並べ替える
    """
    # starters は [(pos, player), ...] のリスト
    # 一旦、並べ替え用に選手リストを作る
    working_list = starters[:]
    lineup = [None] * 9

    # --- 打順決定ロジック ---

    # 4番：最強のパワー (power)
    working_list.sort(key=lambda x: x[1].power, reverse=True)
    lineup[3] = working_list.pop(0)

    # 1番：最強の走力 (speed)
    working_list.sort(key=lambda x: x[1].speed, reverse=True)
    lineup[0] = working_list.pop(0)

    # 3番：ミートとパワーの総合力
    working_list.sort(key=lambda x: (x[1].meet + x[1].power), reverse=True)
    lineup[2] = working_list.pop(0)

    # 2番：残った中でミート (meet) が一番高い
    working_list.sort(key=lambda x: x[1].meet, reverse=True)
    lineup[1] = working_list.pop(0)

    # 5, 6番：残ったパワー順
    working_list.sort(key=lambda x: x[1].power, reverse=True)
    lineup[4] = working_list.pop(0)
    lineup[5] = working_list.pop(0)

    # 7, 8, 9番：残りをミート順
    working_list.sort(key=lambda x: x[1].meet, reverse=True)
    lineup[6] = working_list.pop(0)
    lineup[7] = working_list.pop(0)
    lineup[8] = working_list.pop(0)

    return lineup