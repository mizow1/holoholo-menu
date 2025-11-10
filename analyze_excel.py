import pandas as pd
import sys

# UTF-8で出力
sys.stdout.reconfigure(encoding='utf-8')

# Excelファイルを読み込む
xls = pd.ExcelFile('ホロホロタロット追加メニュー.xlsx', engine='openpyxl')

print('シート名:', xls.sheet_names)
print()

for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name)
    print(f'=== {sheet_name} シート ===')
    print(f'行数: {len(df)}, 列数: {len(df.columns)}')
    print(f'列名: {list(df.columns)}')
    print(f'\n最初の5行:')
    print(df.head().to_string())
    print('\n' + '='*80 + '\n')
