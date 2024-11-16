import streamlit as st
import glob
import pandas as pd
import os
import shutil
import datetime
import re
import my_function as my_func
import dvd_copy_web

# アプリのタイトルと説明
st.title("在庫と棚卸データ管理アプリ")
st.write("在庫データを管理し、棚卸データExcelシートを生成するWebアプリケーションです。")

# DVDコピー操作
if st.button("DVDコピーを実行"):
    dvd_copy_web.dvd_copy()
    st.success("DVDコピーが完了しました。")

# DVDとフォルダパスの設定
#path_dvd = "D:\\"

# ユーザーディレクトリのパスを取得
home_directory = os.path.expanduser('~')
folder_path_1 = os.path.join(home_directory, 'Desktop', '退避DVD')
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

# 在庫データの読み込みと処理
df_zaiko = my_func.read_zaiko_3(read_path_1)
#df_zaiko = my_func.read_zaiko_3(path_dvd)

date = pd.to_datetime(df_zaiko['処理日'].min(), format='%Y%m%d').strftime('%Y年%m月%d日')
df_zaiko = df_zaiko.groupby(['商品CD']).agg(
    {'出荷後在庫': 'sum', '出荷前在庫': 'sum', 'S': 'first', 'M': 'first'}
).reset_index()

# 棚データの読み込みと処理
df_tana = my_func.read_tana(read_path_2)
df = df_tana.merge(df_zaiko, how='left', on='商品CD')
df['入数'] = df['M'] // df['S']
df['出荷後在庫_BL'] = df['出荷後在庫'] // df['S']
df['出荷後在庫_ケース'] = df['出荷後在庫_BL'] // df['入数']
df['出荷後在庫_余り'] = df['出荷後在庫_BL'] % df['入数']
df['出荷前在庫_BL'] = df['出荷前在庫'] // df['S']
df['出荷前在庫_ケース'] = df['出荷前在庫_BL'] // df['入数']
df['出荷前在庫_余り'] = df['出荷前在庫_BL'] % df['入数']

# 処理したデータの表示
st.subheader("処理済みデータ")
st.write(df)

# Excelファイルの保存
path_old = os.path.join(folder_path_2, '棚卸シート.xlsx')
path_new = os.path.join(folder_path_2, f"棚卸シート{date}.xlsx")

if st.button("Excelファイルを生成"):
    shutil.copy(path_old, path_new)
    with pd.ExcelWriter(path_new, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='棚卸データ', index=True, header=1)
        df_zaiko.to_excel(writer, sheet_name='在庫データ', index=True, header=1)
        df_tana.to_excel(writer, sheet_name='棚データ', index=True, header=1)
    st.success(f"Excelファイルが作成されました: {path_new}")
    st.write("以下のリンクからダウンロードできます。")
    st.download_button(label="Excelファイルをダウンロード", data=open(path_new, "rb").read(), file_name=f"棚卸シート_{date}.xlsx")

