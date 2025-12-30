# ライブラリインポート
from openpyxl import Workbook
from openpyxl import load_workbook


# テストコード
def test():

    file_path = 'test.xlsx'

    wb = load_workbook(filename=file_path, data_only=True)

    sheet_p = wb['test_p']
    sheet_b = wb['test_b']


    for row in sheet_p:
        values = [cell.value for cell in row]
        print(values)

    for row in sheet_b:
        values = [cell.value for cell in row]
        print(values)