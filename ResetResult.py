import pandas as pd

def reset_result(file_path):
    """
    Excelのの成績列を0にリセットする
    """

    excel_data = pd.read_excel(file_path, sheet_name=None)  # sheet_name=None で全シート読み込み

    for sheet_name, df in excel_data.items():
        
        if sheet_name.endswith('_p'):   # 投手シートの場合（末尾が _p）
            # 「減少体力」以降の列をリセット対象にする
            if '減少体力' in df.columns:
                start_idx = df.columns.get_loc('減少体力')
                cols_to_reset = df.columns[start_idx:]
                df[cols_to_reset] = 0
        
        elif sheet_name.endswith('_b'): # 野手シートの場合（末尾が _b）
            # 「蓄積疲労」以降の列をリセット対象にする
            if '蓄積疲労' in df.columns:
                start_idx = df.columns.get_loc('蓄積疲労')
                cols_to_reset = df.columns[start_idx:]
                df[cols_to_reset] = 0
        
    # 保存
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for sheet_name, data in excel_data.items():
            data.to_excel(writer, sheet_name=sheet_name, index=False)