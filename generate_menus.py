import pandas as pd
from datetime import datetime, timedelta
import random

# カードデータを読み込む
card_df = pd.read_csv('card_name.csv', encoding='shift-jis')
category_df = pd.read_csv('category_id.csv', encoding='utf-8')

# カテゴリー別のメニューテンプレート
menu_templates = {
    1: {  # 両思い
        'name': 'あの人との愛を深める方法',
        'catch': '二人の愛をもっと深めたい',
        'caption': 'あの人との関係をさらに深めるには？　ハワイアンタロットが、二人の愛を育むヒントをお伝えします。',
        'items': [
            '今のあの人の気持ち',
            '二人の関係を深めるために大切なこと',
            'これからの二人の未来',
            'あなたが心がけるべきこと'
        ]
    },
    2: {  # 片思い
        'name': 'あの人の本当の気持ち',
        'catch': 'あの人は私をどう思っている？',
        'caption': 'あの人の本心を知りたい…　ハワイアンタロットが、あの人の隠された気持ちを明らかにします。',
        'items': [
            '今のあの人の気持ち',
            'あの人があなたに抱いている印象',
            '二人の関係が進展する可能性',
            'あなたが取るべきアプローチ'
        ]
    },
    3: {  # 相手の気持ち
        'name': 'あの人の本音を知る',
        'catch': 'あの人の本当の気持ちは？',
        'caption': 'あの人は何を考えているの？　ハワイアンタロットが、あの人の本音を読み解きます。',
        'items': [
            'あの人が今感じていること',
            'あの人があなたに望んでいること',
            'あの人の隠れた感情',
            'これから二人はどうなる？'
        ]
    },
    4: {  # 不倫
        'name': 'この恋の未来と決断',
        'catch': 'この関係をどうすべき？',
        'caption': '複雑な関係の中で悩むあなたへ。ハワイアンタロットが、この恋の行方と最善の選択を示します。',
        'items': [
            'あの人の本当の気持ち',
            'この関係の未来',
            'あなたが直面する課題',
            '幸せになるための選択'
        ]
    },
    5: {  # 夜の相性
        'name': '二人の深い絆と相性',
        'catch': '心も体も通じ合える？',
        'caption': '二人の深いレベルでの相性は？　ハワイアンタロットが、二人の特別な絆を鑑定します。',
        'items': [
            '二人の肉体的な相性',
            '二人の心の繋がり',
            '関係を深めるポイント',
            'より満たされる関係になるには'
        ]
    },
    6: {  # 結婚
        'name': 'あの人との結婚運',
        'catch': 'あの人と結婚できる？',
        'caption': 'あの人との結婚は実現する？　ハワイアンタロットが、二人の結婚運を詳しく鑑定します。',
        'items': [
            'あの人の結婚への意識',
            '二人が結婚に至る可能性',
            '結婚に向けて乗り越えるべき課題',
            '幸せな結婚のためにすべきこと'
        ]
    },
    7: {  # 人生
        'name': 'あなたの人生の転機',
        'catch': '人生の岐路に立つあなたへ',
        'caption': '人生の大きな選択を前にしたあなたへ。ハワイアンタロットが、最良の道を照らします。',
        'items': [
            '今のあなたが置かれている状況',
            'これから訪れる転機',
            'あなたが選ぶべき道',
            '未来を切り拓くためのアドバイス'
        ]
    },
    8: {  # 仕事
        'name': 'あなたの仕事運と成功',
        'catch': '仕事で成功するには？',
        'caption': 'キャリアアップしたい、成功したい…　ハワイアンタロットが、あなたの仕事運を鑑定します。',
        'items': [
            '今のあなたの仕事運',
            '成功のために必要なこと',
            'あなたの才能と強み',
            'キャリアアップのタイミング'
        ]
    },
    9: {  # 復縁
        'name': 'あの人との復縁の可能性',
        'catch': 'もう一度やり直せる？',
        'caption': 'あの人ともう一度…　ハワイアンタロットが、復縁の可能性と最善の行動を示します。',
        'items': [
            '別れた後のあの人の気持ち',
            '復縁できる可能性',
            '復縁を妨げているもの',
            '復縁するためにすべきこと'
        ]
    },
    10: {  # 出会い
        'name': '運命の出会いはいつ？',
        'catch': '素敵な出会いが欲しい',
        'caption': '運命の人との出会いはいつ？　ハワイアンタロットが、あなたの恋愛運と出会いを鑑定します。',
        'items': [
            'これから訪れる出会い',
            '運命の人の特徴',
            '出会いのタイミングとチャンス',
            '出会いを引き寄せるためにすべきこと'
        ]
    }
}

