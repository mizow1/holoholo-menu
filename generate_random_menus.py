import pandas as pd
from datetime import datetime, timedelta
import random

# カードデータを読み込む
card_df = pd.read_csv('card_name.csv', encoding='utf-8')
category_df = pd.read_csv('category_id.csv', encoding='utf-8')

# カテゴリー別の多様なメニューテンプレート
menu_templates_pool = {
    1: [  # 両思い
        {
            'name': '今の関係をもっと深めるには？　二人の愛の行方は？',
            'catch': '二人の絆を深める秘訣',
            'caption': 'もっと愛を深めたい…　二人の関係は今後どうなる？　ハワイアンタロットが、愛を育む方法と二人の未来を鑑定します。',
            'items': [
                '今のあの人の本当の気持ち',
                'あの人があなたに求めていること',
                '二人の愛を深めるためのアドバイス',
                'これからの二人の関係',
                '二人の絆を強くするために必要なこと',
                '二人が幸せになるための課題',
                '愛を育むために大切にすべきこと',
                'あなたが心がけるべきこと',
                'あの人の隠れた願い',
                '二人の未来に待っている幸せ'
            ]
        },
        {
            'name': 'あの人は私のこと本気？　二人の愛の深さと未来',
            'catch': 'あの人の本気度を知りたい',
            'caption': 'あの人は本気で私を愛してる？　ハワイアンタロットが、あの人の本音と二人の愛の深さを明らかにします。',
            'items': [
                'あの人の愛の深さ',
                'あの人が考える二人の未来',
                'あの人があなたに惹かれている理由',
                '二人の愛をさらに強くする方法',
                'あの人の隠れた不安',
                '愛を長続きさせる秘訣',
                '二人が乗り越えるべき課題',
                'より深い信頼関係を築くには',
                'あの人が望む関係性',
                '二人の愛の未来予想図'
            ]
        }
    ],
    2: [  # 片思い
        {
            'name': 'あの人は私のこと意識してる？　想いを届ける方法は？',
            'catch': '片思いを実らせたい',
            'caption': 'あの人に気持ちを伝えたい…　私のことどう思ってる？　ハワイアンタロットが、あの人の本音と恋を実らせる方法を教えます。',
            'items': [
                '今のあの人の気持ち',
                'あの人があなたに抱いている印象',
                '恋が実る可能性',
                'あなたが取るべきアプローチ',
                'あの人に好意を伝える最適なタイミング',
                '二人の関係を進展させる方法',
                'あの人の心を掴むポイント',
                '避けるべき行動',
                'あの人の恋愛観',
                '想いが叶う未来'
            ]
        },
        {
            'name': '脈あり？　なし？　あの人の本心と恋の行方',
            'catch': 'あの人の気持ちが知りたい',
            'caption': 'あの人は私に脈あり？　それとも…　ハワイアンタロットが、あの人の本心と片思いの行方を完全鑑定します。',
            'items': [
                'あの人が感じている気持ち',
                '脈ありサイン',
                'あの人の恋愛状況',
                '告白の成功率',
                'あなたの魅力をアピールする方法',
                '二人の距離を縮めるチャンス',
                'あの人が求める理想のタイプ',
                '恋を進展させる具体的な行動',
                'ライバルの存在',
                '片思いの結末'
            ]
        }
    ],
    3: [  # 相手の気持ち
        {
            'name': 'あの人の本音が知りたい！　隠された気持ちは？',
            'catch': 'あの人の本当の気持ち',
            'caption': 'あの人は何を考えているの？　本音が見えない…　ハワイアンタロットが、あの人の隠された気持ちを明らかにします。',
            'items': [
                '今あの人が感じていること',
                'あの人が口にしない本音',
                'あなたに対する好意のレベル',
                'あの人が望んでいること',
                'あの人の心の中の葛藤',
                'あなたへの隠れた感情',
                '二人の関係をどう思っているか',
                'あの人が抱えている悩み',
                'これからあの人はどう動くか',
                'あの人の本心を引き出す方法'
            ]
        }
    ],
    4: [  # 不倫
        {
            'name': 'この恋はどうなる？　あの人の本音と未来',
            'catch': '複雑な恋の行方',
            'caption': '複雑な関係に悩むあなたへ。あの人の本当の気持ちは？　この恋の未来は？　ハワイアンタロットが真実を明らかにします。',
            'items': [
                'あの人の本当の気持ち',
                'あの人が家庭をどう考えているか',
                'この関係の未来',
                'あなたが選ぶべき道',
                'あの人があなたに求めているもの',
                '関係を続けるリスク',
                'この恋で得られるもの',
                '幸せになるための決断',
                '周囲の影響',
                '最良の結末に向けて'
            ]
        }
    ],
    5: [  # 夜の相性
        {
            'name': '二人の深い絆と相性　心も体も満たされる？',
            'catch': '深いレベルでの相性',
            'caption': '二人の深い絆は？　心も体も通じ合える？　ハワイアンタロットが、二人の相性を詳しく鑑定します。',
            'items': [
                '二人の肉体的な相性',
                '精神的な結びつき',
                'お互いが満たされるポイント',
                '関係をより深めるアドバイス',
                'あの人が求めていること',
                '二人だけの特別な絆',
                'より満たされる関係になるには',
                'お互いの欲求を理解する',
                '深い愛情を育む方法',
                '二人の未来の関係性'
            ]
        }
    ],
    6: [  # 結婚
        {
            'name': 'あの人は結婚を考えてる？　結婚の可能性は？',
            'catch': 'あの人との結婚運',
            'caption': 'あの人と結婚できる？　いつ結婚できる？　ハワイアンタロットが、二人の結婚運と結婚への道筋を鑑定します。',
            'items': [
                'あの人の結婚への本音',
                '結婚に至る可能性',
                '結婚のタイミング',
                '結婚を実現するために必要なこと',
                'あの人が結婚相手に求める条件',
                '二人が乗り越えるべき課題',
                '結婚後の生活イメージ',
                '家族の理解を得る方法',
                '幸せな結婚への準備',
                '結婚に向けた具体的なステップ'
            ]
        }
    ],
    7: [  # 人生
        {
            'name': '人生の岐路に立つあなたへ　選ぶべき道は？',
            'catch': '人生の転機を見極める',
            'caption': '大きな決断を前にしたあなたへ。どの道を選ぶべき？　ハワイアンタロットが、あなたの人生の最良の選択を照らします。',
            'items': [
                '今あなたが置かれている状況',
                'これから訪れる大きな転機',
                '選択肢A：この道の先にあるもの',
                '選択肢B：別の道の可能性',
                'あなたの潜在能力',
                '決断の時期',
                '人生を好転させるヒント',
                '避けるべき落とし穴',
                '本当の幸せへの道',
                '未来を切り拓くメッセージ'
            ]
        },
        {
            'name': '今の人生このままでいい？　変化すべきことは？',
            'catch': '人生を見つめ直す',
            'caption': 'このままの人生でいい？　何か変えるべき？　ハワイアンタロットが、あなたの人生に必要な変化を教えます。',
            'items': [
                '今の人生の評価',
                '変化が必要な分野',
                'あなたが本当に望んでいること',
                '変化を起こすタイミング',
                '新しい道に進む勇気',
                '手放すべきもの',
                '大切にすべき価値観',
                'あなたの才能を活かす方法',
                '人生を豊かにするヒント',
                '理想の未来への道筋'
            ]
        }
    ],
    8: [  # 仕事
        {
            'name': '仕事運はどう？　キャリアアップのチャンスは？',
            'catch': '仕事で成功する秘訣',
            'caption': '今の仕事で成功できる？　転職すべき？　ハワイアンタロットが、あなたの仕事運とキャリアの方向性を鑑定します。',
            'items': [
                '今のあなたの仕事運',
                '職場での評価',
                'キャリアアップのチャンス',
                'あなたの強みと才能',
                '成功するために必要なスキル',
                '転職の可能性',
                '収入アップの見込み',
                '職場の人間関係',
                '仕事で成功するタイミング',
                'キャリアの未来予想'
            ]
        },
        {
            'name': '天職は？　適職は？　あなたが輝ける仕事',
            'catch': 'あなたの天職診断',
            'caption': '今の仕事は自分に合ってる？　本当にやりたいことは？　ハワイアンタロットが、あなたの天職と適職を明らかにします。',
            'items': [
                'あなたの本当の才能',
                '向いている仕事の分野',
                '天職に就くタイミング',
                '今の仕事を続けるべきか',
                'やりがいを感じる仕事',
                'キャリアチェンジの可能性',
                '経済的な成功の見込み',
                '仕事で幸せになる方法',
                '才能を開花させるヒント',
                '理想のキャリアパス'
            ]
        }
    ],
    9: [  # 復縁
        {
            'name': 'あの人は私のこと覚えてる？　復縁の可能性は？',
            'catch': 'もう一度やり直したい',
            'caption': 'あの人ともう一度…　私のこと覚えてる？　復縁できる？　ハワイアンタロットが、復縁の可能性と方法を鑑定します。',
            'items': [
                '別れた後のあの人の気持ち',
                'あの人は今でもあなたを思い出す？',
                '復縁の可能性',
                '復縁を妨げているもの',
                'あの人の今の恋愛状況',
                '復縁に向けて取るべき行動',
                '連絡を取るベストなタイミング',
                'やり直せる関係になるには',
                '復縁後の二人の関係',
                '最終的な結末'
            ]
        },
        {
            'name': 'あの人と復縁できる？　やり直すために必要なこと',
            'catch': '復縁への道',
            'caption': '別れたあの人が忘れられない…　もう一度やり直せる？　ハワイアンタロットが、復縁への道筋を示します。',
            'items': [
                'あの人の本当の気持ち',
                '別れた原因への後悔',
                '復縁のチャンス',
                'あなたが変えるべきこと',
                '冷却期間の必要性',
                '復縁のアプローチ方法',
                'あの人の心を取り戻す秘訣',
                '過去を乗り越える方法',
                '新しい関係を築くために',
                '復縁の成功率と時期'
            ]
        }
    ],
    10: [  # 出会い
        {
            'name': '運命の出会いはいつ？　どこで？　相手の特徴は？',
            'catch': '運命の出会いを知りたい',
            'caption': '素敵な出会いが欲しい！　いつ？　どこで？　ハワイアンタロットが、運命の出会いと理想の相手を詳しく鑑定します。',
            'items': [
                '運命の出会いの時期',
                '出会いの場所とシチュエーション',
                '運命の人の特徴',
                '運命の人の性格',
                '出会いを引き寄せる方法',
                'あなたの恋愛運',
                '出会いのチャンスを逃さないために',
                '理想の相手との相性',
                '恋愛が始まるきっかけ',
                '幸せな恋愛の未来'
            ]
        },
        {
            'name': 'いい出会いがない…　恋愛運を上げる方法は？',
            'catch': '恋愛運アップの秘訣',
            'caption': '全然いい出会いがない…　どうすれば？　ハワイアンタロットが、恋愛運を上げて素敵な出会いを引き寄せる方法を教えます。',
            'items': [
                '今のあなたの恋愛運',
                '出会いがない原因',
                '恋愛運を上げる方法',
                '出会いを引き寄せる行動',
                'あなたの魅力を高めるヒント',
                '理想の相手のタイプ',
                '出会いのチャンスが訪れる場所',
                '避けるべき恋愛パターン',
                '幸せな恋愛を始めるタイミング',
                '運命の人との出会いを確実にする方法'
            ]
        }
    ]
}

