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
        self.attributes('-alpha', 0.5)  # 设置窗口半透明
        self.attributes('-topmost', True)  # 设置窗口始终位于顶部
        self.geometry('%dx%d+%d+%d' % (WINDOW_WIDTH, BUTTON_HEIGHT*2, (self.winfo_screenwidth()-WINDOW_WIDTH)/2, BUTTON_HEIGHT+10))  # 设置窗口大小
        self.config(background='black')  # 设置框架黑色
        self.extended = False  # 是否展开,初始为没有

        # 显示时间和内存
        self.time_memory_label = tk.Label(self, background='black', foreground='white')  # 显示时间的标签
        self.time_memory_label.place(x=0, y=0, width=WINDOW_WIDTH-SMALL_BUTTON_WIDTH, height=BUTTON_HEIGHT*2)
        self.get_time_memory()  # 获取时间和内存

        # 时间标签可以拖动
        self.time_memory_label.bind('<Button-1>', self.set_pos)
        self.time_memory_label.bind('<B1-Motion>', self.move)

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

    def get_time_memory(self):  # 获取时间和内存
        mem = psutil.virtual_memory()
        total = float(mem.total)/1024**3
        used = float(mem.used)/1024**3
        self.time_memory_label.config(text=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+f'\n内存: {used:.2f}G / {total:.2f}G')  # 更改显示的时间文字
        self.after(1000, self.get_time_memory)  # 一秒后再次执行此函数

    def move(self, event):  # 移动事件
        new_x = self.winfo_x()+event.x-self.click_x
        new_y = self.winfo_y()+event.y-self.click_y
        self.geometry('%dx%d+%d+%d' % (WINDOW_WIDTH, BUTTON_HEIGHT*2+self.extended*self.tool_frame.winfo_height(), new_x, new_y))

    def set_pos(self, event):  # 设置点击位置
        self.click_x, self.click_y = event.x, event.y

    def extend(self, event):  # 展开
        self.extended = not self.extended
        self.attributes('-alpha', 0.8 if self.extended else 0.5)  # 设置窗口透明度
        self.extend_button.config(text='↑' if self.extended else '↓')
        self.geometry('%dx%d' % (WINDOW_WIDTH, BUTTON_HEIGHT*2+self.extended*self.tool_frame.winfo_height()))


if __name__ == '__main__':
    Window().mainloop()
