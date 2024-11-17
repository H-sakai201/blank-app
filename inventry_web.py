import streamlit as st
import glob
import pandas as pd
import os
import shutil
import datetime
import re
import dvd_copy_web
import streamlit as st
import time  # 処理をシミュレーションするためのモジュール（実際の処理に置き換え）

# アプリのタイトルと説明
st.title("棚卸シート作成アプリ")

#tashoファイルをコピー
dvd_copy_web.dvd_copy()

# ユーザーディレクトリのパスを取得
home_directory = os.path.expanduser('~')
folder_path_1 = os.path.join(home_directory, 'Desktop', '棚卸シート', '棚番データ')
folder_path_2 = os.path.join(home_directory, 'Desktop', '棚卸シート')

# 退避DVDフォルダ内のすべてのSEJ_BKUP*フォルダをリストアップ
folders = glob.glob(os.path.join(folder_path_1, 'SEJ_BKUP*'))

# フォルダ名から6桁の数字を抽出してソート
def extract_number(folder_name):
    match = re.search(r'SEJ_BKUP(\d{6})$', os.path.basename(folder_name))
    return int(match.group(1)) if match else 0

folders.sort(key=extract_number, reverse=True)

# 最大値と2番目の値のフォルダを取得
read_path_1 = folders[0] + '\\' if len(folders) > 0 else None
read_path_2 = folders[1] + '\\' if len(folders) > 1 else None

#在庫データの読み込み
df_zaiko = pd.read_csv(
    'D:/VSCENZAI.CSV',
    encoding='shift_jis',
    usecols=[0, 6, 9, 10, 11, 13, 15],
    header=None,
    names=['処理日', '商品CD', 'S', 'M', '賞味期限', '出荷後在庫', '出荷前在庫']
)

# データ型変換
df_zaiko['処理日'] = pd.to_datetime(df_zaiko['処理日'], format='%Y%m%d', errors='coerce')
df_zaiko[['商品CD', 'S', 'M', '出荷後在庫', '出荷前在庫']] = df_zaiko[['商品CD', 'S', 'M', '出荷後在庫', '出荷前在庫']].apply(pd.to_numeric, errors='coerce')

#データ処理日の取得（フォルダ名、フォルダ内のファイルソート用）
date = pd.to_datetime(df_zaiko['処理日'].min(), format='%Y%m%d').strftime('%Y年%m月%d日')

df_zaiko = df_zaiko.groupby(['商品CD']).agg(
    {'出荷後在庫': 'sum', '出荷前在庫': 'sum', 'S': 'first', 'M': 'first'}
).reset_index()

#棚番データの読み込み
df_tana = pd.read_csv(f'{read_path_2}tasho.csv', encoding='shift_jis', usecols=[
        2, 3, 4, 5, 7, 10], header=None, names=['棚1', '棚2', '棚3', '棚4', '商品CD', '商品名'], index_col=None)

df_tana['棚1'] = df_tana['棚1'].astype(str)
df_tana['棚2'] = df_tana['棚2'].astype(str).str.zfill(2)
df_tana['棚3'] = df_tana['棚3'].astype(str)
df_tana['棚4'] = df_tana['棚4'].astype(str)

df_tana['棚番'] = df_tana['棚1']+df_tana['棚2']+df_tana['棚3'] + df_tana['棚4']
df_tana['棚番'] = df_tana['棚番'].astype('int64')
df_tana = df_tana[['棚番', '商品CD', '商品名']]
df_tana = df_tana.sort_values(by='棚番', ascending=True)

#在庫データと棚番データの結合
df = df_tana.merge(df_zaiko, how='left', on='商品CD')
df['入数'] = df['M'] // df['S']
df['出荷後在庫_BL'] = df['出荷後在庫'] // df['S']
df['出荷後在庫_ケース'] = df['出荷後在庫_BL'] // df['入数']
df['出荷後在庫_余り'] = df['出荷後在庫_BL'] % df['入数']
df['出荷前在庫_BL'] = df['出荷前在庫'] // df['S']
df['出荷前在庫_ケース'] = df['出荷前在庫_BL'] // df['入数']
df['出荷前在庫_余り'] = df['出荷前在庫_BL'] % df['入数']

# Excelファイルの保存
path_old = os.path.join(folder_path_2, '棚卸シート.xlsx')
path_new = os.path.join(folder_path_2, f"棚卸シート{date}.xlsx")

st.subheader("STEP2 : 棚卸シートを作成 ")
if st.button("棚卸シート作成"):
    shutil.copy(path_old, path_new)
    with pd.ExcelWriter(path_new, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='棚卸データ', index=True, header=1)
        df_zaiko.to_excel(writer, sheet_name='在庫データ', index=True, header=1)
        df_tana.to_excel(writer, sheet_name='棚データ', index=True, header=1)
    st.success(f"ファイルが作成されました: {path_new}")
    st.write("以下のリンクからダウンロードできます。")
    st.download_button(label="ファイルをダウンロード", data=open(path_new, "rb").read(), file_name=f"棚卸シート_{date}.xlsx")