# カード選定（各カテゴリーに適したカードを事前に定義）
category_cards = {
    1: [14, 24, 36, 38, 4, 9, 23, 40, 3, 22, 27, 37, 12, 26, 42, 43],  # 両思い
    2: [14, 24, 3, 23, 40, 9, 36, 38, 22, 4, 27, 42, 12, 26, 37, 43],  # 片思い
    3: [14, 24, 36, 9, 40, 23, 4, 38, 12, 3, 22, 27, 26, 42, 37, 43],  # 相手の気持ち
    4: [14, 24, 3, 22, 12, 26, 27, 37, 23, 4, 9, 40, 36, 38, 42, 43],  # 不倫
    5: [14, 3, 36, 24, 23, 4, 9, 22, 40, 38, 12, 26, 27, 42, 37, 43],  # 夜の相性
    6: [14, 24, 36, 38, 3, 40, 12, 9, 23, 4, 22, 26, 27, 37, 42, 43],  # 結婚
    7: [1, 7, 18, 42, 40, 8, 9, 34, 23, 4, 14, 24, 12, 26, 27, 43],    # 人生
    8: [9, 8, 40, 34, 4, 23, 35, 33, 1, 7, 14, 24, 22, 12, 26, 43],    # 仕事
    9: [14, 24, 3, 9, 36, 38, 12, 26, 22, 4, 23, 40, 27, 37, 42, 43],  # 復縁
    10: [14, 23, 40, 42, 34, 4, 9, 24, 36, 38, 3, 12, 22, 26, 27, 43]  # 出会い
}

def get_card_name(card_id):
    """カードIDから名称を取得"""
    card = card_df[card_df['カードID'] == card_id]
    if len(card) > 0:
        return card.iloc[0]['名称']
    return ''

def get_card_keyword(card_id):
    """カードIDからキーワードを取得"""
    card = card_df[card_df['カードID'] == card_id]
    if len(card) > 0:
        return card.iloc[0]['キーワード']
    return ''

def get_card_summary(card_id):
    """カードIDから概要を取得"""
    card = card_df[card_df['カードID'] == card_id]
    if len(card) > 0:
        return card.iloc[0]['概要']
    return ''

def escape_sql_string(s):
    """SQL文字列のエスケープ処理"""
    return s.replace("'", "''")

