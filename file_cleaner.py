#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件清理工具
根据主图目录和副图目录，删除找不到对应主图的副图文件
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading


class FileCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件清理工具")
        self.root.geometry("600x400")
        
        # 变量
        self.main_dir = tk.StringVar()
        self.sub_dir = tk.StringVar()
        self.log_text = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 主图目录选择
        ttk.Label(main_frame, text="主图目录:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.main_dir, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="选择", command=self.select_main_dir).grid(row=0, column=2, padx=5)
        
        # 副图目录选择
        ttk.Label(main_frame, text="副图目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.sub_dir, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="选择", command=self.select_sub_dir).grid(row=1, column=2, padx=5)
        
        # 执行按钮
        self.execute_btn = ttk.Button(main_frame, text="开始清理", command=self.start_cleanup)
        self.execute_btn.grid(row=2, column=0, columnspan=3, pady=20)
        
        # 日志区域
        ttk.Label(main_frame, text="操作日志:").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        # 创建滚动文本框
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.log_text = tk.Text(log_frame, height=15, yscrollcommand=scrollbar.set)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.log_text.yview)
    
    def select_main_dir(self):
        directory = filedialog.askdirectory(title="选择主图目录")
        if directory:
            self.main_dir.set(directory)
            self.log(f"已选择主图目录: {directory}")
    
    def select_sub_dir(self):
        directory = filedialog.askdirectory(title="选择副图目录")
        if directory:
            self.sub_dir.set(directory)
            self.log(f"已选择副图目录: {directory}")
    
    def log(self, message):
        """添加日志消息"""
        if self.log_text:
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
            self.root.update_idletasks()
    
    def get_main_image_name(self, sub_image_path):
        """
        根据副图文件名生成主图文件名
        规则: 副图文件名.substring(0,originalName.indexOf("_副图"))+suffix
        """
        file_path = Path(sub_image_path)
        original_name = file_path.stem  # 不含扩展名的文件名
        suffix = file_path.suffix  # 扩展名
        
        # 查找"_副图"的位置
        if "_副图" in original_name:
            main_name = original_name[:original_name.index("_副图")] + suffix
            return main_name
        else:
            # 如果没有"_副图"，返回原文件名
            return file_path.name
    
    def find_main_image(self, main_dir, main_image_name):
        """
        在主图目录中查找主图文件（包括子目录）
        返回找到的文件路径，如果找不到返回None
        """
        main_path = Path(main_dir)
        if not main_path.exists():
            return None
        
        # 递归查找文件
        for file_path in main_path.rglob(main_image_name):
            if file_path.is_file():
                return file_path
        
        return None
    
    def cleanup_empty_dirs(self, directory):
        """
        删除空目录（递归）
        """
        deleted_dirs = []
        dir_path = Path(directory)
        
        # 从最深层开始遍历
        for dir_item in sorted(dir_path.rglob("*"), reverse=True):
            if dir_item.is_dir():
                try:
                    # 检查目录是否为空
                    if not any(dir_item.iterdir()):
                        dir_item.rmdir()
                        deleted_dirs.append(str(dir_item))
                        self.log(f"删除空目录: {dir_item}")
                except OSError:
                    # 目录不为空或无法删除，跳过
                    pass
        
        return deleted_dirs
    
    def cleanup_files(self):
        """执行清理操作"""
        main_dir = self.main_dir.get()
        sub_dir = self.sub_dir.get()
        
        if not main_dir or not sub_dir:
            messagebox.showerror("错误", "请先选择主图目录和副图目录！")
            return
        
        if not os.path.exists(main_dir):
            messagebox.showerror("错误", f"主图目录不存在: {main_dir}")
            return
        
        if not os.path.exists(sub_dir):
            messagebox.showerror("错误", f"副图目录不存在: {sub_dir}")
            return
        
        self.log("=" * 50)
        self.log("开始清理操作...")
        self.log(f"主图目录: {main_dir}")
        self.log(f"副图目录: {sub_dir}")
        self.log("=" * 50)
        
        sub_path = Path(sub_dir)
        deleted_files = []
        kept_files = []
        errors = []
        
        # 遍历副图目录中的所有文件（包括子目录）
        for sub_file in sub_path.rglob("*"):
            if sub_file.is_file():
                # 获取主图文件名
                main_image_name = self.get_main_image_name(sub_file)
                
                # 在主图目录中查找
                main_image_path = self.find_main_image(main_dir, main_image_name)
                
                if main_image_path is None:
                    # 找不到主图，删除副图
                    try:
                        sub_file.unlink()
                        deleted_files.append(str(sub_file))
                        self.log(f"删除副图: {sub_file.name} (未找到主图: {main_image_name})")
                    except Exception as e:
                        error_msg = f"删除失败: {sub_file} - {str(e)}"
                        errors.append(error_msg)
                        self.log(f"错误: {error_msg}")
                else:
                    kept_files.append(str(sub_file))
                    self.log(f"保留副图: {sub_file.name} (找到主图: {main_image_path})")
        
        # 清理空目录
        self.log("\n开始清理空目录...")
        deleted_dirs = self.cleanup_empty_dirs(sub_dir)
        
        # 显示结果
        self.log("\n" + "=" * 50)
        self.log("清理完成！")
        self.log(f"删除文件数: {len(deleted_files)}")
        self.log(f"保留文件数: {len(kept_files)}")
        self.log(f"删除空目录数: {len(deleted_dirs)}")
        if errors:
            self.log(f"错误数: {len(errors)}")
        self.log("=" * 50)
        
        # 显示完成对话框
        result_msg = f"清理完成！\n\n删除文件: {len(deleted_files)} 个\n保留文件: {len(kept_files)} 个\n删除空目录: {len(deleted_dirs)} 个"
        if errors:
            result_msg += f"\n错误: {len(errors)} 个"
        
        messagebox.showinfo("完成", result_msg)
        self.execute_btn.config(state="normal")
    
    def start_cleanup(self):
        """在新线程中启动清理操作"""
        if not self.main_dir.get() or not self.sub_dir.get():
            messagebox.showerror("错误", "请先选择主图目录和副图目录！")
            return
        
        # 确认对话框
        result = messagebox.askyesno(
            "确认",
            "确定要开始清理吗？\n此操作将删除找不到对应主图的副图文件，且无法撤销！"
        )
        
        if not result:
            return
        
        # 禁用按钮
        self.execute_btn.config(state="disabled")
        
        # 在新线程中执行清理
        thread = threading.Thread(target=self.cleanup_files, daemon=True)
        thread.start()


def main():
    root = tk.Tk()
    app = FileCleanerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

