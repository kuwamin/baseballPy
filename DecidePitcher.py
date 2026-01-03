# テストコード
def decide_pitcher(pitchers):
    candidates = pitchers[:]
    starters_pitcher = None

    for p in candidates:
        if p.role == "先":
            starters_pitcher = ("先発", p)
            break

    return starters_pitcher
