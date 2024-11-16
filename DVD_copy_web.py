import os
import datetime
import shutil
import psutil

# 書き込みドライブの指定
def dvd_copy():
    def my_makedirs(path):
        if not os.path.isdir(path):
            os.makedirs(path)
    

    # ドライブの情報を取得
    drives = psutil.disk_partitions()

    # ドライブのマウントポイントを格納するリストを定義
    disc_list = [drive.mountpoint for drive in drives]

    # DVDドライブのマウントポイントと日付文字列
    read_path = None
    date_str = None

    # DVDドライブを検出するためにタイプやラベルを調べる
    for disc_mount in disc_list:
        # ドライブタイプが"cdrom"または"media"に関連する場合、DVDドライブと仮定
        if "cdrom" in disc_mount.lower() or "media" in disc_mount.lower():
            if os.path.exists(disc_mount):  # 存在確認
                read_path = disc_mount
                # ドライブの作成日時を取得
                x = os.path.getctime(read_path)
                dt = datetime.datetime.fromtimestamp(x)
                date_str = dt.strftime("%y%m%d")
                break

        if read_path is None:
            print("DVDドライブが見つかりませんでした。")
        return

    """"
    # ドライブの情報を取得
    drives = psutil.disk_partitions()

    # ドライブのマウントポイントを格納するリストを定義
    disc_list = [drive.mountpoint for drive in drives]
    # ドライブのマウントポイントを格納するリストを定義

    # ドライブのパスを表示して確認
    for disc_mount in disc_list:
        print(disc_mount)


    # DVDドライブのマウントポイントと日付文字列
    read_path = None
    date_str = None

    # DVDドライブのマウントポイントを推測
    for drive in drives:
        if 'cdrom' in drive.device.lower() or 'dvd' in drive.device.lower():
            if os.path.exists(drive.mountpoint):
                read_path = drive.mountpoint
                # ドライブの作成日時を取得
                x = os.path.getctime(read_path)
                dt = datetime.datetime.fromtimestamp(x)
                date_str = dt.strftime("%y%m%d")
                break


    # DVDドライブのマウントポイントを推測
    for disc_mount in disc_list:
        if "cdrom" in disc_mount.lower() or "media" in disc_mount.lower():
            if os.path.exists(disc_mount):  # 存在確認
                read_path = disc_mount
                # ドライブの作成日時を取得
                x = os.path.getctime(read_path)
                dt = datetime.datetime.fromtimestamp(x)
                date_str = dt.strftime("%y%m%d")
                break
    """
                
    if read_path is None:
        print("DVDドライブが見つかりませんでした。")
        return

    # 読み込み（DVD）と書き込み先（USB）を取得
    for disc_mount in disc_list:
        disc_opts = next(
            (drive.opts for drive in drives if drive.mountpoint == disc_mount),
            None
        )
        if "rw" in disc_opts:  # USBの可能性があるドライブ
            write_path = disc_mount
            # USBドライブのパスを設定
            e = f'{write_path}退避DVD\\SEJ_BKUP{date_str}' + "\\"
            my_makedirs(e)

            # DVDからUSBへコピー
            for root, dirs, files in os.walk(read_path):
                for file in files:
                    src_path = os.path.join(root, file)
                    dst_path = src_path.replace(read_path, e)
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    shutil.copyfile(src_path, dst_path)

            break

    # Googleドライブのパスを設定
    g_drive_available = False
    g = r"G:\マイドライブ\退避DVD\SEJ_BKUP" + date_str + "\\"
    if "G:\\" in disc_list:  # Googleドライブがマウントされている場合
        g_drive_available = True

    if g_drive_available:
        my_makedirs(g)
        for root, dirs, files in os.walk(read_path):
            for file in files:
                src_path = os.path.join(root, file)
                dst_path = src_path.replace(read_path, g)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copyfile(src_path, dst_path)
    else:
        print("Googleドライブがマウントされていません。")

    # デスクトップのパスを取得
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    desktop_backup_path = os.path.join(desktop_path, "退避DVD", f"SEJ_BKUP{date_str}")
    my_makedirs(desktop_backup_path)

    # DVDからデスクトップへコピー
    for root, dirs, files in os.walk(read_path):
        for file in files:
            src_path = os.path.join(root, file)
            subdir = os.path.relpath(root, read_path)
            dst_dir = os.path.join(desktop_backup_path, subdir)
            os.makedirs(dst_dir, exist_ok=True)
            dst_path = os.path.join(dst_dir, file)
            shutil.copyfile(src_path, dst_path)
