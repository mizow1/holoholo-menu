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

def get_seed_value(contents_id, function_type):
    """contents_idから関数タイプ別のユニークなシード値を生成

    大きな素数を使ってシードの分散を改善し、異なる関数で同じシード値にならないようにする
    """
    prime = 7919  # 大きな素数
    offset_map = {
        'cards': 0,
        'title': 1,
        'catch': 2,
        'caption': 3,
        'components': 4,
        'items': 5
    }
    offset = offset_map.get(function_type, 0)
    return contents_id * prime + offset * 97

# カードデータを読み込む
card_df = pd.read_csv('card_name.csv', encoding='utf-8')
category_df = pd.read_csv('category_id.csv', encoding='utf-8')

# 全44カードのIDリスト
ALL_CARDS = list(range(1, 45))

# カテゴリー別の基本構成要素（大幅に拡充 - 各要素20パターン以上）
category_components = {
    1: {  # 両思い
        'themes': ['愛の深まり', '関係の進展', '二人の未来', '絆の強化', '愛の確認', '関係の安定', '愛の成長', '二人の幸せ', '心の繋がり', '愛の形', '永遠の絆', '真実の愛', '運命の絆', '心の調和', '愛の輝き', '二人の軌跡', '魂の繋がり', '愛の深化', '関係の成熟', '永続する愛'],
        'subjects': ['あの人', 'パートナー', '恋人', '大切な人', '愛する人', '二人', 'あの方', 'その人', '彼', '彼女', '運命の人', '最愛の人', '特別な人', 'かけがえのない人', 'ソウルメイト', '伴侶', '愛しい人', '心の支え', '人生の伴走者', '共に歩む人'],
        'concerns': ['本当の気持ち', '深層心理', '隠れた想い', '本音', '真実の感情', '心の奥', '秘めた思い', '内面', '本心', '真の気持ち', '偽らざる思い', '心の声', '素直な感情', '率直な想い', '内なる声', '魂の叫び', '真摯な思い', '誠実な気持ち', '純粋な感情', '正直な心'],
        'futures': ['進む道', '今後の二人', '将来の関係', '未来の姿', 'これからの展開', '二人の行方', '関係の方向性', '先の見通し', '運命の道筋', '歩む未来', '待ち受ける未来', '築く未来', '迎える明日', '訪れる展開', '紡ぐ未来', '描く未来図', '辿る道', '開ける未来', '続く物語', '結ばれる運命'],
        'actions': ['続けるべきこと', '大切にすること', '心がけること', '意識すべきこと', '実践すること', '行うべきこと', '守るべきこと', '育むべきこと', '磨くべきこと', '高めるべきこと', '深めるべきこと', '忘れてはならないこと', '貫くべきこと', '持ち続けるべきこと', '大事にすること', '尊重すること', '維持すること', '発展させること', '強化すること', '充実させること']
    },
    2: {  # 片思い
        'themes': ['恋の成就', '想いの実現', '片想いの行方', '恋愛成就', '恋の進展', '想いの伝わり', '恋の可能性', '願いの成就', '恋の結末', '愛の実り', '恋の結実', '想いの到達', '恋の完成', '愛の開花', '恋の勝利', '想いの成果', '恋の達成', '愛の獲得', '恋の実現', '想いの結晶'],
        'subjects': ['憧れの人', 'あの人', '好きな人', '想い人', '気になる人', 'その人', '心惹かれる人', '特別な存在', '思い続ける人', '恋する相手', '意中の人', '慕う人', '求める人', '追いかける人', '夢見る相手', '憧憬の対象', '理想の人', '想いを寄せる人', '恋い焦がれる人', '心奪われた人'],
        'concerns': ['現在の感情', '今の気持ち', '心の中', '本当の想い', '隠れた感情', '真実の心', '秘めた気持ち', '内心', '本音の部分', '正直な感情', '偽りない想い', '素の気持ち', '心の奥底', '真の感情', '率直な心', '誠実な想い', '純粋な気持ち', '心の真実', '魂の声', '内なる想い'],
        'futures': ['恋の結末', '想いの行方', '二人の未来', '恋の成り行き', '関係の展開', '恋の先行き', '二人の可能性', '恋の結果', '未来の関係', '先の展望', '恋の到達点', '想いの帰結', '二人の運命', '恋の顛末', '関係の結論', '恋の終着点', '二人の方向性', '恋の完結', '想いの終点', '関係の未来図'],
        'actions': ['避けるべきこと', '注意すること', '心がけること', '実行すべきこと', '控えること', '意識すること', '行動すべきこと', '気をつけること', '大切にすること', '忘れないこと', '守るべきこと', '続けること', 'やめるべきこと', '改善すること', '強化すること', '変えること', '維持すること', '高めること', '磨くこと', '発展させること']
    },
    3: {  # 相手の気持ち
        'themes': ['真意の把握', '本音の理解', '感情の真相', '心の読解', '想いの本質', '気持ちの実態', '心情の解明', '感情の核心', '想いの深層', '気持ちの真実', '心の真相', '感情の本体', '想いの正体', '心情の実像', '気持ちの実相', '感情の真髄', '想いの真意', '心の本音', '感情の深部', '想いの真実'],
        'subjects': ['その人', 'あの人', '相手', '気になる人', '大切な人', 'あの方', '特定の人', '問題の人', '心配な人', '知りたい相手', '対象の人', '当の本人', '例の人', '意中の人', '関心のある人', '注目の相手', '気がかりな人', '見守る相手', '思う人', '想いを寄せる人'],
        'concerns': ['偽らざる思い', '心の真実', '正直な想い', '本当の感情', '真の気持ち', '素直な心', '率直な想い', '誠実な感情', '内心の声', '心の奥底', '本音の部分', '隠れた想い', '秘めた感情', '深層の心', '真摯な思い', '純粋な気持ち', '正直な心情', '偽りない感情', '本心からの想い', '魂の叫び'],
        'futures': ['今後の展開', '先行きの様子', '未来の動向', 'これからの変化', '先の見通し', '今後の推移', '将来の姿', '先々の状況', '未来の形', '今後の成り行き', '先の展望', '将来像', '今後の方向性', '先行きの予測', '未来予想図', '今後の流れ', '先の動き', '将来展望', '今後の見込み', '先々の見通し'],
        'actions': ['効果的な方法', '適切な行動', '賢明な選択', '正しい対応', '最善の策', '有効な手段', '的確な判断', '適当な処置', '妥当な行い', '相応しい態度', '望ましい姿勢', '理想的な対応', '推奨される行動', '薦められる方法', '勧める手段', '良い選択', '正解の道', '最適解', 'ベストな対応', '賢い判断']
    },
    4: {  # 不倫
        'themes': ['葛藤', '禁断の愛', '複雑な関係', '運命の選択', '心の迷い', '愛と罪悪感', '秘密の恋', '許されぬ愛', '究極の選択', '心の分裂', '道徳との葛藤', '理性と感情', '背徳の愛', '隠れた想い', '二つの顔', '内なる戦い', '揺れる心', '倫理との対峙', '秘められた関係', '運命の岐路'],
        'subjects': ['忘れられない人', 'あの人', '特別な存在', '心惹かれる人', '運命の人', 'その人', '魅力的な相手', '心奪われた人', '愛する人', '想い人', '離れられない人', '大切な存在', '唯一無二の人', '求める相手', '憧れの人', '心の支え', '精神的支柱', '魂の伴侶', '理想の相手', '運命の相手'],
        'concerns': ['あなたへの愛', '真実の想い', '本当の気持ち', '心の声', '偽らざる感情', '深い愛情', '秘めた想い', '真摯な愛', '本音の愛', '心からの想い', '誠実な気持ち', '純粋な愛', '真の感情', '率直な想い', '素直な愛', '正直な心', '内なる愛', '魂の叫び', '心の真実', '深層の想い'],
        'futures': ['選択の先', '運命の分岐点', '二人の未来', '関係の行方', '決断の結果', '選んだ道', '未来の姿', '運命の帰結', '関係の結末', '選択の果て', '決断の先', '二人の結論', '運命の終着点', '関係の完結', '選択後の世界', '決めた未来', '関係の到達点', '運命の最終形', '二人の帰着', '選択の帰結'],
        'actions': ['決断すべきこと', '考えるべきこと', '見つめ直すこと', '問うべきこと', '判断すべきこと', '選ぶべきこと', '覚悟すること', '向き合うこと', '受け入れること', '理解すること', '決意すること', '見極めること', '吟味すること', '熟考すること', '検討すること', '省みること', '振り返ること', '再考すること', '思案すること', '選択すること']
    },
    5: {  # 夜の相性
        'themes': ['調和', '深化', '一体感', '絆の深まり', '親密さ', '心身の融合', '相性の真実', '二人の秘密', '特別な時間', '魂の共鳴', '完全な調和', '究極の一体感', '深い結びつき', '肉体と精神', '愛の極致', '二人だけの世界', '心身の調和', '完璧な相性', '特別な絆', '深い繋がり'],
        'subjects': ['あの方', 'パートナー', '相手', 'その人', '愛する人', '大切な人', '運命の人', '特別な存在', '心を許す人', '魂の伴侶', '二人', 'あの人', '愛しい人', '心通う相手', '理解し合える人', '一体となる人', '共鳴する相手', '心身を委ねる人', '信頼する人', '結ばれた相手'],
        'concerns': ['調和', '相性', '一体感', '満足度', '深まり', '心地よさ', '充実感', '幸福感', '親密度', '繋がり', '共鳴度', '適合性', '調和度', '合致度', 'マッチング', '波長', 'フィーリング', 'ケミストリー', 'シナジー', 'ハーモニー'],
        'futures': ['深化', '発展', '進化', '成長', '高まり', '深まり', '強化', '充実', '向上', '昇華', '熟成', '洗練', '完成', '開花', '結実', '到達', '極致', '完璧', '理想', '究極'],
        'actions': ['意識すること', '大切にすること', '高めること', '深めること', '磨くこと', '育むこと', '強化すること', '向上させること', '充実させること', '発展させること', '極めること', '追求すること', '研ぎ澄ますこと', '洗練させること', '完成させること', '昇華させること', '成熟させること', '豊かにすること', '深化させること', '進化させること']
    },
    6: {  # 結婚
        'themes': ['永遠の絆', '結婚生活', '夫婦の未来', '家庭の築き方', '二人の人生', '結婚の意味', '生涯のパートナー', '家族の形成', '共同生活', '人生の伴侶', '結婚の真実', '夫婦の絆', '家庭の基盤', '二人の誓い', '婚姻関係', '夫婦の道', '家庭運営', '結婚の本質', '永続する関係', '生涯の約束'],
        'subjects': ['結婚相手', 'パートナー', '配偶者', '伴侶', '生涯の伴侶', '運命の人', '将来の夫', '将来の妻', '人生の伴走者', '共に歩む人', 'かけがえのない人', '選んだ相手', '誓い合った人', '結ばれる人', '共にする人', '添い遂げる人', '支え合う相手', '分かち合う人', '築く相手', '歩む伴侶'],
        'concerns': ['結婚の意思', '真剣度', '覚悟', '決意', '本気度', '誠実さ', '真摯な想い', '結婚への想い', '将来への考え', '家族への思い', '責任感', 'commitment', '献身度', '真剣さ', '本音', '真意', '心の準備', '決断力', '覚悟の程', '本当の気持ち'],
        'futures': ['結婚後の生活', '夫婦の未来', '家庭の将来', '二人の人生', '結婚生活', '家族の未来', '共同生活', '人生設計', '将来設計', '夫婦の道のり', '家庭の形', '二人の歩み', '結婚の行方', '家族の姿', '共に築く未来', '二人の運命', '家庭運営', '夫婦の軌跡', '生活の展望', '人生の設計図'],
        'actions': ['準備すべきこと', '覚悟すること', '学ぶべきこと', '理解すること', '話し合うこと', '決めること', '確認すること', '考えること', '築くべきこと', '育むべきこと', '大切にすること', '尊重すること', '協力すること', '支え合うこと', '理解し合うこと', '譲り合うこと', '思いやること', '信頼すること', '尊敬すること', '愛し合うこと']
    },
    7: {  # 人生
        'themes': ['人生の岐路', '運命の方向性', '生きる意味', '人生の目的', '天命', '使命', '人生設計', '自己実現', '生きがい', '人生の価値', '存在意義', '人生哲学', '生の意味', '人生の真実', '運命の道', '人生の軌跡', '生き方', '人生観', '価値観', '人生の選択'],
        'subjects': ['あなた自身', '自分', '本当のあなた', '魂', '内なる自己', '真の自分', '本来の姿', '深層の自己', '潜在的な自分', '本質的な存在', '真実の自己', '核心の自分', '根源的な存在', '本当の姿', '素の自分', '純粋な自己', '原初の自分', '本来の存在', '真の姿', '魂の本質'],
        'concerns': ['心の幸せ', '生きがい', '人生の満足', '充実感', '幸福感', '心の平安', '内なる喜び', '真の幸せ', '心の充足', '精神的満足', '魂の喜び', '人生の意義', '存在価値', '生の充実', '心の豊かさ', '精神の安寧', '魂の充足', '真の満足', '深い喜び', '究極の幸せ'],
        'futures': ['現在地点', '今の立ち位置', '現状', '現在の状況', '今の段階', '現時点', '今この瞬間', '現在の位置', '今の場所', '現段階', '今のステージ', '現在のフェーズ', '今の時点', '現時の状態', '今の状況', '現在のレベル', '今の立場', '現時点の状態', '今の境遇', '現在の環境'],
        'actions': ['人生の指針', '進むべき道', '選ぶべき方向', '歩むべき道', '目指す方向性', '取るべき道筋', '選択すべき道', '進むべき方向', '向かうべき先', '辿るべき道', '歩むべき方向', '選ぶべき道筋', '進むべき方針', '取るべき方向', '目指すべき道', '向かうべき方向', '辿るべき方向', '歩くべき道', '選択すべき方向', '進むべき道筋']
    },
    8: {  # 仕事
        'themes': ['仕事運', 'キャリア', '職業的成功', '仕事の発展', '職場環境', 'プロフェッショナル', '仕事の充実', 'キャリアパス', '職業的満足', '仕事の成果', 'ビジネス運', '職業運', 'キャリア形成', '仕事の実現', '職業的達成', '仕事の成就', 'プロとしての道', '職業的成長', '仕事の完成', 'キャリアの確立'],
        'subjects': ['あなた', '自分自身', '職業人としての自分', 'プロとしてのあなた', 'ビジネスパーソン', '社会人', '働くあなた', 'キャリア形成者', '職業的存在', '仕事人', 'プロフェッショナル', '職人', 'ビジネスマン', 'ワーカー', '従事者', '実務者', 'キャリアウーマン', '職業人', '稼ぐ者', '働き手'],
        'concerns': ['仕事との向き合い方', '職業意識', 'プロ意識', '仕事への姿勢', '職業倫理', '仕事観', 'キャリア観', '職業観', '労働観', '仕事哲学', 'プロ精神', '職人気質', 'ワークスタイル', '仕事への思い', '職業への想い', 'キャリアへの考え', '仕事の価値観', '職業的信念', '仕事への信念', 'プロとしての誇り'],
        'futures': ['仕事の将来性', 'キャリアの行方', '職業的未来', '仕事の見通し', 'キャリアパス', '職業的展望', '仕事の先行き', 'キャリアの展開', '職業的方向性', '仕事の可能性', 'キャリアの未来', '職業的な道', '仕事の発展性', 'キャリア展望', '職業的成長', '仕事の進展', 'キャリアビジョン', '職業的到達点', '仕事の結実', 'キャリアゴール'],
        'actions': ['効果的な方法', '成功の秘訣', '実践すべきこと', '重視すべき点', '意識すべきこと', '取り組むべきこと', '磨くべき能力', '高めるべきスキル', '発展させること', '強化すべき点', '改善すべきこと', '継続すべきこと', '追求すべきこと', '究めるべきこと', '身につけること', '習得すること', '鍛えること', '育成すること', '開発すること', '向上させること']
    },
    9: {  # 復縁
        'themes': ['関係の再構築', 'やり直し', '復縁の可能性', '再び結ばれる運命', '関係の修復', '二度目のチャンス', 'もう一度の愛', '再会の意味', '縁の再生', '愛の復活', '絆の再建', '関係の蘇生', '愛の再燃', '縁の復活', '再スタート', '新たな始まり', '関係の再生', '絆の修復', '愛の再構築', '関係の再開'],
        'subjects': ['別れた相手', '元恋人', '忘れられない人', '過去の恋人', 'かつての相手', '以前の恋人', '昔の相手', '元パートナー', '過去の愛', '失った人', '別れたあの人', 'もう一度会いたい人', 'やり直したい相手', '未練のある人', '思い出の人', '戻りたい相手', '再会したい人', '縁を繋ぎたい人', '心残りの相手', '忘れられぬ人'],
        'concerns': ['今の想い', '現在の気持ち', '復縁への意思', 'やり直す気持ち', '過去への想い', '未練', '心残り', '後悔', '愛の残滓', '消えない想い', '忘れられない気持ち', 'まだある愛', '残る感情', '諦めきれない想い', '戻りたい気持ち', 'もう一度の想い', '再会への願い', '復縁への願望', 'やり直したい思い', '縁の再生願望'],
        'futures': ['復縁の可能性', 'やり直しの見込み', '二人の再会', '関係の再開', '縁の復活', '愛の再燃', '二度目のチャンス', '関係の修復', '絆の再構築', '再スタートの可能性', '復縁の展望', 'やり直せる未来', '二人の再生', '関係の蘇生', '愛の復活', '縁の再生', '再び結ばれる未来', 'もう一度の関係', '二人の再建', '復縁後の未来'],
        'actions': ['取るべき行動', '実行すべきこと', '心がけること', '避けるべきこと', '準備すること', '整理すべきこと', '理解すること', '受け入れること', '反省すること', '改善すること', '変えるべきこと', '成長すること', '学ぶべきこと', '考え直すこと', '見つめ直すこと', '決断すること', '選択すること', '判断すること', '覚悟すること', '行動に移すこと']
    },
    10: {  # 出会い
        'themes': ['運命の出会い', '新しい出会い', '縁の始まり', '恋の予感', '出会いの運命', '新たな縁', '恋愛運', '出会いのチャンス', '運命の人', '理想の相手', '素敵な出会い', '特別な縁', '出会いの奇跡', '恋の始まり', '縁結び', '出会いの幸運', '新しい恋', '運命的な出会い', '出会いの予兆', '恋愛の予感'],
        'subjects': ['あなた', '自分自身', '恋を求めるあなた', '出会いを待つあなた', '愛を探すあなた', '恋愛運のあなた', '縁を求める自分', '運命の相手を待つ自分', '理想を持つあなた', '幸せを求めるあなた', '愛に飢えたあなた', '恋に憧れる自分', '出会いを願うあなた', '素敵な人を探すあなた', '運命を信じるあなた', '縁を大切にするあなた', '愛を信じる自分', '幸せを掴みたいあなた', '出会いに期待するあなた', '恋の扉を開くあなた'],
        'concerns': ['今の恋愛運', '出会いの運勢', '恋愛傾向', '魅力度', 'モテ運', '恋愛適性', '恋の運命', '出会いの運', '恋愛の波', '縁の強さ', '恋愛エネルギー', '出会いの引力', '恋の磁力', '魅力の輝き', '恋愛オーラ', '出会いの波動', '恋の予感度', '縁の巡り', '恋愛バイオリズム', '出会いの好機'],
        'futures': ['出会いの時期', '縁の訪れ', '恋の始まり', '運命の瞬間', '出会いのタイミング', '理想の人との出会い', '素敵な縁', '新しい恋', '運命の相手', '特別な出会い', '恋愛の始動', '縁の結び', '出会いの実現', '理想との遭遇', '運命的瞬間', '恋の開始', '縁の成立', '出会いの成就', '理想の実現', '運命の成就'],
        'actions': ['引き寄せる方法', '出会うための行動', '魅力を高めること', '準備すべきこと', '心がけること', '実践すること', '磨くべきこと', '意識すること', '大切にすること', '高めること', '開くこと', '広げること', '積極性', '前向きさ', 'ポジティブさ', 'オープンマインド', '自分磨き', '内面の充実', '外見の向上', '魅力の開発']
    }
}

