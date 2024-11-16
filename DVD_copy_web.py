import os
import datetime
import shutil
import psutil
import win32file

"""
#win32file で示されるディスクの種類
0: ドライブの種類を判別できない
1: ドライブが存在しない
2: リムーバブルディスク（フロッピーディスクやUSBメモリなど）
3: 固定ディスク（ハードディスクやSSDなど）
4: リモートディスク（ネットワークドライブなど）
5: CD-ROMドライブ（DVDやBDなど）
6: RAMディスク（メモリを仮想的にディスクとして使うもの）
"""

# 書き込みドライブの指定


def dvd_copy():
    def my_makedirs(path):
        if not os.path.isdir(path):
            os.makedirs(path)

    # ドライブの情報を取得
    drives = psutil.disk_partitions()

    # ドライブのマウントポイントを格納するリストを定義
    disc_list = []

    # ドライブの情報の中から、マウントポイントを取り出す
    for drive in drives:
        # マウントポイントをリストに追加
        disc_list.append(drive)

    # DVDドライブのマウントポイントとその他の変数を外に定義
    read_path = None
    date_str = None

    # DVDドライブのマウントポイントを取得
    for disc in disc_list:
        disc_mount = disc.mountpoint
        drive_type = win32file.GetDriveType(disc_mount)
        # DVDドライブの場合
        if drive_type == 5:
            read_path = disc_mount
            # 経過秒数をdatetimeオブジェクトに変換する
            x = os.path.getctime(read_path)
            dt = datetime.datetime.fromtimestamp(x)
            date_str = dt.strftime("%y%m%d")
            break  # DVDドライブが見つかったらループを終了

    if read_path is None:
        print("DVDドライブが見つかりませんでした。")
        exit()

    # 読み込み（dvd）、書き込みの(usb)のディレクトリを取得
    for disc in disc_list:
        disc_mount = disc.mountpoint
        disc_opts = disc.opts
        drive_type = win32file.GetDriveType(disc_mount)
        # USBドライブの場合
        if drive_type == 2:
            # 書き込みドライブ
            write_path = disc_mount
            # usbドライブのパスを設定
            e = f'{write_path}退避DVD\\SEJ_BKUP{date_str}' + "\\"
            my_makedirs(e)  # usb drive

            for root, dirs, files in os.walk(read_path):
                for file in files:  # ファイルごとに処理する
                    src_path = os.path.join(root, file)  # コピー元のパスを作る
                    dst_path = src_path.replace(read_path, e)  # コピー先のパスを作る
                    os.makedirs(os.path.dirname(dst_path),
                                exist_ok=True)  # コピー先のフォルダがなければ作る
                    shutil.copyfile(src_path, dst_path)  # ファイルをコピーする

            break  # USBドライブが見つかったらループを終了

    # ②googleドライブ
    g_drive_available = False
    g = r"G:\マイドライブ\退避DVD\SEJ_BKUP" + date_str + "\\"
    # Googleドライブがマウントされているか確認
    for disc in disc_list:
        disc_mount = disc.mountpoint
        if disc_mount == "G:\\":
            g_drive_available = True
            break

    if g_drive_available:
        my_makedirs(g)  # google drive

        # GoogleDriveにDVDドライブ内のすべてのファイルを書き込み先にコピーする
        # DVDドライブ内のすべてのフォルダとファイルを走査する
        for root, dirs, files in os.walk(read_path):
            for file in files:  # ファイルごとに処理する
                src_path = os.path.join(root, file)  # コピー元のパスを作る
                dst_path = src_path.replace(read_path, g)  # コピー先のパスを作る
                os.makedirs(os.path.dirname(dst_path),
                            exist_ok=True)  # コピー先のフォルダがなければ作る
                shutil.copyfile(src_path, dst_path)  # ファイルをコピーする
    else:
        print("Googleドライブがマウントされていません。")

    # ③デスクトップのパスを取得
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')

    # デスクトップ上の退避DVDフォルダのパスを設定
    desktop_backup_path = os.path.join(
        desktop_path, "退避DVD", f"SEJ_BKUP{date_str}")

    # デスクトップ上の退避DVDフォルダがなければ作成
    my_makedirs(desktop_backup_path)

    # DVDドライブ内のすべてのフォルダとファイルを走査し、デスクトップにコピー
    for root, dirs, files in os.walk(read_path):
        for file in files:  # ファイルごとに処理
            src_path = os.path.join(root, file)  # コピー元のパス
            # コピー先のディレクトリ構造を作成
            subdir = os.path.relpath(root, read_path)
            dst_dir = os.path.join(desktop_backup_path, subdir)
            os.makedirs(dst_dir, exist_ok=True)  # コピー先のフォルダがなければ作る
            dst_path = os.path.join(dst_dir, file)  # コピー先のパス
            shutil.copyfile(src_path, dst_path)  # ファイルをコピー
