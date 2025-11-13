#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
メニュー重複チェックスクリプト
全SQLファイルからメニュー名を抽出して重複を検出
"""

import re
import glob
from collections import Counter

def extract_menu_names():
    """全SQLファイルからメニュー名を抽出"""
    menu_names = []

    # menu_1*.sqlファイルを検索
    sql_files = sorted(glob.glob('menu_1*.sql'))

    print(f'検出したSQLファイル: {len(sql_files)}個')

    for sql_file in sql_files:
        try:
            with open(sql_file, 'r', encoding='utf-8') as f:
                content = f.read()

                # メニュー名を抽出（mana_contentsテーブルのINSERT文から）
                match = re.search(r"INSERT INTO flowt_seimei\.mana_contents.*?\((\d+),\s*'([^']+)'", content, re.DOTALL)
                if match:
                    contents_id = match.group(1)
                    menu_name = match.group(2)
                    menu_names.append((contents_id, menu_name, sql_file))
        except Exception as e:
            print(f'エラー: {sql_file} - {e}')

    return menu_names

def check_duplicates(menu_names):
    """重複チェック"""
    # メニュー名だけを抽出
    names_only = [name for _, name, _ in menu_names]

    # 重複をカウント
    name_counts = Counter(names_only)

    # 重複があるか確認
    duplicates = {name: count for name, count in name_counts.items() if count > 1}

    if duplicates:
        print('\n[警告] 重複メニューが見つかりました！')
        print('=' * 60)
        for name, count in sorted(duplicates.items(), key=lambda x: x[1], reverse=True):
            print(f'{count}個: {name}')
            # どのファイルに含まれているか表示
            for contents_id, menu_name, sql_file in menu_names:
                if menu_name == name:
                    print(f'  - {sql_file} (ID: {contents_id})')
        print('=' * 60)
        return False
    else:
        print('\n[OK] 重複なし！全メニューがユニークです。')
        print('=' * 60)
        print(f'総メニュー数: {len(menu_names)}')
        print(f'ユニークメニュー数: {len(set(names_only))}')
        print('=' * 60)

        # サンプルを表示
        print('\nサンプル（最初の10個）:')
        for i, (contents_id, menu_name, sql_file) in enumerate(menu_names[:10], 1):
            print(f'{i}. ID{contents_id}: {menu_name}')

        return True

if __name__ == '__main__':
    print('メニュー重複チェックを開始します...\n')

    menu_names = extract_menu_names()

    if menu_names:
        is_unique = check_duplicates(menu_names)

        if is_unique:
            print('\n重複チェック完了: 問題なし')
        else:
            print('\n重複チェック完了: 修正が必要です')
    else:
        print('メニューファイルが見つかりませんでした。')
