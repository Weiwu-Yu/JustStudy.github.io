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
#import platform as _pt
import random
import re
import time
import tkinter as tk
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

# 直接运行与打包成exe的文件路径不一样，以获取需要用到的资源
def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
 
    return os.path.normpath(os.path.join(base_path, relative_path))

# 原Go_pi用colorama模块打印的不同颜色信息在重定向时更改为UI控件的标签颜色
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

# 重定向类，负责将原Go_pi代码print的内容保存在队列中，以便主UI界面获取
class RedirectedIO:
    def __init__(self, widget):
        self.widget = widget
        self.pattern = re.compile(r'(\033\[\d+m)')  # 返回的正则表达式对象用于识别和处理ANSI转义序列，\033匹配ANSI转义序列的引导字符（ESC，是colorama模块用于控制终端的输出格式）。在Python字符串中,\033是八进制表示法,等同于十六进制的\x1B
        self.current_directory = os.getcwd()
        self.log_file_path = os.path.join(self.current_directory, "xGMI_auto_GUI_log.txt")
        self.log_file_lock = threading.Lock()  # 添加线程锁
        self.ensure_log_file_exists()  
        self.log_file = open(self.log_file_path, "a", encoding="utf-8")  
        self.widget_state_lock = threading.Lock()  # 用于保护widget状态更改的锁  
  
    def ensure_log_file_exists(self):  
        if not os.path.exists(self.log_file_path) or os.stat(self.log_file_path).st_size == 0:  
            with open(self.log_file_path, "w", encoding="utf-8") as f:  
                creation_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  
                f.write(f"This log file created at: {creation_time}\n\n")  
        
    def write(self, text, tag=None):
        with self.widget_state_lock:  # 使用 with 语句来管理锁，确保锁在适当的时候被释放
            self.widget.config(state=tk.NORMAL)  

        with self.log_file_lock:
            if "\r" in text:
                current_line_start = self.widget.index("insert linestart")
                current_line_end = self.widget.index("insert lineend")
                self.widget.delete(current_line_start, current_line_end)
                #self.widget.delete("end-1l linestart", tk.END)
                text = text.replace("\r", "")
 
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
            #self.widget.insert(tk.END, text, tag)
            self.widget.see(tk.END) 
            self.widget.update_idletasks()
            self.widget.config(state=tk.DISABLED)

            self.log_file.write(part)
            self.log_file.flush()

    def flush(self):
        pass

    def close(self):
        self.log_file.close()
        #如果在 write() 方法中发生异常，文件可能不会被正确关闭。考虑使用 try...finally 结构或上下文管理器（with 语句）来确保文件总是被关闭
  
