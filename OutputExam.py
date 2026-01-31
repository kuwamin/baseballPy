import pandas as pd

def output_exam(file_path, team_name_1, team_name_2, all_players):
    excel_data = pd.read_excel(file_path, sheet_name=None)
    
    mapping = {
        '試合数': 'games', '打席': 'pa', '打数': 'ab', '安打': 'hits',
        '単打': 'singles', '二塁打': 'doubles', '三塁打': 'triples',
        '本塁打': 'hr', '打点': 'rbi', '四球': 'walks', '死球': 'hbp',
        '三振': 'so', '得点圏打数': 'risp_ab', '得点圏安打': 'risp_hits',
        '登板数': 'games', '先発数': 'starts', '勝利': 'wins', '敗北': 'losses', 
        'セーブ': 'saves', 'ホールド': 'holds', '完投': 'complete_games', 
        '完封': 'shutouts', '打者数': 'bf', '被安打': 'hits_allowed',
        '被本塁打': 'hr_allowed', '与四球': 'walks_allowed', '与死球': 'hbp_allowed',
        '奪三振': 'strikeouts', '失点': '失点', '自責点': '自責点', 'QS': 'qs', 'HQS': 'hqs',
        '得点圏被打数': 'risp_bf', '得点圏被安打': 'risp_hits_allowed'
    }

    for player in all_players:
        is_batter = hasattr(player, 'position')
        t_name = team_name_1 if player.team == team_name_1 else team_name_2
        target_sheet = f"{t_name}_{'b' if is_batter else 'p'}"

        if target_sheet in excel_data:
            df = excel_data[target_sheet]
            idx_list = df.index[df['名前'] == player.name]
            if not idx_list.empty:
                idx = idx_list[0]
                
                # 1. 通常項目の加算
                for col, key in mapping.items():
                    if col in df.columns and key in player.stats:
                        val = player.stats[key]
                        if val > 0:
                            df.at[idx, col] = (0 if pd.isna(df.at[idx, col]) else df.at[idx, col]) + val

                # 2. 蓄積疲労の更新 (投手・野手共通)
                df.at[idx, '蓄積疲労'] = player.accumulated_fatigue

                # 3. 投手専用の更新
                if not is_batter:
                    df.at[idx, '減少体力'] = player.fatigue_stamina
                    
                    if 'outs_pitched' in player.stats and player.stats['outs_pitched'] > 0:
                        cur = 0.0 if pd.isna(df.at[idx, 'イニング数']) else df.at[idx, 'イニング数']
                        total_outs = int(cur) * 3 + round((cur - int(cur)) * 10) + player.stats['outs_pitched']
                        df.at[idx, 'イニング数'] = (total_outs // 3) + (total_outs % 3 / 10.0)

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for sheet_name, df in excel_data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)