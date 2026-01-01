import pandas as pd

def test(file_path='test.xlsx'):
    """
    能力値を保持し、成績（スタッツ）列のみを0にリセットする
    """
    try:
        excel_data = pd.read_excel(file_path, sheet_name=None)

        for sheet_name, df in excel_data.items():
            # 投手シートの場合（末尾が _p と想定）
            if sheet_name.endswith('_p'):
                # 「登板数」以降の列をリセット対象にする
                if '登板数' in df.columns:
                    start_idx = df.columns.get_loc('登板数')
                    # 指定したインデックス以降のすべての列を0にする
                    cols_to_reset = df.columns[start_idx:]
                    df[cols_to_reset] = 0

            # 野手シートの場合（末尾が _b と想定）
            elif sheet_name.endswith('_b'):
                # 「試合数」以降の列をリセット対象にする
                if '試合数' in df.columns:
                    start_idx = df.columns.get_loc('試合数')
                    cols_to_reset = df.columns[start_idx:]
                    df[cols_to_reset] = 0
            
            print(f"Sheet '{sheet_name}' の成績エリアをリセットしました。")

        # 保存
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for sheet_name, data in excel_data.items():
                data.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"\n完了: {file_path} の能力値を維持し、成績のみリセットしました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")