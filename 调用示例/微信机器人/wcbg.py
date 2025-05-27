"""微信后台操作(WeChat background operation)
对微信窗口实现基本控制
对消息实现监听或收发
处理添加好友和问题回答
"""
from time import sleep
# 导入第三方库
import uiautomation
import win32api
import win32gui
import win32con

class WeChatBackgroundOperation:
    """微信后台操作类"""
    def __init__(self, wc_name = None, wc_id = None):
        """初始化类
        参数：
        wc_name ： 微信名，默认None(仅在控制多个微信时需要填写)
        wc_id : 微信号，默认None(仅在控制多个微信时需要填写)
        """
        """初始化属性定义"""
        self.wc_win = self.get_wc_win(wc_name, wc_id)        #  获得指定的微信或当前微信
        self.hwnd = self.get_hwnd(wc_name)   # 调用方法获得微信的窗口句柄(填入wc名代表多开微信)
        self.wc_name, self.wc_id, self.wc_area = self.get_user_info(False)   # 获得用户信息(最小化窗口)

        """标题栏(title_bar)[窗口控制按钮]"""
        # 微信-最后控件-控件0-控件0-最后控件-控件1(工具栏)[里面的子控件就是窗口控制按钮了]
        self.top_button = self.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetLastChildControl().GetChildren()[0].GetFirstChildControl()  # 置顶（复合按钮）按钮
        self.min_button = self.top_button.G  # 最小化按钮
        self.max_button = self.min_button.GetNextSiblingControl()  # 最大化按钮
        self.close_button = self.max_button.GetNextSiblingControl()  # 关闭按钮
        """导航栏(共5个按钮)"""
        # 微信-最后一格控件-1控件-导航(子控件就是导航栏的按钮了)
        self.avatar_button = self.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetChildren()[0]   # 头像按钮
        self.chat_button = self.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetChildren()[1]     # 聊天按钮
        self.contacts_button = self.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetChildren()[2] # 通讯录按钮
        self.collect_button = self.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetChildren()[3]  # 收藏按钮
        self.chat_files_button = self.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetChildren()[4]   # 聊天文件按钮
        self.friends_circle_button = self.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetChildren()[5]   # 朋友圈按钮
        self.mini_program_button = self.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetChildren()[6] # 小程序 按钮
        self.phone_button = self.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetChildren()[7]    # 手机(手机文件传输)按钮
        self.settings_and_others_button = self.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetChildren()[8]  # 设置和其他按钮
        """初始化调用的方法"""



    """属性初始化的相关方法"""
    @staticmethod
    def get_hwnd():
        """获得微信的窗口句柄(当且仅当一个微信才能用)
        返回值： hwnd ： 窗口句柄，如果没有句柄则直接返回错误
        """
        hwnd = win32gui.FindWindow("WeChatMainWndForPC", "微信")  # 类名和标题
        if not bool(win32gui.IsWindow(hwnd)):    # 判断句柄是否有效
            raise EnvironmentError("请检查是否已经登录并打开微信了")
        return hwnd # 如果句柄有效就返回句柄

    @staticmethod
    def hwnd_find_controls(hwnd):
        """通过句柄获得窗口控件
        参数： hwnd : 句柄
        返回值： 如果句柄有效则返回控件对象，否则返回None
        """
        if bool(win32gui.IsWindow(hwnd)):  # 判断句柄是否有效
            return uiautomation.ControlFromHandle(hwnd)
        return None

    def get_wc_win(self, wx_name = None, wc_id = None):
        """获得微信窗口对象
        参数：
        wx_name ： 微信名(默认None)，仅在多开微信时才能用上
        wc_id : 微信号，默认None(仅在控制多个微信时需要填写)
        返回值：
        """
        suspicious_wc_win = list() # 存放所有微信名相同的窗口控件对象
        desktop_wins = uiautomation.GetRootControl().GetChildren()  # 获取当前桌面对象
        for win in desktop_wins:
            # 考虑到上百个微信，这里这种方法处理
            if win.Name != "微信" or win.ClassName != "WeChatMainWndForPC":
                continue    # 跳过
            # 过滤掉了非微信窗口后，开始过滤非指定账号(微信-最后控件-控件0-控件1(工具栏)-头像按钮(名称是微信名))
            elif win.GetChildren()[-1].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().Name == wx_name:
                suspicious_wc_win.append(win)
        if len(suspicious_wc_win) == 0:
            raise EnvironmentError("请检查是否已经登录并打开微信了")
        elif len(suspicious_wc_win) == 1:   # 仅仅有











    def get_user_info(self, hide = False):
        """获得用户信息(最小化窗口)
        参数： hide ： 是否最小化窗口
        返回值：
        wc_name ； 微信名
        wc_id ： 微信号
        wc_area ： 地区名
        """
        if hide: win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)    # 调用win的api最小化窗口
        # 微信-最后一格控件-1控件-导航-1控件(头像按钮avatar_button)
        self.back_click(self.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetChildren()[0])  # 后台点击头像这个按钮
        avatar_win = self.wc_win.GetFirstChildControl() # 获得微信下的第一个窗口(小窗口有的的时候这个就有效)
        # 判断是否是头像窗口(通过类名和标题判断)
        if avatar_win.ClassName == "ContactProfileWnd" and avatar_win.Name == "微信":  # 怕渲染需要时间导致控件无法读取(应该不会吧，想改while)
            # 微信-控件1(微信小窗口)-控件0-控件0-控件0-控件0-控件1(里面的子控件就是需要提取的内容)
            infos_button = avatar_win.GetChildren()[1].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetChildren()[1]
            # 控件1(里面的子控件就是需要提取的内容)-控件0-名字文本控件
            wc_name = infos_button.GetFirstChildControl().GetFirstChildControl().Name
            # 控件1(里面的子控件就是需要提取的内容)-控件1-控件0-有2个控件(2为微信名)
            wc_id = infos_button.GetChildren()[1].GetFirstChildControl().GetChildren()[1].Name
            # 控件1(里面的子控件就是需要提取的内容)-控件1-控件1-有2个控件(2为地方名)
            wc_area = infos_button.GetChildren()[1].GetChildren()[1].GetChildren()[1].Name
            avatar_win.Hide()   # 隐藏头像小窗口
        else:   # 这里干个保险吧
            raise EnvironmentError("读取头像窗口控件失败(关掉窗口或失去焦点就会导致这样)")
        return wc_name, wc_id, wc_area

    """窗口控制方法"""
    @staticmethod
    def click(control):
        """鼠标瞬移到控件中心点击
        参数：control：控件对象
        """
        uiautomation.Click(control.BoundingRectangle.xcenter(), control.BoundingRectangle.ycenter())

    def back_click(self,control):
        """向窗口发送点击消息
        参数：control：控件对象
        """
        # 获取控件中心x和y的绝对坐标
        screen_x, screen_y = control.BoundingRectangle.xcenter(),control.BoundingRectangle.ycenter()
        # 把屏幕坐标转换为客户端坐标（应用窗口的坐标）
        client_x, client_y = win32gui.ScreenToClient(self.hwnd, (screen_x, screen_y))
        # 坐标转换，16位的整数（通常是坐标值）合并成一个32位的长整型值
        long_position = win32api.MAKELONG(client_x, client_y)
        control.SetFocus()  # 设置焦点(如果不设置焦点窗口就不接收消息)
        # 模拟鼠标移动到窗口上
        # win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, long_position)
        # 模拟鼠标按下(窗口句柄和客户端坐标)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        # 模拟鼠标弹起(窗口句柄和客户端坐标)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)

    def max_win(self):
        """最大化窗口
        """
        win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)

    @staticmethod
    def close_win(hwnd):
        """关闭窗口（如果输入的不是父窗口则关闭的是子窗口）
        参数：
        hwnd ： 需要关闭的窗口的句柄
        """
        # 发送 WM_CLOSE 消息来请求关闭窗口
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    @staticmethod
    def hide_window(hwnd):
        """通过窗口句柄隐藏窗口
        参数：
        hwnd ： 需要隐藏的窗口的句柄
        """
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)  # 隐藏

    @staticmethod
    def show_window(hwnd):
        """通过窗口句柄显示窗口
        参数：
        hwnd ： 需要显示的窗口的句柄
        """
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)  # 显示

    @staticmethod
    def top_win(hwnd):
        """将窗口置顶
        hwnd ： 窗口的句柄
        """
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,  # 置顶层
            0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
        )

    @staticmethod
    def cancel_top_win(hwnd):
        """取消窗口置顶
        hwnd ： 窗口的句柄
        """
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_NOTOPMOST,  # 取消置顶
            0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
        )

    """消息接收和处理相关方法"""
    def is_new_messages(self):
        """判断是否有新的消息(不仅仅是群和好友的消息，如果开启了消息免打扰则无法获取)
        返回值 ： 如果有消息则返回True，否则返回False
        """
        return bool(self.chat_button.GetLegacyIAccessiblePattern().Value)  # LegacyIAccessible.Value

    def is_new_friend(self):
        """判断通讯录是否有新消息(新好友)"""
        return bool(self.contacts_button.GetLegacyIAccessiblePattern().Value)

    def is_friends_circle(self):
        """朋友圈是否有新的消息"""
        return bool(self.friends_circle_button.GetLegacyIAccessiblePattern().Value)


"""一定要记得写边写代码边写文档"""











"""代码随笔"""

if __name__ == '__main__':
    wc = WeChatBackgroundOperation()
    print(f"实验微信名：{wc.wc_name}\n实验微信ID：{wc.wc_id}\n实验微信地区：{wc.wc_area}")
    print(f"是否有新消息：{"有" if wc.is_new_messages() else "无"}")
    print(f"是否有新朋友：{"有" if wc.is_new_friend() else "无"}")
    # wc.back_click(wc.top_button)