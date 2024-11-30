# -*- coding: utf-8 -*-
'''
# datetime: 2024/10/31
# author: Yu.Wei-wu
# telephone: 18395393599
# Tsinghua Source: https://pypi.tuna.tsinghua.edu.cn/simple
'''

try:
    import pyi_splash
    import time
    import random

    i = 1
    text=f'Loading...Progress{i:.2f}%'
    pyi_splash.update_text(text)
    num = random.random()*100 + 1
    while True:   
        if num < 100 and num > i:
            i = num
            text=f'Loading...Progress{i:.2f}%'
            pyi_splash.update_text(text)
            time.sleep(1)
            num = random.random()*100 + 1
            continue
        elif num < 100 and not num > i:
            num = random.random()*100 + 1
            continue
        else:
            break
    pyi_splash.update_text('Loading...Progress100%')
    time.sleep(1)
    pyi_splash.close()
except ImportError:
    pass

import sys
import os
import code
import readline as r
import rlcompleter
import random
import re
import time
import tkinter as tk
from tkinter import colorchooser
from tkinter import font  
from tkinter import simpledialog, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from datetime import datetime 
import pyautogui
from selenium import webdriver  
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchWindowException 
import cv2  
import numpy as np
from subprocess import CREATE_NO_WINDOW
import threading  
from queue import Queue
import webbrowser

# 给定一个16进制颜色返回一个更亮的颜色
def lighten_hex_color(hex_color, factor=0.9):
    # 确保输入是一个有效的十六进制颜色字符串
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color format")
    
    # 将十六进制颜色转换为RGB元组
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # 根据因子减少每个颜色通道的值
    r_new = int(r * factor)
    g_new = int(g * factor)
    b_new = int(b * factor)
    
    # 确保新的颜色值不会变成负数
    r_new = max(0, r_new)
    g_new = max(0, g_new)
    b_new = max(0, b_new)
    
    # 将新的RGB值转换回十六进制颜色字符串
    return '#{:02x}{:02x}{:02x}'.format(r_new, g_new, b_new)

# 直接运行与打包成exe的文件路径不一样，以获取需要用到的资源
def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
 
    return os.path.normpath(os.path.join(base_path, relative_path))

# 全局字典，用于将ANSI转义序列映射到标签名称和样式(原Go_pi用colorama模块打印的不同颜色信息在重定向时更改为UI控件的标签颜色)
ANSI_TO_TAG = {
    "\033[31m": "tag_red",
    "\033[32m": "tag_green",
    "\033[33m": "tag_yellow", 
    "\033[39m": "tag_black",
    "\033[91m": "tag_light_red",
    "\033[92m": "tag_light_green",
    "\033[0m": "tag_reset"
}
ANSI_STYLES = {
    "tag_red": {"foreground": "red"}, 
    "tag_green": {"foreground": "green"},
    "tag_yellow": {"foreground": "yellow"},
    "tag_black": {"foreground": "black"},
    "tag_light_red": {"foreground": "DeepPink"},
    "tag_light_green": {"foreground": "lime"},
    "tag_reset": {"foreground": "black"}
}

# 自定义一个继承 Canvas 的上下键按钮的类，自动更新传入控件的值, 功能等同于 Spinbox
class CustomSpinbox(tk.Canvas):
    def __init__(self, parent, controlled_widget, direction="", from_=0, to=500, initialvalue=1, bg="lightgray", *args, **kwargs):
        super().__init__(parent, 
                         bg=bg, 
                         width=25, 
                         height=25,
                         highlightthickness=0,
                         *args, **kwargs)
        self.controlled_widget = controlled_widget
        self.direction = direction
        self.from_value = from_
        self.to_value = to
        self.current_custom_spinbox_value = tk.IntVar(value=initialvalue)
        self.bg = bg
        self.is_continue_incrementing = False
        self.is_continue_decrementing = False

        self.bind("<Configure>", self.redraw_spinbox_rectangle)    
        self.current_custom_spinbox_value.trace_add("write", self.update_entry)

    def redraw_spinbox_rectangle(self, event=None):
        self.delete("all")
        width = self.winfo_width()-5
        height = self.winfo_height()  
        self.hover_bg = 'black'

        if self.direction == "l":
            points = [  
                (0, height/3),  
                (5*width/12, 0),  
                (5*width/12, height/4),  
                (5*width/6, height/4),   
                (11*width/12, height/3), 
                (width, height/2), 
                (11*width/12, 5*height/6),  
                (5*width/6, 11*height/12),
                (7*width/12, height),
                (width/2, height),
                (2*width/3, 5*height/6),
                (3*width/4, 5*height/6),
                (5*width/6, 2*height/3),
                (3*width/4, 5*height/12),
                (5*width/12, 5*height/12),
                (5*width/12, 2*height/3),
                (0, height/4)
            ]
        elif self.direction == "r":
            points = [  
                (width, height/3),  
                (7*width/12, 0),  
                (7*width/12, height/4),  
                (width/6, height/4),   
                (width/12, height/3), 
                (0, height/2), 
                (width/12, 5*height/6),  
                (width/6, 11*height/12),
                (5*width/12, height),
                (width/2, height),
                (width/3, 5*height/6),
                (width/4, 5*height/6),
                (width/6, 2*height/3),
                (width/4, 5*height/12),
                (7*width/12, 5*height/12),
                (7*width/12, 2*height/3),
                (width, height/4)
            ]
        self.custom_arrow = self.create_polygon(points, 
                                                fill=lighten_hex_color(self.bg),
                                                outline=lighten_hex_color(self.bg), 
                                                smooth=True) 
        self.enable_customspinbox()
    
    def enable_customspinbox(self):
        self.bind("<Enter>", self.on_enter)  
        self.bind("<Leave>", self.on_leave)  
        if self.direction == "l":
            self.bind("<ButtonPress-1>", self.start_decrement)
            self.bind("<ButtonRelease-1>", self.stop_decrement)
        elif self.direction == "r":
            self.bind("<ButtonPress-1>", self.start_increment) 
            self.bind("<ButtonRelease-1>", self.stop_increment)  

    def disable_customspinbox(self):
        self.unbind("<Enter>")
        self.unbind("<Leave>")
        self.unbind("<ButtonPress-1>")
        self.unbind("<ButtonRelease-1>")

    def on_enter(self, e):       
        self.itemconfig(self.custom_arrow, 
                        fill=self.hover_bg, 
                        outline=self.hover_bg)
  
    def on_leave(self, e):
        self.itemconfig(self.custom_arrow, 
                        fill=lighten_hex_color(self.bg), 
                        outline=lighten_hex_color(self.bg))   
        
    def start_increment(self, event=None):
        self.is_continue_incrementing = True
        self.increment()

    def stop_increment(self, event=None):
        self.is_continue_incrementing = False

    def increment(self, event=None):
        if self.is_continue_incrementing:
            try:
                new_value = int(''.join(char for char in self.controlled_widget.get() if char.isdigit())) + 1
            except:
                new_value = self.current_custom_spinbox_value.get() + 1
            if new_value <= self.to_value:
                self.current_custom_spinbox_value.set(new_value)
            else:
                self.current_custom_spinbox_value.set(0)
            self.after(100, self.increment)
    
    def start_decrement(self, event=None):
        self.is_continue_decrementing = True
        self.decrement()

    def stop_decrement(self, event=None):
        self.is_continue_decrementing = False
        
    def decrement(self, event=None):
        if self.is_continue_decrementing:
            try:
                new_value = int(''.join(char for char in self.controlled_widget.get() if char.isdigit())) - 1
            except:
                new_value = self.current_custom_spinbox_value.get() - 1
            if new_value >= self.from_value:
                self.current_custom_spinbox_value.set(new_value)
            else:
                self.current_custom_spinbox_value.set(500)
            self.after(100, self.decrement)

    def update_entry(self, *args):
        self.controlled_widget.delete(0, tk.END)
        self.controlled_widget.insert(0, str(self.current_custom_spinbox_value.get()))

    def update_color(self, new_color):
        self.bg = new_color
        self.config(bg=self.bg)
        self.redraw_spinbox_rectangle(None) 

# 重定向类，负责将原Go_pi代码print的内容保存在队列中，以便主UI界面获取
class RedirectedIO:
    """
    单个处理线程：在 __init__ 方法中启动一个单独的线程来处理队列中的所有写入请求。
    线程间通信: 使用队列作为线程间通信的唯一方式。主线程(写入线程)将数据放入队列,而处理线程则从队列中取出数据以便后续更新UI。
    UI更新同步: 使用Tkinter的 after 方法或类似的机制来安排UI更新在主线程中执行。
    """
    def __init__(self, widget):
        self.widget = widget
        self.pattern = re.compile(r'(\033\[\d+m)') # 返回的正则表达式对象用于识别和处理ANSI转义序列，\033匹配ANSI转义序列的引导字符（ESC，是colorama模块用于控制终端的输出格式）。在Python字符串中,\033是八进制表示法,等同于十六进制的\x1B
        self.queue = Queue()
        self.textarea_widget_state_lock = threading.Lock()  # 用于保护textarea控件更新的锁，防止其余线程更新文本区UI  
        threading.Thread(target=self._process_queue_thread, daemon=True).start() # 启动一个守护线程来处理队列中的信息

    # 主线程UI中会调用的函数：将信息放入队列，而不是直接更新控件    
    def write(self, text, tag=None):
        self.queue.put((text, tag))
    
    # 从队列中取出信息并更新控件（更新控件在主线程中运行）
    def _process_queue_thread(self):
        while True:
            try:
                # 从队列中获取一个项目（阻塞直到有项目可用）
                text, tag = self.queue.get(block=True)
                # 使用Tkinter的after方法在主线程中更新UI
                # 注意，由于 after(0, ...) 会将 _update_widget方法安排到主线程的事件循环中的下一个空闲时间执行，
                # 因此可能会有多个 _update_widget 调用被排队等待执行。
                # 这通常不是问题，因为Tkinter的事件循环会按顺序处理它们。
                self.widget.after(0, self._update_widget, text, tag)
            except self.queue.Empty:
                # 如果队列为空，则退出循环（但实际上由于block=True，这不会发生）
                break

    #从队列中取出信息并更新控件（是在主线程中运行）
    def _update_widget(self, text, tag):
        with self.textarea_widget_state_lock:  # 使用 with 语句来管理锁
            # 控件可编辑，插入信息
            self.widget.config(state=tk.NORMAL)  

            # 每次更新文本的内容中只改变了其中的数字部分，显示时只显示最新的内容
            if "\r" in text:
                current_line_start = self.widget.index("insert linestart")
                current_line_end = self.widget.index("insert lineend")
                self.widget.delete(current_line_start, current_line_end)
                #self.widget.delete("end-1l linestart", tk.END)
                text = text.replace("\r", "")

            # 展示文本内容，如果原始信息中使用了colorama模块，则使用ANSI转义序列打印有颜色的文本
            parts = self.pattern.split(text)
            current_tag = tag
            for part in parts:
                if part in ANSI_TO_TAG:
                    tag_name = ANSI_TO_TAG[part]
                    if tag_name not in self.widget.tag_names():
                        self.widget.tag_configure(tag_name, **ANSI_STYLES[tag_name])
                    current_tag = tag_name
                else:
                    self.widget.insert(tk.END, part, current_tag)
            self.widget.see(tk.END) 
            #self.widget.update_idletasks()# 由于是在after方法中，所以不需要再次调用update_idletasks()，Tkinter会自动处理空闲任务

            # 控件恢复默认，用户不可编辑
            self.widget.config(state=tk.DISABLED)

    def flush(self):
        pass

