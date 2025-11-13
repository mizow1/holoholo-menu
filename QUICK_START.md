# クイックスタートガイド

## 3ステップでメニュー生成

### ステップ1：依頼JSONを作成

```bash
python generate_truly_unique_menus.py --request 1043 1043
```

→ `reading_requests_1043_1043.json` が生成される

---

### ステップ2：Claudeに鑑定文を生成してもらう

**Claudeへの依頼文（コピペ用）**:

```
reading_requests_1043_1043.json を読み込んで、以下の要件で鑑定文を生成してください：

【要件】
1. 各項目の "reading_text" を埋める
2. カードの「キーワード」と「概要」を具体的に活用
3. 占い項目に対して明確な答えを提示
4. 300文字以上の充実した内容
5. 定型文は一切使用しない

【追加】
メニュー全体の情報も追加してください：
- "menu_name": メニュー内容を反映した魅力的なタイトル（項目数を明示）
- "catch": 短くキャッチーなフレーズ
- "caption": 2-3文でメニュー内容の核心を説明

完成したら readings_filled_1043_1043.json として保存してください。
```

---

### ステップ3：SQLファイルを生成

```bash
python generate_truly_unique_menus.py --generate readings_filled_1043_1043.json
```

→ `menu_1043.sql` が生成される

---

## チェックポイント

### 生成後の確認

```bash
# SQLファイルの先頭を確認
head -n 20 menu_1043.sql
```

**確認項目**:
- ✅ name が魅力的
- ✅ catch がキャッチー
- ✅ caption が具体的
- ✅ 鑑定文にカード名が含まれている
- ✅ 鑑定文が300文字以上

---

## 複数メニューの生成

### 一度に5個生成する場合

```bash
# ステップ1
python generate_truly_unique_menus.py --request 1043 1047

# ステップ2: Claudeに依頼
# reading_requests_1043_1047.json を処理してもらう

# ステップ3
python generate_truly_unique_menus.py --generate readings_filled_1043_1047.json
```

→ `menu_1043.sql`, `menu_1044.sql`, ... `menu_1047.sql` が生成される

---

## トラブルシューティング

### エラー：カードIDが不正

→ `card_name.csv` を確認（カードID 1-44が存在すること）

### エラー：JSONの形式が不正

→ JSONファイルをJSONフォーマッターで確認

### 鑑定文が短すぎる

→ Claudeに「300文字以上」を強調して再依頼

### タイトルが魅力的でない

→ Claudeに「メニューの8項目の内容を反映した、ユーザーの興味を惹きつける魅力的なタイトル」を再依頼

---

## テンプレート

### Claudeへの依頼文テンプレート

```
reading_requests_[ID]_[ID].json を読み込んで、以下の要件で高品質な鑑定文を生成してください：

【鑑定文の要件】
1. 各項目の "reading_text" に300文字以上の鑑定文を記入
2. カード情報を必ず活用：
   - card_name: カード名を明示
   - card_keyword: キーワードの意味を解釈
   - card_summary: 概要を具体的なアドバイスに展開
3. 占い項目（item_name）に対して明確な答えを提示
4. 定型文は絶対に使用しない（「あなたの未来は明るく〜」等の汎用表現は禁止）
5. 具体的なアドバイスを含める

【タイトルの要件】
メニュー全体に以下を追加：
- "menu_name": メニュー内容を反映した魅力的なタイトル
  - 項目数を明示（例：◆8つの真実）
  - ユーザーの核心的な悩みに直結する表現
  - 視覚的アクセント（◆や【】を使用）
- "catch": 10-20文字の短くキャッチーなフレーズ
  - 「完全解明」「徹底鑑定」等のインパクトある言葉
- "caption": 2-3文でメニュー内容を説明
  - 疑問形を使うとユーザーの共感を得やすい
  - 例：「相手は今あなたに何を感じている？」

完成したJSONを readings_filled_[ID]_[ID].json として保存してください。
```

---

**参考**: 詳細は `CLAUDE_MENU_GENERATION_GUIDE.md` を参照
