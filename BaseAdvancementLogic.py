def base_advancement_logic(result, game_condition):

    b1, b2, b3 = game_condition[0], game_condition[1], game_condition[2]
    outs = game_condition[3]
    old_score = game_condition[4] # 更新前のスコアを保持
    score = old_score

    if result == "1B":
        score += b3
        b3, b2, b1 = b2, b1, 1

    elif result == "2B":
        score += (b3 + b2)
        b3, b2, b1 = b1, 1, 0

    elif result == "3B":
        score += (b3 + b2 + b1)
        b3, b2, b1 = 1, 0, 0

    elif result == "HR":
        score += (b3 + b2 + b1 + 1)
        b3, b2, b1 = 0, 0, 0

    elif result in ["BB", "HBP"]:
        if b1 == 1 and b2 == 1 and b3 == 1:
            score += 1
        elif b1 == 1 and b2 == 1:
            b3 = 1
        elif b1 == 1:
            b2 = 1
        b1 = 1

    elif result in ["OUT", "SO"]:
        outs += 1

    # game_conditionリストを更新
    game_condition[0], game_condition[1], game_condition[2] = b1, b2, b3
    game_condition[3] = outs
    game_condition[4] = score

    return game_condition