def generate_result_text(card_id, item_text, category_id):
    """鑑定文を生成"""
    card_name = get_card_name(card_id)
    card_keyword = get_card_keyword(card_id)
    card_summary = get_card_summary(card_id)

    # カードの紹介部分のバリエーション（ハッシュ値でパターン選択）
    pattern_num = (card_id + len(item_text)) % 5

    if pattern_num == 0:
        intro = f"【{card_name}】のカードが出ました。このカードは「{card_summary}」を意味します。"
    elif pattern_num == 1:
        intro = f"【{card_name}】のカードが出ました。カードのテーマは「{card_summary}」です。"
    elif pattern_num == 2:
        intro = f"【{card_name}】のカードが示されました。「{card_summary}」というメッセージが込められています。"
    elif pattern_num == 3:
        intro = f"出たカードは【{card_name}】。{card_summary}ことを示す重要なカードです。"
    else:
        intro = f"【{card_name}】のカードが出ました。{card_name}は{card_keyword}を象徴し、{card_summary}ことを教えてくれます。"

    # カテゴリーと項目に応じた具体的な内容を生成
    if '気持ち' in item_text:
        variations = [
            f"{item_text}について、{card_keyword}のエネルギーが強く働いています。あの人は今、{card_keyword}に関わる感情を抱いているようです。誠実に向き合うことで、二人の関係は良い方向へ進んでいくでしょう。",
            f"{item_text}に関して、カードは{card_keyword}の影響を示しています。{card_keyword}という気持ちがあの人の心に芽生えています。お互いの気持ちを大切にすることで、より深い絆が育まれます。",
            f"{item_text}を見ると、{card_keyword}というキーワードが浮かび上がります。あの人の心には{card_keyword}に関連する思いがあります。素直な気持ちで接することが、関係を深める鍵となるでしょう。"
        ]
    elif '相性' in item_text or '関係' in item_text:
        variations = [
            f"{item_text}において、{card_keyword}が重要な鍵となります。二人の間には{card_keyword}のエネルギーが流れています。お互いを尊重し合うことで、より良い関係を築いていけるでしょう。",
            f"二人の{item_text}には、{card_keyword}という要素が深く関わっています。{card_keyword}を意識することで、関係はさらに調和のとれたものになります。",
            f"{item_text}を見ると、{card_keyword}がテーマとなっています。この{card_keyword}を大切にすることで、二人の絆はより強固なものとなるでしょう。"
        ]
    elif '未来' in item_text or 'これから' in item_text or '訪れる' in item_text or 'タイミング' in item_text:
        variations = [
            f"{item_text}には、{card_keyword}に関わる出来事が待っています。{card_keyword}のエネルギーを感じたら、それは大切なサインです。前向きに受け止めることで、幸せな未来へと繋がっていきます。",
            f"{item_text}について、カードは{card_keyword}の訪れを告げています。{card_keyword}というテーマに心を開くことで、新しい展開が生まれるでしょう。",
            f"{item_text}には{card_keyword}のエネルギーが流れ込んできます。この{card_keyword}を受け入れることで、望む方向へと進んでいけるはずです。"
        ]
    elif 'アドバイス' in item_text or 'すべき' in item_text or '心がけ' in item_text or '引き寄せる' in item_text:
        variations = [
            f"{item_text}として、{card_keyword}を意識することが大切です。日々の中で{card_keyword}を心がけることで、道は自然と開けていきます。自分を信じて一歩ずつ進んでいきましょう。",
            f"{item_text}は、{card_keyword}がキーワードとなります。{card_keyword}の気持ちを持って行動することで、望む結果へと近づいていけるでしょう。",
            f"{item_text}には、{card_keyword}という視点が必要です。{card_keyword}を大切にすることで、あなたの願いは現実へと近づいていきます。"
        ]
    elif '特徴' in item_text or '印象' in item_text or 'どんな' in item_text:
        variations = [
            f"{item_text}を見ると、{card_keyword}というキーワードが浮かび上がります。{card_keyword}に関連する要素が、大きな特徴となっているようです。",
            f"{item_text}には、{card_keyword}という性質が強く表れています。この{card_keyword}を理解することで、より深い洞察が得られるでしょう。",
            f"カードが示す{item_text}は、{card_keyword}がテーマとなっています。{card_keyword}という観点から捉えることで、本質が見えてきます。"
        ]
    else:
        variations = [
            f"{item_text}について、{card_keyword}という視点から捉えることが重要です。{card_keyword}のエネルギーを意識することで、新たな気づきが得られるはずです。",
            f"{item_text}には{card_keyword}が深く関わっています。{card_keyword}を理解し、受け入れることで、状況は好転していくでしょう。",
            f"{item_text}を考える上で、{card_keyword}がキーとなります。{card_keyword}の本質を見つめることで、答えが見つかるはずです。"
        ]

    # バリエーションの中から選択（ハッシュ値で決定）
    variation_idx = (card_id * 3 + len(item_text) * 7) % len(variations)
    main_text = variations[variation_idx]

    return intro + main_text

def calculate_start_date(contents_id):
    """公開日を計算（contents_id=1042が2026-01-01基準）"""
    base_date = datetime(2026, 1, 1)
    base_id = 1042
    days_diff = contents_id - base_id
    start_date = base_date + timedelta(days=days_diff)
    return start_date.strftime('%Y-%m-%d %H:%M:%S')

