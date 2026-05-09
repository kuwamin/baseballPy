from operator import itemgetter

from modules import database
from modules import selectors

# 別のファイルで作る予定、あるいは既存の成績取得関数
# もし未作成なら、このファイルの下部に補助関数として定義しても良いです
from modules import stats
from modules.models import Batter, Pitcher


def display_season_result_batter(file_path: str, team_list: list[str]) -> None:
    """
    全チームの最終打撃成績とベストオーダーを表示する

    Args:
        - file_path : 読み込み対象となるExcelファイルのパス
        - team_list : チームのリスト

    Returns:
        - None
    """
    print("\n" + "=" * 20)
    print("  全チーム 最終打撃成績")
    print("=" * 20)

    for team_name in team_list:
        print(f"\n--- {team_name} ベストオーダー ---")
        # データ取得
        _, batters = database.Aquire_data(file_path, team_name)

        # スタメンと打順を決定
        starters_list = selectors.decide_batter(batters, False)
        starters_batter = selectors.decide_order(starters_list)

        starter_players = {player for _, player in starters_batter}

        # チーム合計集計用
        t_ab, t_h, t_db, t_tr, t_hr, t_w, t_hbp, t_sf, t_so, t_tb = (
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        )

        # スタメン9人の表示
        for i, (pos, player) in enumerate(starters_batter, 1):
            stats_str = stats.get_batter_stats(player)
            print(f"{i}番 ({pos}) {player.name} [{stats_str}]")

            s = player.stats
            t_ab += s.get("ab", 0)
            t_h += s.get("hits", 0)
            t_db += s.get("doubles", 0)
            t_tr += s.get("triples", 0)
            t_hr += s.get("hr", 0)
            t_w += s.get("walks", 0)
            t_hbp += s.get("hbp", 0)
            t_sf += s.get("sac_fly", 0)
            t_so += s.get("so", 0)

            t_tb += (
                s.get("singles", 0)
                + s.get("doubles", 0) * 2
                + s.get("triples", 0) * 3
                + s.get("hr", 0) * 4
            )

        # 控え選手の表示
        print(f"\n[{team_name} 控え選手]")
        for player in batters:
            if player not in starter_players:
                stats_str = stats.get_batter_stats(player)
                print(f"控 ({player.position}) {player.name} [{stats_str}]")

                s = player.stats
                t_ab += s.get("ab", 0)
                t_h += s.get("hits", 0)
                t_db += s.get("doubles", 0)
                t_tr += s.get("triples", 0)
                t_hr += s.get("hr", 0)
                t_w += s.get("walks", 0)
                t_hbp += s.get("hbp", 0)
                t_sf += s.get("sac_fly", 0)
                t_so += s.get("so", 0)

                t_tb += (
                    s.get("singles", 0)
                    + s.get("doubles", 0) * 2
                    + s.get("triples", 0) * 3
                    + s.get("hr", 0) * 4
                )

        # チームスタッツ算出
        team_avg = t_h / t_ab if t_ab > 0 else 0
        denom_obp = t_ab + t_w + t_hbp + t_sf
        team_obp = (t_h + t_w + t_hbp) / denom_obp if denom_obp > 0 else 0
        team_slg = t_tb / t_ab if t_ab > 0 else 0

        print("-" * 30)
        print(
            f"チーム通算打率: {team_avg:.3f}  チーム通算OPS: {team_obp + team_slg:.3f}"
        )


def display_season_result_pitcher(file_path: str, team_list: list[str]) -> None:
    """
    全チームの最終投手成績を表示する

    Args:
        - file_path : 読み込み対象となるExcelファイルのパス
        - team_list : チームのリスト

    Returns:
        - None
    """
    print("\n" + "=" * 20)
    print("  全チーム 全投手成績")
    print("=" * 20)

    for team_name in team_list:
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


def display_team_ranking(file_path: str, team_list: list[str]) -> None:
    """
    シーズン終了後のチーム順位を表示

    Args:
        - file_path : 読み込み対象となるExcelファイルのパス
        - team_list : チームのリスト

    Returns:
        - None
    """

    team_stats = []

    for team_name in team_list:
        wins = 0
        losses = 0

        pitchers, _ = database.Aquire_data(file_path, team_name)

        for p in pitchers:
            s = p.stats
            wins += s.get("wins", 0)
            losses += s.get("losses", 0)

        total_games = wins + losses
        win_rate = wins / total_games

        # チーム情報をリストに追加
        team_stats.append(
            {"name": team_name, "wins": wins, "losses": losses, "win_rate": win_rate}
        )

    # 勝率が高い順にソート
    ranking = sorted(team_stats, key=itemgetter("win_rate"), reverse=True)

    top_wins = ranking[0]["wins"]
    top_losses = ranking[0]["losses"]

    print("\n")
    for i, team in enumerate(ranking, 1):
        # ゲーム差の計算：((首位の勝 - 首位の負) - (当該チームの勝 - 当該チームの負)) / 2
        games_behind = ((top_wins - top_losses) - (team["wins"] - team["losses"])) / 2.0
        games_behind_str = f"{games_behind:4.1f}" if i != 1 else "---"

        # 整列して表示
        print(
            f"{i:>2}位  {team["name"]:<10} {team['wins']:>3}  {team['losses']:>3}  {team['win_rate']:>6.3f}  {games_behind_str:>8}"
        )


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