class HoverButton(tk.Canvas):  
    def __init__(self, master=None, text='', radius=10, color=None, command=None, **kw):  
        super().__init__(master, width=100, height=50, highlightthickness=0, **kw)
        self.text = text
        self.radius = radius
        self.color = color
        self.command = command

        self.bind("<Configure>", self.redraw_rectangle)  
        self.redraw_rectangle(None)  
  
    def redraw_rectangle(self, event=None):
        self.delete("all")
        
        width = self.winfo_width()  
        height = self.winfo_height()

        self.font_normal = font.Font(family='Arial', size=10)  
        self.font_hover = font.Font(family='Arial', size=10, weight='bold')  
        self.default_bg = self.color
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
        self.bind("<Button-1>", self.on_click)
        self.bind("<FocusIn>", self.on_click)

    def on_enter(self, e):
        self.itemconfig(self.text_id, font=self.font_hover)  
        if self.itemcget(self.text_id, "text") == "confirm":       
            self.itemconfig(self.rect_id, fill=self.hover_bg_1, outline='black')
        else:
            self.itemconfig(self.rect_id, fill=self.hover_bg_2, outline='black')
  
    def on_leave(self, e):
        self.itemconfig(self.rect_id, fill=self.default_bg, outline='')  
        self.itemconfig(self.text_id, font=self.font_normal)  
  
    def on_click(self, event=None):
        if self.command is not None:  
            self.command(event)
 
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("xGMI_auto")
        #self.root.attributes("-topmost", True)  # 程序始终在屏幕最上方
        #self.root.geometry("800x600")
        #self.root.state("zoomed")
        import base64
        with open(get_path("assets/logo.ico"), 'rb') as open_icon:
            b64str = base64.b64encode(open_icon.read())
        #self.root.iconbitmap(get_path("assets/1.ico"))
        from base64 import b64decode
        icon_img = b64str
        icon_img = b64decode(icon_img)
        icon_img = ImageTk.PhotoImage(data=icon_img)
        self.root.tk.call('wm', 'iconphoto', self.root._w, icon_img)
        #self.root.configure(bg="blue")
        self.root.config(bg="#F5F5F5")
        self.root.minsize(1500,550)

        self.create_menu()
        self.is_installing_driver = False

        frame_left = tk.Frame(root)  
        #frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        frame_left.grid(row=0, column=0, sticky="nsew")
        frame_right = tk.Frame(root)  
        #frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        frame_right.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)
        frame_right.grid_columnconfigure(0, weight=1)
        frame_right.grid_rowconfigure(0, weight=1)
        
        self.browser_type_label = tk.Label(frame_left, text="浏览器: ")
        self.browser_type_label.grid(row=0, column=0, sticky='w', padx=5)
        self.browser_type_var = tk.IntVar(value=1)
        self.browser_type = {  
            1: 'Edge',  
            2: 'Chrome'
        }
        self.browser_radio_buttons = []
        for j, (browser_type_key, browser_type_value) in enumerate(self.browser_type.items(), start=1):  
            rb = tk.Radiobutton(frame_left, 
                                value=browser_type_key,
                                text=browser_type_value, 
                                variable=self.browser_type_var, 
                                command=self.select_browser_radio)
            if j == 1:
                rb.grid(row=0, column=j, sticky='w', padx=50)
            else:
                rb.grid(row=0, column=j-1, sticky='w', padx=300) 
            self.browser_radio_buttons.append(rb)

        # 初始驱动路径
        self.driver_path_label = tk.Label(frame_left, text="驱动路径:")  
        self.driver_path_label.grid(row=1, column=0, sticky='w', padx=5, pady=10)  
        self.driver_path_var = tk.StringVar(value="")  
        self.driver_path_entry = tk.Entry(frame_left, textvariable=self.driver_path_var, width=50, state='readonly')  
        self.driver_path_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=10)
        # 根据初始浏览器选择设置驱动路径显示文本
        self.select_browser_radio()  # 调用一次以设置初始状态
        self.driver_info_dialog = None

        self.entries_vars_current_value = []
        self.entries_vars_default_value = []
        self.test_item_label = tk.Label(frame_left, text="xGMI测试项: ")
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
            rb = tk.Radiobutton(frame_left, text=value, variable=self.test_item_var, value=key, command=self.update_estimated_time_entry)
            rb.grid(row=i+1, column=1, sticky='w', padx=5)
            rb.bind("<Return>", self.select_test_item_radio_ok)
            rb.bind("<Tab>", self.select_test_item_radio_tab)
            self.test_item_radio_buttons.append(rb)
            
        self.username_var = tk.StringVar()
        self.username_var.set("Please enter your NTID username")
        self.default_username_var = tk.StringVar()
        self.default_username_var.set("hu.demi@inventec.com.cn")
        self.entries_vars_current_value.append(self.username_var.get())
        self.entries_vars_default_value.append(self.default_username_var.get())
        self.password_var = tk.StringVar()
        self.password_var.set("Password")
        self.default_password_var = tk.StringVar()
        self.default_password_var.set("Ev@20240912")
        self.entries_vars_current_value.append(self.password_var.get())
        self.entries_vars_default_value.append(self.default_password_var.get())
        self.username_label = tk.Label(frame_left, text="AMD用户名: ")
        self.username_label.grid(row=7, column=0, sticky='w', padx=5, pady=10)
        self.username_entry = tk.Entry(frame_left, textvariable=self.username_var, width=len(self.username_var.get())+5)
        self.username_entry.grid(row=7, column=1, sticky='ew', padx=5, pady=10)  
        self.password_label = tk.Label(frame_left, text="AMD密码: ")
        self.password_label.grid(row=8, column=0, sticky='w', padx=5, pady=10)
        self.password_entry = tk.Entry(frame_left, textvariable=self.password_var, show= '*')
        self.password_entry.grid(row=8, column=1, sticky='ew', padx=5, pady=10)
        self.username_entry.bind("<FocusIn>", self.on_username_focus_in)  
        self.username_entry.bind("<FocusOut>", self.on_username_focus_out)
        self.password_entry.bind("<FocusIn>", self.on_password_focus_in)  
        self.password_entry.bind("<FocusOut>", self.on_password_focus_out)
        self.username_entry.bind("<Return>", self.handle_enter)
        self.password_entry.bind("<Return>", self.handle_enter)

        self.runtimes_var = tk.StringVar()
        self.runtimes_var.set("Please enter the number to loop through")
        self.entries_vars_current_value.append(self.runtimes_var.get())
        self.entries_vars_default_value.append(self.runtimes_var.get())
        self.runtimes_label = tk.Label(frame_left, text="测试/解锁次数:")
        self.runtimes_label.grid(row=9, column=0, sticky='w', padx=5, pady=10)
        self.runtimes_entry = tk.Entry(frame_left, textvariable=self.runtimes_var, width=len(self.runtimes_var.get())+5)
        self.runtimes_entry.grid(row=9, column=1, sticky='ew', padx=5, pady=10)
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
        self.estimated_time_label = tk.Label(frame_left, text="预估一次时间: ")
        self.estimated_time_label.config(font=self.default_font)
        self.estimated_time_label.grid(row=10, column=0, sticky='w', padx=5, pady=10)
        image_path = get_path("assets/Estimated_time.png")
        self.original_image = Image.open(image_path)
        self.hover_window = None
        self.estimated_time_label.bind("<Enter>", self.label_on_enter)
        self.estimated_time_label.bind("<Leave>", self.label_on_leave)
        #self.estimated_time_label.bind("<Button-1>", self.label_on_click)
        self.estimated_time_entry = tk.Entry(frame_left, textvariable=self.estimated_time_var, width=len(self.estimated_time_var.get())+5)
        self.estimated_time_entry.grid(row=10, column=1, sticky='ew', padx=5, pady=10)
        #self.test_item_var.trace_add("write", self.update_estimated_time_entry)
        self.estimated_time_entry.bind("<FocusIn>", self.on_estimated_time_focus_in)  
        self.estimated_time_entry.bind("<FocusOut>", self.on_estimated_time_focus_out)
        self.estimated_time_entry.bind("<Return>", self.handle_enter)
        
        self.entries = [self.username_entry, self.password_entry, self.runtimes_entry, self.estimated_time_entry]
        self.entries_var = [self.username_var, self.password_var, self.runtimes_var, self.estimated_time_var]
        
        self.button_confirm = HoverButton(frame_left, text="confirm", color = "lightgray", command=self.handle_confirm_button)
        self.button_confirm.grid(row=11, column=1, sticky='w', padx=20, pady=20)
        self.button_cancel = HoverButton(frame_left, text="cancel", color = "lightgray", command=self.handle_cancel_button)
        self.button_cancel.grid(row=11, column=1, sticky='e', padx=300, pady=20)

        self.text_area = ScrolledText(frame_right, wrap=tk.WORD, state=tk.DISABLED, bg='lightgray', fg='black', font=("Courier", 10))
        self.text_area.grid(sticky='nsew', padx=10, pady=10)
        self.text_area.tag_configure("GREEN", foreground="green")
        self.text_area.tag_configure("RED", foreground="red")
        self.text_area.tag_configure("CYAN", foreground="cyan")
        self.text_area.tag_configure("YELLOW", foreground="yellow")
        self.text_area.tag_configure("BOLD", font=("Helvetica", 10, "bold"), foreground="green")
        sys.stdout = RedirectedIO(self.text_area)
        sys.stderr = RedirectedIO(self.text_area)

        self.window_closed = False
        self.input_popup = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # 主循环和后台线程并行，需要使用threading.Event事件对象机制来同步管理事件状态--在后台线程中实时安全地访问和检查事件的值
        self.input_ready_event = threading.Event()
        # 标志变量，指示驱动是否可用
        self.driver_is_good = False
        # 标志变量，指示驱动是否已完全启动
        self.driver_fully_booted_is_ok = False

    def set_input_ready_event(self, value):
        self.input_ready_event.set() if value else self.input_ready_event.clear()
 
    # 主程序关闭释放资源和恢复变量值
    def on_closing(self):
        if messagebox.askokcancel("Quit", "APP is closing...Do you want to quit?"):
            # 正在下载driver的提示变量恢复默认值
            if self.is_installing_driver:
                self.is_installing_driver = False
            # 将用以替换python的input函数的输入窗口关闭
            if self.input_popup is not None and self.input_popup.winfo_exists():
                self.input_popup.destroy()
            sys.stdout.close()
            self.window_closed = True
            self.root.quit()
            self.root.destroy()

    #  所有资源和信息显示为需要的信息
    def click_confirm_button_to_change_entry_info(self):
        # 将所有的输入框锁定不可编辑
        for entry in enumerate(self.entries, start=1):
            entry[1].config(state='readonly')
        # 将浏览器类型和测试项锁定
        all_radio_buttons = self.browser_radio_buttons + self.test_item_radio_buttons
        for rb in all_radio_buttons:
            rb.config(state=tk.DISABLED)
        # 测试项锁定的时候不再可使用tab选择
        self.test_item_radio_is_enabled = False
        # 所有准备已就绪
        self.set_input_ready_event(True)
        for i, entry in enumerate(self.entries, start=1):
            if not entry.get():
                self.entries_vars_current_value[i] = self.entries_vars_current_value[i]
                self.entries_var[i-1].set(self.entries_vars_default_value[i])
                self.root.focus_set()
            else:
                if i == 4:
                    if "Default one estimated time for test" in entry.get():
                        self.entries_vars_current_value[i] = self.default_time
                        self.entries_var[i-1].set(self.default_time)
                    else:
                        one_time = ''
                        for char in entry.get():
                            if char.isdigit():
                                one_time += char
                        self.entries_vars_current_value[i] = int(one_time)
                elif i == 1 and entry.get() == "Please enter your NTID username":
                    self.entries_vars_current_value[i] = self.entries_vars_default_value[i]
                    self.entries_var[i-1].set(self.entries_vars_default_value[i])
                    self.entries_vars_current_value[i+1] = self.entries_vars_default_value[i+1]
                    self.entries_var[i].set(self.entries_vars_default_value[i+1])
                    i = 3
                    self.root.focus_set()
                else:
                    self.entries_vars_current_value[i] = entry.get()

    # 所有资源和信息确认按钮，启动测试确认件
    def handle_confirm_button(self, event):
        # 提示正在下载驱动，还没有使用自动下载的驱动
        if self.is_installing_driver:
            self.show_driver_download_info()
        # 执行输入框的信息提炼函数
        self.click_confirm_button_to_change_entry_info()

    # 所有资源和信息恢复默认
    def click_cancel_button_to_restore(self):
        # 将所有的输入框恢复可编辑
        for entry in enumerate(self.entries, start=1):
            entry[1].config(state='normal')
        # 浏览器类型和测试项可重新选择
        all_radio_buttons = self.browser_radio_buttons + self.test_item_radio_buttons
        for rb in all_radio_buttons:
            rb.config(state=tk.NORMAL)
        # 测试项可使用tab选择的变量
        self.test_item_radio_is_enabled = True
        # 所有准备未就绪
        self.set_input_ready_event(False)
        # 驱动是否可用的状态标志恢复默认
        self.driver_is_good = False
        # 驱动是否完全启动的状态标志恢复默认
        self.driver_fully_booted_is_ok = False
        
    # 所有资源和信息取消按钮，取消测试确认键
    def handle_cancel_button(self, event):
        if self.input_ready_event.is_set() and self.driver_is_good:
            if self.driver_fully_booted_is_ok:
                if messagebox.askokcancel("Note", f"Cancelling will close the currently running web.\n (If you have closed the browser yourself, you can ignore this message.)\n Are you sure you want to cancel?"):
                    self.print_colored("The previous driver has been closed, Please click confirm to retest\n", "YELLOW")
                    print("")
                    self.click_cancel_button_to_restore()
            else:
                messagebox.showinfo("Driver Info - Startup Status(ongoing)", f"The browser is starting up. Please try again later. \n"
                                    "After the startup is complete, you can see the words 'Successfully initialize of WebDriver' on the right.")
        else:
            self.click_cancel_button_to_restore()   

    def handle_enter(self, event):
        self.entries = [self.username_entry, self.password_entry, self.runtimes_entry, self.estimated_time_entry]
        idx = self.entries.index(event.widget)
        if idx < len(self.entries) - 1:
            self.entries[idx + 1].focus_set()
        else:
            self.button_confirm.focus_set()

    def print_colored(self, text, tag=None, i=999):
        while not self.input_ready_event.is_set():
            if self.window_closed:
                sys.exit()
            self.root.update()
        text = text
        if i == 999:
            sys.stdout.write(text, tag)
            return text
        else:
            self.user_input_display = self.entries_vars_current_value[i]
            if i == 0 or i == 4:
                text = text + str(self.user_input_display) + "\n"
            elif i == 2:
                text = text + '*' * len(self.user_input_display) + "\n"
            else:
                text = text + self.user_input_display + "\n"
            sys.stdout.write(text, tag)
            return self.user_input_display

    def create_menu(self):  
        # 创建菜单栏  
        menu_bar = tk.Menu(self.root)  
        self.root.config(menu=menu_bar)  
     
        # 创建文件菜单项  
        file_menu = tk.Menu(menu_bar, tearoff=0)  
        menu_bar.add_cascade(label="File", menu=file_menu)  

        driver_menu = tk.Menu(file_menu, tearoff=0) 
        file_menu.add_command(label="Use default driver", command=self.use_default_driver)
        file_menu.add_cascade(label="Get new driver", menu=driver_menu)
        # 添加获取驱动的选项  
        driver_menu.add_command(label="Open", command=self.get_driver_from_folder)
        driver_menu.add_separator()
        driver_menu.add_command(label="Install", command=self.start_driver_installation_Prepare) 

    def use_default_driver(self):
        if self.input_ready_event.is_set():
            print("您已锁定测试选项,请先单击“cancel”,然后选择")
            return
        if self.is_installing_driver:
            self.show_driver_download_info()
        else:
            self.select_browser_radio()

    def get_driver_from_folder(self): 
        if self.input_ready_event.is_set():
            print("您已锁定测试选项,请先单击“cancel”,然后选择")
            return
        if self.is_installing_driver:
            self.show_driver_download_info()
        else:
            # 打开已经下载好的Edge驱动  
            file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])  
            if file_path:  
                self.driver_path_var.set(file_path)
                if "chrome" in file_path.split("\\")[-1].lower():
                    self.browser_type_var.set(2) 
                else:
                    self.browser_type_var.set(1)
                for rb in self.browser_radio_buttons:
                    rb.config(state=tk.DISABLED)

    def start_driver_installation_Prepare(self):
        if self.input_ready_event.is_set():
            print("您已锁定测试选项,请先单击“cancel”,然后选择")
            return
        if self.is_installing_driver:
            self.show_driver_download_info()
            return
        # 显示下载状态，防止在下载过程中操作错误
        self.is_installing_driver = True
        # 禁用浏览器选择按钮（如果它们之前没有被禁用的话）
        for rb in self.browser_radio_buttons:
            rb.config(state=tk.DISABLED)
        # 在主线程中请求用户是否指定驱动版本
        self.driver_version = simpledialog.askstring("Driver Version", "指定一个版本或者直接点击按钮下载最新版本:")
        self.root.after(0, self.start_driver_installation_threading)

    def start_driver_installation_threading(self):
        # 创建一个守护线程来安装驱动
        thread = threading.Thread(target=self.get_driver_automatically, daemon=True)
        thread.start()

    def get_driver_automatically(self): 
        # 自动下载Edge驱动  
        try:  
            selected_browser = self.browser_type_var.get()
            if selected_browser == 1:  # Edge
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                if self.driver_version:
                    driver_path = EdgeChromiumDriverManager(version=self.driver_version).install() 
                else:
                    driver_path = EdgeChromiumDriverManager().install()    
            else:   #Chrome
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
        finally:
            self.is_installing_driver = False

    def show_success_message(self, driver_path):
        if self.driver_info_dialog is not None:
            self.driver_info_dialog_close()
        messagebox.showinfo("Driver Info - Installation Status(success)", f"Driver installed successfully!\nPath: {driver_path}")
        self.driver_path_var.set(driver_path) 
 
    def show_error_message(self, error_message):
        if self.driver_info_dialog is not None:
            self.driver_info_dialog_close()
        import webbrowser
        error_window = tk.Toplevel(self.root)
        error_window.title("Driver Info - Installation Status(Error)")
        
        first_frame_error_prompt = tk.Frame(error_window)
        first_frame_error_prompt.pack(pady=10)
        if self.driver_version:
            error_text = "Failed to install driver(网络错误或驱动版本格式不对,请检查重试或自行下载后执行File->Get new driver->open):"
        else:
            error_text = "Failed to install driver(网络错误或权限不足,请检查重试或自行下载后执行File->Get new driver->open):"
        error_info_label = tk.Label(first_frame_error_prompt, text=error_text, font=font.Font(weight='bold'))
        error_info_label.pack(side="top", padx=5)
        #error_info = tk.Label(first_frame_error_prompt, text=error_message, fg="red")
        #error_info.pack(side="left", padx=5, pady=2)
        # 使用Text小部件和滚动条显示长错误信息
        error_text_widget = tk.Text(first_frame_error_prompt, wrap="word", height=3, fg="red", font=("Arial", 10))
        error_text_widget.pack(side="left", fill="both", expand=True, padx=5)
        # 插入错误信息并禁用编辑
        error_text_widget.insert("1.0", error_message)
        error_text_widget.config(state="disabled")
        # 添加滚动条
        scroll_bar = tk.Scrollbar(first_frame_error_prompt, command=error_text_widget.yview)
        scroll_bar.pack(side="right", fill="y")
        error_text_widget.config(yscrollcommand=scroll_bar.set)

        second_frame_download_driver = tk.Frame(error_window)
        second_frame_download_driver.pack(pady=10)
        if self.browser_type_var.get() == 1:
            edgedriver_download_label = tk.Label(second_frame_download_driver, text="Download the Edge WebDriver from: >>>", font=font.Font(weight='bold'), justify='left')
            edgedriver_download_label.pack(side="left", padx=5)
            edgedriver_download_link_label = tk.Label(second_frame_download_driver, 
                                                    text="https://developer.microsoft.com/zh-cn/microsoft-edge/tools/webdriver/", 
                                                    fg="blue", cursor="hand2", font=font.Font(size=14))
            edgedriver_download_link_label.pack(side="left")
            edgedriver_download_link_label.bind("<Button-1>", lambda e: webbrowser.open("https://developer.microsoft.com/zh-cn/microsoft-edge/tools/webdriver/"))
        else:
            googledriver_download_label = tk.Label(second_frame_download_driver, text="Download the Chrome WebDriver from: >>>", font=font.Font(weight='bold'), justify='left')
            googledriver_download_label.pack(side="left", padx=5)
            googledriver_download_link1_label = tk.Label(second_frame_download_driver, 
                                                    text="谷歌官网 https://chromedriver.storage.googleapis.com/index.html", 
                                                    fg="blue", cursor="hand2", font=font.Font(size=14))
            googledriver_download_link1_label.pack(pady=2)
            googledriver_download_link1_label.bind("<Button-1>", lambda e: webbrowser.open("https://chromedriver.storage.googleapis.com/index.html"))
            googledriver_download_link2_label = tk.Label(second_frame_download_driver, 
                                                    text="最新版本 https://googlechromelabs.github.io/chrome-for-testing/", 
                                                    fg="blue", cursor="hand2", font=font.Font(size=14))
            googledriver_download_link2_label.pack(pady=2)
            googledriver_download_link2_label.bind("<Button-1>", lambda e: webbrowser.open("https://googlechromelabs.github.io/chrome-for-testing/"))
            googledriver_download_link3_label = tk.Label(second_frame_download_driver, 
                                                    text="阿里镜像站 https://registry.npmmirror.com/binary.html?path=chromedriver/", 
                                                    fg="blue", cursor="hand2", font=font.Font(size=14))
            googledriver_download_link3_label.pack(pady=2)
            googledriver_download_link3_label.bind("<Button-1>", lambda e: webbrowser.open("https://registry.npmmirror.com/binary.html?path=chromedriver/"))

        third_frame_image = tk.Frame(error_window)
        third_frame_image.pack(pady=10)
        try:
            if self.browser_type_var.get() == 1:
                edgedriver_image_path = get_path("assets/edge_driver_install_tutorial.png")  # 替换为您的图片路径
            else:
                edgedriver_image_path = get_path("assets/chrome_driver_install_tutorial.png")  # 替换为您的图片路径
            edgedriver_image = Image.open(edgedriver_image_path)
            edgedriver_image_scale_factor = 0.7
            edgedriver_image = edgedriver_image.resize(
                (int(edgedriver_image.width * edgedriver_image_scale_factor), 
                 int(edgedriver_image.height * edgedriver_image_scale_factor)),
                 Image.LANCZOS
            )  # 调整图片大小以适应窗口
            edgedriver_photo = ImageTk.PhotoImage(edgedriver_image)
            image_label = tk.Label(third_frame_image, image=edgedriver_photo)
            image_label.image = edgedriver_photo  # 保持对图片的引用，防止被垃圾回收
            image_label.pack()
        except Exception as img_error:
            print(f"Failed to load image: {img_error}")
    
    def show_driver_download_info(self):
        if self.driver_info_dialog is not None:
            self.driver_info_dialog.focus_set()
            return
        else:
            self.driver_info_dialog = tk.Toplevel(self.root)
            self.driver_info_dialog.title("Driver Info - Installation Status(ongoing)")

            # 显示文本信息
            text1 = "The driver you requested is being downloaded automatically. Please wait~"
            text2 = f"The driver you are currently using is:    {self.driver_path_var.get()}"
            text3 = "After the driver download is completed, you will be prompted as follows:"
            text4 = "(Similarly, if the download fails, there will also be a prompt.)"
            text1_label = tk.Label(self.driver_info_dialog, text=text1)
            text1_label.pack(pady=5)
            text2_label = tk.Label(self.driver_info_dialog, text=text2)
            text2_label.pack(pady=5)
            text3_label = tk.Label(self.driver_info_dialog, text=text3)
            text3_label.pack(pady=5)
            text4_label = tk.Label(self.driver_info_dialog, text=text4)
            text4_label.pack(pady=5)

            driver_installing_image_path = get_path("assets/driver_install_success.png")
            driver_installing_image = Image.open(driver_installing_image_path)
            driver_installing_image_scale_factor = 0.7
            driver_installing_image = driver_installing_image.resize(
                (int(driver_installing_image.width * driver_installing_image_scale_factor), 
                int(driver_installing_image.height * driver_installing_image_scale_factor)),
                Image.LANCZOS
            )
            driver_installing_photo = ImageTk.PhotoImage(driver_installing_image)
            img_label = tk.Label(self.driver_info_dialog, image=driver_installing_photo)
            img_label.image = driver_installing_photo  # 保持对图片的引用，防止被垃圾回收
            img_label.pack()

            self.driver_info_dialog.protocol("WM_DELETE_WINDOW", self.driver_info_dialog_close)

    def driver_info_dialog_close(self):
        self.driver_info_dialog.destroy()
        self.driver_info_dialog = None

    def select_browser_radio(self):
        # 启用浏览器选择按钮
        for rb in self.browser_radio_buttons:
            rb.config(state=tk.NORMAL)
        selected_browser = self.browser_type_var.get()
        if selected_browser == 1:  # Edge
            get_edge_driver_path = get_path("assets/msedgedriver.exe")
            self.driver_path_var.set(f"Edge默认驱动:    {get_edge_driver_path}") 
        else: # Chrome
            get_Google_driver_path = get_path("assets/msedgedriver1.exe")
            self.driver_path_var.set(f"Google默认驱动:  {get_Google_driver_path}")

    def get_clean_driver_path(self):
        """
        返回当前浏览器的驱动路径。若文件不存在，抛出异常提示
        """
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

    def select_test_item_radio_ok(self, e):
        for rb in self.test_item_radio_buttons:
            rb.config(state=tk.DISABLED)
        self.test_item_radio_is_enabled = False

    def select_test_item_radio_tab(self, e):
        if self.test_item_radio_is_enabled:
            current_value = self.test_item_var.get()
            next_value = current_value + 1 if current_value < len(self.test_items) else 5
            self.test_item_var.set(next_value)
            self.update_estimated_time_entry()

    def on_username_focus_in(self, event):  
        if self.username_var.get() and self.username_var.get()=='Please enter your NTID username':
            if not event.widget.cget("state") == "readonly":
                self.username_var.set("")
      
    def on_username_focus_out(self, event):  
        if not self.username_var.get():  
            self.username_var.set("Please enter your NTID username")
            self.entries_vars_current_value[1] = self.username_var.get()
            self.password_entry.config(fg="black", show="*")
            self.password_var.set("Password")
            self.entries_vars_current_value[2] = self.password_var.get()

    def on_password_focus_in(self, event):
        if self.username_var.get() and not self.username_var.get()=='Please enter your NTID username':
            if self.password_var.get():
                self.password_entry.config(fg="black", show="*")
                if not event.widget.cget("state") == "readonly":
                    self.password_var.set("")
        else:
            self.password_entry.config(fg="red", show="")
            self.password_entry.delete(0, tk.END)  
            self.password_entry.insert(0, "请先输入账户名！")
            self.username_entry.focus_set()   
      
    def on_password_focus_out(self, event):
        if self.username_var.get() and not self.username_var.get()=='Please enter your NTID username':
            if not self.password_var.get():
                self.password_entry.config(fg="black", show="*")
                self.password_var.set("Password")
                self.entries_vars_current_value[2] = self.password_var.get() 
        else:
            self.password_entry.config(fg="red", show="")
            self.password_entry.delete(0, tk.END)  
            self.password_entry.insert(0, "请先输入账户名！")
            self.username_entry.focus_set()

    def on_runtimes_focus_in(self, event):
        if self.runtimes_var.get() and self.runtimes_var.get()=='Please enter the number to loop through':
            if not event.widget.cget("state") == "readonly":
                self.runtimes_var.set("")
      
    def on_runtimes_focus_out(self, event):  
        if not self.runtimes_var.get():  
            self.runtimes_var.set("Please enter the number to loop through")
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
            if not event.widget.cget("state") == "readonly":
                self.estimated_time_var.set("")
                self.entries_vars_current_value[4] = self.default_time
      
    def on_estimated_time_focus_out(self, event):  
        if not self.estimated_time_var.get():
            self.default_time = {1: 3800, 2: 1500, 3: 2300, 4: 2800, 5: 4300}.get(self.test_item_var.get(), 0)
            self.estimated_time_var.set(f"Default one estimated time for test {self.test_items[self.test_item_var.get()]} is {self.default_time}s")
            self.entries_vars_current_value[4] = self.default_time

    def label_on_enter(self, event):
        if self.hover_window is None:
            self.hover_window = tk.Toplevel(self.root)
            self.hover_window.transient(self.root)
            self.hover_window.attributes("-topmost", True)
            self.hover_window.overrideredirect(True)
            self.hover_window.geometry(f"+{self.root.winfo_pointerx()}+{self.root.winfo_pointery()}")
            self.hover_window.lift()

            width, height = self.root.winfo_width(), self.root.winfo_height()
            resized_image = self.original_image.resize((int(width * 0.5), int(height * 0.8)), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized_image)
            self.image_label = tk.Label(self.hover_window, image=self.photo)
            self.image_label.grid()
        self.default_font.config(weight="bold")
        self.estimated_time_label.config(fg="blue", cursor="hand2")        

    def label_on_leave(self, event):
        if self.hover_window is not None:
            self.hover_window.destroy()
            self.hover_window = None
        self.default_font.config(weight="normal")
        self.estimated_time_label.config(fg="black")

    def get_user_input(self, prompt):
        self.input_popup = tk.Toplevel(self.root)
        self.input_popup.title("Input Required")
        self.input_popup.transient(self.root)
        self.input_popup.attributes("-topmost", True)

        #label = tk.Label(input_popup, text=prompt)
        #label.pack(pady=10)
        bg_color = self.input_popup.cget("bg")
        label = tk.Text(self.input_popup, height=2, width=50, wrap="word", bg=bg_color, bd=0, highlightthickness=0)
        label.pack(pady=10)

        def random_color():
            return "#%06x" % random.randint(0, 0xFFFFFF)
        special_texts = ["y/n", "ip", "address/name"]
        
        start_idx = 1.0
        for word in re.split(r"(\s+)", prompt):
            if any(special_word in word.lower() for special_word in special_texts):
                color = random_color()
                label.insert(start_idx, word, ("bold", color, "center"))
            else:
                label.insert(start_idx, word, "center")
            start_idx = label.index(f"{start_idx} + {len(word)}c")

        label.tag_configure("center", justify="center")
        label.tag_configure("bold", font=("Helvetica", 10, "bold"))
        label.tag_configure(color, foreground=random_color())

        label.config(state=tk.DISABLED) 

        user_input = tk.StringVar()

        input_entry = tk.Entry(self.input_popup, textvariable=user_input)
        input_entry.pack(pady=5)
        input_entry.focus_set()

        submit_button = tk.Button(self.input_popup, text="Submit", command=lambda: on_submit())
        submit_button.pack(pady=10)

        def on_submit():
            self.input_popup.destroy()

        def check_input(event=None):
            if user_input.get():
                on_submit()
            else:
                input_entry.focus_set()

        input_entry.bind("<Return>", check_input)

        self.input_popup.wait_window()
        return user_input.get()

