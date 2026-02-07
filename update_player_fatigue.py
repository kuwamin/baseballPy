recovery_map = {'A': 40, 'B': 35, 'C': 30, 'D': 25, 'E': 20, 'F': 15, 'G': 10}
pos_fatigue_map = {
        '捕': 2.0, '遊': 1.7, '二': 1.5, '中': 1.2,
        '三': 1.1, '右': 1.0, '一': 1.0, '左': 0.8, '指': 0.6
    }

def update_player_fatigue_p(pitchers_1, pitcher_records_1, pitchers_2, pitcher_records_2):
    

    for team_pitchers in [pitchers_1, pitchers_2]:
        played_pitchers = [r[0] for r in (pitcher_records_1 if team_pitchers == pitchers_1 else pitcher_records_2)]
        for p in team_pitchers:
            # 共通：回復ステータスによる基礎回復値の算出
            base_recover = recovery_map.get(p.recovery, 15)
            
            if p in played_pitchers:
                # 1. 試合に出た投手
                pitch_load = p.stats.get('bf', 0) * 4
                p.fatigue_stamina += pitch_load
                # 蓄積疲労：負荷から回復値を微量差し引く（回復が高いと溜まりにくい）
                p.accumulated_fatigue += (pitch_load * 0.2) - (base_recover * 0.01)
            else:
                # 試合に出ていない投手
                # 減少体力の回復
                p.fatigue_stamina = max(0, p.fatigue_stamina - base_recover)
                
                if p.role == "先":
                    # 2. 試合に出ていない先発
                    p.accumulated_fatigue -= (base_recover * 0.2)
                else:
                    # 3. 試合に出ていない先発以外
                    p.accumulated_fatigue -= (base_recover * 0.02)
            
            # 最終的な下限処理
            p.accumulated_fatigue = max(0, p.accumulated_fatigue)


def update_player_fatigue_b(batters_1, starters_batter_1, batters_2, starters_batter_2):
    for team_batters, starters in [(batters_1, starters_batter_1), (batters_2, starters_batter_2)]:
        active_pos_map = {s[1]: s[0] for s in starters}
        
        for b in team_batters:
            base_recover = recovery_map.get(b.recovery, 15)
            
            if b in active_pos_map:
                # 1. 試合に出た野手
                active_pos = active_pos_map[b]
                fatigue_weight = pos_fatigue_map.get(active_pos, 1.0)
                # 加算分から回復分を引く（相殺）
                b.accumulated_fatigue += fatigue_weight - (base_recover * 0.01)
            else:
                # 2. 試合に出なかった野手
                b.accumulated_fatigue -= (base_recover * 0.05)
            
            # 最終的な下限処理
            b.accumulated_fatigue = max(0, b.accumulated_fatigue)