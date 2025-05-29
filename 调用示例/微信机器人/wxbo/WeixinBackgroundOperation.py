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

class WeixinBackgroundOperation:
    """微信后台操作类"""
    def __init__(self, wx_name = None, wx_id = None):
        """初始化类
        参数：
        wx_name ： 微信名，默认None(仅在控制多个微信时需要填写)
        wx_id : 微信号，默认None(仅在控制多个微信时需要填写)
        """
        """初始化属性定义"""
        self.wx_name = None  # 用户微信名
        self.wx_id = None  # 用户微信号
        self.wx_area = None  # 用户微信地区
        self.hwnd = None  # 窗口句柄
        self.wx_win: uiautomation.Control = None  # 窗口控件对象
        # self.get_wx_win()
        self.hwnd = self.get_hwnd()
        self.wx_win = self.hwnd_find_controls(self.hwnd)

    """属性初始化的相关方法"""

    @staticmethod
    def get_hwnd():
        """获得微信的窗口句柄(当且仅当一个微信才能用)
        返回值： hwnd ： 窗口句柄，如果没有句柄则直接返回错误
        """
        hwnd = win32gui.FindWindow("mmui::MainWindow", "微信")  # 类名和标题
        if not bool(win32gui.IsWindow(hwnd)):  # 判断句柄是否有效
            print(hwnd)
            raise EnvironmentError("请检查是否已经登录并打开微信了")
        return hwnd  # 如果句柄有效就返回句柄

    @staticmethod
    def hwnd_find_controls(hwnd):
        """通过句柄获得窗口控件
        参数： hwnd : 句柄
        返回值： 如果句柄有效则返回控件对象，否则返回None
        """
        if bool(win32gui.IsWindow(hwnd)):  # 判断句柄是否有效
            return uiautomation.ControlFromHandle(hwnd)
        return None

    # def get_wx_win(self, wx_name = None, wx_id = None):
    #     """绑定获得微信窗口对象
    #     参数：
    #     wx_name ： 微信名(默认None)，仅在多开微信时才能用上
    #     wx_id : 微信号，默认None(仅在控制多个微信时需要填写)
    #     返回值： 微信窗口对象
    #     """
    #     all_wx_win = list()  # 存放所有微信窗口
    #     homonymous_wx_win = list()  # 存放同名的微信窗口
    #     desktop_wins = uiautomation.GetRootControl().GetChildren()  # 获取当前桌面对象
    #     for win in desktop_wins:
    #         # 考虑到上百个微信，这里这种方法处理
    #         if win.Name != "微信" or win.ClassName != "WeChatMainWndForPC":
    #             continue  # 跳过
    #         else:  # 把单个或多个微信窗口控件加入列表
    #             all_wx_win.append(win)
    #     if len(all_wx_win) == 0:  # 没有找到任何的微信窗口
    #         raise EnvironmentError("请检查是否已经登录并打开微信了")
    #     elif len(all_wx_win) == 1:  # 仅仅有一个微信代表仅仅开了一个微信
    #         self.hwnd, self.wx_win = all_wx_win[0].NativeWindowHandle, all_wx_win[0]  # 录入窗口对象（这个必须在前）
    #         self.wx_name, self.wx_id, self.wx_area = self.get_user_info(True)  # 录入用户属性
    #         return all_wx_win[0]  # 拿到微信窗口后返回
    #     elif len(all_wx_win) >= 2:  # 多个微信窗口
    #         if not wx_name:  # 微信名为空或没填就触发警告(以下需要用到微信名)
    #             raise ValueError("请填写微信名，检测到微信多开需要微信名进行判断")
    #         for wx_win in all_wx_win:  # 遍历多个微信的窗口
    #             # 过滤掉了非微信窗口后，开始过滤非指定账号(微信-最后控件-控件0-控件1(工具栏)-头像按钮(名称是微信名))
    #             if wx_win.GetChildren()[
    #                 -1].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().Name == wx_name:
    #                 homonymous_wx_win.append(wx_win)  # 把符合用户微信名的窗口添加到同名列表
    #         if len(homonymous_wx_win) == 0:  # 没有这个窗口
    #             raise EnvironmentError(f"没有找到微信名：{wx_name} 的微信窗口，请检查是否已经登录并打开此微信")
    #         elif len(homonymous_wx_win) == 1:  # 同名窗口列表为1 代表没有其他同名窗口
    #             self.hwnd, self.wx_win = homonymous_wx_win[0].NativeWindowHandle, homonymous_wx_win[
    #                 0]  # 录入非同名窗口对象（这个必须在前）
    #             self.wx_name, self.wx_id, self.wx_area = self.get_user_info(True)  # 录入用户属性
    #             return all_wx_win[0]  # 拿到微信窗口后返回
    #         elif len(homonymous_wx_win) >= 2:  # 有2个微信名相同的微信窗口
    #             if not wx_id:  # 检测微信号是否填写
    #                 raise ValueError("请填写微信号，检测到微信多开且有同名需要微信号进行判断")
    #             for wx_win in homonymous_wx_win:  # 从同微信名的微信窗口中找
    #                 self.hwnd, self.wx_win = wx_win.NativeWindowHandle, wx_win  # 窗口属性临时传入可疑窗口控件对象(为了下面的方法调用)
    #                 self.wx_name, self.wx_id, self.wx_area = self.get_user_info(True)  # 获得用户信息(最小化窗口)
    #                 if wx_id == self.wx_id:  # 调用方法拿到微信号进行对比
    #                     return wx_win
    #             raise EnvironmentError(f"请检查微信号是否填写正确，没有找到微信号对得上的窗口，")
    #     return None  # 其他情况就放回空值

    """窗口控制方法"""

    @staticmethod
    def click(control):
        """鼠标瞬移到控件中心点击
        参数：control：控件对象
        """
        uiautomation.Click(control.BoundingRectangle.xcenter(), control.BoundingRectangle.ycenter())

    def back_click(self, control):
        """向窗口发送点击消息
        参数：control：控件对象
        """
        # 获取控件中心x和y的绝对坐标
        screen_x, screen_y = control.BoundingRectangle.xcenter(), control.BoundingRectangle.ycenter()
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

    @staticmethod
    def max_win(hwnd):
        """最大化窗
        参数：
        hwnd ： 需要关闭的窗口的句柄
        """
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

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

if __name__ == '__main__':
    wx = WeixinBackgroundOperation()    # 实例化对象
    print(wx.hwnd)
    wx.top_win(wx.hwnd)
    # wx.close_win(wx.hwnd)
    # print(0x809A2)
