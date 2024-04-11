

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from src.sbom_builder import process_build 

def save_and_open_file():
    package_lock_path = package_lock_entry.get()
    output_file = output_file_entry.get()

    if not package_lock_path or not output_file:
        messagebox.showerror("错误", "请输入 package-lock.json 文件路径和要保存的 Excel 文件路径及名称！")
        return

    excel_file= process_build(package_lock_path, output_file) 
    
    if not excel_file:
        messagebox.showerror("错误", "执行出错了，请查看输出信息")
        return

    # 提示用户是否打开文件
    open_file = messagebox.askyesno("提示", "APP_软件物料清单生成成功，是否要打开输出文件？")
    if open_file:
        os.system(f"start excel {excel_file}")

def browse_package_lock():
    filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    package_lock_entry.delete(0, tk.END)
    package_lock_entry.insert(0, filename)

def browse_output_file():
    filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, filename)

def set_initial_paths():
    current_dir = os.getcwd()
    package_lock_initial_path = os.path.join(current_dir,"files", "package-lock.json")
    output_file_initial_path = os.path.join(current_dir, "_output", "MDIS-APP_软件物料清单.xlsx")
    package_lock_entry.insert(0, package_lock_initial_path)
    output_file_entry.insert(0, output_file_initial_path)

# 创建主窗口
root = tk.Tk()
root.title("软件物料清单生成工具")

# 创建输入框和按钮
package_lock_label = tk.Label(root, text="package-lock.json 文件路径：")
package_lock_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
package_lock_entry = tk.Entry(root, width=50)
package_lock_entry.grid(row=0, column=1, padx=5, pady=5)
package_lock_browse_button = tk.Button(root, text="浏览", command=browse_package_lock)
package_lock_browse_button.grid(row=0, column=2, padx=5, pady=5)

output_file_label = tk.Label(root, text="Excel 文件路径及名称：")
output_file_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1, padx=5, pady=5)
output_file_browse_button = tk.Button(root, text="浏览", command=browse_output_file)
output_file_browse_button.grid(row=1, column=2, padx=5, pady=5)

save_button = tk.Button(root, text="生成并打开文件", command=save_and_open_file)
save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# 设置初始路径
set_initial_paths()

root.mainloop()