# 自定义画布按钮
class HoverButton(tk.Canvas):  
    def __init__(self, master=None, event=None, text='', radius=10, color=None, command=None, **kw):  
        super().__init__(master, width=100, height=50, highlightbackground=color, **kw)
        self.text = text
        self.radius = radius
        self.color = color
        self.command = command
        self.event = event
        self.bind("<Configure>", self.redraw_button_rectangle)  
  
    def redraw_button_rectangle(self, event=None):
        self.delete("all")
        
        width = self.winfo_width()  
        height = self.winfo_height()

        self.font_normal = font.Font(family='Arial', size=10)  
        self.font_hover = font.Font(family='Arial', size=10, weight='bold')  
        self.default_bg = lighten_hex_color(self.color)
        self.hover_bg_1 = 'lightgreen'
        self.hover_bg_2 = 'lightblue'  

        points = [  
            (self.radius, 0),  
            (width-self.radius, 0),  
            (width, self.radius),  
            (width, height-self.radius),  
            (width-self.radius, height),  
            (self.radius, height),  
            (0, height-self.radius),  
            (0, self.radius)  
        ]
  
        self.rect_id = self.create_polygon(points, fill=self.default_bg, smooth=True)
        self.text_id = self.create_text(width/2, height/2, text=self.text, font=self.font_normal, anchor='center')  

        self.bind("<Enter>", self.on_enter)  
        self.bind("<Leave>", self.on_leave)
        self.bind("<FocusIn>", self.on_enter)
        self.bind("<FocusOut>", self.on_leave)  
        self.bind("<Button-1>", self.on_click)
        self.bind("<Return>", self.on_click)

    def on_enter(self, e):
        self.itemconfig(self.text_id, font=self.font_hover)  
        if self.itemcget(self.text_id, "text") == "confirm":       
            self.itemconfig(self.rect_id, fill=self.hover_bg_1, outline='black')
        else:
            self.itemconfig(self.rect_id, fill=self.hover_bg_2, outline='black')
  
    def on_leave(self, e):
        if self.itemcget(self.text_id, "text") == "confirm" and self.event.is_set(): 
            return
        self.itemconfig(self.rect_id, fill=self.default_bg, outline='')  
        self.itemconfig(self.text_id, font=self.font_normal)

    def on_click(self, event=None):
        if self.command is not None:  
            self.command(event)

    def update_color(self, new_color):
        self.color = new_color
        self.config(highlightbackground=self.color)
        self.redraw_button_rectangle(None) 

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Genoa_xGMI_auto")
        #self.root.attributes("-topmost", True)  # 窗口始终在屏幕最上方
        #self.root.state("zoomed") # 窗口将启动时最大化
        #self.root.iconbitmap(get_path("assets/1.ico")) # iconphoto更通用,仅在Windows上有效，不使用iconbitmap
        import base64 # 导入base64模块，用于处理二进制数据
        with open(get_path("assets/logo.ico"), 'rb') as open_icon:
            b64str = base64.b64encode(open_icon.read()) # 防止文件出错，获得引用后及时关闭， 将图标文件读取并编码为base64字符串  
        root_icon_img = b64str
        root_icon_img = base64.b64decode(root_icon_img) # 解码base64字符串
        root_icon_img = ImageTk.PhotoImage(data=root_icon_img) # 将解码后的数据转换为ImageTk.PhotoImage对象
        self.root.tk.call('wm', 'iconphoto', self.root._w, root_icon_img) # 设置窗口图标
        self.theme_color = '#F5F5F5'  # 默认主题颜色浅灰色
        self.root.config(bg=self.theme_color)
        self.root.minsize(2000,550)

        # 设置默认的鼠标样式
        self.default_cursor = 'arrow'
        self.dragging_cursor = 'fleur'
        # 变量来记录是否正在拖动窗口
        self.dragging = False
        # 变量来记录鼠标和窗口的初始位置
        self.init_x, self.init_y = None, None
        self.init_window_x, self.init_window_y = None, None
        # 绑定事件
        self.root.bind("<ButtonPress-1>", self.root_on_mouse_press)
        self.root.bind("<B1-Motion>", self.root_on_mouse_drag)
        self.root.bind("<ButtonRelease-1>", self.root_on_mouse_release) 
        # 初始化窗口配置
        self.root.config(cursor=self.default_cursor)

        self.estimated_label_ignore_root_click = False
        #self.root.bind("<Button-1>", self.on_root_click)
        self.root.bind('<Escape>', self.on_closing)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.prev_width, self.prev_height = self.root.winfo_width(), self.root.winfo_height()
        self.prev_x, self.prev_y = self.root.winfo_x(), self.root.winfo_y()
        self.root.bind("<Configure>", self.root_on_configure)

        self.create_menus()
        # 设置窗口图标（使用PNG图片需要PIL库处理）
        # iconphoto方法接受的Image对象必须是PhotoImage类型，方法接受的图像必须是 RGB 模式，并且大小通常应该适合作为窗口图标（例如，32x32 像素）
        self.toplevel_icon = Image.open(get_path("assets/logo.ico"))
        self.toplevel_icon_photo = ImageTk.PhotoImage(self.toplevel_icon)
        # root相关变量初始化
        self.window_closed = False
        self.input_popup = None
        # 驱动标志变量初始化
        self.driver_is_good = False # 标志变量，指示驱动是否可用
        self.driver_fully_booted_is_ok = False # 标志变量，指示驱动是否已完全启动
        self.is_installing_driver = False # 标志变量，指示是否正在自动下载驱动驱动
        self._is_key_bound = [False, False, False, False]  # 标志变量，通过绑定和移绑key按键功能指示每个entry输入框是否可编辑，直接使用控件参数state="DISABLED"会导致颜色不可设置
        self.error_window = None
        self.driver_info_dialog = None
        # 保存log的内容初始化
        self.save_log_content = ""
        # 开启验证功能的标志变量初始化
        self.is_enabled_val_if_run_successfully = False
        self.verification_window = None
        self.vf_upload_image_file_path = get_path("assets/template.jpeg")
        # 获取帮助的窗口初始化
        self.about_window = None
        self.cool_emoji_photo = self.resize_image(get_path("assets/cool_emoji.png"), 0.08)
        self.cry_emoji_photo = self.resize_image(get_path("assets/cry_emoji.png"), 0.08)
        self.errot_plug_photo = self.resize_image(get_path("assets/Error_plug.png"), 0.08)

        # 主循环和后台线程并行，需要使用threading.Event事件对象机制来同步管理事件状态--在后台线程中实时安全地访问和检查事件的值
        self.start_prepare_event = threading.Event()
        self.username_and_password_ready_event = threading.Event()
        self.runtimes_ready_event = threading.Event()
        self.estimated_time_ready_event = threading.Event()
        self.all_input_ready_event = threading.Event()

        self.frame_left = tk.Frame(self.root, bg=self.theme_color)  
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        self.frame_right = tk.Frame(self.root, bg=self.theme_color)  
        self.frame_right.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=1)
        self.frame_left.grid_columnconfigure(1, weight=1)
        for i in range(11):
            self.frame_left.grid_rowconfigure(i, weight=1)
        
        self.browser_type_label = tk.Label(self.frame_left, text="浏览器: ", bg=self.theme_color)
        self.browser_type_label.grid(row=0, column=0, sticky='w', padx=5)
        self.browser_type_var = tk.IntVar(value=1)
        self.browser_type = {  
            1: 'Edge',  
            2: 'Chrome'
        }
        self.request_download_browser = "Edge"
        self.browser_radio_buttons = []
        self.browser_radio_is_enabled = True
        for j, (browser_type_key, browser_type_value) in enumerate(self.browser_type.items(), start=1):  
            rb = tk.Radiobutton(self.frame_left, 
                                value=browser_type_key,
                                text=browser_type_value, 
                                variable=self.browser_type_var, 
                                command=self.select_browser_radio,
                                bg=self.theme_color)
            rb.bind("<Tab>", self.handle_enter)
            rb.bind("<Return>", self.select_radio_ok)
            if j == 1:
                rb.grid(row=0, column=1, sticky='w', padx=50)
            else:
                rb.grid(row=0, column=1, sticky='e', padx=300) 
            self.browser_radio_buttons.append(rb)
        # root窗口使用tab键重新聚焦时执行
        self.browser_radio_buttons[0].bind('<FocusIn>', self.root_re_focus_in_browser_type_radio)

        # 初始驱动路径
        self.driver_path_label = tk.Label(self.frame_left, text="驱动路径:", bg=self.theme_color)  
        self.driver_path_label.grid(row=1, column=0, sticky='w', padx=5, pady=10)  
        self.driver_path_var = tk.StringVar(value="")  
        self.driver_path_entry = tk.Entry(self.frame_left,
                                          textvariable=self.driver_path_var, 
                                          bg=lighten_hex_color(self.theme_color),
                                          highlightcolor="black", 
                                          highlightthickness=0.5)  
        self.driver_path_entry.grid(row=1, column=1, columnspan=2, sticky='ew', padx=5, pady=10)
        self.driver_path_entry.bind('<Key>', lambda event: 'break')
        self.driver_path_entry.bind('<Tab>', self.handle_enter)
        self.driver_path_entry.bind("<Return>", self.handle_enter)
        # 根据初始浏览器选择设置驱动路径显示文本
        self.select_browser_radio()  # 调用一次以设置初始状态

        self.entries_vars_current_value = []
        self.entries_vars_default_value = []
        self.test_item_label = tk.Label(self.frame_left, text="xGMI测试项: ", bg=self.theme_color)
        self.test_item_label.grid(row=4, column=0, sticky='w', padx=5)
        self.test_item_var = tk.IntVar(value=1)
        self.test_item_radio_is_enabled = True
        self.entries_vars_current_value.append(self.test_item_var.get())
        self.entries_vars_default_value.append(self.test_item_var.get())
        self.test_items = {  
            1: 'GSA Stress',  
            2: '4-Point Parallel^2 Test',  
            3: '4-Point Test',  
            4: 'Margin Search(BER9)',  
            5: 'Margin Search(BER10)'  
        }
        self.test_item_radio_buttons = []
        for i, (key, value) in enumerate(self.test_items.items(), start=1):  
            rb = tk.Radiobutton(self.frame_left, text=value, variable=self.test_item_var, value=key, command=self.update_estimated_time_entry, bg=self.theme_color)
            rb.grid(row=i+1, column=1, sticky='w', padx=5)
            rb.bind("<Return>", self.select_radio_ok)
            rb.bind("<Tab>", self.select_test_item_radio_tab)
            self.test_item_radio_buttons.append(rb)
            
        self.username_var = tk.StringVar()
        self.username_var.set("Please enter your NTID username(if leave blank or no change, use defult username)")
        self.default_username_var = tk.StringVar()
        self.default_username_var.set("hu.demi@inventec.com.cn")
        self.entries_vars_current_value.append(self.username_var.get())
        self.entries_vars_default_value.append(self.default_username_var.get())
        self.password_var = tk.StringVar()
        self.password_var.set("Please enter your NTID password(if leave blank or no change, use defult password)")
        self.default_password_var = tk.StringVar()
        self.default_password_var.set("Ev@20240912")
        self.entries_vars_current_value.append(self.password_var.get())
        self.entries_vars_default_value.append(self.default_password_var.get())
        self.username_label = tk.Label(self.frame_left, text="AMD用户名: ", bg=self.theme_color)
        self.username_label.grid(row=7, column=0, sticky='w', padx=5, pady=10)
        self.username_entry = tk.Entry(self.frame_left, textvariable=self.username_var, bg=lighten_hex_color(self.theme_color), highlightcolor="black", highlightthickness=0.5)
        self.username_entry.grid(row=7, column=1, columnspan=2, sticky='ew', padx=5, pady=10)  
        self.password_label = tk.Label(self.frame_left, text="AMD密码: ", bg=self.theme_color)
        self.password_label.grid(row=8, column=0, sticky='w', padx=5, pady=10)
        self.password_entry = tk.Entry(self.frame_left, textvariable=self.password_var, show= '*', bg=lighten_hex_color(self.theme_color), highlightcolor="black", highlightthickness=0.5)
        self.password_entry.grid(row=8, column=1, columnspan=2, sticky='ew', padx=5, pady=10)
        self.password_eye_open_photo = self.resize_image(get_path("assets/eye_open.png"), 0.1)
        self.password_eye_close_photo = self.resize_image(get_path("assets/eye_close.png"), 0.1)
        self.password_is_show_eye = tk.Label(self.frame_left,
                                             image=self.password_eye_close_photo,
                                             bg=lighten_hex_color(self.theme_color),
                                             cursor="exchange")
        self.password_is_show_eye.grid(row=8, column=2, sticky='e', padx=10, pady=10)
        self.username_entry.bind("<FocusIn>", self.on_username_focus_in)  
        self.username_entry.bind("<FocusOut>", self.on_username_focus_out)
        self.password_entry.bind("<FocusIn>", self.on_password_focus_in)  
        self.password_entry.bind("<FocusOut>", self.on_password_focus_out)
        self.username_entry.bind("<Return>", self.handle_enter)
        self.password_entry.bind("<Return>", self.handle_enter)
        self.password_entry_is_visible = False
        self.password_is_show_eye.bind("<Button-1>", self.change_password_entry_visibility)

        self.runtimes_var = tk.StringVar()
        self.runtimes_var.set("Please enter the number to loop through(default:1)")
        self.entries_vars_current_value.append(self.runtimes_var.get())
        self.entries_vars_default_value.append(self.runtimes_var.get())
        self.runtimes_label = tk.Label(self.frame_left, text="测试/解锁次数:", bg=self.theme_color)
        self.runtimes_label.grid(row=9, column=0, sticky='w', padx=5, pady=10)
        self.runtimes_entry = tk.Entry(self.frame_left, textvariable=self.runtimes_var, bg=lighten_hex_color(self.theme_color), highlightcolor="black", highlightthickness=0.5)
        self.runtimes_entry.grid(row=9, column=1, sticky='ew', padx=5, pady=10)
        self.runtimes_left_spinbox = CustomSpinbox(self.frame_left, self.runtimes_entry, direction="l", bg=self.theme_color, cursor="left_side")
        self.runtimes_left_spinbox.grid(row=9, column=2, sticky='e', padx=(0, 35), pady=10)
        self.runtimes_right_spinbox = CustomSpinbox(self.frame_left, self.runtimes_entry, direction="r", bg=self.theme_color, cursor="right_side")
        self.runtimes_right_spinbox.grid(row=9, column=2, sticky='e', padx=5, pady=10)
        self.runtimes_entry.bind("<FocusIn>", self.on_runtimes_focus_in)  
        self.runtimes_entry.bind("<FocusOut>", self.on_runtimes_focus_out)
        self.runtimes_entry.bind("<Return>", self.handle_enter)

        self.default_time = {1: 3800, 2: 1500, 3: 2300, 4: 2800, 5: 4300}.get(self.test_item_var.get(), 0)
        self.estimated_time_var = tk.StringVar()
        self.estimated_time_var.set(f"Default one estimated time for test {self.test_items[self.test_item_var.get()]} is {self.default_time}s")
        self.entries_vars_current_value.append(self.default_time)
        self.entries_vars_default_value.append(self.default_time)
        self.default_font = font.Font(self.runtimes_label, self.runtimes_label.cget("font"))
        self.default_font.config(underline=1)
        self.estimated_time_label = tk.Label(self.frame_left, text="预估一次时间: ", bg=self.theme_color)
        self.estimated_time_label.config(font=self.default_font)
        self.estimated_time_label.grid(row=10, column=0, sticky='w', padx=5, pady=10)
        image_path = get_path("assets/Estimated_time.png")
        self.original_image = Image.open(image_path)
        self.estimated_label_hover_window = None
        self.estimated_label_is_clicked = False
        self.estimated_time_label.bind("<Enter>", self.estimated_label_on_enter)
        self.estimated_time_label.bind("<Leave>", self.estimated_label_on_leave)
        self.estimated_time_label.bind("<Button-1>", self.estimated_label_on_click)
        self.estimated_time_entry = tk.Entry(self.frame_left, textvariable=self.estimated_time_var, bg=lighten_hex_color(self.theme_color), highlightcolor="black", highlightthickness=0.5)
        self.estimated_time_entry.grid(row=10, column=1, columnspan=2, sticky='ew', padx=5, pady=10)
        self.estimated_time_entry.bind("<FocusIn>", self.on_estimated_time_focus_in)  
        self.estimated_time_entry.bind("<FocusOut>", self.on_estimated_time_focus_out)
        self.estimated_time_entry.bind("<Return>", self.handle_enter)
        
        self.all_radio_buttons = self.browser_radio_buttons + self.test_item_radio_buttons
        self.labels = [self.browser_type_label, self.driver_path_label, self.test_item_label, self.username_label, self.password_label, self.runtimes_label, self.estimated_time_label]
        self.entries = [self.username_entry, self.password_entry, self.runtimes_entry, self.estimated_time_entry]
        self.entries_var = [self.username_var, self.password_var, self.runtimes_var, self.estimated_time_var]
        
        self.button_confirm = HoverButton(self.frame_left, self.all_input_ready_event, text="confirm", color=self.theme_color, command=self.handle_confirm_button, cursor="hand2")
        self.button_confirm.grid(row=11, column=1, sticky='w', padx=20, pady=20)
        self.button_cancel = HoverButton(self.frame_left, text="cancel", color=self.theme_color, command=self.handle_cancel_button, cursor="hand2")
        self.button_cancel.grid(row=11, column=1, sticky='e', padx=300, pady=20)
        self.button_cancel.bind("<Tab>", self.handle_enter)

        self.text_area = ScrolledText(self.frame_right, wrap=tk.WORD, state=tk.DISABLED, bg=lighten_hex_color(self.theme_color), fg='black', font=("Courier", 10))
        self.text_area.grid(sticky='nsew', padx=10, pady=10)
        self.text_area.tag_configure("GREEN", foreground="green")
        self.text_area.tag_configure("RED", foreground="red")
        self.text_area.tag_configure("CYAN", foreground="cyan")
        self.text_area.tag_configure("YELLOW", foreground="yellow")
        self.text_area.tag_configure("BOLD", font=("Helvetica", 10, "bold"), foreground="green")
        sys.stdout = RedirectedIO(self.text_area)
        sys.stderr = RedirectedIO(self.text_area)

    # 主root窗户鼠标按下不松口更改样式
    def root_on_mouse_press(self, event):
        # 执行预估时间的图片标签处理
        self.on_root_click(event)
        if ((event.widget not in self.entries) and 
            (event.widget != self.driver_path_entry) and 
            (event.widget != self.text_area) and
            (event.widget != self.estimated_time_label) and
            (event.widget != self.button_confirm) and
            (event.widget != self.button_cancel) and
            (event.widget != self.password_is_show_eye) and
            (event.widget != self.runtimes_left_spinbox) and
            (event.widget != self.runtimes_right_spinbox)):
            self.root.focus_set()
            # 鼠标按下时，更改鼠标样式并记录初始位置
            self.root.config(cursor=self.dragging_cursor)
            self.dragging = True
            self.init_x, self.init_y = event.x, event.y
            self.init_window_x, self.init_window_y = self.root.winfo_x(), self.root.winfo_y()

    # 主root窗户鼠标按下拖动窗口移动窗口位置
    def root_on_mouse_drag(self, event):
        # 鼠标拖动时，更新窗口位置
        if self.dragging:
            delta_x = event.x - self.init_x
            delta_y = event.y - self.init_y
            self.root.geometry(f"+{self.init_window_x + delta_x}+{self.init_window_y + delta_y}")
 
    # 主root窗户鼠标按下释放恢复样式
    def root_on_mouse_release(self, event):
        # 鼠标释放时，恢复默认的鼠标样式
        self.root.config(cursor=self.default_cursor)
        self.dragging = False

    # 主root窗口位置或者大小变化时也执行root点击函数
    def root_on_configure(self, event):
        new_width, new_height = self.root.winfo_width(), self.root.winfo_height()
        new_x, new_y = self.root.winfo_x(), self.root.winfo_y()
        if ((new_width != self.prev_width) 
            or (new_height != self.prev_height)
            or (new_x != self.prev_x)
            or (new_y != self.prev_y)):
            self.prev_width = new_width
            self.prev_height = new_height
            self.prev_x = new_x
            self.prev_y = new_y
            self.on_root_click(event)
   
    # 屏幕点击事件, 处理预估时间的弹出窗口的销毁
    def on_root_click(self, event):
        # 检查是否应该忽略这个点击事件
        if self.estimated_label_ignore_root_click:
            self.estimated_label_ignore_root_click = False  # 重置标志
            return
        # 如果不应该忽略，则设置屏幕已点击状态变量为True
        else:
            if self.estimated_label_hover_window is not None:
                self.estimated_label_hover_window.destroy()
                self.estimated_label_hover_window = None  
                self.estimated_label_ignore_root_click = True
                self.estimated_label_is_clicked = not self.estimated_label_is_clicked
                
    # 主程序关闭释放资源和恢复变量值
    def on_closing(self, event=None):
        if messagebox.askokcancel("Quit", "APP is closing...Do you want to quit?"):
            # 正在下载driver的提示变量恢复默认值
            if self.is_installing_driver:
                self.is_installing_driver = False
            # 将用以替换python的input函数的输入窗口关闭
            if self.input_popup is not None and self.input_popup.winfo_exists():
                self.input_popup.destroy()
            self.window_closed = True
            self.root.quit()
            self.root.destroy()

    # 打印有颜色的文本输出到textarea中
    def print_colored(self, text, tag=None, i=999):
        # 直接打印文本
        if i == 999:
            sys.stdout.write(text, tag)
            self.save_log_content += text
            return text
        # 特定文本（输入框的信息）处理一下再打印
        else:
            self.all_entries_information_update()
            self.user_input_display = self.entries_vars_current_value[i]
            if i == 0 or i == 4:
                text = text + str(self.user_input_display) + "\n"
            elif i == 2:
                text = text + '*' * len(self.user_input_display) + "\n"
            else:
                text = text + self.user_input_display + "\n"
            self.save_log_content += text
            sys.stdout.write(text, tag)
            return self.user_input_display

    # 调整图片
    def resize_image(self, path, image_factor=0.5):
        image = Image.open(path)
        image = image.resize(
            (int(image.width * image_factor), 
             int(image.height * image_factor)),
             Image.LANCZOS
        ) # 调整图片大小以适应窗口
        return ImageTk.PhotoImage(image)
    
    # UI菜单
    def create_menus(self):  
        # 创建菜单栏  
        menu_bar = tk.Menu(self.root) 
        self.root.config(menu=menu_bar)  
     
        # 创建文件的下拉菜单对象，tearoff=0表示不自动分离菜单
        file_menu = tk.Menu(menu_bar, tearoff=0)  
        # 创建文件相关的菜单项
        menu_bar.add_cascade(label="File", menu=file_menu)  
        # 文件菜单选项：使用默认驱动
        file_menu.add_command(label="Use default driver", command=self.use_default_driver)
        driver_menu = tk.Menu(file_menu, tearoff=0) 
        # 文件菜单选项：获取新的驱动
        file_menu.add_cascade(label="Get new driver", menu=driver_menu)
        # 文件菜单选项：获取新的驱动 -> 打开自己下载的驱动
        driver_menu.add_command(label="Open", command=self.get_driver_from_folder)
        # 分割线
        driver_menu.add_separator()
        # 文件菜单选项：获取新的驱动 -> 自动下载最新的驱动
        driver_menu.add_command(label="Install", command=self.start_driver_installation_Prepare)
        # 文件菜单选项：保存显示的信息
        file_menu.add_command(label="Save log", command=self.save_log)
        # 文件菜单选项：程序关闭
        file_menu.add_command(label="Exit", command=self.on_closing)

        # 创建测试功能相关菜单项
        self.options_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Options", menu=self.options_menu) 
        self.options_menu.add_command(label="Enable VF",command=self.add_run_if_successful_verification_function)
        
        # 创建视觉效果主题相关菜单项
        view_menu = tk.Menu(menu_bar, tearoff=0) 
        menu_bar.add_cascade(label="View", menu=view_menu) 
        view_menu.add_command(label="Default theme", command=self.restore_theme_color)
        view_menu.add_command(label="Change theme", command=self.change_theme_color)
        
        # 创建帮助菜单项
        help_menu = tk.Menu(menu_bar, tearoff=0)  
        menu_bar.add_cascade(label="Help", menu=help_menu) 
        help_menu.add_command(label="Usage introduction", command=self.get_Usage_introduction) 
        help_menu.add_command(label="About", command=self.get_About)  

    # 可以在菜单中选择使用默认的驱动
    def use_default_driver(self):
        if self.all_input_ready_event.is_set():
            self.print_colored("您已锁定测试选项,请先单击“cancel”,然后选择\n")
            return
        if self.is_installing_driver:
            self.show_driver_download_info()
        else:
            self.select_browser_radio()
            # 启用浏览器选择按钮
            for rb in self.browser_radio_buttons:
                rb.config(state=tk.NORMAL)
            self.browser_radio_is_enabled = True

    # 根据浏览器选择默认的驱动
    def select_browser_radio(self):
        selected_browser = self.browser_type_var.get()
        if selected_browser == 1:  # Edge
            get_edge_driver_path = get_path("assets/msedgedriver.exe")
            self.driver_path_var.set(f"Edge默认驱动:    {get_edge_driver_path}") 
            self.request_download_browser = "Edge"
        else: # Chrome
            get_Google_driver_path = get_path("assets/chromedriver.exe")
            self.driver_path_var.set(f"Google默认驱动:  {get_Google_driver_path}")
            self.request_download_browser = "Chrome"

    # 可以在菜单中选择使用用户自己已经安装的驱动
    def get_driver_from_folder(self): 
        if self.all_input_ready_event.is_set():
            self.print_colored("您已锁定测试选项,请先单击“cancel”,然后选择\n")
            return
        if self.is_installing_driver:
            self.show_driver_download_info()
        else:
            # 打开已经下载好的Edge驱动  
            driver_file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])  
            if driver_file_path:  
                self.driver_path_var.set(driver_file_path)
                if "chrome" in driver_file_path.split("\\")[-1].lower():
                    self.browser_type_var.set(2) 
                    self.request_download_browser = "Chrome"
                else:
                    self.browser_type_var.set(1)
                    self.request_download_browser = "Edge"
                for rb in self.browser_radio_buttons:
                    rb.config(state=tk.DISABLED)
                self.browser_radio_is_enabled = False

    # 可以在菜单中选择下载驱动，则准备开始下载前的工作
    def start_driver_installation_Prepare(self):
        if self.all_input_ready_event.is_set():
            self.print_colored("您已锁定测试选项,请先单击“cancel”,然后选择\n")
            return
        # 如果正在下载的线程没有结束，则提示正在下载，不重复执行下载任务
        if self.is_installing_driver:
            self.show_driver_download_info()
            return
        # 显示下载状态，防止在下载过程中操作错误
        self.is_installing_driver = True
        # 禁用浏览器选择按钮（如果它们之前没有被禁用的话）
        for rb in self.browser_radio_buttons:
            rb.config(state=tk.DISABLED)
        # 禁用浏览器使用tab
        self.browser_radio_is_enabled = False
        # 在主线程中请求用户是否指定驱动版本
        self.driver_version = simpledialog.askstring("Driver Version", "指定一个版本或者直接点击按钮下载最新版本:")
        self.start_driver_installation_threading()

    # 开启下载driver子线程任务
    def start_driver_installation_threading(self):
        # 创建一个守护线程来安装驱动
        thread = threading.Thread(target=self.get_driver_automatically, daemon=True)
        thread.start()

    # 执行下载driver子线程
    def get_driver_automatically(self): 
        # 自动下载Edge驱动  
        try:  
            selected_browser = self.browser_type_var.get()
            if selected_browser == 1:  # Edge
                self.request_download_browser = "Edge"
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                if self.driver_version:
                    driver_path = EdgeChromiumDriverManager(version=self.driver_version).install() 
                else:
                    driver_path = EdgeChromiumDriverManager().install()    
            else:   #Chrome
                self.request_download_browser = "Chrome"
                from webdriver_manager.chrome import ChromeDriverManager
                if self.driver_version:
                    driver_path = ChromeDriverManager(version=self.driver_version).install()
                else:
                    driver_path = ChromeDriverManager().install()
            # 由于Tkinter不是线程安全的，我们需要确保更新UI的操作在主线程中执行
            self.root.after(0, self.show_success_message, driver_path)
        except Exception as e:  
            self.root.after(0, self.show_error_message, str(e))
            self.select_browser_radio()
            # 启用浏览器选择按钮
            for rb in self.browser_radio_buttons:
                rb.config(state=tk.NORMAL)
            self.browser_radio_is_enabled = True
        finally:
            self.is_installing_driver = False

    # 展示下载成功信息，并设置driver组件的显示情况
    def show_success_message(self, driver_path):
        if self.driver_info_dialog is not None and self.driver_info_dialog.winfo_exists():
            self.driver_info_dialog.destroy()
        if self.error_window is not None and self.error_window.winfo_exists():
            self.error_window.destroy()
        messagebox.showinfo("Driver Info - Installation Status(success)", f"Driver installed successfully!\nPath: {driver_path}")
        self.driver_path_var.set(driver_path) 
        if "chrome" in self.driver_path_var.get().split("\\")[-1].lower():
            self.browser_type_var.set(2) 
        else:
            self.browser_type_var.set(1)
 
    # 展示下载出错信息，提示下载链接
    def show_error_message(self, error_message):
        if self.driver_info_dialog is not None and self.driver_info_dialog.winfo_exists():
            self.driver_info_dialog.destroy()

        if self.error_window is not None and self.error_window.winfo_exists():
            self.error_window.destroy()

        self.error_window = tk.Toplevel(self.root, bg=self.theme_color)
        self.error_window.iconphoto(False, self.cry_emoji_photo)
        self.error_window.title("Driver Info - Installation Status(Error)")
        self.error_window.resizable(False, False)
        
        self.first_frame_error_prompt = tk.Frame(self.error_window, bg=self.theme_color)
        self.first_frame_error_prompt.pack(pady=10)
        self.errot_plug_photo_label = tk.Label(self.first_frame_error_prompt, image=self.errot_plug_photo, bg=self.theme_color)
        self.errot_plug_photo_label.image = self.errot_plug_photo
        self.errot_plug_photo_label.pack(side="left")
        if self.driver_version:
            error_text = "Failed to install driver(网络错误或驱动版本格式不对,请检查重试或自行下载后执行File->Get new driver->Open):"
        else:
            error_text = "Failed to install driver(网络错误或权限不足,请检查重试或自行下载后执行File->Get new driver->Open):"
        self.error_info_label = tk.Label(self.first_frame_error_prompt, text=error_text, font=font.Font(weight='bold'), bg=self.theme_color)
        self.error_info_label.pack(side="top", padx=5)
        self.error_text_widget = tk.Text(self.first_frame_error_prompt, wrap="word", height=3, fg="red", font=("Arial", 10), bg=self.theme_color)
        self.error_text_widget.pack(side="left", fill="both", expand=True, padx=5)
        # 插入错误信息并禁用编辑
        self.error_text_widget.insert("1.0", error_message)
        self.error_text_widget.config(state="disabled")
        # 添加滚动条
        self.error_scroll_bar = tk.Scrollbar(self.first_frame_error_prompt, command=self.error_text_widget.yview)
        self.error_scroll_bar.pack(side="right", fill="y")
        self.error_text_widget.config(yscrollcommand=self.error_scroll_bar.set)

        self.second_frame_download_driver = tk.Frame(self.error_window, bg=self.theme_color)
        self.second_frame_download_driver.pack(pady=10)
        if self.browser_type_var.get() == 1:
            self.edgedriver_download_label = tk.Label(self.second_frame_download_driver, text="Download the Edge WebDriver from: >>>", font=font.Font(weight='bold'), justify='left', bg=self.theme_color)
            self.edgedriver_download_label.pack(side="left", padx=5)
            self.edgedriver_download_link_label = tk.Label(self.second_frame_download_driver, 
                                                    text="https://developer.microsoft.com/zh-cn/microsoft-edge/tools/webdriver/", 
                                                    fg="blue", cursor="hand2", font=font.Font(size=14), bg=self.theme_color)
            self.edgedriver_download_link_label.pack(side="left")
            self.edgedriver_download_link_label.bind("<Button-1>", lambda e: webbrowser.open("https://developer.microsoft.com/zh-cn/microsoft-edge/tools/webdriver/"))
        else:
            self.googledriver_download_label = tk.Label(self.second_frame_download_driver, text="Download the Chrome WebDriver from: >>>", font=font.Font(weight='bold'), justify='left', bg=self.theme_color)
            self.googledriver_download_label.pack(side="left", padx=5)
            self.googledriver_download_link1_label = tk.Label(self.second_frame_download_driver, 
                                                    text="谷歌官网 https://chromedriver.storage.googleapis.com/index.html", 
                                                    fg="blue", cursor="hand2", font=font.Font(size=14), bg=self.theme_color)
            self.googledriver_download_link1_label.pack(pady=2)
            self.googledriver_download_link1_label.bind("<Button-1>", lambda e: webbrowser.open("https://chromedriver.storage.googleapis.com/index.html"))
            self.googledriver_download_link2_label = tk.Label(self.second_frame_download_driver, 
                                                    text="最新版本 https://googlechromelabs.github.io/chrome-for-testing/", 
                                                    fg="blue", cursor="hand2", font=font.Font(size=14), bg=self.theme_color)
            self.googledriver_download_link2_label.pack(pady=2)
            self.googledriver_download_link2_label.bind("<Button-1>", lambda e: webbrowser.open("https://googlechromelabs.github.io/chrome-for-testing/"))
            self.googledriver_download_link3_label = tk.Label(self.second_frame_download_driver, 
                                                    text="阿里镜像站 https://registry.npmmirror.com/binary.html?path=chromedriver/", 
                                                    fg="blue", cursor="hand2", font=font.Font(size=14), bg=self.theme_color)
            self.googledriver_download_link3_label.pack(pady=2)
            self.googledriver_download_link3_label.bind("<Button-1>", lambda e: webbrowser.open("https://registry.npmmirror.com/binary.html?path=chromedriver/"))

        self.third_frame_download_image = tk.Frame(self.error_window, bg=self.theme_color)
        self.third_frame_download_image.pack(pady=10)
        try:
            if self.browser_type_var.get() == 1:
                edgedriver_image_path = get_path("assets/edge_driver_install_tutorial.png")  # 替换为您的图片路径
            else:
                edgedriver_image_path = get_path("assets/chrome_driver_install_tutorial.png")  # 替换为您的图片路径
            edgedriver_photo = self.resize_image(edgedriver_image_path, 0.7)
            self.download_image_label = tk.Label(self.third_frame_download_image, image=edgedriver_photo, bg=self.theme_color)
            self.download_image_label.image = edgedriver_photo  # 保持对图片的引用，防止被垃圾回收
            self.download_image_label.pack()
        except Exception as img_error:
            self.print_colored(f"Failed to load image: {img_error}\n")
    
    # 展示正在下载驱动的提示
    def show_driver_download_info(self):
        if self.driver_info_dialog is not None and self.driver_info_dialog.winfo_exists():
            self.driver_info_dialog.focus_set()
            return
        else:
            self.driver_info_dialog = tk.Toplevel(self.root, bg=self.theme_color)
            self.driver_info_dialog.iconphoto(False, self.toplevel_icon_photo)
            self.driver_info_dialog.title("Driver Info - Installation Status(ongoing)")
            self.driver_info_dialog.resizable(False, False)

            # 显示文本信息
            text1 = f"The {self.request_download_browser} driver you requested is being downloaded automatically. Please wait~"
            text2 = f"The driver you are currently using is:    {self.driver_path_var.get()}"
            text3 = "After the driver download is completed, you will be prompted as follows:"
            text4 = "(Similarly, if the download fails, there will also be a prompt.)"
            self.driver_info_dialog_text1_label = tk.Label(self.driver_info_dialog, text=text1, bg=self.theme_color)
            self.driver_info_dialog_text1_label.pack(pady=5)
            self.driver_info_dialog_text2_label = tk.Label(self.driver_info_dialog, text=text2, bg=self.theme_color)
            self.driver_info_dialog_text2_label.pack(pady=5)
            self.driver_info_dialog_text3_label = tk.Label(self.driver_info_dialog, text=text3, bg=self.theme_color)
            self.driver_info_dialog_text3_label.pack(pady=5)
            self.driver_info_dialog_text4_label = tk.Label(self.driver_info_dialog, text=text4, bg=self.theme_color)
            self.driver_info_dialog_text4_label.pack(pady=5)

            driver_installing_photo = self.resize_image(get_path("assets/driver_install_success.png"), 0.7)
            self.driver_info_dialog_img_label = tk.Label(self.driver_info_dialog, image=driver_installing_photo, bg=self.theme_color)
            self.driver_info_dialog_img_label.image = driver_installing_photo  # 保持对图片的引用，防止被垃圾回收
            self.driver_info_dialog_img_label.pack()

    # 返回当前浏览器的驱动路径。若文件不存在，抛出异常提示
    def get_clean_driver_path(self):
        # 获取清理前的路径
        raw_path = self.driver_path_var.get()
        # 去除前缀信息和多余空格
        if "Edge默认驱动:" in raw_path:
            raw_path = raw_path.replace("Edge默认驱动:", "").strip()
        elif "Google默认驱动:" in raw_path:
            raw_path = raw_path.replace("Google默认驱动:", "").strip()
        if not os.path.exists(raw_path):
            self.driver_is_good = False
            raise FileNotFoundError(f"\nDriver not found at path: {raw_path}")
        self.driver_is_good = True
        return raw_path

    # 保存日志
    def save_log(self):
        log_file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=[("Text files", "*.txt")],
            initialdir=os.getcwd(),
            initialfile="Genoa_xGMI_auto_log")
        if log_file_path:
            try:
                with open(log_file_path, 'w', encoding="utf-8") as log_file:
                    creation_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                    log_file.write(f"This log file created at: {creation_time}\n\n {self.save_log_content}")
                    self.print_colored(f"Log file saved successfully to: {log_file_path}\n") 
                    self.print_colored("\n")
            except Exception as e:
                self.print_colored(f"Failed to save log: {e}\n", "RED") 
                self.print_colored("\n")   
        else:
            self.print_colored("Save log cancelled.\n", "YELLOW")  

    # 是否添加验证成功运行脚本的功能
    def add_run_if_successful_verification_function(self):
        if self.all_input_ready_event.is_set():
            self.print_colored("已锁定,测试运行中,请先单击“cancel”,然后选择\n", "YELLOW")
            return
        
        # 切换状态
        self.is_enabled_val_if_run_successfully = not self.is_enabled_val_if_run_successfully
        
        # 删除原标签后添加新的验证功能菜单项标签
        if self.is_enabled_val_if_run_successfully:
            self.print_colored("Enabled VF\n")
            for index in range(self.options_menu.index("end") + 1):
                if self.options_menu.entrycget(index, "label") == "Enable VF":
                    self.options_menu.delete(index)
                    break
            new_label = "Enable VF      ✔"
            # 创建或打开已有的窗口上传图片
            if not self.verification_window:
                self.upload_template_image()
        else:
            if self.verification_window and not self.verification_window.winfo_viewable():
                self.verification_window.deiconify()
            
            if messagebox.askokcancel("Note", f"Are you sure you want to cancel VF?"):    
                for index in range(self.options_menu.index("end") + 1):
                    if self.options_menu.entrycget(index, "label") == "Enable VF      ✔":
                        self.options_menu.delete(index)
                        break
                new_label = "Enable VF"
                if self.verification_window is not None and self.verification_window.winfo_exists():
                    self.verification_window.destroy()
                    self.verification_window = None
                self.print_colored("Canceled VF\n")
            else:
                self.is_enabled_val_if_run_successfully = not self.is_enabled_val_if_run_successfully
                for index in range(self.options_menu.index("end") + 1):
                    if self.options_menu.entrycget(index, "label") == "Enable VF      ✔":
                        self.options_menu.delete(index)
                        break
                new_label = "Enable VF      ✔"
                self.verification_window.focus_set()

        self.options_menu.add_command(label=new_label, command=self.add_run_if_successful_verification_function)

    # 如是启动验证功能就上传模板图片
    def upload_template_image(self):
        # 加载默认背景图和上传按钮图
        example_image_path = get_path("assets/template.jpeg")
        upload_icon_path = get_path("assets/upload_img.png")
        default_background_image_path = get_path("assets/Background_image.jpg") 
        
        self.verification_window = tk.Toplevel(self.root, bg=self.theme_color)
        self.verification_window.iconphoto(False, self.toplevel_icon_photo)
        self.verification_window.focus_set()
        self.verification_window.title("Verification Function")
        self.verification_window.resizable(False, False)
        self.verification_window.protocol("WM_DELETE_WINDOW", lambda: self.verification_window.withdraw())
        self.verification_window.bind("<Escape>", lambda event: self.verification_window.withdraw())

        # 显示提示文本1
        self.verification_window_text1_label = tk.Label(self.verification_window, 
                                                        text="Enabled the verification function to verify whether the xGMI test script runs successfully. \nPlease provide a template image(Right) based on the example image(Left).", 
                                                        justify=tk.LEFT, 
                                                        font=font.Font(size=12),
                                                        bg=self.theme_color)
        self.verification_window_text1_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)
        
        # 显示提示文本2和确认按钮
        self.verification_window_ok_button_frame = tk.Frame(self.verification_window, bg=self.theme_color)
        self.verification_window_ok_button_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        # 为了使框架内的grid布局生效，我们需要配置行和列的权重
        for i in range(2):  # 只配置两行
            self.verification_window_ok_button_frame.grid_rowconfigure(i, weight=1)
            self.verification_window_ok_button_frame.grid_columnconfigure(i, weight=1)
        self.verification_window_text2_label = tk.Label(self.verification_window_ok_button_frame, 
                                                        text="(If do not upload image and insist on using the VF function, the default image(Left) will be used)",  
                                                        bg=self.theme_color)
        self.verification_window_text2_label.grid(row=0, column=0, sticky="nsew", padx=100, pady=5)
        self.verification_window_ok_button =  tk.Button(self.verification_window_ok_button_frame, 
                                                        text="Ok", 
                                                        cursor="heart", 
                                                        bg=lighten_hex_color(self.theme_color), 
                                                        width=10)
        self.verification_window_ok_button.grid(row=0, column=1, sticky="e", padx=50)
        self.verification_window_ok_button.bind("<Button-1>", lambda event: self.verification_window.withdraw())

        # 显示提示模板图片（默认模板图片）
        verification_window_example_photo = self.resize_image(example_image_path, 0.8)
        self.verification_window_example_label = tk.Label(self.verification_window, 
                                                            image=verification_window_example_photo, 
                                                            bg=self.theme_color)
        self.verification_window_example_label.image = verification_window_example_photo  # 保持对图像的引用，防止被垃圾回收
        self.verification_window_example_label.grid(row=2, column=0, padx=20, pady=20)

        # 创建上传按钮的框架
        self.verification_window_upload_button_frame = tk.Frame(self.verification_window, bg=self.theme_color)
        self.verification_window_upload_button_frame.grid(row=2, column=1, padx=20, pady=20)

        # 用于显示上传的图像或默认背景图（初始时显示背景图）
        self.verification_window_uploaded_image_label = tk.Label(self.verification_window_upload_button_frame, bg=self.theme_color)
        self.verification_window_uploaded_image_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.verification_window_default_background_image = Image.open(default_background_image_path)
        self.verification_window_default_background_image = self.verification_window_default_background_image.resize(
            (verification_window_example_photo.width(), 
            verification_window_example_photo.height()),
            Image.LANCZOS
        ) # 调整图片大小以适应窗口
        self.verification_window_default_background_image = ImageTk.PhotoImage(self.verification_window_default_background_image)
        self.verification_window_uploaded_image_label.config(image=self.verification_window_default_background_image)
        self.verification_window_uploaded_image_label.image = self.verification_window_default_background_image  # 保持对图像的引用

        # 加载上传按钮的图片文本组合
        verification_window_upload_icon_photo = self.resize_image(upload_icon_path, 0.05)
        self.verification_window_upload_icon_label = tk.Label(self.verification_window_upload_button_frame, image=verification_window_upload_icon_photo, cursor="hand2", bg=self.theme_color)
        self.verification_window_upload_icon_label.image = verification_window_upload_icon_photo  # 保持对图像的引用
        self.verification_window_upload_icon_label.grid(row=0, column=0, padx=5, pady=20, sticky="e")
        self.verification_window_upload_text_label = tk.Label(self.verification_window_upload_button_frame, text="Upload template image here", cursor="hand2", bg=self.theme_color)
        self.verification_window_upload_text_label.grid(row=0, column=1, padx=5, pady=20, sticky="w")

        # 上传图片后要显示的按钮（用来恢复默认或者重新上传）
        self.verification_window_use_defalt_image_button = tk.Button(self.verification_window, text="Use default", cursor="hand2", bg=lighten_hex_color(self.theme_color))
        self.verification_window_use_defalt_image_button.grid_remove()
        self.verification_window_reload_image_button = tk.Button(self.verification_window, text="Re-upload", cursor="hand2", bg=lighten_hex_color(self.theme_color))
        self.verification_window_reload_image_button.grid_remove()
        self.verification_window_uploaded_image = None
        self.vf_upload_image_pre_file_path = ""
              
        def default_VF_button_click(event=None):
            self.verification_window_use_defalt_image_button.unbind("<Button-1>")
            self.verification_window_reload_image_button.unbind("<Button-1>")
            self.verification_window_use_defalt_image_button.grid_remove()
            self.verification_window_reload_image_button.grid_remove()

            self.verification_window_uploaded_image_label.config(image=self.verification_window_default_background_image)
            self.verification_window_uploaded_image_label.image = self.verification_window_default_background_image  # 保持对图像的引用
            
            self.verification_window_upload_icon_label.grid()
            self.verification_window_upload_text_label.grid()

            self.vf_upload_image_file_path = example_image_path

        def reload_VF_image_thread(event=None):
            # 禁用按钮以防止在文件选择期间重复点击
            self.verification_window_use_defalt_image_button.unbind("<Button-1>")
            self.verification_window_reload_image_button.unbind("<Button-1>")
            # 为防止选择文件时主GUI冻结无法更新按钮的状态而使用的线程
            threading.Thread(target=reload_VF_button_select_file, daemon=True).start()

        def reload_VF_button_select_file():
            self.vf_upload_image_file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
            self.root.after(0, reload_VF_button_click)

        def reload_VF_button_click():
            if self.vf_upload_image_file_path:
                self.vf_upload_image_pre_file_path = self.vf_upload_image_file_path
                self.verification_window_uploaded_image = Image.open(self.vf_upload_image_file_path)
                self.verification_window_uploaded_image = self.verification_window_uploaded_image.resize(
                    (verification_window_example_photo.width(), 
                     verification_window_example_photo.height()),
                     Image.LANCZOS
                ) # 调整图片大小以适应窗口
                self.verification_window_uploaded_image = ImageTk.PhotoImage(self.verification_window_uploaded_image)
                self.verification_window_uploaded_image_label.config(image=self.verification_window_uploaded_image)
                self.verification_window_uploaded_image_label.image = self.verification_window_uploaded_image  # 保持对图像的引用
            else:
                self.vf_upload_image_file_path = self.vf_upload_image_pre_file_path
            if self.verification_window is not None and self.verification_window.winfo_exists():
                self.verification_window.focus_set()
            self.verification_window_use_defalt_image_button.bind("<Button-1>", default_VF_button_click)
            self.verification_window_reload_image_button.bind("<Button-1>", reload_VF_image_thread)

        def on_upload_button_frame_click(event=None):
            self.verification_window_upload_icon_label.unbind("<Button-1>")
            self.verification_window_upload_text_label.unbind("<Button-1>")
            self.vf_upload_image_file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
            if self.vf_upload_image_file_path:
                self.vf_upload_image_pre_file_path = self.vf_upload_image_file_path
                # 隐藏或移除上传按钮框架
                self.verification_window_upload_icon_label.grid_remove()
                self.verification_window_upload_text_label.grid_remove()
                # 显示用来恢复默认或者重新上传的两个按钮
                self.verification_window_use_defalt_image_button.grid(row=3, column=0, padx=50, pady=20, sticky="e")
                self.verification_window_reload_image_button.grid(row=3, column=1, padx=50, pady=20, sticky="w")
                self.verification_window_use_defalt_image_button.bind("<Button-1>", default_VF_button_click)
                self.verification_window_reload_image_button.bind("<Button-1>", reload_VF_image_thread)

                # 显示上传的图片（覆盖背景图）
                self.verification_window_uploaded_image = Image.open(self.vf_upload_image_file_path)
                self.verification_window_uploaded_image = self.verification_window_uploaded_image.resize(
                    (verification_window_example_photo.width(), 
                     verification_window_example_photo.height()),
                     Image.LANCZOS
                ) # 调整图片大小以适应窗口
                self.verification_window_uploaded_image = ImageTk.PhotoImage(self.verification_window_uploaded_image)
                self.verification_window_uploaded_image_label.config(image=self.verification_window_uploaded_image)
                self.verification_window_uploaded_image_label.image = self.verification_window_uploaded_image  # 保持对图像的引用
            else:
                self.vf_upload_image_file_path = example_image_path
            if self.verification_window is not None and self.verification_window.winfo_exists():
                self.verification_window.focus_set()
            self.verification_window_upload_icon_label.bind("<Button-1>", on_upload_button_frame_click)
            self.verification_window_upload_text_label.bind("<Button-1>", on_upload_button_frame_click)

        # 绑定点击事件
        self.verification_window_upload_icon_label.bind("<Button-1>", on_upload_button_frame_click)
        self.verification_window_upload_text_label.bind("<Button-1>", on_upload_button_frame_click)
    
    # 主题颜色应用到控件上
    def configure_all_widget_colors(self):
        self.root.config(bg=self.theme_color)
        self.frame_left.config(bg=self.theme_color)
        self.frame_right.config(bg=self.theme_color)
        for rb in self.all_radio_buttons:
            rb.config(bg=self.theme_color)
        for label in self.labels:
            label.config(bg=self.theme_color) 
        self.driver_path_entry.config(bg=lighten_hex_color(self.theme_color))    
        for entry in enumerate(self.entries, start=1):
            entry[1].config(bg=lighten_hex_color(self.theme_color))
        self.text_area.config(bg=lighten_hex_color(self.theme_color))
        self.button_confirm.config(background=self.theme_color)
        self.button_cancel.config(background=self.theme_color)
        self.button_confirm.update_color(self.theme_color)
        self.button_cancel.update_color(self.theme_color)
        self.password_is_show_eye.config(background=lighten_hex_color(self.theme_color))
        self.runtimes_left_spinbox.update_color(self.theme_color)
        self.runtimes_right_spinbox.update_color(self.theme_color)
        if self.estimated_label_hover_window is not None and self.estimated_label_hover_window.winfo_exists():
            self.estimated_label_hover_window.config(bg=self.theme_color)
            self.estimated_image_label.config(bg=self.theme_color)
        if self.error_window is not None and self.error_window.winfo_exists():
            self.error_window.config(bg=self.theme_color)
            self.first_frame_error_prompt.config(bg=self.theme_color)
            self.second_frame_download_driver.config(bg=self.theme_color)
            self.third_frame_download_image.config(bg=self.theme_color)
            self.error_info_label.config(bg=self.theme_color)
            self.error_text_widget.config(bg=self.theme_color)
            if self.browser_type_var.get() == 1:
                self.edgedriver_download_label.config(bg=self.theme_color)
                self.edgedriver_download_link_label.config(bg=self.theme_color)
            else:
                self.googledriver_download_label.config(bg=self.theme_color)
                self.googledriver_download_link1_label.config(bg=self.theme_color)
                self.googledriver_download_link2_label.config(bg=self.theme_color)
                self.googledriver_download_link3_label.config(bg=self.theme_color)
            self.download_image_label.config(bg=self.theme_color)
        if self.driver_info_dialog is not None and self.driver_info_dialog.winfo_exists():
            self.driver_info_dialog.config(bg=self.theme_color)
            self.driver_info_dialog_text1_label.config(bg=self.theme_color)
            self.driver_info_dialog_text2_label.config(bg=self.theme_color)
            self.driver_info_dialog_text3_label.config(bg=self.theme_color)
            self.driver_info_dialog_text4_label.config(bg=self.theme_color)
            self.driver_info_dialog_img_label.config(bg=self.theme_color)
        if self.verification_window is not None and self.verification_window.winfo_exists():
            self.verification_window.config(bg=self.theme_color)
            self.verification_window_example_label.config(bg=self.theme_color)
            self.verification_window_text1_label.config(bg=self.theme_color)
            self.verification_window_ok_button_frame.config(bg=self.theme_color)
            self.verification_window_text2_label.config(bg=self.theme_color)
            self.verification_window_ok_button.config(bg=lighten_hex_color(self.theme_color))
            self.verification_window_upload_button_frame.config(bg=self.theme_color)
            self.verification_window_upload_icon_label.config(bg=self.theme_color)
            self.verification_window_upload_text_label.config(bg=self.theme_color)
            self.verification_window_uploaded_image_label.config(bg=self.theme_color)
            self.verification_window_use_defalt_image_button.config(bg=lighten_hex_color(self.theme_color))
            self.verification_window_reload_image_button.config(bg=lighten_hex_color(self.theme_color))
        if self.about_window is not None and self.about_window.winfo_exists():
            self.about_window.config(bg=self.theme_color)
            self.about_label_image.config(bg=self.theme_color)
            self.about_label_info1.config(bg=self.theme_color)
            self.about_label_link_url.config(bg=self.theme_color)
            self.about_label_info2.config(bg=self.theme_color)
        if self.input_popup is not None and self.input_popup.winfo_exists():
            self.input_popup.config(bg=self.theme_color)
            self.input_popup_text_label.config(bg=self.theme_color)
            self.input_popup_input_entry.config(bg=lighten_hex_color(self.theme_color))
            self.input_popup_submit_button.config(bg=lighten_hex_color(self.theme_color))

    # 恢复默认主题颜色
    def restore_theme_color(self):
        self.theme_color = "#F5F5F5"
        self.configure_all_widget_colors()

    # 改变主题颜色
    def change_theme_color(self):
        new_color = colorchooser.askcolor(title="Choose a color", parent=self.root, initialcolor=self.theme_color)
        if new_color[1]:  # 如果用户选择了颜色
            self.theme_color = new_color[1]
            self.configure_all_widget_colors()

    # 关于程序使用方法
    """
    （展示包括网线,开ihdt等硬件配置）
    """
    def get_Usage_introduction(self):
        a = 0

    # 关于程序声明
    def get_About(self):
        if self.about_window is not None and self.about_window.winfo_exists():
            self.about_window.focus_set()
            return
        else:
            self.about_window = tk.Toplevel(self.root, bg=self.theme_color)
            self.about_window.iconphoto(False, self.toplevel_icon_photo)
            self.about_window.title("About Application")
            self.about_window.resizable(False, False)

            # 加载并显示图片
            help_image_path = get_path("assets\Help.png")
            help_image = Image.open(help_image_path)
            help_image = help_image.resize((150, 150),Image.LANCZOS)  # 调整图片大小以适应窗口
            photo = ImageTk.PhotoImage(help_image)
            self.about_label_image = tk.Label(self.about_window, image=photo, bg=self.theme_color)
            self.about_label_image.image = photo  # 保持对图像的引用,防止垃圾回收
            self.about_label_image.grid(row=0, column=0, padx=10, pady=10)    

            # 可点击的链接标签
            def open_help_url(event=None):
                webbrowser.open("https://github.com/beggin-noob")

            def enter_help_url(event=None):
                event.widget.config(fg="blue")
            
            def leave_help_url(event=None):
                event.widget.config(fg="black")

            # 显示说明信息
            about_info_text = """
            This program is an automated tool designed to simplify and enhance the process of multiple unlocks required in AMD CPU related testing. It is built on a solid foundation, inspired by the framework and code principles of AMD Gopi software.
            This application is currently customized for Bytedance's web use, specifically for KVM operation of machines to automatically run test scripts. 
            By utilizing advanced programming techniques and user-friendly interfaces, it reduces the time and effort required for manual testing, eliminating the need to constantly stare at the machine while ensuring the accuracy and consistency of our test results.
            
            If you encounter any problems or have improvement suggestions, please contact me, but only for private testing purposes. 
            You can find my contact information and more detailed information on the project in the GitHub repository:"""
            self.about_label_info1 = tk.Label(self.about_window, text=about_info_text, wraplength=1000, justify=tk.LEFT, bg=self.theme_color)
            self.about_label_info1.grid(row=0, column=1, padx=10, sticky=tk.W+tk.E)

            self.about_label_link_url = tk.Label(self.about_window, text="https://github.com/beggin-noob", cursor="hand2", bg=self.theme_color)
            self.about_label_link_url.grid(row=1, column=1, padx=10, sticky=tk.W)
            self.about_label_link_url.bind("<Button-1>", open_help_url)
            self.about_label_link_url.bind("<Enter>", enter_help_url)
            self.about_label_link_url.bind("<Leave>", leave_help_url)
    
            self.about_label_info2 = tk.Label(self.about_window, text="       Thank you for using our application!", wraplength=1000, bg=self.theme_color)
            self.about_label_info2.grid(row=2, column=1, padx=10, sticky=tk.W)

    # 所有准备就绪的状态用线程事件设置
    def set_all_input_ready_event(self, value):
        self.all_input_ready_event.set() if value else self.all_input_ready_event.clear()

    # 开始准备的状态用线程事件设置
    def set_start_prepare_event(self, value):
        self.start_prepare_event.set() if value else self.start_prepare_event.clear()

    # 用户名和密码准备就绪的状态用线程事件设置
    def set_username_and_password_ready_event(self, value):
        self.username_and_password_ready_event.set() if value else self.username_and_password_ready_event.clear()
    
    # 运行次数准备就绪的状态用线程事件设置
    def set_runtimes_ready_event(self, value):
        self.runtimes_ready_event.set() if value else self.runtimes_ready_event.clear()
    
    # 预估时间准备就绪的状态用线程事件设置
    def set_estimated_time_ready_event(self, value):
        self.estimated_time_ready_event.set() if value else self.estimated_time_ready_event.clear()

    # 输入框的信息提炼
    def all_entries_information_update(self):
        for i, entry in enumerate(self.entries, start=1):
            if not entry.get():
                self.entries_var[i-1].set(self.entries_vars_default_value[i])
                self.root.focus_set()
            else:
                if i == 4 and "Default one estimated time for test" in entry.get():
                    self.entries_vars_current_value[i] = self.default_time
                    self.entries_var[i-1].set(self.default_time)
                elif i == 1 and entry.get() == "Please enter your NTID username(if leave blank or no change, use defult username)":
                    self.entries_vars_current_value[i] = self.entries_vars_default_value[i]
                    self.entries_var[i-1].set(self.entries_vars_default_value[i])
                    self.entries_vars_current_value[i+1] = self.entries_vars_default_value[i+1]
                    self.entries_var[i].set(self.entries_vars_default_value[i+1])
                    i = 3
                    self.root.focus_set()
                else:
                    self.entries_vars_current_value[i] = entry.get()

    #  所有状态锁定
    def click_confirm_button_to_setup(self):
        # 将所有的输入框锁定不可编辑
        self.driver_path_entry.unbind('<Tab>')
        for entry in enumerate(self.entries, start=1):
            entry[1].bind('<Key>', lambda event: 'break')
        self._is_key_bound = [True, True, True, True]
        self.runtimes_left_spinbox.disable_customspinbox()
        self.runtimes_right_spinbox.disable_customspinbox()
        # 将浏览器类型和测试项锁定
        for rb in self.all_radio_buttons:
            rb.config(state=tk.DISABLED)
        # 浏览器项锁定的时候不再可使用tab选择
        self.browser_radio_is_enabled = False
        # 测试项锁定的时候不再可使用tab选择
        self.test_item_radio_is_enabled = False
        
    # 所有资源和信息确认按钮，启动测试确认件
    def handle_confirm_button(self, event):
        for rb in self.all_radio_buttons:
            rb.config(state=tk.DISABLED)
        # 浏览器项锁定的时候不再可使用tab选择
        self.browser_radio_is_enabled = False # 这两句其实是在click_confirm_button_to_setup函数里执行了，但是为了防止程序不能及时锁定，在此直接执行
        # 提示正在下载驱动，还没有使用自动下载的驱动
        if self.is_installing_driver:
            self.show_driver_download_info()
         # 准备开始
        self.set_start_prepare_event(True)
        self.set_username_and_password_ready_event(True)
        self.set_runtimes_ready_event(True)
        self.set_estimated_time_ready_event(True)
        self.all_entries_information_update()

    # 所有状态恢复默认
    def click_cancel_button_to_restore(self):
        # 将所有的输入框恢复可编辑
        self.driver_path_entry.bind('<Tab>', self.handle_enter)
        for entry in enumerate(self.entries, start=1):
            entry[1].unbind('<Key>')
        self._is_key_bound = [False, False, False, False]
        self.runtimes_left_spinbox.enable_customspinbox()
        self.runtimes_right_spinbox.enable_customspinbox()
        # 浏览器类型和测试项可重新选择
        for rb in self.all_radio_buttons:
            rb.config(state=tk.NORMAL)
        # 浏览器项可使用tab选择的变量
        self.browser_radio_is_enabled = True
        # 测试项可使用tab选择的变量
        self.test_item_radio_is_enabled = True
        # 确认按钮恢复
        self.button_confirm.update_color(self.theme_color) 
        # 未准备开始
        self.set_start_prepare_event(False)
        # 所有准备未就绪
        self.set_username_and_password_ready_event(False)
        self.set_runtimes_ready_event(False)
        self.set_estimated_time_ready_event(False)
        self.set_all_input_ready_event(False)
        # 驱动是否可用的状态标志恢复默认
        self.driver_is_good = False
        # 驱动是否完全启动的状态标志恢复默认
        self.driver_fully_booted_is_ok = False
        
    # 所有资源和信息取消按钮，取消测试确认键
    def handle_cancel_button(self, event):
        if self.start_prepare_event.is_set() and not self.all_input_ready_event.is_set():
            self.click_cancel_button_to_restore() 
        if self.all_input_ready_event.is_set() and self.driver_is_good:
            if self.driver_fully_booted_is_ok:
                if messagebox.askokcancel("Note", f"Cancelling will close the currently running web.\n (If you have closed the browser yourself, you can ignore this message.)\n Are you sure you want to cancel?"):
                    self.print_colored("\nThe previous driver has been closed, Please click confirm to retest\n", "YELLOW")
                    self.print_colored("\n")
                    self.click_cancel_button_to_restore()
            else:
                messagebox.showinfo("Driver Info - Startup Status(ongoing)", f"The browser is starting up. Please try again later. \n"
                                    "After the startup is complete, you can see the words 'Successfully initialize of WebDriver' on the right.")
        else:
            self.click_cancel_button_to_restore()   

    # 焦点聚焦到root窗口时使用tab会聚焦到第一个浏览器radio，设置这时候的显示
    def root_re_focus_in_browser_type_radio(self, event=None):
        if self.browser_radio_is_enabled:
            self.browser_type_var.set(1)
            self.select_browser_radio()
    
    # 绑定radiobutton的tab键和所有输入框的tab/Enter键聚焦
    def handle_enter(self, event):
        # 如果选择了浏览器1则使用tab聚焦到浏览器2
        if event.widget == self.browser_radio_buttons[0]:
            if self.browser_radio_is_enabled:
                self.browser_type_var.set(2)
                self.select_browser_radio()
        # 如果选择了浏览器2则使用tab聚焦到浏览器输入框
        elif event.widget == self.browser_radio_buttons[1]: 
            self.driver_path_entry.focus_set()
        # 如果选择了浏览器输入框则使用tab聚焦到测试项第一项
        elif event.widget == self.driver_path_entry:
            if self.test_item_radio_is_enabled:
                self.test_item_var.set(1)
                self.update_estimated_time_entry()
            else:
                self.entries[0].focus_set()
        # 如果选择了取消按钮则使用tab聚焦到浏览器1
        elif event.widget == self.button_cancel:
            if self.browser_radio_is_enabled:
                self.browser_type_var.set(1)
                self.select_browser_radio()
        else:
            idx = self.entries.index(event.widget)
            if idx < len(self.entries) - 1:
                self.entries[idx + 1].focus_set()
            else:
                self.button_confirm.focus_set()

    # 设置radiobutton确认的状态
    def select_radio_ok(self, event=None):
        if event.widget in self.browser_radio_buttons:
            for rb in self.browser_radio_buttons:
                rb.config(state=tk.DISABLED)
            self.browser_radio_is_enabled = False
        if event.widget in self.test_item_radio_buttons:
            for rb in self.test_item_radio_buttons:
                rb.config(state=tk.DISABLED)
            self.test_item_radio_is_enabled = False

    def select_test_item_radio_tab(self, e):
        if self.test_item_radio_is_enabled:
            current_value = self.test_item_var.get()
            if current_value < len(self.test_items):
                next_value = current_value + 1 
            else:
                next_value = 5
            self.test_item_var.set(next_value)
            self.update_estimated_time_entry()

    def on_username_focus_in(self, event):  
        if self.username_var.get() and self.username_var.get()=='Please enter your NTID username(if leave blank or no change, use defult username)':
            if not self._is_key_bound[0]:
                self.username_var.set("")
      
    def on_username_focus_out(self, event):  
        if not self.username_var.get():  
            self.username_var.set("Please enter your NTID username(if leave blank or no change, use defult username)")
            self.entries_vars_current_value[1] = self.username_var.get()
            self.password_entry.config(fg="black", show="*")
            self.password_var.set("Please enter your NTID password(if leave blank or no change, use defult password)")
            self.entries_vars_current_value[2] = self.password_var.get()
        else:
            if self.password_var.get() == '请先输入账户名！':
                self.password_entry.config(fg="black", show="*")

    def on_password_focus_in(self, event):
        if self.username_var.get() and not self.username_var.get()=='Please enter your NTID username(if leave blank or no change, use defult username)':
            if self.password_var.get():
                self.password_entry.config(fg="black", show="*")
                if not self._is_key_bound[1] and (self.password_var.get()=="Please enter your NTID password(if leave blank or no change, use defult password)" or self.password_var.get()=="请先输入账户名！"):
                    self.password_var.set("")
        else:
            self.password_entry.config(fg="red", show="")
            self.password_entry.delete(0, tk.END)  
            self.password_entry.insert(0, "请先输入账户名！")
            self.username_entry.focus_set()   
      
    def on_password_focus_out(self, event):
        if self.username_var.get() and not self.username_var.get()=='Please enter your NTID username(if leave blank or no change, use defult username)':
            if not self.password_var.get():
                self.password_entry.config(fg="black", show="*")
                self.password_var.set("Please enter your NTID password(if leave blank or no change, use defult password)")
                self.entries_vars_current_value[2] = self.password_var.get() 
        else:
            self.password_entry.config(fg="red", show="")
            self.password_entry.delete(0, tk.END)  
            self.password_entry.insert(0, "请先输入账户名！")
            self.username_entry.focus_set()

    def change_password_entry_visibility(self, event=None):
        if self.password_entry.get() == "请先输入账户名！":
            return
        if self.password_entry_is_visible:
            self.password_entry.config(fg="black", show="*")
            self.password_is_show_eye.config(image=self.password_eye_close_photo)
        else:
            self.password_entry.config(fg="black", show="")
            self.password_is_show_eye.config(image=self.password_eye_open_photo)
        self.password_entry_is_visible = not self.password_entry_is_visible

    def on_runtimes_focus_in(self, event):
        if self.runtimes_var.get() and self.runtimes_var.get()=='Please enter the number to loop through(default:1)':
            if not self._is_key_bound[2]:
                self.runtimes_var.set("")
      
    def on_runtimes_focus_out(self, event):  
        if not self.runtimes_var.get():  
            self.runtimes_var.set("Please enter the number to loop through(default:1)")
            self.entries_vars_current_value[3] = self.runtimes_var.get()

    def update_estimated_time_entry(self, *args):
        self.default_time = {1: 3800, 2: 1500, 3: 2300, 4: 2800, 5: 4300}.get(self.test_item_var.get(), 0)
        self.estimated_time_var.set(f"Default one estimated time for test {self.test_items[self.test_item_var.get()]} is {self.default_time}s")
        self.entries_vars_current_value[0] = self.test_item_var.get()
        self.entries_vars_current_value[4] = self.default_time
        self.entries_vars_default_value[0] = self.test_item_var.get()
        self.entries_vars_default_value[4] = self.default_time
        self.test_item_radio_buttons[self.test_item_var.get()-1].focus_set()

    def on_estimated_time_focus_in(self, event):  
        if self.estimated_time_var.get() and "Default one estimated time for test" in self.estimated_time_var.get():
            if not self._is_key_bound[3]:
                self.estimated_time_var.set("")
                self.entries_vars_current_value[4] = self.default_time
      
    def on_estimated_time_focus_out(self, event):  
        if not self.estimated_time_var.get():
            self.default_time = {1: 3800, 2: 1500, 3: 2300, 4: 2800, 5: 4300}.get(self.test_item_var.get(), 0)
            self.estimated_time_var.set(f"Default one estimated time for test {self.test_items[self.test_item_var.get()]} is {self.default_time}s")
            self.entries_vars_current_value[4] = self.default_time

    def estimated_label_on_enter(self, event):
        self.default_font.config(weight="bold")
        self.estimated_time_label.config(fg="blue", cursor="hand2")  
        if self.estimated_label_hover_window is None:
            self.estimated_label_hover_window = tk.Toplevel(self.root, bg=self.theme_color)
            self.estimated_label_hover_window.transient(self.root)
            self.estimated_label_hover_window.attributes("-topmost", True)
            self.estimated_label_hover_window.overrideredirect(True)
            self.estimated_label_hover_window.geometry(f"+{self.root.winfo_pointerx()}+{self.root.winfo_pointery()}")
            self.estimated_label_hover_window.lift()

            width, height = self.root.winfo_width(), self.root.winfo_height()
            resized_image = self.original_image.resize((int(width * 0.5), int(height * 0.8)), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized_image)
            self.estimated_image_label = tk.Label(self.estimated_label_hover_window, image=self.photo, bg=self.theme_color)
            self.estimated_image_label.grid() 

    def estimated_label_on_leave(self, event):
        self.default_font.config(weight="normal")
        self.estimated_time_label.config(fg="black")
        if not self.estimated_label_is_clicked and self.estimated_label_hover_window is not None:
            self.estimated_label_hover_window.destroy()
            self.estimated_label_hover_window = None  

    def estimated_label_on_click(self, event):
        self.estimated_label_ignore_root_click = True
        self.estimated_label_is_clicked = not self.estimated_label_is_clicked
    
    def get_user_input(self, prompt):
        self.input_popup = tk.Toplevel(self.root, bg=self.theme_color)
        self.input_popup.iconphoto(False, self.toplevel_icon_photo)
        self.input_popup.title("Input Required")
        self.input_popup.transient(self.root)
        self.input_popup.attributes("-topmost", True)
        self.input_popup.resizable(False, False)
        
        self.input_popup_text_label = tk.Text(self.input_popup, height=2, width=50, wrap="word", bg=self.theme_color, bd=0, highlightthickness=0)
        self.input_popup_text_label.pack(pady=10)

        def random_color():
            return "#%06x" % random.randint(0, 0xFFFFFF)
        special_texts = ["y/n", "ip", "address/name"]
        
        color = ""
        start_idx = 1.0
        for word in re.split(r"(\s+)", prompt):
            if any(special_word in word.lower() for special_word in special_texts):
                color = random_color()
                self.input_popup_text_label.insert(start_idx, word, ("bold", color, "center"))
            else:
                self.input_popup_text_label.insert(start_idx, word, "center")
            start_idx = self.input_popup_text_label.index(f"{start_idx} + {len(word)}c")

        self.input_popup_text_label.tag_configure("center", justify="center")
        self.input_popup_text_label.tag_configure("bold", font=("Helvetica", 10, "bold"))
        self.input_popup_text_label.tag_configure(color, foreground=random_color())

        self.input_popup_text_label.config(state=tk.DISABLED) 

        user_input = tk.StringVar()

        self.input_popup_input_entry = tk.Entry(self.input_popup, textvariable=user_input, bg=lighten_hex_color(self.theme_color))
        self.input_popup_input_entry.pack(pady=5)
        self.input_popup_input_entry.focus_set()

        self.input_popup_submit_button = tk.Button(self.input_popup, text="Submit", command=lambda: input_popup_close(), bg=lighten_hex_color(self.theme_color))
        self.input_popup_submit_button.pack(pady=10)
        
        def input_popup_close():
            self.input_popup.destroy()

        def check_input(event=None):
            if user_input.get():
                input_popup_close()
            else:
                self.input_popup_input_entry.focus_set()

        self.input_popup_input_entry.bind("<Return>", check_input)

        self.input_popup.wait_window()
        return user_input.get()

