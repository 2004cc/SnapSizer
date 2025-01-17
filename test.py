import tkinter as tk
from tkinter import messagebox
import pygetwindow as gw
import pyautogui
import keyboard
import threading


# 全局变量，保存所有窗口的状态信息
window_info_list = []


# 获取当前活动窗口并调整大小和位置
def get_active_window():
    window = gw.getActiveWindow()
    if window:
        return window
    else:
        print("No active window found.")
        return None


# 上半屏
def move_window_to_upper_half():
    window = get_active_window()
    if window:
        window.resizeTo(pyautogui.size().width, pyautogui.size().height // 2)
        window.moveTo(0, 0)


# 下半屏
def move_window_to_lower_half():
    window = get_active_window()
    if window:
        window.resizeTo(pyautogui.size().width, pyautogui.size().height // 2)
        window.moveTo(0, pyautogui.size().height // 2)


# 左半屏
def move_window_to_left_half():
    window = get_active_window()  # 获取当前活动窗口
    if window:
        window.resizeTo(pyautogui.size().width // 2, pyautogui.size().height)
        window.moveTo(0, 0)


# 右半屏
def move_window_to_right_half():
    window = get_active_window()  # 获取当前活动窗口
    if window:
        window.resizeTo(pyautogui.size().width // 2, pyautogui.size().height)
        window.moveTo(pyautogui.size().width // 2, 0)


# 中间半屏
def move_window_to_middle_half():
    window = get_active_window()
    if window:
        screen_width, screen_height = pyautogui.size()
        new_width = screen_width // 2
        new_height = screen_height

        # 计算新的位置（将窗口置于屏幕的中间）
        new_left = screen_width // 4  # 中心对齐
        new_top = 0                  # 中心对齐
        window.resizeTo(new_width, new_height)
        window.moveTo(new_left, new_top)


# 左上屏（占屏幕的1/4）
def move_window_to_top_left():
    window = get_active_window()
    if window:
        window.resizeTo(pyautogui.size().width // 2, pyautogui.size().height // 2)
        window.moveTo(0, 0)


# 右上屏（占屏幕的1/4）
def move_window_to_top_right():
    window = get_active_window()
    if window:
        window.resizeTo(pyautogui.size().width // 2, pyautogui.size().height // 2)
        window.moveTo(pyautogui.size().width // 2, 0)


# 左下屏（占屏幕的1/4）
def move_window_to_bottom_left():
    window = get_active_window()
    if window:
        window.resizeTo(pyautogui.size().width // 2, pyautogui.size().height // 2)
        window.moveTo(0, pyautogui.size().height // 2)


# 右下屏（占屏幕的1/4）
def move_window_to_bottom_right():
    window = get_active_window()
    if window:
        window.resizeTo(pyautogui.size().width // 2, pyautogui.size().height // 2)
        window.moveTo(pyautogui.size().width // 2, pyautogui.size().height // 2)


# 最大化窗口
def maximize_window():
    window = get_active_window()
    if window:
        window.maximize()



# 缩小窗口
def shrink_window():
    window = get_active_window()
    if window:
        current_width, current_height = window.width, window.height
        # 计算缩小比例（例如 95%）
        scale_factor = 0.95
        # 计算新的窗口尺寸（保持长宽比）
        new_width = int(current_width * scale_factor)
        new_height = int(current_height * scale_factor)

        # 计算当前窗口的中心点
        center_x = window.left + current_width // 2
        center_y = window.top + current_height // 2

        # 调整窗口大小
        window.resizeTo(new_width, new_height)

        # 将窗口移动到新的中心位置
        window.moveTo(center_x - new_width // 2, center_y - new_height // 2)

        # 确保窗口内部内容不被影响：这里的逻辑可以保证只调整窗口的大小
        # 确保不影响 GUI 元素如字体、按钮等（在 tkinter 中确保不会缩放组件）


def enlarge_window():
    window = get_active_window()
    if window:
        current_width, current_height = window.width, window.height
        # 计算放大比例（例如 105%）
        scale_factor = 1.05
        # 计算新的窗口尺寸（保持长宽比）
        new_width = int(current_width * scale_factor)
        new_height = int(current_height * scale_factor)

        # 计算当前窗口的中心点
        center_x = window.left + current_width // 2
        center_y = window.top + current_height // 2

        # 调整窗口大小
        window.resizeTo(new_width, new_height)

        # 将窗口移动到新的中心位置
        window.moveTo(center_x - new_width // 2, center_y - new_height // 2)

        # 确保窗口内部内容不被影响：同样，确保不会影响窗口内的组件和内容


# 保存窗口的状态信息
def save_window_state(window):
    # 判断当前窗口是否已经存在于列表中
    for info in window_info_list:
        if info["id"] == window._hWnd:
            # 如果窗口信息已保存，就直接返回
            print(f"Window {info['title']} is already saved.")
            return

    # 如果窗口没有保存，保存窗口信息
    window_info = {
        "title": window.title,
        "id": window._hWnd,  # 唯一标识符
        "center": (window.left + window.width // 2, window.top + window.height // 2),
        "size": (window.width, window.height),
        "position": (window.left, window.top)
    }
    window_info_list.append(window_info)  # 保存窗口信息
    print(f"Window {window.title} saved.")


# 恢复窗口状态
def restore_window():
    window = get_active_window()
    if window:
        # 查找窗口信息
        for info in window_info_list:
            if info["id"] == window._hWnd:
                # 恢复窗口的大小和位置
                window.resizeTo(info["size"][0], info["size"][1])
                window.moveTo(info["position"][0], info["position"][1])

                # 将该窗口从列表中删除
                window_info_list.remove(info)

                print(f"Window {info['title']} restored and removed from list.")
                return

        messagebox.showinfo("Window Not Found", "Window information not found in the list.")




# 图形界面类
class WindowResizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Window Resizer")

        # 获取屏幕的尺寸
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # 设置窗口的初始尺寸
        window_width = 1280
        window_height = 720

        # 计算窗口的位置，使其居中
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        # 设置窗口的尺寸和位置
        self.master.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        # 设置最大和最小尺寸
        self.master.maxsize(screen_width, screen_height)
        self.master.minsize(160, 90)

        # 设置窗口的内容
        self.label = tk.Label(master, text="This window is used for testing.", font=("Arial", 16), anchor="center")
        self.label.pack(side="top", anchor="center", pady=10)

        # 每次点击更新活动窗口并保存其信息
        self.master.bind("<Button-1>", self.on_window_click)  # 鼠标左键点击事件，保存窗口信息

    def on_window_click(self, event):
        window = get_active_window()
        if window:
            # 如果是第一次点击该窗口，保存窗口信息
            save_window_state(window)


# 快捷键监听部分
def listen_for_hotkeys():
    # 快捷键绑定到相应的操作
    keyboard.add_hotkey('shift+win+left', move_window_to_left_half)
    keyboard.add_hotkey('shift+win+right', move_window_to_right_half)
    keyboard.add_hotkey('shift+win+up', move_window_to_upper_half)
    keyboard.add_hotkey('shift+win+down', move_window_to_lower_half)
    keyboard.add_hotkey('shift+win+space', move_window_to_middle_half)
    keyboard.add_hotkey('shift+win+U', move_window_to_top_left)
    keyboard.add_hotkey('shift+win+I', move_window_to_top_right)
    keyboard.add_hotkey('shift+win+J', move_window_to_bottom_left)
    keyboard.add_hotkey('shift+win+K', move_window_to_bottom_right)
    keyboard.add_hotkey('shift+win+enter', maximize_window)
    keyboard.add_hotkey('shift+win+-', shrink_window)
    keyboard.add_hotkey('shift+win+=', enlarge_window)
    keyboard.add_hotkey('shift+win+backspace', restore_window)

    keyboard.wait('esc')  # 按 'esc' 退出监听


# 启动图形界面
def start_gui():
    root = tk.Tk()
    app = WindowResizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    # 启动快捷键监听线程
    hotkey_thread = threading.Thread(target=listen_for_hotkeys)
    hotkey_thread.daemon = True
    hotkey_thread.start()

    # 启动图形界面
    start_gui()

