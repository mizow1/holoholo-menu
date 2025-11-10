import pandas as pd

# Excelファイル読み込み
df = pd.read_excel('ホロホロタロット追加メニュー.xlsx', sheet_name='メニュー')

# カラム名を確認
print('カラム名:', df.columns.tolist())
print()

# メニューIDを数値に変換
df['メニューID'] = pd.to_numeric(df['メニューID'], errors='coerce')

# 最新のメニューIDを確認
max_id = df['メニューID'].max()
print(f'最新のメニューID: {max_id}')

# メニュー1044の確認
menu_1044 = df[df['メニューID'] == 1044]
if not menu_1044.empty:
    print('\nメニュー1044は既に存在します:')
    print(menu_1044.to_string())
else:
    print('\nメニュー1044は存在しません。新規作成可能です。')

# 最近のメニューを表示
print('\n最近のメニュー（上位5件）:')
recent = df.nlargest(5, 'メニューID')
print(recent.to_string())
