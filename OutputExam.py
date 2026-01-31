import pandas as pd

def output_exam(file_path, team_name_1, team_name_2, all_players):
    """
    試合結果と疲労度をExcelに保存する
    """
    excel_data = pd.read_excel(file_path, sheet_name=None)
    
    mapping = {
        # 野手項目
        '試合数': 'games', '打席': 'pa', '打数': 'ab', '安打': 'hits',
        '単打': 'singles', '二塁打': 'doubles', '三塁打': 'triples',
        '本塁打': 'hr', '打点': 'rbi', '四球': 'walks', '死球': 'hbp',
        '三振': 'so', '得点圏打数': 'risp_ab', '得点圏安打': 'risp_hits',
        
        # 投手項目
        '登板数': 'games', '先発数': 'starts', '勝利': 'wins', '敗北': 'losses', 
        'セーブ': 'saves', 'ホールド': 'holds', '完投': 'complete_games', 
        '完封': 'shutouts', '打者数': 'bf', '被安打': 'hits_allowed',
        '被本塁打': 'hr_allowed', '与四球': 'walks_allowed', '与死球': 'hbp_allowed',
        '奪三振': 'strikeouts', '失点': '失点', '自責点': '自責点', 'QS': 'qs', 'HQS': 'hqs',
        '得点圏被打数': 'risp_bf', '得点圏被安打': 'risp_hits_allowed'
    }

    for player in all_players:
        p_team = getattr(player, 'team', 'None')
        p_name = getattr(player, 'name', 'None')
        is_batter = hasattr(player, 'position')
        
        target_sheet = ""
        if p_team == team_name_1:
             target_sheet = team_name_1 + "_b" if is_batter else team_name_1 + "_p"
        elif p_team == team_name_2:
             target_sheet = team_name_2 + "_b" if is_batter else team_name_2 + "_p"

        if target_sheet in excel_data:
            df = excel_data[target_sheet]
            condition = df['名前'] == p_name
            if condition.any():
                idx = df.index[condition][0]
                
                # --- 1. 通常項目の加算 ---
                for excel_col, stats_key in mapping.items():
                    if excel_col in df.columns and stats_key in player.stats:
                        add_val = player.stats[stats_key]
                        if add_val > 0:
                            current_val = df.at[idx, excel_col]
                            if pd.isna(current_val): current_val = 0
                            df.at[idx, excel_col] = current_val + add_val

                # --- 2. 投手特有：イニング数の更新ロジック ---
                if not is_batter and 'outs_pitched' in player.stats:
                    new_outs = player.stats['outs_pitched']
                    if new_outs > 0:
                        current_inning_val = df.at[idx, 'イニング数']
                        if pd.isna(current_inning_val): current_inning_val = 0.0
                        
                        curr_whole = int(current_inning_val)
                        curr_frac = round((current_inning_val - curr_whole) * 10)
                        total_outs = (curr_whole * 3) + curr_frac + new_outs
                        
                        new_whole = total_outs // 3
                        new_frac = total_outs % 3
                        df.at[idx, 'イニング数'] = new_whole + (new_frac / 10.0)

                # --- 3. 疲労度の更新ロジック（上書き） ---
                if not is_batter:
                    # playerオブジェクトから現在の疲労度を取得
                    # game関数で計算済みの値をそのまま代入（上書き）する
                    if hasattr(player, 'fatigue_stamina') and '減少体力' in df.columns:
                        df.at[idx, '減少体力'] = player.fatigue_stamina
                    
                    if hasattr(player, 'accumulated_fatigue') and '蓄積疲労' in df.columns:
                        df.at[idx, '蓄積疲労'] = player.accumulated_fatigue
                        
            else:
                print(f"  -> [失敗] {target_sheet} 内に名前 '{p_name}' が見つかりません")
        else:
            # チーム名決定ロジックとの兼ね合いで、対象外チームの処理はスキップされる仕様
            pass

    # 全シートをExcelファイルに書き戻す
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for sheet_name, df in excel_data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)