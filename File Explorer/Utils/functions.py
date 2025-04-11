import os
import datetime
import tkinter as tk
import psutil
import win32api


def load_files(file_path):
    print(f"loading: {file_path}")
    files = os.listdir(file_path)
    return files


def get_file_size(file_path):
    file_stats = os.stat(file_path)

    # file size in bytes
    bytes = file_stats.st_size

    # convert bytes to KB
    kb = int(bytes / 1024)

    if kb == 0:
        return "0 KB"


    # saperate the file size into three digits
    kb = "{:,}".format(kb)


    print(f"File size: {kb} KB")



    return f"{kb} KB"





def open_dir(file_path, dir_history, tabletree, file_img, folder_img):
    # this is how th file path looks like: ['C:\\', 'Windows']
    print(f"Opening dir: {file_path}")

    for file in load_files(file_path):
        file_dir = f"{dir_history.get_current_dir()}/{file}"



        file_stats = os.stat(file_dir)
        print(file_stats)
        creation_time = datetime.datetime.fromtimestamp(file_stats.st_ctime, tz=datetime.timezone.utc)
        creation_time = creation_time.strftime('%Y-%m-%d %H:%M:%S')
        modification_time = datetime.datetime.fromtimestamp(file_stats.st_mtime)
        modification_time = modification_time.strftime('%Y-%m-%d %H:%M:%S')
        last_access_time = datetime.datetime.fromtimestamp(file_stats.st_atime)
        last_access_time = last_access_time.strftime('%Y-%m-%d %H:%M:%S')
        file_size = get_file_size(file_dir)
        # file_size = f"{round(file_stats.st_size / 1024, 2)} KB"

        permission = oct(file_stats.st_mode)

        if os.path.isfile(file_dir):
            file_type = file.split(".")[-1]
            print(file_type)
            tabletree.insert("", index=tk.END, values=(file, file_type, creation_time, modification_time, file_size), image=file_img)
        if os.path.isdir(file_dir):
            tabletree.insert("", index=tk.END, values=(file, "Folder",creation_time, modification_time, ""), image=folder_img)



# get the disk usage of the hard drive
def disk_usage(drive_letter):
    hdd = psutil.disk_usage(drive_letter)

    total = round(hdd.total / 1024 / 1024 / 1024, 2)
    used = round(hdd.used / 1024 / 1024 / 1024, 2)
    free = round(hdd.free / 1024 / 1024 / 1024, 2)

    print(f"DISK Total: {total} GB")
    print(f"Disk Used: {used} GB")
    print(f"Disk Free: {free} GB")

    return total, used, free



def open_file(selected_items):
    print("opening file")
    file_stats = os.stat(selected_items[0])
    print(file_stats)
    creation_time = datetime.datetime.fromtimestamp(file_stats.st_ctime)
    modification_time = datetime.datetime.fromtimestamp(file_stats.st_mtime)
    last_access_time = datetime.datetime.fromtimestamp(file_stats.st_atime)
    permission = oct(file_stats.st_mode)


    print(f"Creation Time: {creation_time}")
    print(f"Modification Time: {modification_time}")
    print(f"Last Access Time: {last_access_time}")
    print(f"Permission: {permission}")
    print("opening the selected item")
    for i in selected_items:
        if not i.endswith(".png"):
            continue
        os.startfile(i)
        print(i)
    print("open complete")
    selected_items.clear()



def get_drives_info():
    # List all logical drives
    partitions = psutil.disk_partitions()
    print(f"Partitions: {partitions}")
    drives = []

    # Filter out partitions that have no media (skip 'no media' drives)
    for partition in partitions:
        # Check if the partition is mounted and has a valid device
        if partition.fstype and partition.device != '::':
            try:
                drives_info = win32api.GetVolumeInformation(partition.mountpoint)
                drives.append([partition.mountpoint, drives_info[0]])
            except Exception as e:
                print(f"Error getting volume information for {partition.mountpoint}: {e}")
    print(drives)
    return drives