import pandas as pd
import sys
import random
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

# Excelファイル読み込み
df = pd.read_excel('ホロホロタロット追加メニュー.xlsx')
df_contents = df[df['contents_id'].notna()].copy()
df_contents = df_contents[['contents_id', 'name', 'caption', 'category']].copy()
df_contents = df_contents.drop_duplicates(subset=['contents_id'])
df_contents = df_contents[df_contents['contents_id'].apply(lambda x: isinstance(x, (int, float)) and x > 0)]

# 100件のメニューだけを取得
df_contents = df_contents.head(100)

def generate_comment_for_menu(name, caption, category):
    """メニューの内容に合わせたコメントを生成"""
    name_str = str(name) if pd.notna(name) else ""
    caption_str = str(caption) if pd.notna(caption) else ""
    category_str = str(category) if pd.notna(category) else ""

    # キーワードベースでコメントを生成
    comments_pool = []

    # 結婚関連
    if '結婚' in name_str or '結婚' in caption_str:
        comments_pool = [
            '結婚相手がどんな人か分かって嬉しい。',
            '運命の人の姿が見えてきた気がします。',
            '結婚相手のプロフィール、すごく詳しく教えてもらえました。',
            '理想の結婚相手像が明確になりました。',
            '結婚できるか不安でしたが、希望が持てました。',
            '結婚運について知れて良かったです。',
        ]
    # 復縁関連
    elif '復縁' in name_str or '復活愛' in name_str:
        comments_pool = [
            '元彼のこと諦められなくて。少し希望が見えてきました。',
            '別れたあの人の気持ちが分かって良かったです。',
            'やり直せる可能性があるって分かって嬉しい。',
            '復縁できるかもって思えてきました。',
            'あの人の言葉、信じていいか悩んでたので助かりました。',
            'もう一度やり直したい。可能性が見えてきました。',
        ]
    # 片想い関連
    elif '片想い' in name_str or '片思い' in name_str:
        comments_pool = [
            '二人の出会いに意味があったんですね。',
            '片思いの意味が分かった気がします。',
            '出会いの真相が知れて良かったです。',
            'この恋、大切にしようと思いました。',
            '片想いの裏側が分かりました。',
        ]
    # 仕事・職種関連（カテゴリ8）
    elif category_str == '8.0' or category_str == '8' or '仕事' in name_str or '職種' in name_str or 'キャリア' in name_str or '評価' in name_str:
        comments_pool = [
            '職場での評価が気になってたので参考になりました。',
            '周りからどう思われてるか分かってスッキリしました。',
            '自分に合った仕事が分かって良かったです。',
            '幸せになれる職種が分かりました。',
            '転職するか迷ってたので、ヒントをもらえました。',
            '仕事運について知れて良かったです。',
            'キャリアの方向性が見えてきました。',
            '過去と現在の評価の変化が分かりました。',
        ]
    # 人間関係・人生の目的関連（カテゴリ7）
    elif category_str == '7.0' or category_str == '7' or '人間関係' in name_str or '人生' in name_str or '評判' in name_str or '未来' in name_str:
        comments_pool = [
            '周りとの関係を見直すいいきっかけになりました。',
            '人生の目的が少し見えてきた気がします。',
            '自分の生まれた意味、考えたことなかったです。',
            '人間関係で悩んでたので助かりました。',
            '今と未来の自分の姿が分かって良かったです。',
            '1年後の自分が楽しみになってきました。',
            '人生の意味が分かった気がします。',
            '周囲からの評判が気になってたので参考になりました。',
        ]
    # 恋愛・気持ち関連（カテゴリ3、2、9）
    elif category_str in ['3.0', '3', '2.0', '2', '9.0', '9'] or '気持ち' in name_str or '恋' in name_str or 'あの人' in name_str or '彼' in name_str:
        comments_pool = [
            '彼が私のことをどう思ってるのか知れて嬉しい。',
            'あの人の気持ちが分かって安心しました。',
            '彼の本音が知れて良かったです。',
            '恋愛感情があるって分かって嬉しい。',
            'モヤモヤしてた気持ちがスッキリしました。',
            '友情どまりか恋愛感情か分かりました。',
            'あの人の気持ちを知ることができて良かったです。',
        ]
    # 金運関連
    elif '金運' in name_str or 'お金' in name_str:
        comments_pool = [
            '金運アップの方法が分かりました。',
            'お金の使い方を見直すきっかけになりました。',
            '経済的な不安が少し和らぎました。',
        ]
    # デフォルト
    else:
        comments_pool = [
            '占ってもらって良かったです。',
            '参考になりました。ありがとうございます。',
            '当たってる気がします。',
            'すごく詳しく教えてもらえました。',
            '前向きになれました。',
            '悩みが軽くなりました。',
            '希望が持てました。',
        ]

    return random.choice(comments_pool)

# 使用済みコメントを追跡（contents_idごとに）
used_comments = set()

def get_unique_comment(name, caption, category):
    """重複しないコメントを取得"""
    max_attempts = 50
    for _ in range(max_attempts):
        comment = generate_comment_for_menu(name, caption, category)
        if comment not in used_comments:
            used_comments.add(comment)
            return comment
    # 50回試してもダメなら重複を許容
    comment = generate_comment_for_menu(name, caption, category)
    used_comments.add(comment)
    return comment

# 日付生成
def random_date():
    start_date = datetime(2023, 10, 1)
    end_date = datetime(2023, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d 00:00:00')

# SQLファイルの生成
output_lines = []
output_lines.append("INSERT INTO flowt_seimei.mana_comment (contents_id,title,comment,score,approval,`date`) VALUES")

records = []
for idx, row in df_contents.iterrows():
    contents_id = int(row['contents_id'])
    name = row['name']
    caption = row['caption']
    category = row['category']

    comment = get_unique_comment(name, caption, category)
    score = random.randint(3, 5)
    date = random_date()
    records.append(f"\t ({contents_id},NULL,'{comment}',{score},1,'{date}')")

# 10件ごとにINSERT文を分割
chunk_size = 10
for i in range(0, len(records), chunk_size):
    chunk = records[i:i+chunk_size]
    if i > 0:
        output_lines.append("INSERT INTO flowt_seimei.mana_comment (contents_id,title,comment,score,approval,`date`) VALUES")
    for j, record in enumerate(chunk):
        if j < len(chunk) - 1:
            output_lines.append(record[:-1] + ',')
        else:
            output_lines.append(record + ';')

# ファイル保存
timestamp = datetime.now().strftime('%Y%m%d%H%M')
filename = f'mana_comment_{timestamp}.sql'
with open(filename, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f'生成完了: {filename}')
print(f'メニュー数: {len(df_contents)}')
print(f'コメント数: {len(records)}')
print(f'ユニークコメント数: {len(used_comments)}')
print(f'\n最初の10件のコメント確認:')
for i in range(min(10, len(df_contents))):
    row = df_contents.iloc[i]
    print(f"\nID {int(row['contents_id'])}: {str(row['name'])[:40]}...")
    # recordsから該当するコメントを抽出
    comment_match = records[i].split("'")[1]
    print(f"  コメント: {comment_match}")
