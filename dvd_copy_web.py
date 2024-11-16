import tkinter as tk
from tkinter import filedialog
import streamlit as st
import os
import shutil
from datetime import datetime

def dvd_copy():

    # tkinterのファイルダイアログを使用してディレクトリを選択
    root = tk.Tk()
    root.withdraw()  # tkinterのメインウィンドウを非表示にする

    # 最前面にウィンドウを表示
    root.attributes("-topmost", True)


    # D://内のDVDディレクトリを選択
    initial_dir = "D://"
    source_dir = filedialog.askdirectory(
        initialdir=initial_dir,
        title="DVDディレクトリを選択してください"
    )

    # Streamlitでディレクトリ選択の結果を表示
    if source_dir:
        st.write(f"選択されたディレクトリ: {source_dir}")

        # ファイルの作成日時を取得（最初のファイルの作成日時を基準に）
        first_file = next((f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))), None)
        if first_file:
            creation_time = os.path.getctime(os.path.join(source_dir, first_file))
            creation_date = datetime.fromtimestamp(creation_time)
            formatted_date = creation_date.strftime("%y%m%d")
        else:
            st.warning("ディレクトリ内にファイルがありません。")
            exit()

        # ユーザーディレクトリのパスを取得
        home_directory = os.path.expanduser('~')
        folder_path_1 = os.path.join(home_directory, 'Desktop', '退避DVD')

        # コピー先フォルダの作成
        dst_folder_1 = os.path.join(folder_path_1, f"SEJ_BKUP{formatted_date}")
        os.makedirs(dst_folder_1, exist_ok=True)

        g = r"G:\マイドライブ\退避DVD"
        dst_folder_2 = os.path.join(g, f"SEJ_BKUP{formatted_date}")
        os.makedirs(dst_folder_2, exist_ok=True)

        # ディレクトリ内のすべてのファイルをコピー
        for file_name in os.listdir(source_dir):
            source_file = os.path.join(source_dir, file_name)
            if os.path.isfile(source_file):  # ファイルのみコピー
                dst_file_1 = os.path.join(dst_folder_1, file_name)
                dst_file_2 = os.path.join(dst_folder_2, file_name)
                shutil.copyfile(source_file, dst_file_1)
                shutil.copyfile(source_file, dst_file_2)

        # コピー完了メッセージ
        st.success("ディレクトリ内のすべてのファイルがコピーされました。")
    else:
        st.warning("ディレクトリが選択されませんでした。")
