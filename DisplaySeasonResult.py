import AquireData
import DecideBatter
import DecideOrder
import DecidePitcher
import GetSeasonStats

def display_season_result_b(file_path, teams):
    print("\n" + "="*20)
    print("  全チーム 最終打撃成績")
    print("="*20)

    for team_name in teams:
        print(f"\n--- {team_name} ベストオーダー ---")
        _, batters = AquireData.Aquire_data(file_path, team_name)
        
        starters_list = DecideBatter.decide_batter(batters)
        starters_batter = DecideOrder.decide_order(starters_list)
        
        # チーム合計算出用
        t_ab, t_h, t_w, t_hbp, t_sf, t_tb = 0, 0, 0, 0, 0, 0

        for i, (pos, player) in enumerate(starters_batter, 1):
            stats_str = GetSeasonStats.get_batter_stats(player)
            print(f"{i}番 ({pos}) {player.name} [{stats_str}]")
            
            # 合計に加算
            s = player.stats
            t_ab += s.get('ab', 0)
            t_h += s.get('hits', 0)
            t_w += s.get('walks', 0)
            t_hbp += s.get('hbp', 0)
            t_sf += s.get('sac_fly', 0)
            # 長打率/OPS計算用：単打+2*二塁打+3*三塁打+4*本塁打
            t_tb += (s.get('singles', 0) + s.get('doubles', 0)*2 + 
                     s.get('triples', 0)*3 + s.get('hr', 0)*4)

        # チームスタッツ計算
        team_avg = t_h / t_ab if t_ab > 0 else 0
        # OBP = (H + BB + HBP) / (AB + BB + HBP + SF)
        denom_obp = (t_ab + t_w + t_hbp + t_sf)
        team_obp = (t_h + t_w + t_hbp) / denom_obp if denom_obp > 0 else 0
        team_slg = t_tb / t_ab if t_ab > 0 else 0
        
        print(f"チーム打率: {team_avg:.3f}  チームOPS: {team_obp + team_slg:.3f}")


def display_season_result_p(file_path, teams):
    print("\n" + "="*20)
    print("  全チーム 先発投手成績")
    print("="*20)

    for team_name in teams:
        print(f"\n[{team_name}]")
        pitchers, _ = AquireData.Aquire_data(file_path, team_name)
        
        t_outs, t_er = 0, 0

        for p in pitchers:
            s = p.stats
            bf = s.get('bf', 0)
            h = s.get('hits_allowed', 0)
            bb = s.get('walks_allowed', 0)
            hbp = s.get('hbp_allowed', 0)
            
            # この投手のアウト数を算出
            p_outs = bf - (h + bb + hbp)
            
            stats_str = GetSeasonStats.get_pitcher_stats(p)
            print(f"{p.role} {p.name} [{stats_str}] {p.speed}km {p.control} {p.stamina} {p.breaking_ball}")
            
            # チーム合計に加算
            t_outs += p_outs
            t_er += s.get('自責点', 0)

        # チーム防御率 = (合計自責点 * 27) / 合計アウト数
        team_era = (t_er * 27) / t_outs if t_outs > 0 else 0
        print(f"チーム防御率: {team_era:.2f}")