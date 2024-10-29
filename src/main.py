import os
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox 
import logging
logging.basicConfig(level=logging.ERROR)

from config.path_config import save_paths,load_paths
from sbom_builder import process_build
    
def validate_package_lock(package_lock_path):
    if not os.path.isfile(package_lock_path):
        messagebox.showerror("错误", "指定的 package-lock.json 文件路径无效，请重新选择！")
        return False

    # 判断文件是否为有效的 JSON 文件
    try:
        with open(package_lock_path, "r") as f:
            json.load(f)
    except json.JSONDecodeError:
        messagebox.showerror("错误", "指定的 package-lock.json 文件不是有效的 JSON 文件，请重新选择！")
        return False

    # 判断文件是否存在 packages 字段
    with open(package_lock_path, "r") as f:
        data = json.load(f)
        if "packages" not in data:
            messagebox.showerror("错误", "指定的 package-lock.json 文件缺少 packages 字段，请重新选择！")
            return False

    return True

def save_and_open_file():
    package_lock_path = package_lock_entry.get()
    retire_report_path = retire_report_file_entry.get()
    output_file = output_file_entry.get()

    if not package_lock_path or not output_file:
        messagebox.showerror("错误", "请输入 package-lock.json 文件路径和要保存的 Excel 文件路径及名称！")
        return
    
    if not validate_package_lock(package_lock_path):
        return

    excel_file = process_build(package_lock_path, retire_report_path, output_file)

    if not excel_file:
        messagebox.showerror("错误", "生成失败，请查看错误日志！")
        return

    # 缓存用户选择的路径
    save_paths(package_lock_path, retire_report_path, output_file)

    # 提示用户是否打开文件
    open_file = messagebox.askyesno("提示", "生成成功，是否要打开文件？")
    if open_file:
        os.system(f"start excel {excel_file}")

def browse_package_lock():
    filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    package_lock_entry.delete(0, tk.END)
    package_lock_entry.insert(0, filename)

def browse_retire_report():
    filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    retire_report_file_entry.delete(0, tk.END)
    retire_report_file_entry.insert(0, filename)

def browse_output_file():
    filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, filename)
    
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        

try:
    # 主要逻辑
    # 创建主窗口S
    root = tk.Tk()
    root.title("软件物料清单生成工具_V2 @JADE")

    package_lock_label = tk.Label(root, text="package-lock.json 文件路径：")
    package_lock_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    package_lock_entry = tk.Entry(root, width=50)
    package_lock_entry.grid(row=0, column=1, padx=5, pady=5)
    package_lock_browse_button = tk.Button(root, text="浏览", command=browse_package_lock)
    package_lock_browse_button.grid(row=0, column=2, padx=5, pady=5)

    retire_report_file_label = tk.Label(root, text="Retire Report 文件路径及名称：")
    retire_report_file_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    retire_report_file_entry = tk.Entry(root, width=50)
    retire_report_file_entry.grid(row=1, column=1, padx=5, pady=5)
    retire_report_file_browse_button = tk.Button(root, text="浏览", command=browse_retire_report)
    retire_report_file_browse_button.grid(row=1, column=2, padx=5, pady=5) 

    output_file_label = tk.Label(root, text="Excel 文件路径及名称：")
    output_file_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    output_file_entry = tk.Entry(root, width=50)
    output_file_entry.grid(row=2, column=1, padx=5, pady=5)
    output_file_browse_button = tk.Button(root, text="浏览", command=browse_output_file)
    output_file_browse_button.grid(row=2, column=2, padx=5, pady=5) 


    save_button = tk.Button(root, text="生成并打开文件", command=save_and_open_file)
    save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # 绑定回车键到按钮的点击事件
    root.bind('<Return>', lambda event=None: save_and_open_file())

    # 加载初始路径
    package_lock_path, retire_report_path, output_file_path = load_paths()
    package_lock_entry.insert(0, package_lock_path)
    retire_report_file_entry.insert(0, retire_report_path)
    output_file_entry.insert(0, output_file_path)

    root.update_idletasks()
    center_window(root)
    root.mainloop()
except Exception as e:
    logging.error(f"发生未处理异常: {e}")
    messagebox.showerror("错误", "发生未处理异常，请查看日志！")