def escape_sql_string(s):
    """SQL文字列をエスケープ（シングルクォートを2重に）"""
    return str(s).replace("'", "''")

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

def get_random_cards_for_menu(contents_id, num_items):
    """contents_id毎に完全ランダムなカード配列を生成（44枚全てから選択）"""
    random.seed(get_seed_value(contents_id, 'cards'))

    # 全44カードをシャッフル
    all_cards = ALL_CARDS.copy()
    random.shuffle(all_cards)

    # 必要な数×4パターン分のカードを用意（重複なし）
    needed_cards = num_items * 4
    if needed_cards > 44:
        # 44枚以上必要な場合は繰り返し
        result = all_cards * ((needed_cards // 44) + 1)
        return result[:needed_cards]
    else:
        return all_cards[:needed_cards]

def generate_dynamic_item_name(contents_id, item_index, category_id):
    """完全動的に項目名を生成（固定パターンを使用しない）"""
    random.seed(get_seed_value(contents_id, 'items') + item_index)

    components = category_components[category_id]

    # ランダムに要素を選択
    theme = random.choice(components['themes'])
    subject = random.choice(components['subjects'])
    concern = random.choice(components['concerns'])
    future = random.choice(components['futures']) if isinstance(components['futures'], list) else components['futures']
    action = random.choice(components['actions'])

    # 30種類以上の動的パターンから選択
    patterns = [
        f'{subject}の{concern}',
        f'{future}について',
        f'{theme}の真相',
        f'{action}',
        f'{subject}が感じていること',
        f'{concern}の本質',
        f'{future}の可能性',
        f'{theme}における{action}',
        f'{subject}の視点から見た{concern}',
        f'{future}への道筋',
        f'{concern}を深く知る',
        f'{theme}の核心',
        f'{subject}との{future}',
        f'{action}で変わること',
        f'{concern}が示すもの',
        f'{future}の展望',
        f'{theme}を左右する要因',
        f'{subject}が大切にすること',
        f'{concern}の深層',
        f'{future}における{theme}',
        f'{action}の意味',
        f'{subject}の{future}に対する想い',
        f'{concern}から見える真実',
        f'{theme}の行方',
        f'{future}を実現する{action}',
        f'{subject}が望む{concern}',
        f'{concern}と{future}の関係',
        f'{theme}における重要ポイント',
        f'{subject}にとっての{action}',
        f'{future}への{concern}',
        f'{theme}の全体像',
        f'{action}がもたらす{future}',
        f'{subject}の{concern}と{future}',
        f'{concern}における{theme}',
        f'{future}を導く{action}',
        f'{subject}が求める{theme}',
        f'{concern}の意味と{future}',
        f'{theme}としての{action}',
        f'{future}における{subject}の役割',
        f'{concern}が教えてくれること'
    ]

    pattern = random.choice(patterns)
    return pattern

def generate_varied_reading_text(card_id, item_text, category_id, contents_id, item_index, pattern_num):
    """多様性の高い鑑定文を生成（300文字以上）"""
    random.seed(contents_id * 1000 + item_index * 10 + pattern_num)

    card_name = get_card_name(card_id)
    card_keyword = get_card_keyword(card_id)
    card_summary = get_card_summary(card_id)

    # カードの紹介部分（10パターン以上）
    intro_patterns = [
        f"【{card_name}】のカードが出ました。このカードは「{card_summary}」を意味します。",
        f"【{card_name}】のカードが示されました。「{card_summary}」というメッセージが込められています。",
        f"出たカードは【{card_name}】。{card_summary}ことを示す重要なカードです。",
        f"【{card_name}】のカードが現れました。{card_keyword}を象徴し、{card_summary}ことを教えてくれます。",
        f"カードに現れたのは【{card_name}】。テーマは「{card_summary}」です。",
        f"【{card_name}】のカードです。{card_name}が示すのは{card_keyword}であり、{card_summary}ことの重要性です。",
        f"タロットが告げるのは【{card_name}】。{card_keyword}というキーワードで、{card_summary}ことを伝えています。",
        f"【{card_name}】が選ばれました。「{card_summary}」がこのカードの核心的メッセージです。",
        f"ハワイアンタロットの【{card_name}】。{card_keyword}のエネルギーを持ち、{card_summary}ことを説いています。",
        f"【{card_name}】のカードが語りかけます。{card_summary}という智恵を、あなたに授けようとしています。"
    ]

    intro = random.choice(intro_patterns)

    # 本文パターン（カテゴリーと項目内容に応じて20パターン以上）
    main_patterns = [
        f"{item_text}において、{card_keyword}が極めて重要な役割を果たしています。この{card_keyword}のエネルギーを正しく理解し、日々の中で意識することで、あなたの望む方向へと確実に進んでいけるでしょう。時には思いもよらない展開があるかもしれませんが、それもすべて成長のための貴重な経験です。{card_keyword}という視点を持ち続けることで、真実が明らかになり、道が開けていきます。焦らず、一歩ずつ着実に前進してください。",

        f"{item_text}に関して、カードは{card_keyword}という重要なメッセージを伝えています。あなたが今必要としているのは、この{card_keyword}を深く理解し、それを実践に移していくことです。表面的な理解だけでは不十分で、本質的な部分まで掘り下げる必要があります。{card_keyword}の真の意味を悟ることで、状況は大きく好転し、あなたの願いは実現に向かって動き出すでしょう。信じる心を持ち続けてください。",

        f"あなたの{item_text}には、{card_keyword}が深く関わっています。この{card_keyword}というテーマを無視することはできません。むしろ、それを受け入れ、自分のものとすることで、新たな可能性が開けてきます。{card_keyword}のエネルギーは強力で、あなたを望む未来へと導く力を持っています。ただし、それには素直な心と前向きな姿勢が必要です。恐れずに、{card_keyword}と共に歩んでいきましょう。",

        f"カードが示す{item_text}の答えは、{card_keyword}にあります。この{card_keyword}を軸にして物事を考え、行動することで、あなたは正しい道を歩むことができるでしょう。今は混乱や不安があるかもしれませんが、{card_keyword}という羅針盤があれば、必ず目的地に辿り着けます。自分を信じ、{card_keyword}の導きに従ってください。答えは必ずそこにあります。",

        f"{item_text}を考える上で、{card_keyword}は欠かせない要素となっています。{card_keyword}の本質を理解し、それに基づいて判断や選択を行うことが、成功への鍵です。一見困難に思える状況でも、{card_keyword}の視点から見れば、新たな可能性や解決策が見えてくるはずです。柔軟な思考と開かれた心を持って、{card_keyword}のメッセージを受け取りましょう。道は必ず開けます。",

        f"タロットが告げる{item_text}に関する真実は、{card_keyword}に集約されています。{card_keyword}という言葉の中に、あなたが求めている答えのすべてが込められています。これは単なる偶然ではなく、宇宙からのメッセージです。{card_keyword}を深く瞑想し、その意味を自分なりに解釈することで、真実が見えてきます。直感を信じ、心の声に耳を傾けてください。真実はあなたの中にあります。",

        f"{item_text}において最も大切なのは、{card_keyword}という概念を正しく認識することです。{card_keyword}は、あなたの現状を打破し、新たなステージへと導く力を持っています。今はまだピンとこないかもしれませんが、時間をかけて{card_keyword}と向き合うことで、その深い意味が理解できるようになります。急がず、焦らず、{card_keyword}と共に成長していきましょう。未来は明るく輝いています。",

        f"あなたが知りたい{item_text}の核心は、{card_keyword}にあります。{card_keyword}というキーワードが、すべての疑問に対する答えを内包しています。このメッセージを受け取ったということは、あなたが正しい道を歩んでいる証拠です。{card_keyword}を胸に刻み、日々の生活の中で実践していくことで、望む未来が確実に近づいてきます。信念を持って進んでください。",

        f"{item_text}に対するハワイアンタロットの答えは明確です。それは{card_keyword}です。この{card_keyword}という要素を、あなたの人生にどう取り入れるかが、今後の展開を大きく左右します。{card_keyword}は、単なる概念ではなく、実践すべき具体的な指針です。日々の選択や行動の中で{card_keyword}を意識し、それに沿って生きることで、人生は豊かに実り多いものとなるでしょう。",

        f"カードが明かす{item_text}の真実において、{card_keyword}は中心的な役割を果たしています。{card_keyword}を理解することは、単に知識を得ることではなく、自己変容のプロセスでもあります。{card_keyword}のエネルギーを受け入れ、それと一体となることで、あなたは新しい自分に生まれ変わることができます。この機会を逃さず、{card_keyword}という贈り物を大切に受け取ってください。"
    ]

    # 追加のバリエーション（カテゴリー特化型）
    if category_id in [1, 2, 6, 9]:  # 恋愛系
        main_patterns.extend([
            f"{item_text}に秘められた真実は、{card_keyword}によって明らかになります。愛に関わるあらゆる疑問や不安は、{card_keyword}という視点から見直すことで解消されていきます。二人の絆を深め、関係をより良いものにするためには、{card_keyword}を中心に据えた行動が不可欠です。愛は複雑なようで実はシンプル。{card_keyword}さえ忘れなければ、二人の未来は明るく輝くでしょう。",

            f"恋愛における{item_text}を占う上で、{card_keyword}以上に重要なものはありません。{card_keyword}は、二人の関係を支える基盤であり、愛を育む土壌です。この{card_keyword}を大切にし、日々実践することで、関係は確実に深まり、絆は強固なものとなります。時には試練もありますが、{card_keyword}があれば必ず乗り越えられます。愛を信じ、{card_keyword}と共に歩んでください。"
        ])

    if category_id in [7, 8]:  # 人生・仕事系
        main_patterns.extend([
            f"{item_text}という人生の重要なテーマにおいて、{card_keyword}は羅針盤となります。人生の岐路に立ったとき、{card_keyword}を指針とすることで、正しい選択ができるでしょう。{card_keyword}は、あなたの使命や天命とも深く関わっています。この{card_keyword}を追求し、極めることで、あなたの人生は本来あるべき姿へと近づいていきます。運命を信じ、{card_keyword}に従って進んでください。",

            f"キャリアや人生設計における{item_text}を考える際、{card_keyword}は最重要ファクターです。成功者に共通するのは、この{card_keyword}を深く理解し、実践していることです。{card_keyword}という軸をぶらさず、一貫して追求することで、あなたは望む成果を手にすることができるでしょう。焦らず、着実に、{card_keyword}を磨き続けてください。"
        ])

    main_text = random.choice(main_patterns)

    # 締めくくり（5パターン）
    endings = [
        "カードのメッセージを心に留め、前向きに歩んでいってください。",
        "ハワイアンタロットの智恵を信じ、自分の道を進んでください。",
        "この啓示を大切にし、人生をより豊かなものにしていきましょう。",
        "カードが示す道を信じて、勇気を持って一歩を踏み出してください。",
        "タロットの導きに従い、幸せな未来を自らの手で掴み取ってください。"
    ]

    ending = random.choice(endings)

    return intro + main_text + ending

def generate_unique_menu_name(contents_id, category_id):
    """完全ユニークなメニュー名を生成"""
    random.seed(get_seed_value(contents_id, 'title'))

    components = category_components[category_id]

    # ランダムに要素を選択
    theme = random.choice(components['themes'])
    subject = random.choice(components['subjects'])
    concern = random.choice(components['concerns'])
    future = random.choice(components['futures']) if isinstance(components['futures'], list) else components['futures']
    action = random.choice(components['actions'])

    # 50種類以上の動的パターン
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

    return random.choice(name_patterns)

def generate_unique_catch(contents_id, category_id):
    """完全ユニークなキャッチフレーズを生成"""
    random.seed(get_seed_value(contents_id, 'catch'))

    components = category_components[category_id]
    theme = random.choice(components['themes'])
    subject = random.choice(components['subjects'])
    concern = random.choice(components['concerns'])
    future = random.choice(components['futures']) if isinstance(components['futures'], list) else components['futures']

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

    return random.choice(catch_patterns)

def generate_unique_caption(contents_id, category_id):
    """完全ユニークなキャプションを生成"""
    random.seed(get_seed_value(contents_id, 'caption'))

    components = category_components[category_id]
    theme = random.choice(components['themes'])
    subject = random.choice(components['subjects'])
    concern = random.choice(components['concerns'])
    future = random.choice(components['futures']) if isinstance(components['futures'], list) else components['futures']

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

    return random.choice(caption_patterns)

def calculate_start_date(contents_id):
    """公開日を計算（contents_id=1042が2026-01-01基準）"""
    base_date = datetime(2026, 1, 1)
    base_id = 1042
    days_diff = contents_id - base_id
    start_date = base_date + timedelta(days=days_diff)
    return start_date.strftime('%Y-%m-%d %H:%M:%S')

def generate_truly_unique_menu_sql(contents_id):
    """完全にユニークなメニュー用SQLファイルを生成"""
    # カテゴリーをローテーション（1-10をループ）
    category_id = ((contents_id - 1043) % 10) + 1

    # 項目数をランダムに決定（3〜10項目）
    random.seed(contents_id)
    num_items = random.randint(3, 10)

    # 完全ユニークなメニュー名・キャッチ・キャプションを生成
    menu_name = generate_unique_menu_name(contents_id, category_id)
    catch = generate_unique_catch(contents_id, category_id)
    caption = generate_unique_caption(contents_id, category_id)

    # 公開日を計算
    start_date = calculate_start_date(contents_id)

    # contents_id毎に完全ランダムなカード配列を生成
    menu_cards = get_random_cards_for_menu(contents_id, num_items)

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

    # 完全動的に項目名を生成
    items = []
    for i in range(num_items):
        item_name = generate_dynamic_item_name(contents_id, i, category_id)
        items.append(item_name)

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

    # 各項目に4つの結果を生成
    card_index = 0
    for i, item_name in enumerate(items, 1):
        menu_id = int(f"{contents_id}{i:02d}")

        for j in range(1, 5):  # 4パターン
            result_id = int(f"{contents_id}{i:02d}{j:02d}")
            card_id = menu_cards[card_index]
            card_index += 1

            # 多様な鑑定文を生成
            result_body = generate_varied_reading_text(card_id, item_name, category_id, contents_id, i, j)

            result_items.append(f"({contents_id}, {menu_id}, {result_id}, '{escape_sql_string(result_body)}')")
            card_items.append((contents_id, menu_id, result_id, card_id))

    sql += ',\n'.join(result_items) + ';\n\n'

    # カードテーブルを追加
    sql += "-- 4. mana_cardテーブルに追加\n"
    sql += "INSERT INTO flowt_seimei.mana_card (contents_id, menu_id, result_id, body) VALUES\n"

    card_sql_items = []
    for contents_id_val, menu_id, result_id, card_id in card_items:
        card_sql_items.append(f"({contents_id_val}, {menu_id}, {result_id}, {card_id})")

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
        # デフォルトはテスト用の5個
        start_id = 1043
        end_id = 1047

    print('完全ユニークなメニュー生成を開始します...')
    print('=' * 50)

    for contents_id in range(start_id, end_id + 1):
        sql_content = generate_truly_unique_menu_sql(contents_id)

        filename = f'menu_{contents_id}.sql'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(sql_content)

        category_id = ((contents_id - 1043) % 10) + 1
        random.seed(contents_id)
        num_items = random.randint(3, 10)

        print(f'[OK] 生成完了: {filename}')
        print(f'  カテゴリー: {category_id}, 項目数: {num_items}')

    print('=' * 50)
    total = end_id - start_id + 1
    print(f'\n全{total}個のメニューSQLファイルを生成しました！')
    print(f'メニューID: {start_id}〜{end_id}')
    print('\n重複・類似チェックを実施してください。')
