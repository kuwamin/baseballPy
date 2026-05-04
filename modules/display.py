from modules import database
from modules import selectors

# 別のファイルで作る予定、あるいは既存の成績取得関数
# もし未作成なら、このファイルの下部に補助関数として定義しても良いです
from modules import stats
from modules.models import Batter, Pitcher


def display_season_result_b(file_path, teams, is_fatigue_considered):
    """
    全チームの最終打撃成績とベストオーダーを表示する
    """
    print("\n" + "=" * 20)
    print("  全チーム 最終打撃成績")
    print("=" * 20)

    for team_name in teams:
        print(f"\n--- {team_name} ベストオーダー ---")
        # 1. データ取得 (databaseモジュールを使用)
        _, batters = database.Aquire_data(file_path, team_name)

        # 2. スタメンと打順を決定 (selectorsモジュールを使用)
        starters_list = selectors.decide_batter(batters, is_fatigue_considered)
        starters_batter = selectors.decide_order(starters_list)

        starter_players = {p for pos, p in starters_batter}

        # チーム合計集計用
        t_ab, t_h, t_w, t_hbp, t_sf, t_tb = 0, 0, 0, 0, 0, 0

        # 3. スタメン9人の表示
        for i, (pos, player) in enumerate(starters_batter, 1):
            stats_str = stats.get_batter_stats(player)
            print(f"{i}番 ({pos}) {player.name} [{stats_str}]")

            s = player.stats
            t_ab += s.get("ab", 0)
            t_h += s.get("hits", 0)
            t_w += s.get("walks", 0)
            t_hbp += s.get("hbp", 0)
            t_sf += s.get("sac_fly", 0)
            t_tb += (
                s.get("singles", 0)
                + s.get("doubles", 0) * 2
                + s.get("triples", 0) * 3
                + s.get("hr", 0) * 4
            )

        # 4. 控え選手の表示
        print(f"\n[{team_name} 控え選手]")
        for player in batters:
            if player not in starter_players:
                stats_str = stats.get_batter_stats(player)
                print(f"控 ({player.position}) {player.name} [{stats_str}]")

                s = player.stats
                t_ab += s.get("ab", 0)
                t_h += s.get("hits", 0)
                t_w += s.get("walks", 0)
                t_hbp += s.get("hbp", 0)
                t_sf += s.get("sac_fly", 0)
                t_tb += (
                    s.get("singles", 0)
                    + s.get("doubles", 0) * 2
                    + s.get("triples", 0) * 3
                    + s.get("hr", 0) * 4
                )

        # 5. チームスタッツ算出
        team_avg = t_h / t_ab if t_ab > 0 else 0
        denom_obp = t_ab + t_w + t_hbp + t_sf
        team_obp = (t_h + t_w + t_hbp) / denom_obp if denom_obp > 0 else 0
        team_slg = t_tb / t_ab if t_ab > 0 else 0

        print("-" * 30)
        print(
            f"チーム通算打率: {team_avg:.3f}  チーム通算OPS: {team_obp + team_slg:.3f}"
        )


def display_season_result_p(file_path, teams):
    """
    全チームの最終投手成績を表示する
    """
    print("\n" + "=" * 20)
    print("  全チーム 全投手成績")
    print("=" * 20)

    for team_name in teams:
        print(f"\n[{team_name}]")
        pitchers, _ = database.Aquire_data(file_path, team_name)

        t_outs, t_er = 0, 0

        for p in pitchers:
            s = p.stats
            bf = s.get("bf", 0)
            h = s.get("hits_allowed", 0)
            bb = s.get("walks_allowed", 0)
            hbp = s.get("hbp_allowed", 0)

            p_outs = bf - (h + bb + hbp)
            stats_str = stats.get_pitcher_stats(p)
            print(
                f"{p.role} {p.name} [{stats_str}] {p.speed}km {p.control} {p.stamina} {p.breaking_ball}"
            )

            t_outs += p_outs
            t_er += s.get("自責点", 0)

        team_era = (t_er * 27) / t_outs if t_outs > 0 else 0
        print(f"チーム通算防御率: {team_era:.2f}")


def display_starter_batter(starters_batters: list[Batter]) -> None:
    """
    試合開始前の本日のスタメン打順を表示

    Args:
        - starters_batter : 打順組み換え後の Batter のリスト

    Returns:
        - None
    """
    batter_stats_list = [
        stats.get_batter_stats(batter[1]) for batter in starters_batters
    ]

    print("--- 本日のスタメン ---")
    for i, ((game_pos, batter), stats_str) in enumerate(
        zip(starters_batters, batter_stats_list), 1
    ):
        print(f"{i}番 ({game_pos}) {batter.name} [{stats_str}]")


def display_starter_pitcher(starters_pitcher: Pitcher) -> None:
    """
    試合開始前の本日の先発投手を表示

    Args:
        - starters_pitcher : 先発投手の Pitcher インスタンス

    Returns:
        - None
    """
    pitcher_role, pitcher = starters_pitcher
    pitcher_stats_str = stats.get_pitcher_stats(starters_pitcher[1])
    print(
        f"({pitcher_role}) {pitcher.name} [{pitcher_stats_str}] {pitcher.speed}km {pitcher.control} {pitcher.stamina} {pitcher.breaking_ball}"
    )
    print("\n")
