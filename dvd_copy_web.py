import streamlit as st
import os
import shutil
from datetime import datetime

def dvd_copy():
    # ユーザーディレクトリのパスを取得
    home_directory = os.path.expanduser('~')
    folder_path = os.path.join(home_directory, 'Desktop', '棚卸シート', '棚番データ')

    # デフォルトパス
    #default_file_path = "D:/tasho.csv"


    # ファイルアップロードのためのUI
    st.subheader("STEP1 : 棚番データのコピー")
    
    #ファイル選択
    uploaded_file = st.file_uploader("退避DVDからtasho.csvファイルを選択。", type=["csv"])
    
    if uploaded_file is not None:
        # アップロードされたファイルの作成日時を取得（ファイルシステムではなく、選択したファイルから日時を取得）
        creation_time = datetime.now()  # アップロードされたファイルには作成日時がないため、現在日時を使用
        formatted_date = creation_time.strftime("%y%m%d")

        # コピー先フォルダを作成（もし存在しない場合）
        dst_folder = os.path.join(folder_path, f"SEJ_BKUP{formatted_date}")
        os.makedirs(dst_folder, exist_ok=True)

        # 保存先ファイルパス
        dst_path = os.path.join(dst_folder, "tasho.csv")

        # ファイルを一時保存してコピー
        with open(os.path.join(dst_folder, "temp_file.csv"), "wb") as temp_file:
            temp_file.write(uploaded_file.getbuffer())

        # コピー先にファイルを移動
        shutil.move(os.path.join(dst_folder, "temp_file.csv"), dst_path)

        # コピー完了メッセージ
        st.success(f"ファイルがコピーされました: {dst_path}")
    else:
        st.warning("ファイルが選択されていません。")