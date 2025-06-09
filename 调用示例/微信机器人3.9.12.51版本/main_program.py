# 系统库
import sys
import traceback

import win32con
import win32gui

# 第三方库

# 自己写的库
from wcbo import WeChatBackgroundOperation, Contacts, Chats

# wc = WeChatBackgroundOperation()
# wc = WeChatBackgroundOperation("","", False)
# print(f"实验微信名：{wc.wc_name}\n实验微信ID：{wc.wc_id}\n实验微信地区：{wc.wc_area}")

# cts = Contacts(wc)  # 创建通讯录对象，传入整个微信客户端对象
# a = cts.is_same_remark_name(0.02,True)

# cs = Chats(wc)   # 创建聊天对象，传入整个微信客户端对象
# cs.click() # 点击聊天控件并获得会话列表
# cs.get_message_list()   # 获得消息列表
# print(cs.message_list.GetLastChildControl().Name)

# for one_message_control in cs.message_list: #解析整个消息列表
#     cs.split_ont_message(one_message_control,True)  # 单条消息解析
#     print()

# cs.split_ont_message(True)



def exception_hook(all_excepts, value, traceback_obj):
    """捕获未处理的异常
    参数： all_excepts ： 所有的异常类型
    value ： 值
    traceback_obj ： 目标追踪
    """
    # 格式化异常信息
    error_msg = ''.join(traceback.format_exception(all_excepts, value, traceback_obj))
    print("\033[92m=============================以下为错误信息=============================\033[0m")
    print(f"\033[91m{error_msg}\033[0m")
    with open('error.log', 'w') as error_file:   # 写入错误信息
        error_file.write(f"发生错误：\n{error_msg}\n")
    # 退出程序
    # input("\033[93m程序发生异常，优先尝试自行解决，如看不懂错误请把目录下的error.log文件内容给AI或发给作者(QQ邮箱：3058439878@qq.com)。按回车键关闭窗口\033[0m")


# input("测试结束，回车退出")

def get_hwnd():
    """获得微信的窗口句柄(当且仅当一个微信才能用)
    返回值： hwnd ： 窗口句柄，如果没有句柄则直接返回错误
    """
    hwnd = win32gui.FindWindow("WeChatMainWndForPC", "微信")  # 类名和标题
    if not bool(win32gui.IsWindow(hwnd)):  # 判断句柄是否有效
        raise EnvironmentError("请检查是否已经登录并打开微信了")
    return hwnd  # 如果句柄有效就返回句柄

wc_hwnd = get_hwnd()    # 获得窗口句柄
origin_size = win32gui.GetWindowRect(wc_hwnd)  # 初始大小(还原现场使用)
origin_width, origin_height = origin_size[2] - origin_size[0], origin_size[3] - origin_size[1]  # 计算窗口的大小(还原现场使用)
origin_x, origin_y = origin_size[0], origin_size[1] # 初始位置
# 开始隐藏痕迹
point = win32gui.GetWindowRect(wc_hwnd) # 获取窗口左上角和右下角的坐标
win32gui.MoveWindow(wc_hwnd, point[0], point[1], 3840, 2160,False)  # 扩大窗口
size = win32gui.GetWindowRect(wc_hwnd)  # 获取窗口左上角和右下角的坐标
width, height = size[2] - size[0], size[3] - size[1]  # 计算窗口的大小
win32gui.MoveWindow(wc_hwnd, -width, -height, width, height, False) # 移动窗口
win32gui.ShowWindow(wc_hwnd, win32con.SW_SHOW)  # 显示窗口
# win32gui.ShowWindow(wc_hwnd, win32con.SW_MAXIMIZE)  # 最大化窗口
# win32gui.ShowWindow(wc_hwnd, win32con.SW_MINIMIZE)  # 最小化窗口

wc = WeChatBackgroundOperation()
cts = Contacts(wc)
cts.click()
import sys
with open("备注名.txt", "w", encoding="utf8") as file:
    # 重定向stdout到文件
    sys.stdout = file
    sys.excepthook = exception_hook  # 启动报错录入
    cts.find_same_remark_name(0.02,True)

# 还原现场
win32gui.PostMessage(wc_hwnd, win32con.WM_CLOSE, 0, 0)  # 先关闭微信窗口
point = win32gui.GetWindowRect(wc_hwnd) # 获取窗口左上角和右下角的坐标
win32gui.MoveWindow(wc_hwnd, point[0], point[1], origin_width, origin_height,False)  # 恢复窗口大小
width, height = size[2] - size[0], size[3] - size[1]  # 重新计算窗口的大小
win32gui.MoveWindow(wc_hwnd, origin_x, origin_y, origin_width, origin_height, False) # 恢复窗口位置


