def generate_menu_sql(contents_id):
    """メニュー用SQLファイルを生成"""
    # カテゴリーをローテーション（1-10をループ）
    category_id = ((contents_id - 1061) % 10) + 1

    template = menu_templates[category_id]
    menu_name = template['name']
    catch = template['catch']
    caption = template['caption']
    items = template['items']

    # 公開日を計算
    start_date = calculate_start_date(contents_id)

    # このカテゴリー用のカード一覧
    available_cards = category_cards[category_id]

    # SQL生成開始
    sql = f"""-- ========================================
-- 占いメニュー: {menu_name}
-- Contents ID: {contents_id}
-- 作成日: {datetime.now().strftime('%Y-%m-%d')}
-- ========================================

-- 1. mana_contentsテーブルに追加
INSERT INTO flowt_seimei.mana_contents (contents_id, name, catch, caption, category, tag_1, tag_2, tag_3, tag_4, tag_5, start_date) VALUES
({contents_id}, '{escape_sql_string(menu_name)}', '{escape_sql_string(catch)}', '{escape_sql_string(caption)}', {category_id}, NULL, NULL, NULL, NULL, NULL, '{start_date}');

-- 2. mana_menuテーブルに追加
INSERT INTO flowt_seimei.mana_menu (contents_id, menu_id, name) VALUES
"""

    # メニュー項目を追加
    menu_items = []
    for i, item_name in enumerate(items, 1):
        menu_id = int(f"{contents_id}{i:02d}")
        menu_items.append(f"({contents_id}, {menu_id}, '{escape_sql_string(item_name)}')")

    sql += ',\n'.join(menu_items) + ';\n\n'

    # 結果テーブルを追加
    sql += "-- 3. mana_resultテーブルに追加\n"
    sql += "INSERT INTO flowt_seimei.mana_result (contents_id, menu_id, result_id, body) VALUES\n"

    result_items = []
    card_items = []

    # 各結果パターンで使用するカードを事前に決定（重複を避けるため）
    num_patterns = 4  # 各小項目に4つの結果パターン
    num_items = len(items)  # 小項目の数

    # 各パターンごとに使用するカードを選定（パターン内で重複なし）
    pattern_cards = {}
    for pattern_num in range(1, num_patterns + 1):
        # このパターンで使用するカード（小項目の数だけ必要）
        # available_cardsをシャッフルして先頭からnum_items個取得
        shuffled_cards = available_cards.copy()
        # contents_idとpattern_numでシードを設定（再現性のため）
        random.seed(contents_id * 100 + pattern_num)
        random.shuffle(shuffled_cards)
        pattern_cards[pattern_num] = shuffled_cards[:num_items]

    # 各項目に4つの結果を生成
    for i, item_name in enumerate(items, 1):
        menu_id = int(f"{contents_id}{i:02d}")

        for j in range(1, num_patterns + 1):
            result_id = int(f"{contents_id}{i:02d}{j:02d}")

            # このパターンの、この項目のカードを選択
            # i-1: 項目のインデックス（0始まり）
            card_id = pattern_cards[j][i - 1]

            # 鑑定文を生成
            result_body = generate_result_text(card_id, item_name, category_id)

            result_items.append(f"({contents_id}, {menu_id}, {result_id}, '{escape_sql_string(result_body)}')")
            card_items.append((contents_id, menu_id, result_id, card_id))

    sql += ',\n'.join(result_items) + ';\n\n'

    # カードテーブルを追加
    sql += "-- 4. mana_cardテーブルに追加\n"
    sql += "INSERT INTO flowt_seimei.mana_card (contents_id, menu_id, result_id, body) VALUES\n"

    card_sql_items = []
    for contents_id, menu_id, result_id, card_id in card_items:
        card_sql_items.append(f"({contents_id}, {menu_id}, {result_id}, {card_id})")

    sql += ',\n'.join(card_sql_items) + ';\n\n'

    # 確認クエリを追加
    sql += f"""-- ========================================
-- インポート完了
-- ========================================
-- 確認クエリ:
-- SELECT * FROM mana_contents WHERE contents_id = {contents_id};
-- SELECT * FROM mana_menu WHERE contents_id = {contents_id};
-- SELECT * FROM mana_result WHERE contents_id = {contents_id};
-- SELECT * FROM mana_card WHERE contents_id = {contents_id};
"""

    return sql

# メイン処理
if __name__ == '__main__':
    print('メニュー生成を開始します...')

    for contents_id in range(1061, 1081):
        sql_content = generate_menu_sql(contents_id)

        filename = f'menu_{contents_id}.sql'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(sql_content)

        print(f'生成完了: {filename}')

    print('\n全20個のメニューSQLファイルを生成しました！')
