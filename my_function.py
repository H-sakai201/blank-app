import pandas as pd
# VSCENZAIファイルの読み込み（出庫確定前、後の鮮度別在庫)


def read_zaiko(path):
    df_zaiko = pd.read_csv(f'{path}VSCENZAI.CSV', encoding='shift_jis', usecols=[
        6, 9, 10, 11, 13], header=None, names=['商品CD', 'S', 'M', '賞味期限', '出荷後在庫'], index_col=None)
    return df_zaiko


def read_zaiko_2(path):
    df_zaiko = pd.read_csv(f'{path}VSCENZAI.CSV', encoding='shift_jis', usecols=[
        6, 9, 10, 11, 13, 15], header=None, names=['商品CD', 'S', 'M', '賞味期限', '出荷後在庫', '出荷前在庫'], index_col=None)
    return df_zaiko

def read_zaiko_3(path):
    df_zaiko = pd.read_csv(f'{path}VSCENZAI.CSV', encoding='shift_jis', usecols=[
        0,6, 9, 10, 11, 13, 15], header=None, names=['処理日','商品CD', 'S', 'M', '賞味期限', '出荷後在庫', '出荷前在庫'], index_col=None)
    return df_zaiko


# shoaファイルの読み込み（鮮度情報あり)
def read_shohin_1(path):
    df_shohin = pd.read_csv(f'{path}shoa.CSV', encoding='shift_jis', usecols=[
        0, 1, 2, 9, 23, 24], header=None, names=['ベンダーCD', '商品CD',  '適用日', '商品名', '鮮度区分', '鮮度期間'], index_col=None)
    return df_shohin


# shoaファイルの読み込み（鮮度情報なし)
def read_shohin_2(path):
    # shoa.csv(商品情報)の読み込み
    df_shohin = pd.read_csv(f'{path}shoa.csv', encoding='shift_jis', usecols=[
                            1, 2, 7, 9, 13], header=None, names=['商品CD', '適用日', 'Mロット', '商品名', 'Sロット'], index_col=None)

    # ファイルの作成日を取得
    # os.path.getmtime関数でファイルの最終更新日時を取得し、datetimeモジュールで日付に変換
    import os
    import datetime
    file_date = datetime.date.fromtimestamp(os.path.getmtime(path))
    file_date_str = file_date.strftime('%Y%m%d')

    # 文字列型をint(64)型に変換する
    file_date_int = int(file_date_str)

    # ファイル作成日に採用される適用日の抽出
    # 「適用日」が今日以下の行をフィルタリング
    df_shohin = df_shohin[df_shohin['適用日'] <= file_date_int]

    # 商品CDごとに適用日が最大値の行を取得
    max_date_rows = df_shohin.loc[df_shohin.groupby('商品CD')['適用日'].idxmax()]

    # 最終的な結果をmax_date_rowsに格納
    df_shohin = max_date_rows

    return df_shohin

# shoaファイルの読み込み（鮮度情報あり)


def read_shohin_3(path):
    df_shohin = pd.read_csv(f'{path}shoa.CSV', encoding='shift_jis', usecols=[
        0, 1, 2, 9, 23, 24, 45], header=None, names=['ベンダーCD', '商品CD',  '適用日', '商品名', '鮮度区分', '鮮度期間', 'JAN'], index_col=None)
    return df_shohin


# tashoファイルの読み込み（棚番5または6桁変換)
def read_tana(path):
    # tasho.csv（棚番）の読み込み
    df_tana = pd.read_csv(f'{path}tasho.csv', encoding='shift_jis', usecols=[
        2, 3, 4, 5, 7, 10], header=None, names=['棚1', '棚2', '棚3', '棚4', '商品CD', '商品名'], index_col=None)

    df_tana['棚1'] = df_tana['棚1'].astype(str)
    df_tana['棚2'] = df_tana['棚2'].astype(str).str.zfill(2)
    df_tana['棚3'] = df_tana['棚3'].astype(str)
    df_tana['棚4'] = df_tana['棚4'].astype(str)

    df_tana['棚番'] = df_tana['棚1']+df_tana['棚2']+df_tana['棚3'] + df_tana['棚4']
    df_tana['棚番'] = df_tana['棚番'].astype('int64')
    df_tana = df_tana[['棚番', '商品CD', '商品名']]
    df_tana = df_tana.sort_values(by='棚番', ascending=True)
    return df_tana


def read_misek(path):
    df_misek = pd.read_csv(f'{path}MISEK.CSV', encoding='shift_jis', usecols=[
        1, 3], header=None, names=['店舗CD', '店舗名'], index_col=None)

    return df_misek


"""
def read_pk(path):
    df_pk = pd.read_csv(f'{path}pkdata.CSV', encoding='shift_jis', usecols=[
        0, 6, 7, 8, 9], header=None, names=['伝票日付', 'コース', '路順', '店番', '棚番'], index_col=None)

    return df_pk
"""

# PKDATAファイルの読み込み（出荷データ)


"""
def read_pk(path):
    df_pk = pd.read_csv(f'{path}PKDATA.CSV', encoding='shift_jis', usecols=[
        0, 6, 9, 10, 11], header=None, names=['伝票日付', 'コース',  '棚番', 'Sロット', '受注バラ'], index_col=None)
    return df_pk

"""


def read_pk(path):
    df_pk = pd.read_csv(f'{path}pkdata.csv', encoding='shift_jis', usecols=[
        0, 6, 7, 8, 9, 10, 11], header=None, names=['伝票日付', 'コース', '路順', '店舗CD', '棚番', 'Sロット', '受注バラ'], index_col=None)
    return df_pk
