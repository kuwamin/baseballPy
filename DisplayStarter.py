def desplay_starter(starters_batter, starters_pitcher, season_stats_list):

    print("--- 本日のスタメン ---")
    # zipを使ってバッターと成績リストを同時にループさせる
    for i, ((game_pos, batter), stats_str) in enumerate(zip(starters_batter, season_stats_list), 1):
        # 能力値の代わりに引数で受け取った成績文字列を表示
        print(f"{i}番 ({game_pos}) {batter.name} [{stats_str}]")
        
    p_role, pitcher = starters_pitcher
    print(f"({p_role}) {pitcher.name} {pitcher.speed}km {pitcher.control} {pitcher.stamina}")
    print("\n")