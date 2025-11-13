import pandas as pd

# カードマスタデータを読み込む
df = pd.read_csv('card_name.csv', encoding='shift-jis')

# すべてのカード情報を表示
print("=" * 80)
print("カードマスタデータ（44枚）")
print("=" * 80)
for idx, row in df.iterrows():
    print(f"\nカードID: {row['カードID']}")
    print(f"名称: {row['名称']}")
    print(f"読み: {row['読み']}")
    print(f"キーワード: {row['キーワード']}")
    print(f"概要: {row['概要']}")
    print("-" * 80)