class MyError(Exception):       
    pass
class ACPW_Exception(MyError):
    pass
class loop_Exception(MyError):
    pass
class Estimated_Exception(MyError):
    pass

def load_auto_modules(app):
    """
    执行后台任务，并通过队列与主线程通信,用于处理UI界面,并启动web自动测试

    参数：
    app(CLASS): 继承了tk.Tk的App类的实例   

    返回：
    所有次数的解锁结果，最后停留在交互界面
    """

    asd = globals()
    import pysy
    asd.update(locals())
    r.set_completer(rlcompleter.Completer(asd).complete)
    r.parse_and_bind('tab: complete')
    console = code.InteractiveConsole(asd)
    path = get_path('launch_Copy.py')
    console.runcode(r'exec(open(r"{}").read());import Kysy;import sys;sys.ps1 = "\033[1;33m>>>\033[0m "'.format(path))
    
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
            if not app.input_ready_event.is_set():
                # 如果有正在运行的 driver 且 input_ready_event 为 False，则关闭所有打开的浏览器
                if driver is not None:
                    driver.quit()
                    driver = None  # 重置 driver 引用
                # 等待input_ready_event变为True
                app.input_ready_event.wait()
                try:
                    app.root.after(0, lambda: print("The browser is opening, please wait a few seconds..."))
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
                    app.root.after(0, lambda: print("Successfully initialize of WebDriver"))
                    app.driver_fully_booted_is_ok = True
                    return (driver,wait)
                except Exception as e:
                    # 主线程中打印详细的错误信息
                    app.root.after(0, lambda: app.print_colored(f"Error: {e}\n", "RED"))
                    app.root.after(0, lambda: app.print_colored("Browser driver was not started due to an error or missing file.\n", "RED"))
                    app.root.after(0, lambda: print(""))
    
    def input_demand(app):
        while True:
            app.print_colored(f"欢迎使用Genoa xGMI_auto tool \n", "BOLD")
            break

        while True:
            app.print_colored(f"\n")
            try:
                for key,value in app.test_items.items():
                    #if key == 5:
                        #app.print_colored(f"{key}: {value};\n")
                    #else:
                        #app.print_colored(f"{key}: {value};  ")
                    app.print_colored(f"{key}: {value};\n")
                item = app.print_colored("Test item to be run: ", i=0)
                app.print_colored(f"You will run {app.test_items[item]} \n", "GREEN")
                app.input_ready_event(True)

                sdu_username = app.print_colored(f"AMD AC - NTID username: ", i=1)
                sdu_password = app.print_colored(f"AMD PW - Password for user {sdu_username}: ", i=2)
                app.print_colored(f"请稍等，正在校验账户密码...\n")
                try:
                    unlock(sdu_username,sdu_password)
                    result = is_locked()
                    app.print_colored(f"The account && password is correct \n", "GREEN")
                    app.input_ready_event(True)
                except:
                    raise ACPW_Exception
                
                try:
                    num_times_input = app.print_colored("Number to loop through: ", i=3)
                    num_times = ""
                    for char in num_times_input:
                        if char.isdigit():
                            num_times += char
                    num_times = int(num_times)
                    app.print_colored(f"You will run {num_times} times \n", "GREEN")
                    app.input_ready_event(True)
                except:
                    raise loop_Exception

                try:
                    one_time = app.print_colored(f"Approximately run one time(s): ", i=4)
                    if item == 1 and one_time < 3800:
                        app.print_colored(f"--Estimated time is not enough, at least 3800s for GSA Stress \n", "RED")
                        for rb in app.test_item_radio_buttons:
                            rb.config(state=tk.NORMAL)
                            app.test_item_radio_is_enabled = True
                        for entry in [app.username_entry, app.password_entry, app.runtimes_entry, app.estimated_time_entry]:
                            entry.config(state='normal') 
                        app.input_ready_event(False)
                    elif item == 2 and one_time < 1500:
                        app.print_colored(f"--Estimated time is not enough, at least 1500s for 4-Point Parallel^2 Test \n", "RED")
                        for rb in app.test_item_radio_buttons:
                            rb.config(state=tk.NORMAL)
                            app.test_item_radio_is_enabled = True
                        for entry in [app.username_entry, app.password_entry, app.runtimes_entry, app.estimated_time_entry]:
                            entry.config(state='normal')
                        app.input_ready_event(False)
                    elif item == 3 and one_time < 2300:
                        app.print_colored(f"--Estimated time is not enough, at least 2300s for 4-Point Test \n", "RED")
                        for rb in app.test_item_radio_buttons:
                            rb.config(state=tk.NORMAL)
                            app.test_item_radio_is_enabled = True
                        for entry in [app.username_entry, app.password_entry, app.runtimes_entry, app.estimated_time_entry]:
                            entry.config(state='normal')
                        app.input_ready_event(False)
                    elif item == 4 and one_time < 2800:
                        app.print_colored(f"--Estimated time is not enough, at least 2800s for Margin Search(BER9) \n", "RED")
                        for rb in app.test_item_radio_buttons:
                            rb.config(state=tk.NORMAL)
                            app.test_item_radio_is_enabled = True
                        for entry in [app.username_entry, app.password_entry, app.runtimes_entry, app.estimated_time_entry]:
                            entry.config(state='normal')
                        app.input_ready_event(False)
                    elif item == 5 and one_time < 4300:
                        app.print_colored(f"--Estimated time is not enough, at least 4300s for Margin Search(BER10) \n", "RED")
                        for rb in app.test_item_radio_buttons:
                            rb.config(state=tk.NORMAL)
                            app.test_item_radio_is_enabled = True
                        for entry in [app.username_entry, app.password_entry, app.runtimes_entry, app.estimated_time_entry]:
                            entry.config(state='normal')
                        app.input_ready_event(False)
                    else:
                        app.print_colored(f"Your estimated time for test is {one_time}s.\n", "GREEN")
                        app.input_ready_event(True)
                        return sdu_username, sdu_password, num_times, result, one_time, item
                        break
                except:
                    raise Estimated_Exception
                
            except ACPW_Exception as e:
                app.print_colored(f"{e}-- 账号密码错误或者网络已断开，检查后重试\n", "RED")
                for rb in app.test_item_radio_buttons:
                    rb.config(state=tk.NORMAL)
                    app.test_item_radio_is_enabled = True
                for entry in [app.username_entry, app.password_entry, app.runtimes_entry, app.estimated_time_entry]:
                    entry.config(state='normal')
                app.input_ready_event(False)
            except loop_Exception as e:
                app.print_colored(f"{e}-- loop_number invalid, please input a number again \n", "RED")
                for rb in app.test_item_radio_buttons:
                    rb.config(state=tk.NORMAL)
                    app.test_item_radio_is_enabled = True
                for entry in [app.username_entry, app.password_entry, app.runtimes_entry, app.estimated_time_entry]:
                    entry.config(state='normal')
                app.input_ready_event(False)
            except Estimated_Exception as e:
                app.print_colored(f"{e}-- Estimated time is not enough, please input again \n", "RED")
                for rb in app.test_item_radio_buttons:
                    rb.config(state=tk.NORMAL)
                    app.test_item_radio_is_enabled = True
                for entry in [app.username_entry, app.password_entry, app.runtimes_entry, app.estimated_time_entry]:
                    entry.config(state='normal')
                app.input_ready_event(False)
    
    def time_compute(app, time_num, total_sleep_time): 
        first_time = True
        dt_object = datetime.fromtimestamp(time.time())
        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S') 
        app.print_colored(f"run start at {formatted_time} \n", "CYAN")
        start_time = time.time()
        while time.time() - start_time < total_sleep_time:     
            elapsed_time = time.time() - start_time
            time_str = f"{elapsed_time:.2f} seconds"
            if not first_time:
                app.print_colored("\r" + f" This time-{time_num+1} already running {time_str} ") 
            if first_time:  
                app.print_colored(f" This time-{time_num+1} already running {time_str} ")  
                first_time = False  
            time.sleep(1)
        else:
            elapsed_time = time.time() - start_time
            time_str = f"{elapsed_time:.2f} seconds"
            app.print_colored("\r" + f" This time-{time_num+1} already running for {time_str} \n")
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
                            #if val_run_isright():        
                            app.print_colored(f"Successlly run XGMI \n", "GREEN")
                            '''
                            else:
                                app.print_colored(f"KVM canvas unstable \n", "YELLOW")
                                driver.find_element(By.ID, 'cursor_canvas').click()
                                time.sleep(1) 
                                pyautogui.write('./1.sh', interval=0.25)
                                time.sleep(0.5)
                                pyautogui.press('enter')
                            '''
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
                            #if val_run_isright():        
                            app.print_colored(f"Successlly run XGMI \n", "GREEN")
                            '''
                            else:
                                app.print_colored(f"KVM canvas unstable \n", "YELLOW")
                                driver.find_element(By.ID, 'cursor_canvas').click()
                                time.sleep(1) 
                                pyautogui.write('./1.sh', interval=0.25)
                                time.sleep(0.5)
                                pyautogui.press('enter')
                            '''
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
        
    def val_run_isright():
        button_video_menu = wait.until(EC.element_to_be_clickable((By.ID, "button_video_menu")))
        button_video_menu.click()
        capture_screen_button = wait.until(EC.element_to_be_clickable((By.ID, "capture_screen")))
        capture_screen_button.click()
        while True:
            for file in os.listdir(get_path("assets")):
                if ('CaptureScreen' in file) and ('load' not in file):
                    target_image = os.path.normpath(os.path.join(get_path("assets"), file))
                    template_image = get_path('assets/template.jpeg')
                    if find_template_in_image(target_image, template_image):
                        os.remove(target_image)
                        return True
                    else:
                        os.remove(target_image)
                        return False
                        
    def find_template_in_image(target_image_path, template_image_path, threshold=0.85):  
        target_image = cv2.imread(target_image_path, 0)
        template_image = cv2.imread(template_image_path, 0)  
      
        #if target_image is None or template_image is None:  
        #    return False   
      
        res = cv2.matchTemplate(target_image, template_image, cv2.TM_CCOEFF_NORMED)
        #app.print_colored(cv2.minMaxLoc(res))
        loc = np.where(res >= threshold)
        '''
        template_height, template_width = template_image.shape
        for pt in zip(*loc[::-1]): 
            app.print_colored(f"匹配位置: ({pt[0]}, {pt[1]})")
            cv2.rectangle(target_image, pt, (pt[0] + template_width, pt[1] + template_height), (0, 255, 255), 2)     
            cv2.imshow('Matched template', target_image)  
            cv2.waitKey(0)  
            cv2.destroyAllWindows() 
        '''   
        return len(loc[0]) > 0  

    sdu_username, sdu_password, num_times, result, one_time, item = input_demand(app)
    driver, wait = browser_driver_setup(app)
    go_to_ip(app)
    initial_window_handle = operate_browser(app)

    results = []
    for i in range(num_times):
        if i == 0:
            app.print_colored(f"unlock success \n")
            app.print_colored(f'time {i+1} is_locked status is {result} \n')
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
        results.append(result)
        run_xgmi(app,initial_window_handle, item)
        time_compute(app, i, one_time)
        if i == num_times-1:
            break
        ref_Browser(app, initial_window_handle)
    app.print_colored(f"all {num_times}-times status is \n   {results} \n")
    console.interact(banner="Welcome to AMD Go-Pi NDA")

