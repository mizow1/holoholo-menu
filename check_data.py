import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Excelファイルを読み込む
xls = pd.ExcelFile('ホロホロタロット追加メニュー.xlsx', engine='openpyxl')

# メニューシート
menu_df = pd.read_excel(xls, sheet_name='メニュー')
print('=== メニューシート ===')
print(f'最大メニューID: {menu_df["メニューID"].max()}')
print(f'最小メニューID: {menu_df["メニューID"].min()}')
print(f'メニュー数: {menu_df["メニューID"].notna().sum()}')

# 小項目シート
item_df = pd.read_excel(xls, sheet_name='小項目')
print('\n=== 小項目シート ===')
print(f'総小項目数: {item_df["項目ID"].notna().sum()}')
# メニューIDごとの項目数
item_counts = item_df.groupby('メニューID')['項目ID'].count()
print(f'メニューごとの項目数の例（最初の5件）:')
print(item_counts.head())

# 結果シート
result_df = pd.read_excel(xls, sheet_name='結果')
print('\n=== 結果シート ===')
print(f'総結果数: {result_df["結果ID"].notna().sum()}')
print(f'使用カード番号の種類: {sorted(result_df["カード番号"].dropna().unique())}')
# メニューID 301の項目1のカード番号を確認
sample = result_df[(result_df['メニューID'] == 301) & (result_df['項目ID'] == 1)]
print(f'\nメニューID 301, 項目ID 1 のカード番号: {sorted(sample["カード番号"].dropna().unique())}')
print(f'結果数: {len(sample)}')
