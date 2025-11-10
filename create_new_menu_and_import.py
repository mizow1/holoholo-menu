# -*- coding: utf-8 -*-
import sys
import mysql.connector
import pandas as pd
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# config.phpから接続情報を読み込む
with open('config.php', 'r', encoding='utf-8') as f:
    content = f.read()
    # DB_NAMEを抽出
    import re
    db_name = re.search(r"define\('DB_NAME', '(.+?)'\)", content).group(1)
    db_host = re.search(r"define\('DB_HOST', '(.+?)'\)", content).group(1)
    db_user = re.search(r"define\('DB_USER', '(.+?)'\)", content).group(1)
    db_password = re.search(r"define\('DB_PASSWORD', '(.+?)'\)", content).group(1)

# DB接続情報
DB_CONFIG = {
    'host': db_host,
    'user': db_user,
    'password': db_password,
    'database': db_name,
    'charset': 'utf8mb4'
}

# 新メニューの設定
# 既存のcontents_idから次のIDを決定（1001-1008, 1043が使用済み）
NEW_CONTENTS_ID = 1009
MENU_NAME = '【2025年】あなたの運命の転機と訪れる幸運'
CAPTION = '2025年、あなたに訪れる運命の転機とチャンスを、ハワイアンタロットで鑑定します。'
CATEGORY = 7  # 人生・運勢
START_DATE = '2025-01-15 00:00:00'

# 小項目（メニュー）
MENUS = [
    '2025年上半期、あなたに訪れる最大の転機は？',
    'その転機があなたにもたらす幸運と変化',
    '2025年、あなたが手にする最高の結果'
]

# 各メニューのID
MENU_IDS = [
    NEW_CONTENTS_ID * 100 + 1,  # 100901
    NEW_CONTENTS_ID * 100 + 2,  # 100902
    NEW_CONTENTS_ID * 100 + 3   # 100903
]

# 各メニューに使用するカード番号（4枚ずつ）
# カードIDはcard_name.csvを参照（1-44）
CARD_SELECTIONS = [
    [1, 14, 22, 42],   # メニュー1: I'O, ALOHA, PELE, ANUENUE
    [7, 18, 23, 34],   # メニュー2: HUNA, PUEO, LAKA, PUA
    [4, 9, 12, 25]     # メニュー3: MANA, MANO, KANALOA, HULU
]

