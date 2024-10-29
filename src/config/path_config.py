
import os 

# 全局变量
CONFIG_FILE = "config.txt"

def save_paths(package_lock_path, retire_report_path, output_file_path):
    with open(CONFIG_FILE, "w") as f:
        f.write(f"{package_lock_path}\n{retire_report_path}\n{output_file_path}")

def load_paths():
    try:
        with open(CONFIG_FILE, "r") as f:
            package_lock_path,retire_report_path,output_file_path = f.read().splitlines()
            return package_lock_path,retire_report_path,output_file_path
    except FileNotFoundError:
        return "", "", ""