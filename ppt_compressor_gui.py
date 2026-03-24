#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPT现代化无损压缩工具 v3.0 - macOS Big Sur风格图形化界面
毛玻璃效果 + 清晰的选中状态
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import queue

# 导入核心压缩功能
from ppt_compressor_v3 import ModernPPTCompressor


class GlassButton(tk.Canvas):
    """毛玻璃风格按钮 - 带明确选中状态"""
    def __init__(self, parent, text, command=None, primary=False, width=120, height=48, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        self.command = command
        self.text = text
        self.primary = primary
        self.width = width
        self.height = height

        # 颜色配置
        if primary:
            self.bg_normal = "#007AFF"
            self.bg_hover = "#0051D5"
            self.bg_pressed = "#003D99"
            self.fg_color = "white"
        else:
            self.bg_normal = "#F5F5F7"
            self.bg_hover = "#E8E8EA"
            self.bg_pressed = "#D1D1D6"
            self.fg_color = "#1D1D1F"

        self.current_bg = self.bg_normal
        self.is_pressed = False

        # 绘制按钮
        self.draw()

        # 绑定事件
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def draw(self):
        self.delete("all")

        # 绘制阴影（毛玻璃效果）
        if not self.primary:
            self.create_rounded_rect(3, 3, self.width-1, self.height-1, 10,
                                    fill="#00000008", outline="")

        # 绘制主体
        self.create_rounded_rect(0, 0, self.width-4, self.height-4, 10,
                                fill=self.current_bg, outline="")

        # 绘制文字
        self.create_text(self.width/2-2, self.height/2-2, text=self.text,
                        fill=self.fg_color, font=("SF Pro", 14, "bold" if self.primary else "normal"))

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1, x2, y1+radius,
            x2, y2-radius,
            x2, y2, x2-radius, y2,
            x1+radius, y2,
            x1, y2, x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_press(self, event):
        self.is_pressed = True
        self.current_bg = self.bg_pressed
        self.draw()

    def on_release(self, event):
        self.is_pressed = False
        self.current_bg = self.bg_hover
        self.draw()
        if self.command:
            self.command()

    def on_enter(self, event):
        if not self.is_pressed:
            self.current_bg = self.bg_hover
            self.draw()

    def on_leave(self, event):
        self.is_pressed = False
        self.current_bg = self.bg_normal
        self.draw()


class PresetCard(tk.Canvas):
    """压缩档位卡片 - 带清晰选中状态"""
    def __init__(self, parent, preset_key, name, rate, variable, **kwargs):
        super().__init__(parent, width=145, height=80, highlightthickness=0, **kwargs)
        self.preset_key = preset_key
        self.name = name
        self.rate = rate
        self.variable = variable
        self.selected = (variable.get() == preset_key)

        # 绘制卡片
        self.draw()

        # 绑定点击事件
        self.bind("<Button-1>", self.on_click)

        # 监听变量变化
        self.variable.trace_add("write", self.on_variable_change)

    def draw(self):
        self.delete("all")

        if self.selected:
            # 选中状态：蓝色边框 + 蓝色背景
            # 外层阴影
            self.create_rounded_rect(2, 2, 143, 78, 12, fill="#007AFF20", outline="")
            # 主体
            self.create_rounded_rect(0, 0, 141, 76, 12, fill="#007AFF", outline="")
            # 标题
            self.create_text(72, 28, text=self.name, fill="white", font=("SF Pro", 15, "bold"))
            # 比率
            self.create_text(72, 52, text=self.rate, fill="white", font=("SF Pro", 12))
        else:
            # 未选中状态：灰色背景
            # 阴影
            self.create_rounded_rect(2, 2, 143, 78, 12, fill="#00000008", outline="")
            # 主体
            self.create_rounded_rect(0, 0, 141, 76, 12, fill="#F5F5F7", outline="")
            # 边框
            self.create_rounded_rect(0, 0, 141, 76, 12, fill="", outline="#E5E5E7", width=1)
            # 标题
            self.create_text(72, 28, text=self.name, fill="#1D1D1F", font=("SF Pro", 15, "bold"))
            # 比率
            self.create_text(72, 52, text=self.rate, fill="#86868B", font=("SF Pro", 12))

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1, x2, y1+radius,
            x2, y2-radius,
            x2, y2, x2-radius, y2,
            x1+radius, y2,
            x1, y2, x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_click(self, event):
        self.variable.set(self.preset_key)

    def on_variable_change(self, *args):
        old_selected = self.selected
        self.selected = (self.variable.get() == self.preset_key)
        if old_selected != self.selected:
            self.draw()


class GlassEntry(tk.Frame):
    """毛玻璃输入框"""
    def __init__(self, parent, textvariable=None, **kwargs):
        super().__init__(parent, bg="#FFFFFF", **kwargs)

        # 容器
        container = tk.Frame(self, bg="#F5F5F7", highlightthickness=1,
                           highlightbackground="#E5E5E7")
        container.pack(fill="both", expand=True)

        self.entry = tk.Entry(container, textvariable=textvariable,
                             font=("SF Pro", 13),
                             bg="#F5F5F7",
                             fg="#1D1D1F",
                             relief="flat",
                             borderwidth=0,
                             insertbackground="#007AFF")
        self.entry.pack(fill="both", expand=True, padx=14, pady=11)


class PPTCompressorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("")  # 空标题更现代

        # 窗口配置
        window_width = 700
        window_height = 780
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)

        # macOS Big Sur毛玻璃背景色
        self.bg_color = "#FAFAFA"
        self.card_bg = "#FFFFFF"
        self.secondary_bg = "#F5F5F7"
        self.text_primary = "#1D1D1F"
        self.text_secondary = "#86868B"
        self.accent_color = "#007AFF"

        self.root.configure(bg=self.bg_color)

        # 变量
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.preset = tk.StringVar(value="lossless")
        self.is_batch_mode = tk.BooleanVar(value=False)
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()

        # 消息队列
        self.message_queue = queue.Queue()

        # 创建界面
        self.create_widgets()

        # 启动消息处理
        self.process_messages()

        # 设置图标
        try:
            icon_path = Path(__file__).parent / "icon_128.png"
            if icon_path.exists():
                icon = tk.PhotoImage(file=str(icon_path))
                self.root.iconphoto(True, icon)
        except:
            pass

    def create_widgets(self):
        # 主容器
        main = tk.Frame(self.root, bg=self.bg_color)
        main.pack(fill="both", expand=True, padx=35, pady=30)

        # ===== 标题 =====
        tk.Label(main, text="PPT Compressor",
                font=("SF Pro Display", 32, "bold"),
                fg=self.text_primary, bg=self.bg_color).pack(anchor="w")

        tk.Label(main, text="完全保留PNG透明度的无损压缩",
                font=("SF Pro", 15),
                fg=self.text_secondary, bg=self.bg_color).pack(anchor="w", pady=(8, 0))

        # ===== 模式切换卡片 =====
        mode_card = tk.Frame(main, bg=self.card_bg, highlightthickness=1,
                           highlightbackground="#E5E5E7")
        mode_card.pack(fill="x", pady=(30, 20))

        mode_inner = tk.Frame(mode_card, bg=self.card_bg)
        mode_inner.pack(fill="x", padx=20, pady=18)

        tk.Radiobutton(mode_inner, text="📄  单文件压缩",
                      variable=self.is_batch_mode, value=False,
                      font=("SF Pro", 14), bg=self.card_bg, fg=self.text_primary,
                      activebackground=self.card_bg, selectcolor=self.accent_color,
                      command=self.toggle_mode).pack(side="left", padx=15)

        tk.Radiobutton(mode_inner, text="📁  批量压缩",
                      variable=self.is_batch_mode, value=True,
                      font=("SF Pro", 14), bg=self.card_bg, fg=self.text_primary,
                      activebackground=self.card_bg, selectcolor=self.accent_color,
                      command=self.toggle_mode).pack(side="left", padx=15)

        # ===== 文件选择（单文件）=====
        self.file_frame = tk.Frame(main, bg=self.bg_color)
        self.file_frame.pack(fill="x", pady=(0, 20))

        tk.Label(self.file_frame, text="选择PPT文件",
                font=("SF Pro", 14, "bold"),
                fg=self.text_primary, bg=self.bg_color).pack(anchor="w", pady=(0, 10))

        input_row = tk.Frame(self.file_frame, bg=self.bg_color)
        input_row.pack(fill="x")

        GlassEntry(input_row, textvariable=self.input_file).pack(
            side="left", fill="x", expand=True)

        GlassButton(input_row, "浏览", command=self.browse_input_file,
                   width=90, height=44).pack(side="left", padx=(12, 0))

        # ===== 文件夹选择（批量）=====
        self.folder_frame = tk.Frame(main, bg=self.bg_color)

        tk.Label(self.folder_frame, text="输入文件夹",
                font=("SF Pro", 14, "bold"),
                fg=self.text_primary, bg=self.bg_color).pack(anchor="w", pady=(0, 10))

        input_folder_row = tk.Frame(self.folder_frame, bg=self.bg_color)
        input_folder_row.pack(fill="x", pady=(0, 18))

        GlassEntry(input_folder_row, textvariable=self.input_folder).pack(
            side="left", fill="x", expand=True)

        GlassButton(input_folder_row, "浏览", command=self.browse_input_folder,
                   width=90, height=44).pack(side="left", padx=(12, 0))

        tk.Label(self.folder_frame, text="输出文件夹",
                font=("SF Pro", 14, "bold"),
                fg=self.text_primary, bg=self.bg_color).pack(anchor="w", pady=(0, 10))

        output_folder_row = tk.Frame(self.folder_frame, bg=self.bg_color)
        output_folder_row.pack(fill="x")

        GlassEntry(output_folder_row, textvariable=self.output_folder).pack(
            side="left", fill="x", expand=True)

        GlassButton(output_folder_row, "浏览", command=self.browse_output_folder,
                   width=90, height=44).pack(side="left", padx=(12, 0))

        # ===== 压缩质量选择 =====
        tk.Label(main, text="压缩质量",
                font=("SF Pro", 14, "bold"),
                fg=self.text_primary, bg=self.bg_color).pack(anchor="w", pady=(0, 12))

        presets_grid = tk.Frame(main, bg=self.bg_color)
        presets_grid.pack(fill="x", pady=(0, 25))

        presets = [
            ("lossless", "完全无损", "15-30%"),
            ("high", "高质量", "30-50%"),
            ("balanced", "平衡", "50-70%"),
            ("aggressive", "激进", "70-85%"),
        ]

        for i, (key, name, rate) in enumerate(presets):
            card = PresetCard(presets_grid, key, name, rate, self.preset)
            card.pack(side="left", padx=(0 if i == 0 else 10, 0))

        # ===== 操作按钮 =====
        self.compress_btn = GlassButton(main, "开始压缩",
                                       command=self.start_compression,
                                       primary=True, width=630, height=52)
        self.compress_btn.pack(fill="x", pady=(0, 12))

        actions_row = tk.Frame(main, bg=self.bg_color)
        actions_row.pack(fill="x", pady=(0, 25))

        GlassButton(actions_row, "检查依赖", command=self.check_dependencies,
                   width=310, height=42).pack(side="left", fill="x", expand=True)

        GlassButton(actions_row, "清空日志", command=self.clear_log,
                   width=310, height=42).pack(side="left", fill="x", expand=True, padx=(10, 0))

        # ===== 日志 =====
        tk.Label(main, text="压缩日志",
                font=("SF Pro", 14, "bold"),
                fg=self.text_primary, bg=self.bg_color).pack(anchor="w", pady=(0, 10))

        log_card = tk.Frame(main, bg=self.secondary_bg,
                          highlightthickness=1, highlightbackground="#E5E5E7")
        log_card.pack(fill="both", expand=True)

        self.log_text = tk.Text(log_card, font=("SF Mono", 11),
                               bg=self.secondary_bg, fg=self.text_primary,
                               relief="flat", borderwidth=0, wrap="word", height=10)
        self.log_text.pack(fill="both", expand=True, padx=16, pady=14)

        self.log_text.tag_config('success', foreground="#34C759")
        self.log_text.tag_config('error', foreground="#FF3B30")
        self.log_text.tag_config('warning', foreground="#FF9500")
        self.log_text.tag_config('info', foreground=self.accent_color)

        # 初始化
        self.toggle_mode()
        self.log("欢迎使用 PPT Compressor v3.0", 'info')
        self.log("完全保留PNG透明度，真正的无损压缩")
        self.log("-" * 60)

    def toggle_mode(self):
        if self.is_batch_mode.get():
            self.file_frame.pack_forget()
            self.folder_frame.pack(fill="x", pady=(0, 20))
        else:
            self.folder_frame.pack_forget()
            self.file_frame.pack(fill="x", pady=(0, 20))

    def browse_input_file(self):
        filename = filedialog.askopenfilename(
            title="选择PPT文件",
            filetypes=[("PowerPoint文件", "*.pptx *.ppt"), ("所有文件", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            self.log(f"✓ 已选择: {Path(filename).name}", 'success')

    def browse_input_folder(self):
        folder = filedialog.askdirectory(title="选择包含PPT文件的文件夹")
        if folder:
            self.input_folder.set(folder)
            self.log(f"✓ 输入文件夹: {Path(folder).name}", 'success')

    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="选择输出文件夹")
        if folder:
            self.output_folder.set(folder)
            self.log(f"✓ 输出文件夹: {Path(folder).name}", 'success')

    def log(self, message, tag=None):
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        self.log("日志已清空", 'info')

    def check_dependencies(self):
        self.log("-" * 60)
        self.log("正在检查依赖...", 'info')

        import sys
        self.log(f"✓ Python: {sys.version.split()[0]}", 'success')

        try:
            from PIL import Image
            import PIL
            self.log(f"✓ Pillow: {PIL.__version__}", 'success')
        except ImportError:
            self.log("✗ Pillow未安装", 'error')

        import subprocess
        try:
            result = subprocess.run(['oxipng', '--version'],
                                  capture_output=True, timeout=2, text=True)
            if result.returncode == 0:
                version = result.stdout.strip().split()[1] if len(result.stdout.split()) > 1 else ""
                self.log(f"✓ oxipng: {version}", 'success')
            else:
                raise Exception()
        except:
            self.log("⚠ oxipng未安装 (推荐)", 'warning')

        self.log("-" * 60)

    def start_compression(self):
        if self.is_batch_mode.get():
            self.start_batch_compression()
        else:
            self.start_single_compression()

    def start_single_compression(self):
        input_file = self.input_file.get().strip()
        preset = self.preset.get()

        if not input_file:
            messagebox.showerror("错误", "请选择输入文件")
            return

        if not Path(input_file).exists():
            messagebox.showerror("错误", f"文件不存在")
            return

        self.compress_btn.configure(state='disabled')

        thread = threading.Thread(
            target=self.compress_file_thread,
            args=(input_file, None, preset)
        )
        thread.daemon = True
        thread.start()

    def compress_file_thread(self, input_file, output_file, preset):
        try:
            self.message_queue.put(("log", "-" * 60, None))
            self.message_queue.put(("log", f"开始压缩: {Path(input_file).name}", 'info'))
            self.message_queue.put(("log", f"压缩档位: {preset.upper()}", 'info'))

            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                compressor = ModernPPTCompressor(preset=preset)
                compressor.compress_ppt(input_file, output_file)

            output = f.getvalue()
            for line in output.split('\n'):
                if line.strip():
                    tag = None
                    if '✓' in line or '✅' in line:
                        tag = 'success'
                    elif '⚠' in line:
                        tag = 'warning'
                    elif '❌' in line:
                        tag = 'error'
                    self.message_queue.put(("log", line, tag))

            self.message_queue.put(("log", "-" * 60, None))
            self.message_queue.put(("enable_button", None, None))
            self.message_queue.put(("show_success", "压缩完成!", None))

        except Exception as e:
            self.message_queue.put(("log", f"❌ 压缩失败: {str(e)}", 'error'))
            self.message_queue.put(("enable_button", None, None))
            self.message_queue.put(("show_error", f"压缩失败: {str(e)}", None))

    def start_batch_compression(self):
        input_folder = self.input_folder.get().strip()
        output_folder = self.output_folder.get().strip()
        preset = self.preset.get()

        if not input_folder:
            messagebox.showerror("错误", "请选择输入文件夹")
            return

        if not Path(input_folder).exists():
            messagebox.showerror("错误", f"文件夹不存在")
            return

        if not output_folder:
            messagebox.showerror("错误", "请选择输出文件夹")
            return

        Path(output_folder).mkdir(parents=True, exist_ok=True)
        self.compress_btn.configure(state='disabled')

        thread = threading.Thread(
            target=self.batch_compress_thread,
            args=(input_folder, output_folder, preset)
        )
        thread.daemon = True
        thread.start()

    def batch_compress_thread(self, input_folder, output_folder, preset):
        try:
            self.message_queue.put(("log", "-" * 60, None))
            self.message_queue.put(("log", f"开始批量压缩", 'info'))
            self.message_queue.put(("log", "-" * 60, None))

            input_path = Path(input_folder)
            ppt_files = list(input_path.glob("*.pptx")) + list(input_path.glob("*.ppt"))

            if not ppt_files:
                self.message_queue.put(("log", "⚠ 未找到PPT文件", 'warning'))
                self.message_queue.put(("enable_button", None, None))
                return

            self.message_queue.put(("log", f"找到 {len(ppt_files)} 个文件", 'info'))
            self.message_queue.put(("log", "", None))

            success_count = 0
            for i, ppt_file in enumerate(ppt_files, 1):
                try:
                    self.message_queue.put(("log", f"[{i}/{len(ppt_files)}] {ppt_file.name}", 'info'))

                    output_file = Path(output_folder) / ppt_file.name

                    import io
                    from contextlib import redirect_stdout

                    f = io.StringIO()
                    with redirect_stdout(f):
                        compressor = ModernPPTCompressor(preset=preset)
                        compressor.compress_ppt(str(ppt_file), str(output_file))

                    output = f.getvalue()
                    for line in output.split('\n'):
                        if '✅' in line or '减小' in line:
                            self.message_queue.put(("log", line, 'success'))

                    success_count += 1
                    self.message_queue.put(("log", "", None))

                except Exception as e:
                    self.message_queue.put(("log", f"  ✗ 失败: {str(e)}", 'error'))
                    self.message_queue.put(("log", "", None))

            self.message_queue.put(("log", "-" * 60, None))
            self.message_queue.put(("log", f"✓ 完成! 成功: {success_count}/{len(ppt_files)}", 'success'))
            self.message_queue.put(("enable_button", None, None))
            self.message_queue.put(("show_success", f"批量压缩完成!\n成功: {success_count}/{len(ppt_files)}", None))

        except Exception as e:
            self.message_queue.put(("log", f"❌ 失败: {str(e)}", 'error'))
            self.message_queue.put(("enable_button", None, None))
            self.message_queue.put(("show_error", f"失败: {str(e)}", None))

    def process_messages(self):
        try:
            while True:
                msg_type, msg_data, msg_tag = self.message_queue.get_nowait()

                if msg_type == "log":
                    self.log(msg_data, msg_tag)
                elif msg_type == "enable_button":
                    self.compress_btn.configure(state='normal')
                elif msg_type == "show_success":
                    messagebox.showinfo("成功", msg_data)
                elif msg_type == "show_error":
                    messagebox.showerror("错误", msg_data)

        except queue.Empty:
            pass

        self.root.after(100, self.process_messages)


def main():
    root = tk.Tk()

    try:
        root.tk.call('tk', 'scaling', 2.0)
    except:
        pass

    app = PPTCompressorGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
