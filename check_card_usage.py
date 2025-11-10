import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Excelファイルを読み込む
xls = pd.ExcelFile('ホロホロタロット追加メニュー.xlsx', engine='openpyxl')
result_df = pd.read_excel(xls, sheet_name='結果')
card_df = pd.read_csv('card_name.csv', encoding='shift-jis')

print('=== カード情報一覧 ===')
print(card_df[['カードID', '名称', '読み', 'キーワード']].to_string())

print('\n\n=== 既存メニューのカード使用例 ===')
# メニューID 301の例
menu_301 = result_df[result_df['メニューID'] == 301]
for item_id in [1, 2, 3]:
    item_data = menu_301[menu_301['項目ID'] == item_id]
    cards = sorted(item_data['カード番号'].dropna().unique())
    print(f'\nメニューID 301, 項目 {item_id}: カード番号 {cards}')
    for card_num in cards:
        card_info = card_df[card_df['カードID'] == card_num]
        if not card_info.empty:
            print(f'  - {int(card_num)}: {card_info.iloc[0]["名称"]} ({card_info.iloc[0]["読み"]}) - {card_info.iloc[0]["キーワード"]}')

print('\n\n=== 恋愛に適したカード候補 ===')
love_keywords = ['愛', '結合', 'パートナー', 'コミュニケーション', 'インスピレーション', '関係', '調和']
for keyword in love_keywords:
    matching = card_df[card_df['キーワード'].str.contains(keyword, na=False)]
    if not matching.empty:
        for _, row in matching.iterrows():
            print(f'{int(row["カードID"])}: {row["名称"]} ({row["読み"]}) - {row["キーワード"]}')
