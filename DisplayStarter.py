def desplay_starter(starters_batter, starters_pitcher, batter_stats_list, pitcher_stats_str):

    print("--- 本日のスタメン ---")
    for i, ((game_pos, batter), stats_str) in enumerate(zip(starters_batter, batter_stats_list), 1):
        print(f"{i}番 ({game_pos}) {batter.name} [{stats_str}]")
        
    p_role, pitcher = starters_pitcher
    # 投手の名前の横に成績を表示
    print(f"({p_role}) {pitcher.name} [{pitcher_stats_str}] {pitcher.speed}km {pitcher.control} {pitcher.stamina}")
    print("\n")