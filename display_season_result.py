import AquireData
import DecideBatter
import DecideOrder
import GetSeasonStats

def display_season_result_b(file_path, teams, is_fatigue_considered):
    print("\n" + "="*20)
    print("  全チーム 最終打撃成績")
    print("="*20)

    for team_name in teams:
        print(f"\n--- {team_name} ベストオーダー ---")
        # 1. データ取得
        _, batters = AquireData.Aquire_data(file_path, team_name)
        
        # 2. 現在提示いただいた関数でスタメンと打順を決定
        starters_list = DecideBatter.decide_batter(batters, is_fatigue_considered)
        starters_batter = DecideOrder.decide_order(starters_list)
        
        # スタメンに選ばれた選手のオブジェクトを保持（控え判定用）
        starter_players = {p for pos, p in starters_batter}

        # チーム合計集計用変数
        t_ab, t_h, t_w, t_hbp, t_sf, t_tb = 0, 0, 0, 0, 0, 0

        # 3. スタメン9人の表示と集計
        for i, (pos, player) in enumerate(starters_batter, 1):
            stats_str = GetSeasonStats.get_batter_stats(player)
            print(f"{i}番 ({pos}) {player.name} [{stats_str}]")
            
            # 成績加算
            s = player.stats
            t_ab += s.get('ab', 0); t_h += s.get('hits', 0)
            t_w += s.get('walks', 0); t_hbp += s.get('hbp', 0)
            t_sf += s.get('sac_fly', 0)
            t_tb += (s.get('singles', 0) + s.get('doubles', 0)*2 + 
                     s.get('triples', 0)*3 + s.get('hr', 0)*4)

        # 4. 控え選手の表示と集計
        print(f"\n[{team_name} 控え選手]")
        for player in batters:
            # 全選手(batters)のうち、スタメン(starter_players)にいない人を抽出
            if player not in starter_players:
                stats_str = GetSeasonStats.get_batter_stats(player)
                print(f"控 ({player.position}) {player.name} [{stats_str}]")
                
                # 控え選手の成績もチーム全体の数字に合算
                s = player.stats
                t_ab += s.get('ab', 0); t_h += s.get('hits', 0)
                t_w += s.get('walks', 0); t_hbp += s.get('hbp', 0)
                t_sf += s.get('sac_fly', 0)
                t_tb += (s.get('singles', 0) + s.get('doubles', 0)*2 + 
                         s.get('triples', 0)*3 + s.get('hr', 0)*4)

        # 5. チームスタッツ算出（控えも含めた全選手合計）
        team_avg = t_h / t_ab if t_ab > 0 else 0
        denom_obp = (t_ab + t_w + t_hbp + t_sf)
        team_obp = (t_h + t_w + t_hbp) / denom_obp if denom_obp > 0 else 0
        team_slg = t_tb / t_ab if t_ab > 0 else 0
        
        print("-" * 30)
        print(f"チーム通算打率: {team_avg:.3f}  チーム通算OPS: {team_obp + team_slg:.3f}")

def display_season_result_p(file_path, teams):
    print("\n" + "="*20)
    print("  全チーム 全投手成績")
    print("="*20)

    for team_name in teams:
        print(f"\n[{team_name}]")
        # 野手データは不要なので _ で受ける
        pitchers, _ = AquireData.Aquire_data(file_path, team_name)
        
        t_outs, t_er = 0, 0

        # 投手は元々全員ループしているので控え投手も表示される
        for p in pitchers:
            s = p.stats
            bf = s.get('bf', 0)
            h = s.get('hits_allowed', 0)
            bb = s.get('walks_allowed', 0)
            hbp = s.get('hbp_allowed', 0)
            
            # この投手のアウト数を算出 (BF - 安打 - 四死球)
            p_outs = bf - (h + bb + hbp)
            
            stats_str = GetSeasonStats.get_pitcher_stats(p)
            # 詳細パラメータも含めて出力
            print(f"{p.role} {p.name} [{stats_str}] {p.speed}km {p.control} {p.stamina} {p.breaking_ball}")
            
            # チーム合計に加算
            t_outs += p_outs
            t_er += s.get('自責点', 0)

        # チーム防御率 = (合計自責点 * 27) / 合計アウト数
        team_era = (t_er * 27) / t_outs if t_outs > 0 else 0
        print(f"チーム通算防御率: {team_era:.2f}")