# カード別の結果テキスト
RESULTS = {
    # メニュー1の結果
    (100901, 1): '''【I'O】のカードのテーマは「ミステリー」であり、「神秘的な雰囲気」が漂うカードです。2025年上半期、あなたには思いがけない出会いや出来事が訪れます。それは一見、小さな偶然のように見えるかもしれません。しかし、実はあなたの人生を大きく変える「運命の布石」なのです。新しい仕事の話、旧友との再会、ふと立ち寄った場所での気づき…。どれも見逃さないでください。この時期は直感を大切にし、「なぜか気になる」ことに素直に従いましょう。全ては必然として起こっています。''',

    (100901, 14): '''【ALOHA】のカードが出ました。ALOHAは真の愛を意味します。2025年上半期、あなたの人間関係に大きな転機が訪れます。それは恋愛かもしれませんし、友人や家族との関係の深まりかもしれません。これまで表面的だった関係が、真実の絆へと変化していく時期です。エゴや依存のない、純粋な愛情に基づく関係が築かれます。心を開いて、誠実に人と向き合うことで、生涯の宝となる絆が生まれるでしょう。''',

    (100901, 22): '''【PELE】は火山の女神で、情熱を象徴します。2025年上半期、あなたの内側から熱い情熱が湧き上がってきます。これまで諦めていた夢や、封印していた才能が目覚める時です。破壊からの創造というPELEのテーマ通り、古い価値観や習慣を手放すことで、新しい自分が生まれます。恐れずに変化を受け入れてください。あなたの情熱が、周囲の人々も巻き込む大きなエネルギーとなり、予想以上の展開を生み出します。''',

    (100901, 42): '''【ANUENUE】は虹を意味し、多様性と希望の象徴です。2025年上半期、あなたには多方面からのチャンスが舞い込みます。仕事、プライベート、学び、趣味…様々な分野で可能性が広がります。一つに絞る必要はありません。虹のように多彩な経験を楽しむことで、あなたの人生は豊かな色彩に満ちていきます。特に、これまで関わったことのない分野や人々との交流が、大きな転機となるでしょう。''',

    # メニュー2の結果
    (100902, 7): '''【HUNA】のテーマは「秘密」です。この転機によって、あなたは自分でも気づいていなかった才能や魅力を発見します。それは内側に秘められていたもので、今まで表に出る機会がなかっただけ。周囲の人々もあなたの新しい一面に驚き、評価が一変するでしょう。隠れた可能性が開花することで、自信が生まれ、人生の選択肢が大きく広がります。''',

    (100902, 18): '''【PUEO】は導きを象徴するフクロウです。この転機は、あなたの人生における「導き手」との出会いをもたらします。それは指導者、メンター、あるいは新しい価値観かもしれません。その導きによって、進むべき道が明確になり、迷いが消えていきます。また、あなた自身が誰かの導き手となる機会も訪れ、教えることで学ぶという循環が生まれるでしょう。''',

    (100902, 23): '''【LAKA】はフラの女神で、インスピレーションを意味します。この転機によって、あなたの創造性が大きく花開きます。仕事でも趣味でも、独自のアイデアが次々と湧き出てくる時期です。そのインスピレーションを形にすることで、周囲から注目を集め、新しい道が開けます。芸術的な感性も高まり、美しいものや心地よい環境に身を置くことで、さらなる幸運が舞い込むでしょう。''',

    (100902, 34): '''【PUA】は前進を象徴する花です。この転機は、あなたに大きな飛躍のチャンスをもたらします。これまでの努力が一気に実を結び、次のステージへと進む時が来ました。昇進、独立、新しいプロジェクトの開始など、具体的な形で前進が実現します。一歩踏み出す勇気を持てば、想像以上の成果が手に入ります。躊躇せず、自信を持って進んでください。''',

    # メニュー3の結果
    (100903, 4): '''【MANA】は生命エネルギーを意味します。2025年、あなたが手にする最高の結果は「満ち溢れる活力と健康」です。心身ともに充実し、何事にも前向きに取り組める状態になります。このエネルギーは周囲にも伝播し、あなたの存在そのものが人々を励まし、癒す力となります。健康であることが、あらゆる幸運の土台となることを実感するでしょう。''',

    (100903, 9): '''【MANO】はリーダーシップを象徴するサメです。2025年、あなたが手にする最高の結果は「リーダーとしての地位と影響力」です。仕事やコミュニティで中心的な役割を担うことになり、多くの人があなたを頼りにします。責任は重くなりますが、それ以上に大きな達成感と充実感を得られます。あなたの決断が、多くの人の未来を明るく照らすでしょう。''',

    (100903, 12): '''【KANALOA】は海の神で、基盤を意味します。2025年、あなたが手にする最高の結果は「揺るぎない基盤」です。経済的な安定、信頼できる人間関係、確かなスキル…人生の土台がしっかりと築かれます。この基盤があるからこそ、どんな挑戦にも恐れずに取り組める自信が生まれます。長期的な視点で見て、最も価値ある成果を手にする年となるでしょう。''',

    (100903, 25): '''【HULU】はイリュージョンを象徴し、無限の可能性を示します。2025年、あなたが手にする最高の結果は「限界を超える成功」です。これまで「無理だ」と思っていたことが実現します。夢のような出来事が現実となり、周囲も驚くような成果を収めるでしょう。可能性は無限大。あなたの想像力と行動力が、魔法のような結果を生み出します。'''
}

print('=' * 70)
print('新規占いメニュー作成＆MySQLインポートツール')
print('=' * 70)
print(f'\n【作成するメニュー】')
print(f'Contents ID: {NEW_CONTENTS_ID}')
print(f'メニュー名: {MENU_NAME}')
print(f'カテゴリー: {CATEGORY}')
print(f'小項目数: {len(MENUS)}')
print(f'占い結果数: {len(MENUS) * 4}\n')

