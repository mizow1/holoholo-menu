import pandas as pd

# カードデータを読み込む
df = pd.read_csv('card_name.csv', encoding='shift-jis')

print('カード数:', len(df))
print('\nカード一覧:')
print(df[['カードID', '名称', '読み', 'キーワード']].head(20).to_string(index=False))