#执行后台任务，并通过队列与主线程通信,用于处理UI界面,并启动web自动测试
def load_auto_modules(app):
    app.print_colored("欢迎使用Genoa xGMI_auto tool \n", "BOLD")
    app.print_colored("\n")
    
    asd = globals()
    import pysy
    asd.update(locals())
    r.set_completer(rlcompleter.Completer(asd).complete)
    r.parse_and_bind('tab: complete')
    console = code.InteractiveConsole(asd)
    path = get_path('launch_Copy.py')
    app_widget = {
        "app_textarea_width": app.text_area.winfo_width()
    }
    console.runcode(r'exec(open(r"{}").read(), {});import Kysy;import sys;sys.ps1 = "\033[1;33m>>>\033[0m "'.format(path, app_widget))
    app.set_start_prepare_event(False)

    def browser_driver_setup(app):
        driver = None
        if app.browser_type_var.get() == 1:
            edge_options = webdriver.EdgeOptions()
            options = edge_options
        else:
            chrome_options = webdriver.ChromeOptions()
            options = chrome_options

        options.add_argument('start-maximized')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # 使浏览器在脚本执行完成后保持打开状态，参考网址3种方法 https://www.cnblogs.com/muxiaomu/p/16669022.html(关闭原因：对应chrome浏览器厂家提供的浏览器源生驱动文件（chromedriver.exe）自身逻辑设置引起的，方法运行完会自动关闭回收方法中定义的局部变量dr)
        options.add_experimental_option('detach', True)  
        prefs = {
            "download.default_directory": get_path("assets"),
            "download.prompt_for_download": False
        }
        options.add_experimental_option("prefs", prefs)

        while True:
            # 检查Event对象的内部标志是否被设置为True
            if app.all_input_ready_event.is_set():
                try:
                    app.print_colored(f"The {app.request_download_browser} browser driver is initializing, maybe wait a few seconds...\n")
                    if app.browser_type_var.get() == 1:
                        # 指定浏览器驱动路径，对于特定版本selenium可能内置驱动或者浏览器版本提供内置的自动化支持就不需要驱动
                        driver_path = EdgeService(app.get_clean_driver_path())
                        # Windows特定的标志，用于当启动EdgeDriver进程时，不显示任何窗口
                        driver_path.creation_flags = CREATE_NO_WINDOW  
                        driver = webdriver.Edge(service=driver_path, options=options)
                    else:
                        driver_path = ChromeService(app.get_clean_driver_path())
                        driver_path.creation_flags = CREATE_NO_WINDOW 
                        driver = webdriver.Chrome(service=driver_path, options=options)  

                    wait = WebDriverWait(driver, 40)
                    app.print_colored("Successfully initialize of WebDriver\n")
                    app.driver_fully_booted_is_ok = True
                    app.click_confirm_button_to_setup()
                    return (driver,wait)
                except Exception as e:
                    # 主线程中打印详细的错误信息
                    app.print_colored(f"Error: {e}\n", "RED")
                    app.print_colored("Browser driver was not started due to an error or missing file.\n", "RED")
                    app.print_colored("\n")
                    app.print_colored("Re enter information\n")
                    app.click_cancel_button_to_restore()
    
    def input_demand(app):
        # 打印测试项
        for key,value in app.test_items.items():
            app.print_colored(f"{key}: {value};\n")
        # 获取测试项
        item = app.print_colored("Test item to be run: ", i=0)
        app.print_colored(f"You will run {app.test_items[item]} \n", "GREEN")
        # 测试项无问题，指定为不可编辑,不可tab选择
        for rb in app.test_item_radio_buttons:
            rb.config(state=tk.DISABLED)
        app.test_item_radio_is_enabled = False

        # 获取用户名和密码
        sdu_username = app.print_colored("AMD AC - NTID username: ", i=1)
        sdu_password = app.print_colored(f"AMD PW - Password for user {sdu_username}: ", i=2)
        # 账户密码处理
        while True:
            if app.start_prepare_event.is_set():
                if app.username_and_password_ready_event.is_set():
                    try:
                        unlock(sdu_username,sdu_password)
                        result = is_locked()
                        app.print_colored("The account & password is correct \n", "GREEN")
                        # 账户密码无问题，指定为不可编辑
                        readonly_indices = [1, 2]  
                        for index, entry in enumerate(app.entries, start=1):
                            if index in readonly_indices:
                                entry.bind('<Key>', lambda event: 'break')
                        break
                    except Exception as e:
                        app.print_colored(f"{e} -- 账号密码错误或者网络已断开，检查后重试 \n", "RED")
                        app.print_colored("\n")
                        app.set_username_and_password_ready_event(False)
            else:
                break

        # 测试次数处理
        while True:  
            if app.start_prepare_event.is_set():    
                if app.runtimes_ready_event.is_set():
                    try:
                        num_times_input = app.print_colored("Number to loop through: ", i=3)
                        num_times = int(''.join(char for char in num_times_input if char.isdigit()))
                        app.print_colored(f"You will run {num_times} times \n", "GREEN")
                        # 测试次数无问题，指定为不可编辑
                        app.runtimes_entry.bind('<Key>', lambda event: 'break')
                        app.runtimes_left_spinbox.disable_customspinbox()
                        app.runtimes_right_spinbox.disable_customspinbox()
                        break
                    except Exception as e:
                        app.print_colored(f"{e} -- loop_number invalid, please input a number again \n", "RED")
                        app.print_colored("\n")
                        app.set_runtimes_ready_event(False)
            else:
                break
            
        # 预估时间处理
        while True:
            if app.start_prepare_event.is_set():
                if app.estimated_time_ready_event.is_set():
                    try:
                        # 捕获并提示用户预估时间输入的内容
                        one_time_input = app.print_colored("Approximately run one time(s): ", i=4)
                        # 检查输入是否是使用了默认时间为数字类型
                        if isinstance(one_time_input, (int, float)):
                            # 如果是数字类型，直接使用它
                            one_time = int(one_time_input) 
                        else:
                            # 如果是字符串，即用户输入的时间，则从预估时间输入字符串中提取数字并转为整数
                            one_time = int(''.join(char for char in one_time_input if char.isdigit()))
                        # 获取测试项的最小时间要求
                        test_info = {
                            1: {"min_time": 3800, "name": "GSA Stress"},
                            2: {"min_time": 1500, "name": "4-Point Parallel^2 Test"},
                            3: {"min_time": 2300, "name": "4-Point Test"},
                            4: {"min_time": 2800, "name": "Margin Search(BER9)"},
                            5: {"min_time": 4300, "name": "Margin Search(BER10)"}
                        }
                        test_data = test_info.get(item)
                        # 检查是否满足最低测试时间要求
                        if test_data and one_time < test_data["min_time"]:
                            app.print_colored(f"Estimated time is not enough, at least {test_data['min_time']}s for the '{test_data['name']}' test.\n", "RED")
                            app.print_colored("\n")
                            app.set_estimated_time_ready_event(False)
                            continue  # 重新输入
                        # 输出最低测试时间确认信息
                        app.print_colored(f"Your estimated time for '{test_data['name']}' test is {one_time}s.\n", "GREEN")
                        app.print_colored("\n")
                        # 预估时间无问题，指定为不可编辑
                        app.estimated_time_entry.bind('<Key>', lambda event: 'break')
                        app.set_all_input_ready_event(True)
                        # 结束循环
                        return sdu_username, sdu_password, num_times, result, one_time, item
                    except ValueError as e:
                        app.print_colored(f"No valid number found in the Estimated time input, please input a number again.\n", "RED")
                        app.print_colored("\n")
                        app.set_estimated_time_ready_event(False)
            else:
                break

    def time_compute(app, time_num, total_sleep_time): 
        if app.all_input_ready_event.is_set(): 
            first_time = True
            dt_object = datetime.fromtimestamp(time.time())
            formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S') 
            app.print_colored(f"run start at {formatted_time} \n", "CYAN")
            start_time = time.time()
            while time.time() - start_time < total_sleep_time:  
                if app.all_input_ready_event.is_set():   
                    elapsed_time = time.time() - start_time
                    time_str = f"{elapsed_time:.2f} seconds"
                    if not first_time:
                        app.print_colored("\r" + f" This time-{time_num+1} already running {time_str} ") 
                    if first_time:  
                        app.print_colored(f" This time-{time_num+1} already running {time_str} ")  
                        first_time = False  
                    time.sleep(1)
                else:
                    break
            else:
                elapsed_time = time.time() - start_time
                time_str = f"{elapsed_time:.2f} seconds"
                app.print_colored("\r" + f" This time-{time_num+1} already running for {time_str} \n")
            if app.all_input_ready_event.is_set():
                dt_object = datetime.fromtimestamp(time.time())
                formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S') 
                app.print_colored(f"run end at {formatted_time} \n", "CYAN")
        
    def go_to_ip(app):
        driver.get(f'https://{ipaddress}')
        driver.find_element(By.ID, "details-button").click()
        driver.find_element(By.ID, "proceed-link").click()
        app.print_colored(f"Successfully opened the web \n")

    def operate_browser(app):
        login_bytedance(app)

        initial = driver.current_window_handle

        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        except:
            pass
                
        #driver.maximize_window()
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "download"))).click()
        except:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//aside//a[@href='#remote_control' and @tabindex='11']"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, "//aside//a[@href='#remote_control' and @tabindex='12']"))).click()     
            wait.until(EC.element_to_be_clickable((By.ID, "download"))).click()
        app.print_colored(f"Successfully Start KVM \n")
        
        operate_new_window(app, initial)
        return initial

    def login_bytedance(app):
        try:
            user_input = wait.until(EC.presence_of_element_located((By.ID, 'userid')))  
            user_input.send_keys('toutiao')
            pw_input = wait.until(EC.presence_of_element_located((By.ID, 'password')))  
            pw_input.send_keys('toutiao!@#')
            time.sleep(1)
            driver.find_element(By.ID, 'btn-login').click()
            app.print_colored(f"Successfully connected to the machine \n")
        except:
            app.print_colored(f"no login required \n")
        
    def operate_new_window(app, initial):
        new_window = None 
        try:
            wait.until(EC.number_of_windows_to_be(2))  
            new_window_handles = [window for window in driver.window_handles if window != driver.current_window_handle]  
            new_window = new_window_handles.pop()  
            driver.switch_to.window(new_window)
            try:
                status_body = wait.until(EC.visibility_of_element_located((By.ID, "status_body")))
                if "KVM 会话超时" in status_body.text:
                    app.print_colored(f"The KVM session time out \n")
                    ref_Browser(app, initial)
                else:
                    app.print_colored(f"The main session changed or reconnected \n")
                    while True:
                        try:
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "status_ok"))).click()
                        except:
                            pass
                        try:
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "request_full"))).click()
                            wait.until(EC.element_to_be_clickable((By.ID, "status_ok"))).click()
                        except:
                            break
                app.print_colored(f"Successfully reconnect KVM \n")
            except:
                app.print_colored(f"KVM session normal \n")
                pass
        except TimeoutException:  
            app.print_colored(f"No new window opened \n", "RED")
            operate_browser()
        except NoSuchWindowException:  
            app.print_colored(f"Attempted to switch to a closed window error \n", "RED")
            driver.switch_to.window(initial)
            driver.quit()
            go_to_ip(app)
            initial_window_handle = operate_browser(app)
        
    def ref_Browser(app, initial):
        try:
            driver.close() 
            driver.switch_to.window(initial)
            driver.refresh()
            try:
                wait.until(EC.alert_is_present())
                driver.switch_to.alert.accept()
            except:
                app.print_colored(f"Unable to handle pop ups, possibly due to non-native pop ups or other reasons \n", "YELLOW")
            try:  
                KVM_button = wait.until(EC.element_to_be_clickable((By.ID, "download")))
                KVM_button.click()
                while True:
                    try:
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "kvm_alert_danger")))
                        #if 'KVM session已处于活动状态' in idinfo_text.text:
                        time.sleep(3)
                        KVM_button.click()
                    except: 
                        break
                app.print_colored("Successfully start KVM again \n")
                operate_new_window(app, initial)       
            except TimeoutException:
                app.print_colored(f"Session expired \n", "YELLOW")
                operate_browser(app)
        except Exception as e:
            app.print_colored(f"{e} \n", "RED")
            driver.switch_to.window(initial)
            driver.quit()
            go_to_ip(app)
            initial_window_handle = operate_browser(app)
        
    def run_xgmi(app, initial, item):
        if item == 1:
            while True:
                val_Shortcut_keys_result = val_Shortcut_keys(app, initial)
                if len(val_Shortcut_keys_result) < 6:
                    app.print_colored(f"No required shortcut_keys yet \n")
                    add_6Shortcut_keys(app)
                    continue
                else:
                    try:
                        if 'HK_CtrlAltT' in val_Shortcut_keys_result and 'HK_Enter2' in val_Shortcut_keys_result:
                            for i in val_Shortcut_keys_result[:-7:-1]:
                                button_HotKeys = wait.until(EC.element_to_be_clickable((By.ID, "button_HotKeys")))
                                button_HotKeys.click()
                                HK_a = wait.until(EC.element_to_be_clickable((By.ID, i)))
                                HK_a.click()
                                time.sleep(0.5)       
                            if app.is_enabled_val_if_run_successfully:
                                if not val_run_isright(app):        
                                    app.print_colored(f"KVM canvas unstable \n", "YELLOW")
                                    driver.find_element(By.ID, 'cursor_canvas').click()
                                    time.sleep(1) 
                                    pyautogui.write('./1.sh', interval=0.25)
                                    time.sleep(0.5)
                                    pyautogui.press('enter')
                            app.print_colored(f"Successlly run XGMI \n", "GREEN")
                            break
                        else:
                            add_6Shortcut_keys(app)
                            continue
                    except Exception as e:
                        app.print_colored(f"{e} \n", "YELLOW")
                        time.sleep(1)
                        pyautogui.moveTo(1200, 500, duration=0.25)
                        time.sleep(0.5)
                        pyautogui.click(button='right')
                        time.sleep(0.5)
                        pyautogui.moveTo(1150, 660, duration=0.25)
                        pyautogui.click(button='left')
                        pyautogui.moveTo(1000, 660, duration=0.25)
                        pyautogui.click(button='left')
                        pyautogui.write('./1.sh', interval=0.25)
                        time.sleep(0.5)
                        pyautogui.press('enter')
                        pyautogui.moveTo(1200, 500, duration=0.25)
                        time.sleep(0.5)
                        pyautogui.click(button='right')
                        time.sleep(0.5)
                        pyautogui.moveTo(1150, 660, duration=0.25)
                        pyautogui.click(button='left')
                        pyautogui.moveTo(1000, 660, duration=0.25)
                        pyautogui.click(button='left')
                        pyautogui.write('./2.sh', interval=0.25)
                        time.sleep(0.5)
                        pyautogui.press('enter')
                        break
        else:
            while True:
                val_Shortcut_keys_result = val_Shortcut_keys(app, initial)
                if len(val_Shortcut_keys_result) < 3:
                    app.print_colored(f"No required shortcut_keys yet \n")
                    add_3Shortcut_keys(app)
                    continue
                else:
                    try:
                        if 'HK_CtrlAltT' in val_Shortcut_keys_result and 'HK_Enter' in val_Shortcut_keys_result:
                            for i in val_Shortcut_keys_result[:-4:-1]:
                                button_HotKeys = wait.until(EC.element_to_be_clickable((By.ID, "button_HotKeys")))
                                button_HotKeys.click()
                                HK_a = wait.until(EC.element_to_be_clickable((By.ID, i)))
                                HK_a.click()
                                time.sleep(0.5)       
                            if app.is_enabled_val_if_run_successfully:
                                if not val_run_isright(app):        
                                    app.print_colored(f"KVM canvas unstable \n", "YELLOW")
                                    driver.find_element(By.ID, 'cursor_canvas').click()
                                    time.sleep(1) 
                                    pyautogui.write('./1.sh', interval=0.25)
                                    time.sleep(0.5)
                                    pyautogui.press('enter')
                            app.print_colored(f"Successlly run XGMI \n", "GREEN")
                            break
                        else:
                            add_3Shortcut_keys(app)
                            continue
                    except Exception as e:
                        app.print_colored(f"{e} \n", "YELLOW")
                        time.sleep(1)
                        pyautogui.moveTo(1200, 500, duration=0.25)
                        time.sleep(0.5)
                        pyautogui.click(button='right')
                        time.sleep(0.5)
                        pyautogui.moveTo(1150, 660, duration=0.25)
                        pyautogui.click(button='left')
                        pyautogui.moveTo(1000, 660, duration=0.25)
                        pyautogui.click(button='left')
                        pyautogui.write('./1.sh', interval=0.25)
                        time.sleep(0.5)
                        pyautogui.press('enter')
                        break
                    
    def add_3Shortcut_keys(app):
        try:
            button_HotKeys = wait.until(EC.element_to_be_clickable((By.ID, "button_HotKeys")))
            button_HotKeys.click()
            time.sleep(1)
            add_3Shortcut_keys_button = wait.until(EC.element_to_be_clickable((By.ID, "addHotKey")))
            add_3Shortcut_keys_button.click()
            time.sleep(1)

            has_buttons = True  
            div = wait.until(EC.presence_of_element_located((By.ID, "usr_macros_list"))) 
            while has_buttons:
                buttons = div.find_elements(By.TAG_NAME, "button")
                if buttons:
                    for button in buttons:  
                        button.click()  
                        time.sleep(0.5)
                    buttons_after_click = div.find_elements(By.TAG_NAME, "button")  
                    if not buttons_after_click:
                        app.print_colored(f"-->Removed unnecessary shortcuts \n")
                        has_buttons = False  
                else:  
                    has_buttons = False
                    
            usr_macro_add_button = wait.until(EC.element_to_be_clickable((By.ID, "usr_macro_add")))
            usr_macro_add_button.click()
            time.sleep(1)
            #wait.until(EC.element_to_be_clickable((By.ID, "macro_dialog_input"))).click()
            #pyautogui.press('enter')
            macro_dialog_input = wait.until(EC.presence_of_element_located((By.ID, 'macro_dialog_input')))  
            macro_dialog_input.send_keys(Keys.ENTER)
            macro_close_button = wait.until(EC.element_to_be_clickable((By.ID, "macro_close")))
            macro_close_button.click()
            time.sleep(1)
            
            usr_macro_add_button.click()
            time.sleep(1)
            #wait.until(EC.element_to_be_clickable((By.ID, "macro_dialog_input"))).click()
            #keys = ['.', '/', '1', '.', 's', 'h']
            #for key in keys:
                #pyautogui.press(key)
                #time.sleep(0.1)
            macro_dialog_input.send_keys('./1.sh')
            macro_close_button.click()
            time.sleep(1)

            usr_macro_add_button.click()
            time.sleep(1)
            #wait.until(EC.element_to_be_clickable((By.ID, "macro_dialog_input"))).click()
            #pyautogui.hotkey('ctrl', 'alt', 't')
            macro_dialog_input.send_keys(Keys.CONTROL+Keys.ALT+'t')
            macro_close_button.click()
            time.sleep(1)
            
            wait.until(EC.element_to_be_clickable((By.ID, "usr_macro_close"))).click()
            time.sleep(1)
            app.print_colored(f"-->Successlly add shortcuts \n")
        except Exception as e:
            app.print_colored(f"{e} \n", "YELLOW")
            
    def add_6Shortcut_keys(app):
        try:
            button_HotKeys = wait.until(EC.element_to_be_clickable((By.ID, "button_HotKeys")))
            button_HotKeys.click()
            time.sleep(1)
            add_6Shortcut_keys_button = wait.until(EC.element_to_be_clickable((By.ID, "addHotKey")))
            add_6Shortcut_keys_button.click()
            time.sleep(1)

            has_buttons = True  
            div = wait.until(EC.presence_of_element_located((By.ID, "usr_macros_list"))) 
            while has_buttons:
                buttons = div.find_elements(By.TAG_NAME, "button")
                if buttons:
                    for button in buttons:  
                        button.click()  
                        time.sleep(0.5)
                    buttons_after_click = div.find_elements(By.TAG_NAME, "button")  
                    if not buttons_after_click:
                        app.print_colored(f"-->Removed unnecessary shortcuts \n")
                        has_buttons = False  
                else:  
                    has_buttons = False
                    
            usr_macro_add_button = wait.until(EC.element_to_be_clickable((By.ID, "usr_macro_add")))
            usr_macro_add_button.click()
            time.sleep(1)
            #wait.until(EC.element_to_be_clickable((By.ID, "macro_dialog_input"))).click()
            #pyautogui.press('enter')
            macro_dialog_input = wait.until(EC.presence_of_element_located((By.ID, 'macro_dialog_input')))  
            macro_dialog_input.send_keys(Keys.ENTER+'2')
            macro_close_button = wait.until(EC.element_to_be_clickable((By.ID, "macro_close")))
            macro_close_button.click()
            time.sleep(1)

            usr_macro_add_button.click()
            time.sleep(1)
            #wait.until(EC.element_to_be_clickable((By.ID, "macro_dialog_input"))).click()
            #keys = ['.', '/', '2', '.', 's', 'h']
            #for key in keys:
                #pyautogui.press(key)
                #time.sleep(0.1)
            macro_dialog_input.send_keys('./2.sh')
            macro_close_button.click()
            time.sleep(1)

            usr_macro_add_button.click()
            time.sleep(1)
            #wait.until(EC.element_to_be_clickable((By.ID, "macro_dialog_input"))).click()
            #pyautogui.hotkey('ctrl', 'alt', 't', '2')
            macro_dialog_input.send_keys(Keys.CONTROL+Keys.ALT+'t'+'2')
            macro_close_button.click()
            time.sleep(1)
            
            usr_macro_add_button.click()
            time.sleep(1)
            #wait.until(EC.element_to_be_clickable((By.ID, "macro_dialog_input"))).click()
            #pyautogui.press('enter')
            macro_dialog_input.send_keys(Keys.ENTER)
            macro_close_button.click()
            time.sleep(1)
            
            usr_macro_add_button.click()
            time.sleep(1)
            #wait.until(EC.element_to_be_clickable((By.ID, "macro_dialog_input"))).click()
            #keys = ['.', '/', '1', '.', 's', 'h']
            #for key in keys:
                #pyautogui.press(key)
                #time.sleep(0.1)
            macro_dialog_input.send_keys('./1.sh')
            macro_close_button.click()
            time.sleep(1)

            usr_macro_add_button.click()
            time.sleep(1)
            #wait.until(EC.element_to_be_clickable((By.ID, "macro_dialog_input"))).click()
            #pyautogui.hotkey('ctrl', 'alt', 't', '1')
            macro_dialog_input.send_keys(Keys.CONTROL+Keys.ALT+'t')
            macro_close_button.click()
            time.sleep(1)
            
            wait.until(EC.element_to_be_clickable((By.ID, "usr_macro_close"))).click()
            time.sleep(1)
            app.print_colored(f"-->Successlly add shortcuts \n")
        except Exception as e:
            app.print_colored(f"{e} \n", "YELLOW")
            
    def val_Shortcut_keys(app, initial):
        try:
            wait.until(EC.element_to_be_clickable((By.ID, "button_HotKeys"))).click()
            time.sleep(1)
            Shortcut_keys_ul_element = wait.until(EC.presence_of_element_located((By.ID, "usr_macros_menu")))
            Shortcut_keys_li_elements = Shortcut_keys_ul_element.find_elements(By.TAG_NAME, "li")
            app.print_colored("Existing shortcut keys: ")
            
            li_ids = []
            for li_id in Shortcut_keys_li_elements:
                li_id_name = li_id.get_attribute('id')
                li_ids.append(li_id_name)
                app.print_colored(f"{li_id_name} ")
            app.print_colored(f" \n")
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.ID, "button_HotKeys"))).click()
            return li_ids
        except:
            app.print_colored(f"validate/link error \n", "YELLOW")
            while True:
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "status_ok"))).click()
                except:
                    pass
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "request_full"))).click()
                    wait.until(EC.element_to_be_clickable((By.ID, "status_ok"))).click()
                except:
                    break
            '''
            try:
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "request_full"))).click()
                status_ok_button = wait.until(EC.element_to_be_clickable((By.ID, "status_ok")))
                status_ok_button.click()
            except:
                pass
            '''
            return []
        
    def val_run_isright(app):
        button_video_menu = wait.until(EC.element_to_be_clickable((By.ID, "button_video_menu")))
        button_video_menu.click()
        capture_screen_button = wait.until(EC.element_to_be_clickable((By.ID, "capture_screen")))
        capture_screen_button.click()
        while True:
            for file in os.listdir(get_path("assets")):
                if ('CaptureScreen' in file) and ('load' not in file):
                    target_image = os.path.normpath(os.path.join(get_path("assets"), file))
                    template_image = app.vf_upload_image_file_path
                    if find_template_in_image(target_image, template_image):
                        os.remove(target_image)
                        return True
                    else:
                        os.remove(target_image)
                        return False
                        
    def find_template_in_image(target_image_path, template_image_path, threshold=0.999):  
        #target_image = cv2.imread(target_image_path, 0)
        #template_image = cv2.imread(template_image_path, 0)  
        # unicode以避免cv2.imread不识别中文路径，参考https://blog.csdn.net/weixin_43272781/article/details/114644815
        try:
            target_image = cv2.imdecode(np.fromfile(target_image_path,dtype=np.uint8),-1)
            template_image  = cv2.imdecode(np.fromfile(template_image_path,dtype=np.uint8),-1)  
        except Exception as e:
            app.print_colored(f"{e}\n", "RED")
            return False

        if target_image is None or template_image is None: 
            app.print_colored("路径不存在\n", "YELLOW")
            return False   
      
        res = cv2.matchTemplate(target_image,  template_image, cv2.TM_CCOEFF_NORMED)
        #print(cv2.minMaxLoc(res))
        loc = np.where(res >= threshold)

        """
        # 如果图片是三维图像的话shape返回 (height, width, channels)
        template_height, template_width = template_image.shape[:2]
        for pt in zip(*loc[::-1]): 
            app.print_colored(f"匹配位置: ({pt[0]}, {pt[1]})")
            cv2.rectangle(target_image, pt, (pt[0] + template_width, pt[1] + template_height), (0, 255, 255), 2)     
            cv2.imshow('Matched template', target_image)  
            cv2.waitKey(0)  
            cv2.destroyAllWindows() 
        """
           
        return len(loc[0]) > 0  

    driver =None
    while True:
        if not app.start_prepare_event.is_set():
            # 如果有正在运行的 driver且start_prepare_event为False，则关闭所有打开的浏览器
            if driver is not None:
                driver.quit()
                driver = None  # 重置 driver 引用
            app.start_prepare_event.wait()
            app.print_colored("Start checking input information, then prepare for testing\n")
            app.print_colored("\n")
            try:
                item, sdu_username, sdu_password, result, num_times, one_time = input_demand(app)
            except Exception as e:
                # 如果信息输入不全或者不正确时点击取消则先执行cancel-button的第一个条件，并且打印信息
                app.print_colored(f"Error: {e}\n", "RED")
                app.print_colored("Re enter information\n")
            driver, wait = browser_driver_setup(app)
            if app.driver_fully_booted_is_ok:
                go_to_ip(app)
                initial_window_handle = operate_browser(app)

                results = [True] * num_times
                for i in range(num_times):
                    if app.all_input_ready_event.is_set():
                        if i == 0:
                            app.print_colored(f"unlock success \n")
                            app.print_colored(f'time {i+1} is_locked status is {result} \n')
                            results[i] = result                    
                        else:
                            app.print_colored(f"请稍等，正在检查解锁状态...\n")
                            result = is_locked()
                            app.print_colored(f'time {i+1} is_locked status is {result} \n')
                        if result:
                            app.print_colored(f"请稍等，正在解锁...\n")
                            unlock(sdu_username,sdu_password)
                            app.print_colored(f"unlock success \n")
                            app.print_colored(f"请稍等，正在检查解锁状态...\n")
                            result = is_locked()
                            app.print_colored(f'time {i+1} is_locked status is {result} \n')
                        results[i] = result
                        run_xgmi(app,initial_window_handle, item)
                        time_compute(app, i, one_time)
                        if i == num_times-1:
                            break
                        ref_Browser(app, initial_window_handle)
                    else:
                        break
                app.print_colored(f"all {num_times}-times status is \n   {results} \n")
                console.interact(banner="Welcome to AMD Go-Pi NDA")