try:
    # MySQLに接続
    print('MySQLに接続中...')
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print('✓ 接続成功\n')

    # 1. mana_contentsテーブルにデータを挿入
    print('[1/4] mana_contentsテーブルにデータを挿入中...')
    sql_contents = '''
    INSERT INTO mana_contents (contents_id, name, catch, caption, category, start_date)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(sql_contents, (
        NEW_CONTENTS_ID,
        MENU_NAME,
        MENU_NAME[:20],  # catch（短縮版）
        CAPTION,
        CATEGORY,
        START_DATE
    ))
    print(f'✓ Contents ID {NEW_CONTENTS_ID} を追加\n')

    # 2. mana_menuテーブルにデータを挿入
    print('[2/4] mana_menuテーブルにデータを挿入中...')
    sql_menu = '''
    INSERT INTO mana_menu (contents_id, menu_id, name)
    VALUES (%s, %s, %s)
    '''
    for menu_id, menu_name in zip(MENU_IDS, MENUS):
        cursor.execute(sql_menu, (NEW_CONTENTS_ID, menu_id, menu_name))
        print(f'  ✓ Menu ID {menu_id}: {menu_name}')
    print()

    # 3. mana_resultテーブルにデータを挿入
    print('[3/4] mana_resultテーブルにデータを挿入中...')
    sql_result = '''
    INSERT INTO mana_result (contents_id, menu_id, result_id, body)
    VALUES (%s, %s, %s, %s)
    '''
    result_count = 0
    for menu_idx, (menu_id, cards) in enumerate(zip(MENU_IDS, CARD_SELECTIONS), 1):
        for card_idx, card_num in enumerate(cards, 1):
            result_id = int(f"{NEW_CONTENTS_ID}{menu_idx:02d}{card_idx:02d}")
            result_text = RESULTS[(menu_id, card_num)]

            cursor.execute(sql_result, (
                NEW_CONTENTS_ID,
                menu_id,
                result_id,
                result_text
            ))
            result_count += 1
    print(f'  ✓ {result_count}件の占い結果を追加\n')

    # 4. mana_cardテーブルにデータを挿入
    print('[4/4] mana_cardテーブルにデータを挿入中...')
    sql_card = '''
    INSERT INTO mana_card (contents_id, menu_id, result_id, body)
    VALUES (%s, %s, %s, %s)
    '''
    card_count = 0
    for menu_idx, (menu_id, cards) in enumerate(zip(MENU_IDS, CARD_SELECTIONS), 1):
        for card_idx, card_num in enumerate(cards, 1):
            result_id = int(f"{NEW_CONTENTS_ID}{menu_idx:02d}{card_idx:02d}")

            cursor.execute(sql_card, (
                NEW_CONTENTS_ID,
                menu_id,
                result_id,
                card_num
            ))
            card_count += 1
    print(f'  ✓ {card_count}件のカード情報を追加\n')

    # コミット
    conn.commit()
    print('=' * 70)
    print('✓ すべてのデータをMySQLに正常にインポートしました！')
    print('=' * 70)

    # 確認クエリ
    print('\n【確認】')
    cursor.execute(f'SELECT COUNT(*) FROM mana_contents WHERE contents_id = {NEW_CONTENTS_ID}')
    print(f'mana_contents: {cursor.fetchone()[0]}件')

    cursor.execute(f'SELECT COUNT(*) FROM mana_menu WHERE contents_id = {NEW_CONTENTS_ID}')
    print(f'mana_menu: {cursor.fetchone()[0]}件')

    cursor.execute(f'SELECT COUNT(*) FROM mana_result WHERE contents_id = {NEW_CONTENTS_ID}')
    print(f'mana_result: {cursor.fetchone()[0]}件')

    cursor.execute(f'SELECT COUNT(*) FROM mana_card WHERE contents_id = {NEW_CONTENTS_ID}')
    print(f'mana_card: {cursor.fetchone()[0]}件')

except mysql.connector.Error as e:
    print(f'\n✗ エラーが発生しました: {e}')
    conn.rollback()
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print('\nMySQL接続を終了しました。')
