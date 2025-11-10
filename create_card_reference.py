import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# カード情報を読み込む
card_df = pd.read_csv('card_name.csv', encoding='shift-jis')

# カードクイックリファレンスを作成
output = []
output.append('# ハワイアンタロットカード クイックリファレンス\n')
output.append('メニュー作成時にカード選定の参考にしてください。\n\n')

# ジャンル別にカードを分類
categories = {
    '恋愛・人間関係': ['愛', '結合', '関係', 'コミュニケーション', '同情', '変容', '大切'],
    '仕事・成長': ['リーダーシップ', '収穫', '前進', 'トリックスター', '創造', '力を与えること'],
    '精神・内面': ['ミステリー', '無意識', '秘密', 'インスピレーション', '黙想', '意思', '物語'],
    '導き・方向性': ['導き', '勝利', 'タイミング', '移動', '反映'],
    '変化・解放': ['崩壊', '解放', '浄化', '罠', '別離'],
    '基盤・安定': ['基盤', '滋養', '養い', '持続', '尊敬'],
    '献身・儀式': ['献身', '供物', '償い', 'イニシエーション'],
    '特殊': ['イリュージョン', '隆起', '静けさの愛撫', '苦闘・全体']
}

# ジャンル別にカードをリスト化
output.append('## カテゴリー別カード一覧\n\n')
for category, keywords in categories.items():
    output.append(f'### {category}\n\n')
    output.append('| ID | カード名 | 読み | キーワード | 概要 |\n')
    output.append('|----|---------|------|-----------|------|\n')

    for keyword in keywords:
        matching = card_df[card_df['キーワード'].str.contains(keyword, na=False)]
        for _, row in matching.iterrows():
            card_id = int(row['カードID'])
            name = row['名称']
            yomi = row['読み']
            kw = row['キーワード']
            summary = row['概要'][:30] + '...' if len(str(row['概要'])) > 30 else row['概要']
            output.append(f'| {card_id} | {name} | {yomi} | {kw} | {summary} |\n')

    output.append('\n')

# 全カード一覧
output.append('---\n\n')
output.append('## 全カード一覧（ID順）\n\n')
output.append('| ID | カード名 | 読み | キーワード |\n')
output.append('|----|---------|------|----------|\n')

for _, row in card_df.iterrows():
    card_id = int(row['カードID'])
    name = row['名称']
    yomi = row['読み']
    keyword = row['キーワード']
    output.append(f'| {card_id} | {name} | {yomi} | {keyword} |\n')

# ファイルに書き込み
with open('CARD_REFERENCE.md', 'w', encoding='utf-8') as f:
    f.writelines(output)

print('✓ CARD_REFERENCE.md を作成しました！')
print('  44枚のハワイアンタロットカードをカテゴリー別に整理しました。')
