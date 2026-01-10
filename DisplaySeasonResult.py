import AquireData
import DecideBatter
import DecideOrder
import DecidePitcher
import GetSeasonStats

# エクセルから読み込む全チームのリスト
team = ['Hawks', 'Fighters', 'Buffaloes', 'Eagles', 'Lions', 'Marines']

def display_season_result_b(file_path):
    """
    全チームのベストオーダー（スタメン）と最終打撃成績を表示
    """
    print("\n" + "="*20)
    print("  全チーム 最終打撃成績")
    print("="*20)

    for team_name in team:
        print(f"\n--- {team_name} ベストオーダー ---")
        # 最新データを取得
        _, batters = AquireData.Aquire_data(file_path, team_name)
        
        # 最終的な能力・成績に基づいてスタメンと打順を決定
        starters_list = DecideBatter.decide_batter(batters)
        starters_batter = DecideOrder.decide_order(starters_list)
        
        # 各選手の成績文字列を生成
        for i, (pos, player) in enumerate(starters_batter, 1):
            stats_str = GetSeasonStats.get_batter_stats(player)
            print(f"{i}番 ({pos}) {player.name} [{stats_str}]")


def display_season_result_p(file_path):
    """
    全チームの先発投手陣（ローテーション）の最終成績を表示
    """
    print("\n" + "="*20)
    print("  全チーム 先発投手成績")
    print("="*20)

    for team_name in team:
        print(f"\n[{team_name}]")
        pitchers, _ = AquireData.Aquire_data(file_path, team_name)
        
        # クラス定義に合わせて p.aptitude ではなく p.role を参照するように変更
        for p in pitchers:
            if p.role == "先":
                stats_str = GetSeasonStats.get_pitcher_stats(p)
                print(f"(先発) {p.name} [{stats_str}] {p.speed}km {p.control} {p.stamina} {p.breaking_ball}")