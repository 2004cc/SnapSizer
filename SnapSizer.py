import sys
import time
import pygetwindow as gw
import pyautogui
import keyboard
import threading

# 全局变量，保存所有窗口的状态信息
window_info_list = []
last_shrink_time = 0
last_enlarge_time = 0


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
        screen_width, screen_height = pyautogui.size()  # 获取屏幕大小
        window_width, window_height = window.width, window.height

        # 计算窗口的目标大小和位置，确保窗口不超出屏幕边界
        new_width = screen_width
        new_height = screen_height // 2
        new_x = 0
        new_y = screen_height // 2

        # 确保目标位置不会导致窗口出屏
        if new_y + new_height > screen_height:
            new_y = screen_height - new_height  # 调整位置，防止超出下边界

        # 设置窗口的新尺寸和位置
        window.resizeTo(new_width, new_height)
        window.moveTo(new_x, new_y)

        # 确保窗口处于可见状态
        window.restore()

        print(f"Window moved to lower half: {window.title}")


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
        new_top = 0  # 中心对齐
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


# 增加一个时间间隔（例如 0.5 秒）来防止重复操作
def shrink_window():
    global last_shrink_time
    current_time = time.time()

    if current_time - last_shrink_time < 0.1:  # 如果上次操作时间小于0.5秒，则不再执行
        return

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

        last_shrink_time = current_time  # 更新最后一次缩小的时间


def enlarge_window():
    global last_enlarge_time
    current_time = time.time()

    if current_time - last_enlarge_time < 0.1:  # 如果上次操作时间小于0.5秒，则不再执行
        return

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

        last_enlarge_time = current_time  # 更新最后一次放大的时间


def restore_window():
    window = get_active_window()
    if window:
        # 恢复窗口的大小和位置
        for info in window_info_list:
            if info["id"] == window._hWnd:
                window.resizeTo(info["size"][0], info["size"][1])
                window.moveTo(info["position"][0], info["position"][1])
                print(f"Window {info['title']} restored.")
                return
    else:
        return


def save_or_update_window_state(window):
    # 查找窗口信息是否已存在
    for info in window_info_list:
        if info["id"] == window._hWnd:
            # 如果窗口信息已存在，则不进行更新，只保留首次保存的信息
            return

    # 如果窗口信息不存在，保存窗口信息
    window_info = {
        "title": window.title,
        "id": window._hWnd,  # 唯一标识符
        "center": (window.left + window.width // 2, window.top + window.height // 2),
        "size": (window.width, window.height),
        "position": (window.left, window.top),
    }
    try:
        print(f"Window {window.title} saved.")
    except UnicodeEncodeError:
        print(f"Window with title containing invalid characters saved.")

    window_info_list.append(window_info)  # 保存窗口信息

# 动态监控当前活动窗口，确保窗口信息被保存
def monitor_active_window():
    while True:
        window = get_active_window()
        if window:
            # 只保存首次窗口信息，后续不再更新
            save_or_update_window_state(window)
        # 每隔 0.1 秒检查一次UIJ_+
        time.sleep(0.1)

def on_hotkey_pressed(key):
    if key == 'esc':  # 按 ESC 键时退出程序
        print("Esc key pressed, exiting...")
        sys.exit(0)
    elif key == 'shift+win+up':  # 移动窗口到上半屏
        move_window_to_upper_half()
    elif key == 'shift+win+down':  # 移动窗口到下半屏
        move_window_to_lower_half()
    elif key == 'shift+win+left':  # 移动窗口到左半屏
        move_window_to_left_half()
    elif key == 'shift+win+right':  # 移动窗口到右半屏
        move_window_to_right_half()
    elif key == 'shift+win+space':  # 移动窗口到中间半屏
        move_window_to_middle_half()
    elif key == 'shift+win+u':  # 左上角
        move_window_to_top_left()
    elif key == 'shift+win+i':  # 右上角
        move_window_to_top_right()
    elif key == 'shift+win+j':  # 左下角
        move_window_to_bottom_left()
    elif key == 'shift+win+k':  # 右下角
        move_window_to_bottom_right()
    elif key == 'shift+win+-':  # 缩小窗口
        shrink_window()
    elif key == 'shift+win+=':  # 放大窗口
        enlarge_window()
    elif key == 'shift+win+enter':  # 最大化窗口
        maximize_window()
    elif key == 'shift+win+backspace': #恢复窗口
        restore_window()



# 启动热键监听
keyboard.add_hotkey('esc', on_hotkey_pressed, args=('esc',))

# 启动监控窗口的线程UIJkUIJKUIJK
monitor_thread = threading.Thread(target=monitor_active_window)
monitor_thread.daemon = True  # 设为守护线程，主程序退出时会自动退出
monitor_thread.start()

# 进入主循环，等待用户输入
while True:
    for hotkey in ['shift+win+up', 'shift+win+down', 'shift+win+left', 'shift+win+right',
                   'shift+win+space', 'shift+win+u', 'shift+win+i', 'shift+win+j', 'shift+win+k',
                   'shift+win+-', 'shift+win+=', 'shift+win+enter', 'shift+win+backspace']:
        keyboard.add_hotkey(hotkey, on_hotkey_pressed, args=(hotkey,))

    time.sleep(0.1)
