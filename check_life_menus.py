import pandas as pd

# Excelファイル読み込み
df_menu = pd.read_excel('ホロホロタロット追加メニュー.xlsx', sheet_name='メニュー')

# メニューIDを数値に変換
df_menu['メニューID'] = pd.to_numeric(df_menu['メニューID'], errors='coerce')

# カテゴリー7（人生・運勢）のメニューを抽出
# カラム名が文字化けしているので、実際のカラム名を確認
print('カラム名:', df_menu.columns.tolist()[:10])
print()

# カテゴリー列を探す（大カテゴリーまたはカテゴリー）
category_col = None
for col in df_menu.columns:
    if 'カテゴリー' in str(col) or 'category' in str(col).lower():
        category_col = col
        break

if category_col:
    df_menu[category_col] = pd.to_numeric(df_menu[category_col], errors='coerce')
    life_menus = df_menu[df_menu[category_col] == 7].copy()

    print(f'人生・運勢カテゴリー（カテゴリー7）のメニュー数: {len(life_menus)}')
    print('\n既存の人生系メニュー（一部）:')

    # メニュー名の列を探す
    name_col = None
    for col in df_menu.columns:
        if 'メニュー名' in str(col) or 'name' in str(col).lower():
            name_col = col
            break

    if name_col:
        # 有効なメニュー名があるものだけ表示
        valid_life = life_menus[life_menus[name_col].notna() & (life_menus[name_col] != '0')]
        if len(valid_life) > 0:
            for idx, row in valid_life.head(10).iterrows():
                try:
                    print(f"{int(row['メニューID'])} : {row[name_col]}")
                except:
                    pass
        else:
            print('有効な人生系メニューが見つかりませんでした')
else:
    print('カテゴリー列が見つかりませんでした')
