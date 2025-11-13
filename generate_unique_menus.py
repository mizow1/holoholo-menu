import pandas as pd
from datetime import datetime, timedelta
import random
import hashlib

# ハッシュベースのインデックス選択関数
def get_hash_index(contents_id, salt, max_value):
    """contents_idとsaltから一意のインデックスを生成"""
    hash_input = f"{contents_id}_{salt}".encode('utf-8')
    hash_value = int(hashlib.sha256(hash_input).hexdigest(), 16)
    return hash_value % max_value

# カードデータを読み込む
card_df = pd.read_csv('card_name.csv', encoding='utf-8')
category_df = pd.read_csv('category_id.csv', encoding='utf-8')

# カテゴリー別の基本構成要素（大幅に拡充）
category_components = {
    1: {  # 両思い
        'themes': ['愛の深まり', '関係の進展', '二人の未来', '絆の強化', '愛の確認', '関係の安定', '愛の成長', '二人の幸せ', '心の繋がり', '愛の形'],
        'subjects': ['あの人', 'パートナー', '恋人', '大切な人', '愛する人', '二人', 'あの方', 'その人', '彼', '彼女'],
        'concerns': ['本当の気持ち', '深層心理', '隠れた想い', '本音', '真実の感情', '心の奥', '秘めた思い', '内面', '本心', '真の気持ち'],
        'futures': ['これからの関係', '二人の未来', '愛の行方', '関係の展開', '今後の二人', '未来の姿', '将来の関係', '進む道', '訪れる未来', '待つ運命'],
        'actions': ['大切にすべきこと', '心がけること', '必要な行動', 'すべき努力', '意識すること', '実践すべきこと', '取るべき態度', '心に留めること', '忘れないこと', '続けるべきこと']
    },
    2: {  # 片思い
        'themes': ['片思いの行方', '想いの伝え方', '恋の成就', 'アプローチ方法', '距離の縮め方', '気持ちの伝達', '恋愛成功', '想いの実現', '恋の進展', '心の通い'],
        'subjects': ['あの人', '気になる人', '好きな人', 'その人', '憧れの人', '思い人', '想いを寄せる人', '心惹かれる人', '恋する人', '目が離せない人'],
        'concerns': ['今の気持ち', 'あなたへの印象', '意識度', '好意のレベル', '関心度', 'あなたへの評価', '現在の感情', '心の距離', '親近感', '恋愛対象として'],
        'futures': ['恋が実る可能性', '関係の進展', '想いが届く確率', '二人の将来', '恋の結末', '成就の見込み', '進展のチャンス', '未来の関係', '叶う時期', '恋愛の成り行き'],
        'actions': ['取るべきアプローチ', 'アピール方法', '距離の縮め方', '接し方', '会話の仕方', '行動指針', '効果的な方法', 'ベストな態度', '避けるべきこと', '成功の秘訣']
    },
    3: {  # 相手の気持ち
        'themes': ['本音の理解', '気持ちの解明', '心理分析', '真意の把握', '感情の読解', '本心の探求', '内面理解', '気持ちの確認', '真実の発見', '心の解読'],
        'subjects': ['あの人', 'その人', '気になる人', '相手', 'あの方', '彼', '彼女', 'パートナー', '大切な人', '問題の人'],
        'concerns': ['本当の気持ち', '隠された感情', '本音', '内心', '真の想い', '心の内', '秘密の感情', '本心', '実際の気持ち', '偽らざる思い'],
        'futures': ['これからの関係', '今後の展開', '二人の未来', '関係の変化', '将来の姿', '進む方向', '待つ運命', '訪れる変化', '関係の行方', '未来予想'],
        'actions': ['対処法', '接し方', '心がけること', 'すべきこと', '避けるべきこと', 'ベストな行動', '適切な対応', '効果的な方法', '改善策', '解決の糸口']
    },
    4: {  # 不倫
        'themes': ['複雑な恋', '禁断の愛', '秘密の関係', '困難な恋愛', '葛藤', '選択', '決断', '真実の愛', '運命', '覚悟'],
        'subjects': ['あの人', 'その人', '彼', '彼女', '愛する人', '大切な人', 'あの方', '心の人', '忘れられない人', '運命の人'],
        'concerns': ['本当の気持ち', '家庭への想い', 'あなたへの愛', '葛藤', '本音', '真実の感情', '揺れる心', '秘められた想い', '偽らざる気持ち', '心の内'],
        'futures': ['この恋の行方', '関係の未来', '二人の結末', '運命の答え', '待つ結果', '最終的な形', '関係の着地点', '進むべき道', '選択の先', '真の幸せ'],
        'actions': ['決断すべきこと', '考えるべきこと', '覚悟', '選択', '心の準備', '向き合い方', '幸せへの道', '解決策', '最善の選択', '取るべき行動']
    },
    5: {  # 夜の相性
        'themes': ['深い絆', '肉体の相性', '心の繋がり', '親密さ', '満たし合い', '調和', '一体感', '官能', '深層の愛', '真の相性'],
        'subjects': ['二人', 'あの人', 'パートナー', '恋人', '愛する人', 'あの方', 'その人', '大切な人', '彼', '彼女'],
        'concerns': ['肉体的相性', '心の相性', '満足度', '充実感', '一体感', '調和', '欲求の一致', '深い絆', '親密度', '通じ合い'],
        'futures': ['関係の深まり', '絆の強化', '満たされる未来', '調和の向上', 'より良い関係', '深化', '進化', '成熟', '充実', '完成'],
        'actions': ['大切にすべきこと', '意識すること', '高める方法', '深める秘訣', '満たし合う方法', '調和の取り方', '絆を強める方法', '充実させる秘訣', '向上の鍵', '幸福の条件']
    },
    6: {  # 結婚
        'themes': ['結婚運', '生涯のパートナー', '結婚の可能性', '夫婦の未来', '家庭築き', '永遠の絆', '結婚生活', '人生の伴侶', '結婚への道', '夫婦の形'],
        'subjects': ['あの人', 'パートナー', '恋人', '彼', '彼女', 'その人', '大切な人', '愛する人', '運命の人', '生涯の伴侶'],
        'concerns': ['結婚への意識', '結婚観', '家庭への考え', '結婚願望', 'あなたとの結婚', '結婚のタイミング', '結婚への準備', '家族への想い', '生涯の約束', '覚悟'],
        'futures': ['結婚の可能性', '結婚時期', '結婚生活', '夫婦の未来', '家庭の形', '結婚後の関係', '幸せな家庭', '二人の将来', '家族の姿', '生涯の幸せ'],
        'actions': ['結婚への準備', 'すべきこと', '心がけること', '克服すべき課題', '必要な努力', '大切な条件', '幸せの秘訣', '成功の鍵', '築くべきもの', '実現の方法']
    },
    7: {  # 人生
        'themes': ['人生の岐路', '運命の選択', '人生の転機', '生き方', '人生の意味', '使命', '目的', '道の選択', '人生の答え', '真の幸せ'],
        'subjects': ['あなた', '今のあなた', 'あなた自身', 'あなたの人生', 'あなたの運命', 'あなたの道', 'あなたの未来', 'あなたの選択', 'あなたの決断', 'あなたの心'],
        'concerns': ['今の状況', '現在地', '置かれた立場', '抱える問題', '悩み', '迷い', '不安', '葛藤', '課題', '障害'],
        'futures': ['訪れる転機', '未来の姿', '待つ運命', '進む道', '選ぶべき道', '開ける未来', '訪れる変化', '新しい展開', '人生の答え', '幸せの形'],
        'actions': ['すべきこと', '心がけること', '大切な選択', '意識すべきこと', '捨てるべきもの', '掴むべきもの', '進むべき方向', '決断', '行動指針', '生き方']
    },
    8: {  # 仕事
        'themes': ['仕事運', 'キャリア', '成功', '適職', '天職', '才能開花', '出世', '評価', '職場環境', '仕事の意義'],
        'subjects': ['あなた', '今のあなた', 'あなた自身', 'あなたの才能', 'あなたの能力', 'あなたのキャリア', 'あなたの仕事', 'あなたの職場', 'あなたの未来', 'あなたの可能性'],
        'concerns': ['今の仕事運', '現状の評価', '才能', '能力', '強み', '弱み', '適性', '向き不向き', '評価', '立ち位置'],
        'futures': ['キャリアの未来', '成功の可能性', '昇進', '転職', '独立', 'キャリアアップ', '収入アップ', '環境の変化', '新しいチャンス', '仕事の行方'],
        'actions': ['すべきこと', '磨くべきスキル', '心がけること', '活かすべき才能', '伸ばすべき能力', '築くべき人脈', '学ぶべきこと', '努力の方向', '成功の秘訣', 'キャリア戦略']
    },
    9: {  # 復縁
        'themes': ['復縁', 'やり直し', '再会', '再構築', '関係修復', '過去の愛', '忘れられない人', '元恋人', '別れた理由', '再び一緒に'],
        'subjects': ['あの人', '元恋人', '別れた人', 'その人', '忘れられない人', '昔の恋人', 'かつての恋人', '元パートナー', '以前の恋人', 'あの方'],
        'concerns': ['別れた後の気持ち', '今の想い', 'あなたへの気持ち', '心の変化', '後悔', '未練', '記憶', '忘れたか', '思い出すか', '連絡の意思'],
        'futures': ['復縁の可能性', 'やり直せるか', '再会', '関係の再構築', '復縁の時期', '成功の確率', '二人の未来', '新しいスタート', '関係の修復', '愛の再燃'],
        'actions': ['すべきこと', '避けるべきこと', '冷却期間', '連絡方法', 'アプローチ', '変えるべきこと', '反省点', '改善策', '復縁の秘訣', '成功への道']
    },
    10: {  # 出会い
        'themes': ['運命の出会い', '新しい恋', '恋愛運', '理想の相手', '素敵な出会い', '恋の始まり', 'ソウルメイト', '運命の人', '出会いのチャンス', '恋愛の予感'],
        'subjects': ['あなた', '今のあなた', 'あなたの恋愛運', 'あなたの未来', 'あなたの運命', '運命の人', '理想の相手', '素敵な人', '特別な人', '大切な人'],
        'concerns': ['今の恋愛運', '出会いの時期', '恋愛の状況', 'モテ度', '魅力', '恋愛傾向', '恋愛体質', '出会いの障害', '恋愛ブロック', '恋愛の課題'],
        'futures': ['出会いの時期', '運命の人', '理想の相手', '恋の始まり', '新しい恋愛', '素敵な出会い', '運命的な出会い', '特別な人', '生涯のパートナー', '真の愛'],
        'actions': ['引き寄せる方法', '魅力の高め方', '出会いのチャンス', '恋愛運アップ', 'すべきこと', '心がけること', '行くべき場所', '意識すること', '準備すること', '開運行動']
    }
}

