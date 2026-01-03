import pandas as pd

def output_exam(file_path, all_players):

    excel_data = pd.read_excel(file_path, sheet_name=None)
    mapping = {
        '試合数': 'games', '打席': 'pa', '打数': 'ab', '安打': 'hits',
        '単打': 'singles', '二塁打': 'doubles', '三塁打': 'triples',
        '本塁打': 'hr', '打点': 'rbi', '四球': 'walks', '死球': 'hbp',
        '三振': 'so', '得点圏打数': 'risp_pa', '得点圏安打': 'risp_hits'
    }

    for player in all_players:
        # 1. インスタンスが持っている情報の確認
        p_team = getattr(player, 'team', 'None')
        p_name = getattr(player, 'name', 'None')
        is_batter = hasattr(player, 'position')
        
        # 2. シート名の決定ロジックの確認
        target_sheet = ""
        if p_team == "test1":
             target_sheet = "test1_b" if is_batter else "test1_p"
        elif p_team == "test2":
             target_sheet = "test2_b" if is_batter else "test2_p"

        if target_sheet in excel_data:
            df = excel_data[target_sheet]
            # 3. 名前の照合確認
            condition = df['名前'] == p_name
            if condition.any():
                idx = df.index[condition][0]
                
                for excel_col, stats_key in mapping.items():
                    if excel_col in df.columns and stats_key in player.stats:
                        add_val = player.stats[stats_key]
                        if add_val > 0:
                            current_val = df.at[idx, excel_col]
                            if pd.isna(current_val): current_val = 0
                            df.at[idx, excel_col] = current_val + add_val

            else:
                print(f"  -> [失敗] {target_sheet} 内に名前 '{p_name}' が見つかりません")
        else:
            print(f"  -> [失敗] シート '{target_sheet}' がエクセルに存在しません")

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for sheet_name, df in excel_data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)