def main():
    root = tk.Tk()
    app = App(root) 

    # 替换python自带的终端命令行的input函数，用tk的UI组件输入实现同样的效果   
    builtins = globals()['__builtins__']
    builtins.input = app.get_user_input  

    #threading.Thread(target=load_auto_modules, args=(app,)).start()  # 启动一个守护线程来运行自动模块
    threading.Thread(target=lalala, args=(app,), daemon=True).start()  # 启动一个守护线程来运行自动模块

    root.mainloop()

def lalala(app):
    app.print_colored("欢迎使用Genoa xGMI_auto tool \n", "BOLD")
    app.print_colored("\n")
    
    def input_demand(app):
        # 打印测试项
        for key,value in app.test_items.items():
            app.print_colored(f"{key}: {value};\n")
        # 获取测试项
        item = app.print_colored("Test item to be run: ", i=0)
        app.print_colored(f"You will run {app.test_items[item]} \n", "GREEN")
        # 测试项无问题，指定为不可编辑,不可tab选择
        for rb in app.test_item_radio_buttons:
            rb.config(state=tk.DISABLED)
        app.test_item_radio_is_enabled = False

        # 获取用户名和密码
        sdu_username = app.print_colored("AMD AC - NTID username: ", i=1)
        sdu_password = app.print_colored(f"AMD PW - Password for user {sdu_username}: ", i=2)
        # 账户密码处理
        while True:
            if app.start_prepare_event.is_set():
                if app.username_and_password_ready_event.is_set():
                    try:
                        #print_colored("请稍等，正在校验账户密码...\n")
                        #unlock(sdu_username,sdu_password)
                        #result = is_locked()
                        result = True
                        app.print_colored("The account & password is correct \n", "GREEN")
                        # 账户密码无问题，指定为不可编辑
                        readonly_indices = [1, 2]  
                        for index, entry in enumerate(app.entries, start=1):
                            if index in readonly_indices:
                                entry.bind('<Key>', lambda event: 'break')
                        break
                    except Exception as e:
                        app.print_colored(f"{e} -- 账号密码错误或者网络已断开，检查后重试 \n", "RED")
                        app.print_colored("\n")
                        app.set_username_and_password_ready_event(False)
            else:
                break

        # 测试次数处理
        while True:  
            if app.start_prepare_event.is_set():    
                if app.runtimes_ready_event.is_set():
                    try:
                        num_times_input = app.print_colored("Number to loop through: ", i=3)
                        num_times = int(''.join(char for char in num_times_input if char.isdigit()))
                        app.print_colored(f"You will run {num_times} times \n", "GREEN")
                        # 测试次数无问题，指定为不可编辑
                        app.runtimes_entry.bind('<Key>', lambda event: 'break')
                        app.runtimes_left_spinbox.disable_customspinbox()
                        app.runtimes_right_spinbox.disable_customspinbox()
                        break
                    except Exception as e:
                        app.print_colored(f"{e} -- loop_number invalid, please input a number again \n", "RED")
                        app.print_colored("\n")
                        app.set_runtimes_ready_event(False)
            else:
                break
            
        # 预估时间处理
        while True:
            if app.start_prepare_event.is_set():
                if app.estimated_time_ready_event.is_set():
                    try:
                        # 捕获并提示用户预估时间输入的内容
                        one_time_input = app.print_colored("Approximately run one time(s): ", i=4)
                        # 检查输入是否是使用了默认时间为数字类型
                        if isinstance(one_time_input, (int, float)):
                            # 如果是数字类型，直接使用它
                            one_time = int(one_time_input) 
                        else:
                            # 如果是字符串，即用户输入的时间，则从预估时间输入字符串中提取数字并转为整数
                            one_time = int(''.join(char for char in one_time_input if char.isdigit()))
                        # 获取测试项的最小时间要求
                        test_info = {
                            1: {"min_time": 3800, "name": "GSA Stress"},
                            2: {"min_time": 1500, "name": "4-Point Parallel^2 Test"},
                            3: {"min_time": 2300, "name": "4-Point Test"},
                            4: {"min_time": 2800, "name": "Margin Search(BER9)"},
                            5: {"min_time": 4300, "name": "Margin Search(BER10)"}
                        }
                        test_data = test_info.get(item)
                        # 检查是否满足最低测试时间要求
                        if test_data and one_time < test_data["min_time"]:
                            app.print_colored(f"Estimated time is not enough, at least {test_data['min_time']}s for the '{test_data['name']}' test.\n", "RED")
                            app.print_colored("\n")
                            app.set_estimated_time_ready_event(False)
                            continue  # 重新输入
                        # 输出最低测试时间确认信息
                        app.print_colored(f"Your estimated time for '{test_data['name']}' test is {one_time}s.\n", "GREEN")
                        app.print_colored("\n")
                        # 预估时间无问题，指定为不可编辑
                        app.estimated_time_entry.bind('<Key>', lambda event: 'break')
                        app.set_all_input_ready_event(True)
                        # 结束循环
                        return sdu_username, sdu_password, num_times, result, one_time, item
                    except ValueError as e:
                        app.print_colored(f"No valid number found in the Estimated time input, please input a number again.\n", "RED")
                        app.print_colored("\n")
                        app.set_estimated_time_ready_event(False)
            else:
                break

    def driver_start(app):
        # 检查Event对象的内部标志是否被设置为False
        if app.all_input_ready_event.is_set():
            try:
                app.print_colored(f"The {app.request_download_browser} browser driver is initializing, maybe wait a few seconds...\n")
                # 根据选择的浏览器类型初始化对应的选项和驱动路径
                if app.browser_type_var.get() == 1:
                    options = webdriver.EdgeOptions()
                    options.add_experimental_option('detach', True)  #不自动关闭浏览器
                    driver_path = EdgeService(app.get_clean_driver_path())
                    driver=webdriver.Edge(service=driver_path,options=options)
                else:
                    options = webdriver.ChromeOptions()
                    options.add_experimental_option('detach', True)  #不自动关闭浏览器
                    driver_path = ChromeService(app.get_clean_driver_path())
                    driver=webdriver.Chrome(service=driver_path,options=options)
                app.print_colored("Successfully initialize of WebDriver\n")
                app.driver_fully_booted_is_ok = True
                app.click_confirm_button_to_setup()
                driver.get('https://www.baidu.com')
                return driver
            except Exception as e:
                # 主线程中打印详细的错误信息
                app.print_colored(f"Error: {e}\n", "RED")
                app.print_colored("Browser driver was not started due to an error or driver missing/mismatched.\n", "RED")
                app.print_colored("\n")
                app.print_colored("Re enter information\n")
                app.click_cancel_button_to_restore()

    def time_compute(app, time_num, total_sleep_time): 
        if app.all_input_ready_event.is_set(): 
            first_time = True
            dt_object = datetime.fromtimestamp(time.time())
            formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S') 
            app.print_colored(f"run start at {formatted_time} \n", "CYAN")
            start_time = time.time()
            while time.time() - start_time < total_sleep_time: 
                if app.all_input_ready_event.is_set():    
                    elapsed_time = time.time() - start_time
                    time_str = f"{elapsed_time:.2f} seconds"
                    if not first_time:
                        app.print_colored("\r" + f" This time-{time_num+1} already running {time_str} ") 
                    if first_time:  
                        app.print_colored(f" This time-{time_num+1} already running {time_str} ")  
                        first_time = False  
                    time.sleep(1)
                else:
                    break
            else:
                elapsed_time = time.time() - start_time
                time_str = f"{elapsed_time:.2f} seconds"
                app.print_colored("\r" + f" This time-{time_num+1} already running for {time_str} \n")
            if app.all_input_ready_event.is_set():
                dt_object = datetime.fromtimestamp(time.time())
                formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S') 
                app.print_colored(f"run end at {formatted_time} \n", "CYAN")
            
    def val_run_isright(app):
        target_image = os.path.normpath(os.path.join(get_path("assets"), "template.jpeg"))
        template_image = app.vf_upload_image_file_path
        if find_template_in_image(target_image, template_image):
            return True
        else:
            return False
                        
    def find_template_in_image(target_image_path, template_image_path, threshold=0.999):  
        # unicode以避免cv2.imread不识别中文路径，参考https://blog.csdn.net/weixin_43272781/article/details/114644815
        try:
            target_image = cv2.imdecode(np.fromfile(target_image_path,dtype=np.uint8),-1)
            template_image  = cv2.imdecode(np.fromfile(template_image_path,dtype=np.uint8),-1)  
        except Exception as e:
            app.print_colored(f"{e}\n", "RED")
            return False

        if target_image is None or template_image is None: 
            app.print_colored("路径不存在\n", "YELLOW")
            return False   
      
        res = cv2.matchTemplate(target_image,  template_image, cv2.TM_CCOEFF_NORMED)
        #print(cv2.minMaxLoc(res))
        loc = np.where(res >= threshold)

        """
        # 如果图片是三维图像的话shape返回 (height, width, channels)
        template_height, template_width = template_image.shape[:2]
        for pt in zip(*loc[::-1]): 
            app.print_colored(f"匹配位置: ({pt[0]}, {pt[1]})")
            cv2.rectangle(target_image, pt, (pt[0] + template_width, pt[1] + template_height), (0, 255, 255), 2)     
            cv2.imshow('Matched template', target_image)  
            cv2.waitKey(0)  
            cv2.destroyAllWindows() 
        """
           
        return len(loc[0]) > 0  
    
    driver =None
    while True:
        if not app.start_prepare_event.is_set():
            # 如果有正在运行的 driver且start_prepare_event为False，则关闭所有打开的浏览器
            if driver is not None:
                driver.quit()
                driver = None  # 重置 driver 引用
            app.start_prepare_event.wait()
            app.print_colored("Start checking input information, then prepare for testing\n")
            app.print_colored("\n")
            try:
                item, sdu_username, sdu_password, result, num_times, one_time = input_demand(app)
            except Exception as e:
                # 如果信息输入不全或者不正确时点击取消则先执行cancel-button的第一个条件，并且打印信息
                app.print_colored(f"Error: {e}\n", "RED")
                app.print_colored("Re enter information\n")
            driver = driver_start(app)
            #time_compute(app, 0, one_time)\
            if app.driver_fully_booted_is_ok and app.is_enabled_val_if_run_successfully:
                val_run_isright(app)

if __name__ == "__main__":  
    main()