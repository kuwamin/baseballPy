import pandas as pd


def reset_result(file_path):
    """
    Excelの成績列を0にリセットする
    """

    excel_data = pd.read_excel(
        file_path, sheet_name=None
    )  # sheet_name=None で全シート読み込み

    # リセット対象列の定義
    p_cols = [
        "減少体力",
        "蓄積疲労",
        "登板数",
        "先発数",
        "勝利",
        "敗北",
        "セーブ",
        "ホールド",
        "イニング数",
        "完投",
        "完封",
        "打者数",
        "奪三振",
        "与四球",
        "与死球",
        "被本塁打",
        "被安打",
        "失点",
        "自責点",
        "QS",
        "HQS",
        "得点圏被打数",
        "得点圏被安打",
    ]

    b_cols = [
        "蓄積疲労",
        "試合数",
        "打席",
        "打数",
        "安打",
        "単打",
        "二塁打",
        "三塁打",
        "本塁打",
        "打点",
        "四球",
        "死球",
        "三振",
        "犠打",
        "犠飛",
        "盗塁成功",
        "盗塁死",
        "併殺打",
        "得点圏打数",
        "得点圏安打",
    ]

    for sheet_name, df in excel_data.items():

        if sheet_name.endswith("_p"):  # 投手シートの場合（末尾が _p）
            # リストにある列のうち、シートに存在する列のみを0リセット
            cols_to_reset = [c for c in p_cols if c in df.columns]
            df[cols_to_reset] = 0

        elif sheet_name.endswith("_b"):  # 野手シートの場合（末尾が _b）
            # リストにある列のうち、シートに存在する列のみを0リセット
            cols_to_reset = [c for c in b_cols if c in df.columns]
            df[cols_to_reset] = 0

    # 保存
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        for sheet_name, data in excel_data.items():
            data.to_excel(writer, sheet_name=sheet_name, index=False)