def main():
    root = tk.Tk()
    app = App(root)

    # 替换python自带的终端命令行的input函数，用tk的UI组件输入实现同样的效果   
    builtins = globals()['__builtins__']
    builtins.input = app.get_user_input  

    #threading.Thread(target=load_auto_modules, args=(app,)).start()  # 启动后台线程
    threading.Thread(target=lalala, args=(app,), daemon=True).start()  # 启动后台线程

    root.mainloop()

def lalala(app):
    driver = None
    while True:
        # 检查Event对象的内部标志是否被设置为True
        if not app.input_ready_event.is_set():
            # 如果有正在运行的 driver 且 input_ready_event 为 False，则关闭所有打开的浏览器
            if driver is not None:
                driver.quit()
                driver = None  # 重置 driver 引用
            # 等待input_ready_event变为True
            app.input_ready_event.wait()

            try:
                app.root.after(0, lambda: print("The browser is opening, please wait a few seconds..."))
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
                app.root.after(0, lambda: print("Successfully initialize of WebDriver"))
                app.driver_fully_booted_is_ok = True
                driver.get('https://www.baidu.com')
            except Exception as e:
                # 主线程中打印详细的错误信息
                app.root.after(0, lambda: app.print_colored(f"Error: {e}\n", "RED"))
                app.root.after(0, lambda: app.print_colored("Browser driver was not started due to an error or driver missing/mismatched.\n", "RED"))
                app.root.after(0, lambda: print(""))
                app.click_cancel_button_to_restore()

if __name__ == "__main__":  
    main()