# カード選定（各カテゴリーに適したカードを事前に定義）
category_cards = {
    1: [14, 24, 36, 38, 4, 9, 23, 40, 3, 22, 27, 37, 12, 26, 42, 43, 20, 21, 32, 34, 41, 44],  # 両思い
    2: [14, 24, 3, 23, 40, 9, 36, 38, 22, 4, 27, 42, 12, 26, 37, 43, 6, 21, 34, 41, 44, 20],  # 片思い
    3: [14, 24, 36, 9, 40, 23, 4, 38, 12, 3, 22, 27, 26, 42, 37, 43, 11, 20, 21, 32, 41, 44],  # 相手の気持ち
    4: [14, 24, 3, 22, 12, 26, 27, 37, 23, 4, 9, 40, 36, 38, 42, 43, 7, 18, 30, 31, 41, 44],  # 不倫
    5: [14, 3, 36, 24, 23, 4, 9, 22, 40, 38, 12, 26, 27, 42, 37, 43, 20, 21, 32, 41, 44, 6],  # 夜の相性
    6: [14, 24, 36, 38, 3, 40, 12, 9, 23, 4, 22, 26, 27, 37, 42, 43, 13, 20, 21, 32, 41, 44],  # 結婚
    7: [1, 7, 18, 42, 40, 8, 9, 34, 23, 4, 14, 24, 12, 26, 27, 43, 6, 10, 16, 30, 35, 39, 41, 44],  # 人生
    8: [9, 8, 40, 34, 4, 23, 35, 33, 1, 7, 14, 24, 22, 12, 26, 43, 10, 15, 16, 21, 28, 41, 44],  # 仕事
    9: [14, 24, 3, 9, 36, 38, 12, 26, 22, 4, 23, 40, 27, 37, 42, 43, 10, 30, 31, 6, 20, 41, 44],  # 復縁
    10: [14, 23, 40, 42, 34, 4, 9, 24, 36, 38, 3, 12, 22, 26, 27, 43, 1, 6, 18, 21, 41, 44]  # 出会い
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
    """鑑定文を生成（300文字程度を目指す）"""
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

    # カテゴリーと項目に応じた具体的な内容を生成（300文字程度を目指す）
    if '気持ち' in item_text or '本音' in item_text or '感じて' in item_text:
        variations = [
            f"{item_text}について、{card_keyword}のエネルギーが強く働いています。あの人は今、心の奥底で{card_keyword}に関わる深い感情を抱いているようです。表面的には見えにくいかもしれませんが、確実にその気持ちは存在しています。誠実に向き合い、お互いの心を開くことで、二人の関係は今まで以上に良い方向へと進んでいくでしょう。素直な気持ちを大切にしながら、焦らず一歩ずつ進んでください。",
            f"{item_text}に関して、カードは{card_keyword}の影響を強く示しています。{card_keyword}という気持ちが、あの人の心に確かに芽生えています。その感情は時間とともに育っていき、やがて二人の絆を深める大きな力となります。お互いの気持ちを尊重し、思いやりを持って接することで、より深く強い絆が育まれていくはずです。相手のペースを大切にしながら、愛を育んでいきましょう。",
            f"{item_text}を見ると、{card_keyword}というキーワードが明確に浮かび上がってきます。あの人の心には{card_keyword}に関連する思いが満ちており、それがあなたに向けられています。この気持ちを受け止め、素直な心で応えることが、関係を深める鍵となるでしょう。お互いの心を理解し合うことで、二人の愛はさらに美しく花開いていきます。愛を信じて、前に進んでください。"
        ]
    elif '相性' in item_text or '関係' in item_text or '絆' in item_text:
        variations = [
            f"{item_text}において、{card_keyword}が非常に重要な鍵となります。二人の間には{card_keyword}のエネルギーが豊かに流れており、それが関係を支える大きな力となっています。この特別なつながりを大切にし、お互いを深く尊重し合うことで、より良い関係を築いていけるでしょう。共に成長し、支え合いながら、二人だけの特別な絆を育んでいってください。信頼と愛情が、さらなる幸せへの道を開きます。",
            f"二人の{item_text}には、{card_keyword}という要素が深く関わっています。この{card_keyword}を意識し、大切にすることで、関係はさらに調和のとれた美しいものへと変化していきます。お互いの個性を認め合い、それぞれの長所を活かし合うことで、完璧なバランスが生まれます。二人で力を合わせれば、どんな困難も乗り越えられるでしょう。愛と理解をもって、共に歩んでいってください。",
            f"{item_text}を深く見つめると、{card_keyword}が中心的なテーマとなっています。この{card_keyword}を二人で大切に育てることで、絆はより強固で深いものとなります。時には試練もあるかもしれませんが、それを乗り越えることで関係はさらに成熟します。お互いへの信頼と愛情を忘れずに、二人だけの特別な世界を築いていきましょう。その先には、かけがえのない幸せが待っています。"
        ]
    elif '未来' in item_text or 'これから' in item_text or '訪れる' in item_text or 'タイミング' in item_text or '行方' in item_text:
        variations = [
            f"{item_text}には、{card_keyword}に関わる重要な出来事が待っています。{card_keyword}のエネルギーを感じたら、それは人生からの大切なサインです。その瞬間を見逃さず、前向きに受け止めることが重要です。勇気を持って一歩を踏み出すことで、幸せな未来へと確実に繋がっていきます。自分を信じ、流れに身を任せながら、新しい扉を開いていってください。素晴らしい未来があなたを待っています。",
            f"{item_text}について、カードは{card_keyword}の訪れを力強く告げています。{card_keyword}というテーマに心を開き、柔軟に受け入れることで、予想を超える素晴らしい展開が生まれるでしょう。運命は確実にあなたに味方しています。その流れに逆らわず、自然体で進んでいくことが成功の秘訣です。直感を信じ、前向きな気持ちで未来を迎えましょう。きっと期待以上の幸せが訪れます。",
            f"{item_text}には、{card_keyword}のエネルギーが力強く流れ込んできます。この{card_keyword}を素直に受け入れ、ポジティブな姿勢で向き合うことで、望む方向へと確実に進んでいけるはずです。時には不安を感じることもあるかもしれませんが、それは成長の証です。自分の直感を信じ、恐れずに前進してください。あなたの努力と勇気が、必ず素晴らしい結果を引き寄せます。"
        ]
    elif 'アドバイス' in item_text or 'すべき' in item_text or '心がけ' in item_text or '引き寄せる' in item_text or '方法' in item_text or '秘訣' in item_text:
        variations = [
            f"{item_text}として、{card_keyword}を強く意識することが非常に大切です。日々の生活の中で{card_keyword}を心がけ、実践し続けることで、道は自然と開けていきます。小さな一歩の積み重ねが、やがて大きな成果となって現れます。自分を信じ、諦めずに前進し続けてください。困難に直面しても、{card_keyword}の精神を忘れなければ、必ず乗り越えられます。あなたには無限の可能性があります。",
            f"{item_text}において、{card_keyword}がキーワードとなります。{card_keyword}の気持ちを常に持ち続け、それを行動に移していくことで、望む結果へと着実に近づいていけるでしょう。焦る必要はありません。一つひとつ丁寧に積み重ねていくことが、最終的な成功につながります。周囲の声に惑わされず、自分の道を信じて歩んでください。あなたの努力は必ず報われます。",
            f"{item_text}には、{card_keyword}という視点が不可欠です。{card_keyword}を大切にし、それを軸にして行動することで、あなたの願いは着実に現実へと近づいていきます。時には遠回りに感じることもあるかもしれませんが、それも成長のプロセスです。信念を持ち続け、{card_keyword}の精神を忘れずに歩み続ければ、必ず道は開けます。未来は明るく輝いています。"
        ]
    elif '特徴' in item_text or '印象' in item_text or 'どんな' in item_text or 'タイプ' in item_text:
        variations = [
            f"{item_text}を深く見つめると、{card_keyword}というキーワードが鮮明に浮かび上がってきます。{card_keyword}に関連する要素や性質が、非常に大きな特徴となっているようです。この特性を正しく理解し、受け入れることで、物事の本質がより明確に見えてきます。表面的な印象だけでなく、深い部分まで理解しようとする姿勢が大切です。そうすることで、真の姿が明らかになるでしょう。",
            f"{item_text}には、{card_keyword}という性質が強く表れています。この{card_keyword}の要素を深く理解することで、より豊かな洞察が得られるでしょう。一見すると気づかないような細かな部分にも目を向け、全体像を把握することが重要です。{card_keyword}という観点から多角的に捉えることで、本当の姿が見えてきます。先入観を持たず、オープンな心で向き合ってください。",
            f"カードが示す{item_text}は、{card_keyword}が中心的なテーマとなっています。{card_keyword}という観点から捉え、その本質を見極めることが非常に重要です。表層的な理解だけでなく、深い部分まで探求する姿勢を持つことで、真実が明らかになります。焦らず、じっくりと向き合う時間を持つことで、より深い理解に到達できるでしょう。真実は必ず見えてきます。"
        ]
    elif '可能性' in item_text or 'チャンス' in item_text or '見込み' in item_text:
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
    """メニュー用SQLファイルを生成"""
    # カテゴリーをローテーション（1-10をループ）
    category_id = ((contents_id - 1471) % 10) + 1

    # このカテゴリーのテンプレートプールから1つ選択
    templates = menu_templates_pool[category_id]
    template_idx = (contents_id // 10) % len(templates)
    template = templates[template_idx]

    menu_name = template['name']
    catch = template['catch']
    caption = template['caption']
    all_items = template['items']

    # 項目数をランダムに決定（3〜10項目）
    random.seed(contents_id)  # 再現性のためにシードを設定
    num_items = random.randint(3, min(10, len(all_items)))
    items = all_items[:num_items]

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
    print('ランダム項目数メニュー生成を開始します...')
    print('=' * 50)

    for contents_id in range(1471, 1571):
        sql_content = generate_menu_sql(contents_id)

        filename = f'menu_{contents_id}.sql'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(sql_content)

        # 項目数を取得して表示
        category_id = ((contents_id - 1471) % 10) + 1
        random.seed(contents_id)
        templates = menu_templates_pool[category_id]
        template_idx = (contents_id // 10) % len(templates)
        template = templates[template_idx]
        num_items = random.randint(3, min(10, len(template['items'])))

        print(f'[OK] 生成完了: {filename}')
        print(f'  カテゴリー: {category_id}, 項目数: {num_items}')

    print('=' * 50)
    print('\n全100個のメニューSQLファイルを生成しました！')
    print('メニューID: 1471〜1570')
