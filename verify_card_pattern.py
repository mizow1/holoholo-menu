import re

# menu_1067.sqlを検証
with open('menu_1067.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# mana_cardのINSERT文から result_id と card_id を抽出
pattern = r'\(1067, \d+, (\d+), (\d+)\)'
matches = re.findall(pattern, content)

# パターンごとにカードを整理
patterns = {1: [], 2: [], 3: [], 4: []}
for result_id, card_id in matches:
    # result_idの下2桁がパターン番号
    pattern_num = int(result_id[-2:])
    patterns[pattern_num].append(int(card_id))

# 各パターンで重複チェック
print("menu_1067.sql のカードパターン検証結果:\n")
all_ok = True
for pattern_num in range(1, 5):
    cards = patterns[pattern_num]
    unique_cards = set(cards)
    is_ok = len(cards) == len(unique_cards)
    status = "✓ OK" if is_ok else "✗ NG (重複あり)"
    
    print(f"パターン{pattern_num:02d}: {cards} → {status}")
    
    if not is_ok:
        all_ok = False
        # 重複しているカードを表示
        duplicates = [c for c in unique_cards if cards.count(c) > 1]
        print(f"  重複カード: {duplicates}")

print(f"\n総合結果: {'✓ 全パターンOK' if all_ok else '✗ 重複あり'}")
