from openpyxl.utils import get_column_letter
from openpyxl import Workbook
import glob
import pandas as pd
import os.path
# from styleframe import StyleFrame
import datetime
import openpyxl as xl
from openpyxl import load_workbook
import re
import numpy as np  # numpyモジュールをインポート
import my_function as my_func
import sys
import pickle
import os
import shutil
import tkinter as tk
import tkinter.messagebox as messagebox
import DVD_copy

# DVD_copy.py を実行（退避DVDをコピーする）
DVD_copy.dvd_copy()

# データのファイルパスを指定
# ユーザーのホームディレクトリを取得

#退避DVDの読み込み（在庫データのパス）
path_dvd = ('D:\\')

#ホームディレクトリの取得
home_directory = os.path.expanduser('~')

# 名簿データのパス
# デスクトップに'退避DVD'というフォルダを作成しておく。
folder_path_1 = os.path.join(home_directory, 'Desktop','退避DVD')

# 退避dvdフォルダ内のすべてのSEJ_BKUP*フォルダをリストアップ
folders = glob.glob(os.path.join(folder_path_1, 'SEJ_BKUP*'))

# フォルダを作成日時でソート
folders.sort(key=os.path.getctime)

#2番目に最新のフォルダのパスを取得（棚番データのパス）
#read_path_1 = folders[-1]+'\\'
read_path_2 = folders[-2]+'\\'


#補充シートのパス
folder_path_2 = os.path.join(home_directory, 'Desktop',
                                '棚卸シート')

# vscenzai.csv（在庫データの読み込み）
df_zaiko = my_func.read_zaiko_3(path_dvd)

date = df_zaiko['処理日'].min()
date = pd.to_datetime(date, format='%Y%m%d').strftime('%Y年%m月%d日')

df_zaiko = df_zaiko.groupby(['商品CD']).agg(
    {'出荷後在庫': 'sum',
    '出荷前在庫': 'sum',
    'S': 'first',
    'M': 'first',
    }
).reset_index()

# tasho.csv（棚データの読み込み）
df_tana = my_func.read_tana(read_path_2)

#pkdataとtashoを結合して商品CDを取得する
df = df_tana.merge(df_zaiko,how='left',on='商品CD')

df['入数'] = df['M']//df['S']
df['出荷後在庫_BL'] = df['出荷後在庫']//df['S']
df['出荷後在庫_ケース'] = df['出荷後在庫_BL']//df['入数']
df['出荷後在庫_余り'] = df['出荷後在庫_BL']%df['入数']

df['出荷前在庫_BL'] = df['出荷前在庫']//df['S']
df['出荷前在庫_ケース'] = df['出荷前在庫_BL']//df['入数']
df['出荷前在庫_余り'] = df['出荷前在庫_BL']%df['入数']

"""
# NaN を0で置き換える例
df['ケース_余り'] = (df['出荷後在庫_余り'].fillna(0).astype(int).astype(str) + "\n" + "[" + df['出荷後在庫_ケース'].fillna(0).astype(int).astype(str) + "]"                   )
"""

# 上書きする元ファイル名
# ファイルパスの結合
path_old = os.path.join(folder_path_2,'棚卸シート.xlsx')

# 作成するファイル名
path_new = os.path.join(folder_path_2, "棚卸シート"+str(date)+".xlsx")
#path_new = os.path.join(folder_path_2, "棚卸シート_1.xlsx")

shutil.copy(path_old, path_new)

# path_new_1 = r"C:\Users\sakai\Desktop\在庫データ.xlsx"
with pd.ExcelWriter(path_new, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    df.to_excel(
        writer, sheet_name='棚卸データ', index=True, header=1)
    df_zaiko.to_excel(
        writer, sheet_name='在庫データ', index=True, header=1)
    df_tana.to_excel(
        writer, sheet_name='棚データ', index=True, header=1)

# 作成したファイルを開く
os.startfile(path_new)