# カード選定（各カテゴリーに適したカード）
category_cards = {
    1: [14, 24, 36, 38, 4, 9, 23, 40, 3, 22, 27, 37, 12, 26, 42, 43, 20, 21, 32, 34, 41, 44],
    2: [14, 24, 3, 23, 40, 9, 36, 38, 22, 4, 27, 42, 12, 26, 37, 43, 6, 21, 34, 41, 44, 20],
    3: [14, 24, 36, 9, 40, 23, 4, 38, 12, 3, 22, 27, 26, 42, 37, 43, 11, 20, 21, 32, 41, 44],
    4: [14, 24, 3, 22, 12, 26, 27, 37, 23, 4, 9, 40, 36, 38, 42, 43, 7, 18, 30, 31, 41, 44],
    5: [14, 3, 36, 24, 23, 4, 9, 22, 40, 38, 12, 26, 27, 42, 37, 43, 20, 21, 32, 41, 44, 6],
    6: [14, 24, 36, 38, 3, 40, 12, 9, 23, 4, 22, 26, 27, 37, 42, 43, 13, 20, 21, 32, 41, 44],
    7: [1, 7, 18, 42, 40, 8, 9, 34, 23, 4, 14, 24, 12, 26, 27, 43, 6, 10, 16, 30, 35, 39, 41, 44],
    8: [9, 8, 40, 34, 4, 23, 35, 33, 1, 7, 14, 24, 22, 12, 26, 43, 10, 15, 16, 21, 28, 41, 44],
    9: [14, 24, 3, 9, 36, 38, 12, 26, 22, 4, 23, 40, 27, 37, 42, 43, 10, 30, 31, 6, 20, 41, 44],
    10: [14, 23, 40, 42, 34, 4, 9, 24, 36, 38, 3, 12, 22, 26, 27, 43, 1, 6, 18, 21, 41, 44]
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

def generate_unique_menu_components(contents_id, category_id):
    """contents_idに基づいて完全にユニークなメニュー構成要素を生成"""
    random.seed(contents_id)

    components = category_components[category_id]

    # ハッシュベースでユニークな組み合わせを生成
    theme_idx = get_hash_index(contents_id, 'theme', len(components['themes']))
    subject_idx = get_hash_index(contents_id, 'subject', len(components['subjects']))
    concern_idx = get_hash_index(contents_id, 'concern', len(components['concerns']))
    future_idx = get_hash_index(contents_id, 'future', len(components['futures']))
    action_idx = get_hash_index(contents_id, 'action', len(components['actions']))

    theme = components['themes'][theme_idx]
    subject = components['subjects'][subject_idx]
    concern = components['concerns'][concern_idx]
    future = components['futures'][future_idx]
    action = components['actions'][action_idx]

    # メニュー名のパターン（50パターンに拡充）
    name_patterns = [
        f'{subject}の{concern}は？　{future}を知りたい',
        f'{theme}完全鑑定　{subject}との{future}',
        f'{subject}の{concern}と{future}　徹底解明',
        f'{theme}の真実　{future}はどうなる？',
        f'{subject}は本当に…？　{concern}と{future}',
        f'{future}を占う　{subject}の{concern}',
        f'{theme}鑑定　{concern}から{future}まで',
        f'{subject}との{future}は？　{concern}を解明',
        f'{concern}が知りたい！　{subject}との{future}',
        f'{theme}の全て　{future}を完全予測',
        f'{concern}の答え　{subject}の{future}を占う',
        f'{future}への道　{theme}完全ガイド',
        f'{subject}が選ぶ{future}　{concern}の全容',
        f'{theme}徹底鑑定　{concern}と{action}',
        f'{future}の可能性　{subject}の{concern}解明',
        f'{concern}を読み解く　{future}への扉',
        f'{subject}との{theme}　{future}完全予測',
        f'{action}で変わる{future}　{theme}の真相',
        f'{future}が見える　{subject}の{concern}',
        f'{theme}の核心　{concern}から{future}へ',
        f'{subject}は今…？　{concern}と{future}の全て',
        f'{future}の行方　{theme}詳細鑑定',
        f'{concern}の真実　{subject}との{future}は',
        f'{theme}を解く鍵　{future}へのヒント',
        f'{subject}が望む{future}　{concern}徹底分析',
        f'{future}への答え　{theme}完全解明',
        f'{concern}と{action}　{future}を引き寄せる',
        f'{subject}の本心　{future}への{theme}',
        f'{future}の全貌　{concern}詳細占い',
        f'{theme}の結論　{subject}との{future}予測',
        f'{concern}から始まる{future}　{theme}鑑定',
        f'{subject}が目指す{future}　{concern}の本質',
        f'{future}を掴む　{theme}と{action}',
        f'{concern}深掘り　{future}完全ガイド',
        f'{subject}の{theme}　{future}への道筋',
        f'{future}確定版　{concern}全解析',
        f'{theme}の方向性　{subject}の{future}は',
        f'{concern}と未来　{action}で開く{future}',
        f'{subject}との絆　{future}を占う{theme}',
        f'{future}の真相　{concern}徹底検証',
        f'{theme}全公開　{future}への完全マップ',
        f'{concern}の意味　{subject}が迎える{future}',
        f'{future}の展望　{theme}と{action}の関係',
        f'{subject}が感じる{concern}　{future}は',
        f'{theme}完全版　{future}へのロードマップ',
        f'{concern}を知る　{subject}との{future}予想',
        f'{future}の正体　{theme}詳細分析',
        f'{subject}の選択　{concern}が導く{future}',
        f'{theme}大公開　{action}と{future}',
        f'{concern}の全体像　{future}完全解読'
    ]

    # キャッチのパターン（30パターンに拡充）
    catch_patterns = [
        f'{theme}を完全鑑定',
        f'{subject}の真実',
        f'{future}を知る',
        f'{concern}解明',
        f'{theme}の答え',
        f'運命を読み解く',
        f'真実が明らかに',
        f'{theme}の全て',
        f'完全解明',
        f'詳細鑑定',
        f'{future}完全予測',
        f'{concern}の真相',
        f'{theme}徹底分析',
        f'{subject}を占う',
        f'運命の扉を開く',
        f'{future}への道',
        f'{concern}全解明',
        f'{theme}詳細ガイド',
        f'真実の答え',
        f'{future}が見える',
        f'{concern}の全て',
        f'{theme}を読む',
        f'{subject}の未来',
        f'完全ガイド',
        f'{future}予測',
        f'{concern}詳細',
        f'{theme}の核心',
        f'運命鑑定',
        f'{subject}解明',
        f'完全占い'
    ]

    # キャプションのパターン（20パターンに拡充）
    caption_patterns = [
        f'{subject}について知りたい…　{concern}は？　{future}は？　ハワイアンタロットが、{theme}を詳しく鑑定します。',
        f'{concern}が気になる…　{future}はどうなる？　ハワイアンタロットが{subject}の真実を明らかにします。',
        f'{future}を知りたい！　{subject}の{concern}は？　ハワイアンタロットが{theme}を徹底鑑定します。',
        f'{theme}について悩むあなたへ。{subject}の{concern}、{future}をハワイアンタロットが鑑定します。',
        f'{concern}が分からない…　{future}が不安…　ハワイアンタロットが{subject}について詳しく占います。',
        f'{subject}の{concern}、そして{future}…　ハワイアンタロットが{theme}の全てをお伝えします。',
        f'{future}への不安を解消。{subject}の{concern}を、ハワイアンタロットが{theme}として鑑定。',
        f'{concern}の答えが欲しい…　{future}を見通したい…　{theme}をハワイアンタロットで占います。',
        f'{subject}との{theme}。{concern}や{future}について、ハワイアンタロットが詳しく教えます。',
        f'{future}が気になるあなたへ。{concern}を含む{theme}を、ハワイアンタロットが完全鑑定。',
        f'{concern}を解明し、{future}を予測。{subject}について、ハワイアンタロットが{theme}を占います。',
        f'{theme}の真相を知りたい…　{subject}の{concern}と{future}を、ハワイアンタロットが解き明かします。',
        f'{future}の可能性を探る。{concern}から見る{theme}を、ハワイアンタロットで詳しく鑑定します。',
        f'{subject}の本当の{concern}は？　{future}はどうなる？　{theme}をハワイアンタロットが占います。',
        f'{concern}と{future}について。{subject}に関する{theme}を、ハワイアンタロットが徹底解明。',
        f'{future}への道筋が見えてくる。{concern}を軸にした{theme}を、ハワイアンタロットで鑑定。',
        f'{theme}を深く知る。{subject}の{concern}、そして{future}を、ハワイアンタロットが詳しく占います。',
        f'{concern}の本質、{future}の真相。{subject}について、ハワイアンタロットが{theme}を完全鑑定。',
        f'{future}を見据えて。{concern}から読み解く{theme}を、ハワイアンタロットが詳しくお伝えします。',
        f'{subject}との{theme}が明らかに。{concern}と{future}を、ハワイアンタロットが徹底的に占います。'
    ]

    name_idx = get_hash_index(contents_id, 'name_pattern', len(name_patterns))
    catch_idx = get_hash_index(contents_id, 'catch_pattern', len(catch_patterns))
    caption_idx = get_hash_index(contents_id, 'caption_pattern', len(caption_patterns))

    menu_name = name_patterns[name_idx]
    catch = catch_patterns[catch_idx]
    caption = caption_patterns[caption_idx]

    return menu_name, catch, caption, theme, subject, concern, future, action

def generate_unique_items(contents_id, category_id, num_items):
    """完全にユニークな項目を生成"""
    random.seed(contents_id)

    components = category_components[category_id]

    # まず変数を取得
    _, _, _, theme, subject, concern, future, action = generate_unique_menu_components(contents_id, category_id)

    # 項目のバリエーション
    item_patterns = [
        [f'{subject}の{concern}', f'{future}の可能性', f'{action}', f'二人の{theme}'],
        [f'今の{concern}', f'{future}について', f'{subject}が求めること', f'{action}'],
        [f'{concern}の真実', f'{theme}の行方', f'{subject}の本音', f'幸せへの{action}'],
        [f'{subject}の深層心理', f'{future}の展望', f'関係における{theme}', f'大切な{action}'],
        [f'現在の{concern}', f'{future}への道', f'{subject}との{theme}', f'心がける{action}'],
        [f'{concern}を解明', f'{theme}の未来', f'{subject}の想い', f'実践すべき{action}'],
        [f'{subject}が感じていること', f'訪れる{future}', f'{theme}の核心', f'必要な{action}'],
        [f'{concern}の本質', f'{future}の姿', f'{subject}の視点', f'意識する{action}'],
        [f'隠れた{concern}', f'{future}のビジョン', f'{theme}の真相', f'取り組む{action}'],
        [f'{subject}の正直な{concern}', f'待つ{future}', f'{theme}の本当の意味', f'実行する{action}']
    ]

    pattern_idx = get_hash_index(contents_id, 'item_pattern', len(item_patterns))
    base_items = item_patterns[pattern_idx]

    # num_itemsに応じてアイテムを選択・拡張
    if num_items <= len(base_items):
        return base_items[:num_items]
    else:
        # 不足分を追加生成
        extended_items = base_items.copy()
        extra_patterns = [
            f'{theme}についての詳細',
            f'{subject}の隠れた面',
            f'{future}を左右する要因',
            f'改善のための{action}',
            f'{concern}の深層',
            f'最終的な{future}'
        ]
        for i in range(num_items - len(base_items)):
            idx = i % len(extra_patterns)
            extended_items.append(extra_patterns[idx])
        return extended_items[:num_items]

def generate_result_text(card_id, item_text, category_id):
    """鑑定文を生成（300文字程度）"""
    card_name = get_card_name(card_id)
    card_keyword = get_card_keyword(card_id)
    card_summary = get_card_summary(card_id)

    # カードの紹介部分のバリエーション
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

    # カテゴリーと項目に応じた具体的な内容を生成（300文字程度）
    if '気持ち' in item_text or '本音' in item_text or '感じて' in item_text or '想い' in item_text or '心理' in item_text:
        variations = [
            f"{item_text}について、{card_keyword}のエネルギーが強く働いています。あの人は今、心の奥底で{card_keyword}に関わる深い感情を抱いているようです。表面的には見えにくいかもしれませんが、確実にその気持ちは存在しています。誠実に向き合い、お互いの心を開くことで、二人の関係は今まで以上に良い方向へと進んでいくでしょう。素直な気持ちを大切にしながら、焦らず一歩ずつ進んでください。信頼と理解を深めることが、より良い関係を築く鍵となります。",
            f"{item_text}に関して、カードは{card_keyword}の影響を強く示しています。{card_keyword}という気持ちが、あの人の心に確かに芽生えています。その感情は時間とともに育っていき、やがて二人の絆を深める大きな力となります。お互いの気持ちを尊重し、思いやりを持って接することで、より深く強い絆が育まれていくはずです。相手のペースを大切にしながら、愛を育んでいきましょう。心を開いて対話することで、真実が見えてきます。",
            f"{item_text}を見ると、{card_keyword}というキーワードが明確に浮かび上がってきます。あの人の心には{card_keyword}に関連する思いが満ちており、それがあなたに向けられています。この気持ちを受け止め、素直な心で応えることが、関係を深める鍵となるでしょう。お互いの心を理解し合うことで、二人の愛はさらに美しく花開いていきます。愛を信じて、前に進んでください。真摯な態度と誠実な行動が、幸せな未来への道を開きます。"
        ]
    elif '相性' in item_text or '関係' in item_text or '絆' in item_text:
        variations = [
            f"{item_text}において、{card_keyword}が非常に重要な鍵となります。二人の間には{card_keyword}のエネルギーが豊かに流れており、それが関係を支える大きな力となっています。この特別なつながりを大切にし、お互いを深く尊重し合うことで、より良い関係を築いていけるでしょう。共に成長し、支え合いながら、二人だけの特別な絆を育んでいってください。信頼と愛情が、さらなる幸せへの道を開きます。",
            f"二人の{item_text}には、{card_keyword}という要素が深く関わっています。この{card_keyword}を意識し、大切にすることで、関係はさらに調和のとれた美しいものへと変化していきます。お互いの個性を認め合い、それぞれの長所を活かし合うことで、完璧なバランスが生まれます。二人で力を合わせれば、どんな困難も乗り越えられるでしょう。愛と理解をもって、共に歩んでいってください。",
            f"{item_text}を深く見つめると、{card_keyword}が中心的なテーマとなっています。この{card_keyword}を二人で大切に育てることで、絆はより強固で深いものとなります。時には試練もあるかもしれませんが、それを乗り越えることで関係はさらに成熟します。お互いへの信頼と愛情を忘れずに、二人だけの特別な世界を築いていきましょう。その先には、かけがえのない幸せが待っています。"
        ]
    elif '未来' in item_text or 'これから' in item_text or '訪れる' in item_text or 'タイミング' in item_text or '行方' in item_text or '展望' in item_text or '見込み' in item_text:
        variations = [
            f"{item_text}には、{card_keyword}に関わる重要な出来事が待っています。{card_keyword}のエネルギーを感じたら、それは人生からの大切なサインです。その瞬間を見逃さず、前向きに受け止めることが重要です。勇気を持って一歩を踏み出すことで、幸せな未来へと確実に繋がっていきます。自分を信じ、流れに身を任せながら、新しい扉を開いていってください。素晴らしい未来があなたを待っています。",
            f"{item_text}について、カードは{card_keyword}の訪れを力強く告げています。{card_keyword}というテーマに心を開き、柔軟に受け入れることで、予想を超える素晴らしい展開が生まれるでしょう。運命は確実にあなたに味方しています。その流れに逆らわず、自然体で進んでいくことが成功の秘訣です。直感を信じ、前向きな気持ちで未来を迎えましょう。きっと期待以上の幸せが訪れます。",
            f"{item_text}には、{card_keyword}のエネルギーが力強く流れ込んできます。この{card_keyword}を素直に受け入れ、ポジティブな姿勢で向き合うことで、望む方向へと確実に進んでいけるはずです。時には不安を感じることもあるかもしれませんが、それは成長の証です。自分の直感を信じ、恐れずに前進してください。あなたの努力と勇気が、必ず素晴らしい結果を引き寄せます。"
        ]
    elif 'アドバイス' in item_text or 'すべき' in item_text or '心がけ' in item_text or '引き寄せる' in item_text or '方法' in item_text or '秘訣' in item_text or '必要' in item_text or '大切' in item_text:
        variations = [
            f"{item_text}として、{card_keyword}を強く意識することが非常に大切です。日々の生活の中で{card_keyword}を心がけ、実践し続けることで、道は自然と開けていきます。小さな一歩の積み重ねが、やがて大きな成果となって現れます。自分を信じ、諦めずに前進し続けてください。困難に直面しても、{card_keyword}の精神を忘れなければ、必ず乗り越えられます。あなたには無限の可能性があります。",
            f"{item_text}において、{card_keyword}がキーワードとなります。{card_keyword}の気持ちを常に持ち続け、それを行動に移していくことで、望む結果へと着実に近づいていけるでしょう。焦る必要はありません。一つひとつ丁寧に積み重ねていくことが、最終的な成功につながります。周囲の声に惑わされず、自分の道を信じて歩んでください。あなたの努力は必ず報われます。",
            f"{item_text}には、{card_keyword}という視点が不可欠です。{card_keyword}を大切にし、それを軸にして行動することで、あなたの願いは着実に現実へと近づいていきます。時には遠回りに感じることもあるかもしれませんが、それも成長のプロセスです。信念を持ち続け、{card_keyword}の精神を忘れずに歩み続ければ、必ず道は開けます。未来は明るく輝いています。"
        ]
    elif '特徴' in item_text or '印象' in item_text or 'どんな' in item_text or 'タイプ' in item_text or '性格' in item_text or '人柄' in item_text:
        variations = [
            f"{item_text}を深く見つめると、{card_keyword}というキーワードが鮮明に浮かび上がってきます。{card_keyword}に関連する要素や性質が、非常に大きな特徴となっているようです。この特性を正しく理解し、受け入れることで、物事の本質がより明確に見えてきます。表面的な印象だけでなく、深い部分まで理解しようとする姿勢が大切です。そうすることで、真の姿が明らかになるでしょう。",
            f"{item_text}には、{card_keyword}という性質が強く表れています。この{card_keyword}の要素を深く理解することで、より豊かな洞察が得られるでしょう。一見すると気づかないような細かな部分にも目を向け、全体像を把握することが重要です。{card_keyword}という観点から多角的に捉えることで、本当の姿が見えてきます。先入観を持たず、オープンな心で向き合ってください。",
            f"カードが示す{item_text}は、{card_keyword}が中心的なテーマとなっています。{card_keyword}という観点から捉え、その本質を見極めることが非常に重要です。表層的な理解だけでなく、深い部分まで探求する姿勢を持つことで、真実が明らかになります。焦らず、じっくりと向き合う時間を持つことで、より深い理解に到達できるでしょう。真実は必ず見えてきます。"
        ]
    elif '可能性' in item_text or 'チャンス' in item_text or '見込み' in item_text or '確率' in item_text or '実る' in item_text:
        variations = [
            f"{item_text}について、{card_keyword}という視点から見ると、非常にポジティブな兆しが見えています。{card_keyword}のエネルギーが働くことで、想像以上の良い結果が期待できるでしょう。ただし、ただ待つだけでなく、自ら積極的に行動することが重要です。チャンスは準備ができている人のもとに訪れます。前向きな姿勢を保ち、機会を逃さないように心がけてください。成功は目前です。",
            f"{item_text}には、{card_keyword}が深く関わっており、それが良い方向へと導いています。状況は確実に好転しつつあり、あなたにとって有利な展開が期待できます。この流れを最大限に活かすためには、{card_keyword}の精神を忘れずに、タイミングを見極めることが大切です。焦らず、しかし躊躇せずに、適切な瞬間に行動を起こしてください。成功への道は開かれています。",
            f"{item_text}を考える上で、{card_keyword}がキーとなります。{card_keyword}の本質を深く理解し、それに沿って行動することで、望む結果が手に入る可能性は非常に高いでしょう。ただし、油断は禁物です。慎重さと大胆さのバランスを取りながら、着実に前進していくことが成功の秘訣です。あなたの努力と判断力が、必ず素晴らしい結果を引き寄せます。"
        ]
    else:
        variations = [
            f"{item_text}について、{card_keyword}という視点から捉えることが非常に重要です。{card_keyword}のエネルギーを意識し、それに沿って考え、行動することで、新たな気づきと理解が得られるはずです。物事の表面だけでなく、深層にある真実を見極める目を養うことが大切です。直感を信じ、心の声に耳を傾けながら、一歩ずつ前進してください。答えは必ず見つかります。",
            f"{item_text}には、{card_keyword}が深く関わっており、それが全体に大きな影響を与えています。{card_keyword}を正しく理解し、素直に受け入れることで、状況は確実に好転していくでしょう。時には困難に直面することもありますが、それも成長のプロセスの一部です。{card_keyword}の精神を忘れず、粘り強く取り組み続けることで、必ず道は開けます。",
            f"{item_text}を考える上で、{card_keyword}が中心的なキーワードとなります。{card_keyword}の本質をしっかりと見つめ、その意味を深く理解することで、あなたが求めている答えが明確に見えてくるはずです。表面的な理解だけでなく、本質的な部分まで掘り下げる姿勢が大切です。時間をかけて熟考し、真実を見極めてください。必ず光が見えてきます。"
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
    """完全にユニークなメニュー用SQLファイルを生成"""
    # カテゴリーをローテーション（1-10をループ）
    category_id = ((contents_id - 1101) % 10) + 1

    # 項目数をランダムに決定（3〜10項目）
    random.seed(contents_id)
    num_items = random.randint(3, 10)

    # ユニークなメニュー構成要素を生成
    menu_name, catch, caption, theme, subject, concern, future, action = generate_unique_menu_components(contents_id, category_id)

    # ユニークな項目を生成
    items = generate_unique_items(contents_id, category_id, num_items)

    # 公開日を計算
    start_date = calculate_start_date(contents_id)

    # このカテゴリー用のカード一覧
    available_cards = category_cards[category_id]

    # SQL生成開始
    sql = f"""-- ========================================
-- 占いメニュー: {menu_name}
-- Contents ID: {contents_id}
-- カテゴリー: {category_id}
-- 項目数: {num_items}
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

    # 各パターンごとに使用するカードを選定（パターン内で重複なし）
    pattern_cards = {}
    for pattern_num in range(1, num_patterns + 1):
        shuffled_cards = available_cards.copy()
        random.seed(contents_id * 100 + pattern_num)
        random.shuffle(shuffled_cards)
        pattern_cards[pattern_num] = shuffled_cards[:num_items]

    # 各項目に4つの結果を生成
    for i, item_name in enumerate(items, 1):
        menu_id = int(f"{contents_id}{i:02d}")

        for j in range(1, num_patterns + 1):
            result_id = int(f"{contents_id}{i:02d}{j:02d}")
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
    import sys

    # コマンドライン引数で範囲を指定
    if len(sys.argv) >= 3:
        start_id = int(sys.argv[1])
        end_id = int(sys.argv[2])
    else:
        # デフォルトはテスト用の10個
        start_id = 1101
        end_id = 1110

    print('完全ユニークなメニュー生成を開始します...')
    print('=' * 50)

    for contents_id in range(start_id, end_id + 1):
        sql_content = generate_menu_sql(contents_id)

        filename = f'menu_{contents_id}.sql'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(sql_content)

        category_id = ((contents_id - 1101) % 10) + 1
        random.seed(contents_id)
        num_items = random.randint(3, 10)

        print(f'[OK] 生成完了: {filename}')
        print(f'  カテゴリー: {category_id}, 項目数: {num_items}')

    print('=' * 50)
    total = end_id - start_id + 1
    print(f'\n全{total}個のメニューSQLファイルを生成しました！')
    print(f'メニューID: {start_id}〜{end_id}')
