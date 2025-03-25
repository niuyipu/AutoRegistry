import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

def find_file(filename, search_paths):
    """在指定路径下搜索文件，提高搜索效率"""
    for path in search_paths:
        for root, _, files in os.walk(path):
            if filename in files:
                return os.path.join(root, filename).replace("\\", "\\\\")
    return None

def create_reg_file(program_path, project_name):
    """生成注册表文件并输出到 output 目录"""
    reg_content = f'''Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\\{project_name}]
@="URL:{project_name}"
"URL Protocol"="{program_path}"

[HKEY_CLASSES_ROOT\\{project_name}\\DefaultIcon]
@="{program_path}"

[HKEY_CLASSES_ROOT\\{project_name}\\shell]

[HKEY_CLASSES_ROOT\\{project_name}\\shell\\open]

[HKEY_CLASSES_ROOT\\{project_name}\\shell\\open\\command]
@="{program_path}"
'''
    
    os.makedirs("output", exist_ok=True)
    reg_filename = os.path.join("output", f"{project_name}.reg")
    with open(reg_filename, "w", encoding="utf-16") as reg_file:
        reg_file.write(reg_content)
    messagebox.showinfo("成功", f"注册表文件已生成: {reg_filename}")

def threaded_search():
    """使用线程进行搜索，防止 UI 界面卡死"""
    threading.Thread(target=search_file, daemon=True).start()

def search_file():
    filename = entry_filename.get()
    project_name = entry_projectname.get()
    
    if not filename or not project_name:
        messagebox.showwarning("警告", "请输入文件名和项目名！")
        return
    
    messagebox.showinfo("搜索中", "正在搜索文件，请稍候...")
    
    # 仅搜索常见安装目录，减少搜索时间
    common_paths = ["C:\\"]
    
    file_path = find_file(filename, common_paths)
    
    if file_path:
        entry_filepath.delete(0, tk.END)
        entry_filepath.insert(0, file_path)
        create_reg_file(file_path, project_name)
    else:
        messagebox.showerror("错误", "未找到指定文件！")

# 创建GUI界面
root = tk.Tk()
root.title("自动注册表程序")
root.geometry("400x250")

tk.Label(root, text="文件名:").pack(pady=5)
entry_filename = tk.Entry(root, width=40)
entry_filename.pack(pady=5)
entry_filename.insert(0, "inkscape.exe")

tk.Label(root, text="项目名:").pack(pady=5)
entry_projectname = tk.Entry(root, width=40)
entry_projectname.pack(pady=5)
entry_projectname.insert(0, "inkscape")

tk.Button(root, text="搜索文件并生成注册表", command=threaded_search).pack(pady=10)

tk.Label(root, text="文件路径:").pack(pady=5)
entry_filepath = tk.Entry(root, width=40)
entry_filepath.pack(pady=5)

root.mainloop()
