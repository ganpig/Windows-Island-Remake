import subprocess
import time
import tkinter as tk

import psutil

WINDOW_WIDTH = 200
BUTTON_HEIGHT = 30
SMALL_BUTTON_WIDTH = 30
TOOL_LIST = [
    ('命令提示符', 'cmd.exe'),
    ('截图工具', 'snippingtool.exe'),
    ('文件管理器', 'explorer.exe'),
    ('任务管理器', 'taskmgr.exe'),
    ('计算器', 'calc.exe'),
    ('画图', 'mspaint.exe')
]


class Button(tk.Label):
    """
    按钮
    """

    def __init__(self, master, text, command):
        super().__init__(master)
        self.config(text=text, cursor='hand2', background='black', foreground='white')
        self.bind('<Button-1>', command)
        self.bind('<Enter>', lambda x: self.config(background='grey'))
        self.bind('<Leave>', lambda x: self.config(background='black'))


class CmdButton(Button):
    """
    运行命令的按钮
    """

    def __init__(self, master, text, cmdline, x, y):
        self.cmdline = cmdline
        super().__init__(master, text, lambda x: subprocess.Popen(self.cmdline))
        self.place(x=WINDOW_WIDTH//2*x, y=BUTTON_HEIGHT*y, width=WINDOW_WIDTH//2, height=BUTTON_HEIGHT)


class Window(tk.Tk):
    """
    界面
    """

    def __init__(self):
        super().__init__()
        self.overrideredirect(True)  # 设置窗口无边框
        self.attributes('-topmost', True)  # 设置窗口始终位于顶部
        self.config(background='black')  # 设置框架黑色
        self.extended = False  # 是否展开,初始为没有
        self.extend_time = 0  # 上一次展开操作的时间
        self.pos_x = (self.winfo_screenwidth()-WINDOW_WIDTH)//2
        self.pos_y = BUTTON_HEIGHT+10

        # 显示时间和内存
        self.time_memory_label = tk.Label(self, background='black', foreground='white')  # 显示时间的标签
        self.time_memory_label.place(x=0, y=0, width=WINDOW_WIDTH-SMALL_BUTTON_WIDTH, height=BUTTON_HEIGHT*2)

        # 时间标签可以拖动
        self.time_memory_label.bind('<Button-1>', self.on_click)
        self.time_memory_label.bind('<B1-Motion>', self.on_move)

        # 退出按钮
        self.quit_button = Button(master=self, text='×', command=lambda x: self.destroy())
        self.quit_button.place(x=WINDOW_WIDTH-SMALL_BUTTON_WIDTH, y=0, width=SMALL_BUTTON_WIDTH, height=BUTTON_HEIGHT)

        # 展开按钮
        self.extend_button = Button(master=self, text='↓', command=self.extend)
        self.extend_button.place(x=WINDOW_WIDTH-SMALL_BUTTON_WIDTH, y=BUTTON_HEIGHT, width=SMALL_BUTTON_WIDTH, height=BUTTON_HEIGHT)

        # 功能菜单
        self.tool_frame = tk.Frame(self, bg='black')
        self.tool_frame.place(x=0, y=BUTTON_HEIGHT*2, width=WINDOW_WIDTH, height=(len(TOOL_LIST)+1)//2*BUTTON_HEIGHT)

        # 添加功能菜单内容
        for i, (name, command) in enumerate(TOOL_LIST):
            CmdButton(self.tool_frame, name, command, i % 2, i//2)

        self.after(10, self.update_state)

    def update_state(self):  # 刷新窗口状态
        mem = psutil.virtual_memory()
        total = float(mem.total)/1024**3
        used = float(mem.used)/1024**3
        self.time_memory_label.config(text=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+f'\n内存: {used:.2f}G / {total:.2f}G')  # 更改显示的时间文字
        now_time = time.time()
        animation_prog = (min(0.3, now_time-self.extend_time) if self.extended else max(0, 0.3-(now_time-self.extend_time)))/0.3
        self.geometry(f'{WINDOW_WIDTH}x{int(BUTTON_HEIGHT*2+animation_prog*self.tool_frame.winfo_height())}+{self.pos_x}+{self.pos_y}')
        self.attributes('-alpha', 0.5+animation_prog*0.3)  # 设置窗口透明度
        self.after(10, self.update_state)

    def on_click(self, event):  # 点击事件
        self.click_x, self.click_y = event.x, event.y

    def on_move(self, event):  # 移动事件
        self.pos_x = self.winfo_x()+event.x-self.click_x
        self.pos_y = self.winfo_y()+event.y-self.click_y

    def extend(self, event):  # 展开
        now_time = time.time()
        self.extend_time = now_time-(0.3-(now_time-self.extend_time)) if now_time-self.extend_time < 0.3 else now_time
        self.extended = not self.extended
        self.extend_button.config(text='↓↑'[self.extended])


if __name__ == '__main__':
    Window().mainloop()
