"""微信后台操作(WeChat background operation)
对微信窗口实现基本控制
对消息实现监听或收发
处理添加好友和问题回答
"""
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
        self.wc_name = None     # 用户微信名
        self.wc_id = None       # 用户微信号
        self.wc_area = None     # 用户微信地区
        self.hwnd = None        # 窗口句柄
        self.wc_win : uiautomation.Control = None      # 窗口控件对象
        self.get_wc_win(wc_name, wc_id)     # 使用方法绑定窗口并录入属性(获得当前微信或从多开的微信中找到指定的微信)
        """标题栏(title_bar)[窗口控制按钮]"""
        # 微信-最后控件-控件0-控件0-最后控件-控件1(工具栏)[里面的子控件就是窗口控制按钮了]
        # self.top_button = self.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetLastChildControl().GetChildren()[0].GetFirstChildControl()  # 置顶（复合按钮）按钮
        # self.min_button = self.top_button.GetNextSiblingControl()  # 最小化按钮
        # self.max_button = self.min_button.GetNextSiblingControl()  # 最大化按钮
        # self.close_button = self.max_button.GetNextSiblingControl()  # 关闭按钮
        """导航栏(按钮多少可变)"""
        # 微信-最后一格控件-1控件-导航(子控件就是导航栏的按钮了)[这里直接拿所有子控件]
        self.navigation_bar =  self.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetChildren() # 导航栏
        # 遍历固定控件
        self.avatar_button = self.navigation_bar[0]               # 头像按钮
        self.Chats = self.navigation_bar[1]                 # 聊天按钮
        self.Contacts = self.navigation_bar[2]             # 通讯录按钮
        self.Favorites = self.navigation_bar[3]              # 收藏按钮
        self.File_Transfer = self.navigation_bar[4]           # 聊天文件按钮
        self.Mini_Programs = self.navigation_bar[-3]  # 小程序面板
        self.Phone = self.navigation_bar[-2]               # 手机
        self.Settings = self.navigation_bar[-1] # 设置及其他
        # 遍历额外控件
        self.Moments : uiautomation.Control = None   # 朋友圈按钮
        self.Channels : uiautomation.Control = None     # "视频号"
        self.Search : uiautomation.Control = None     # "搜一搜"
        self.News : uiautomation.Control = None # "看一看"
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

    def get_wc_win(self, wc_name = None, wc_id = None):
        """绑定获得微信窗口对象
        参数：
        wc_name ： 微信名(默认None)，仅在多开微信时才能用上
        wc_id : 微信号，默认None(仅在控制多个微信时需要填写)
        返回值： 微信窗口对象
        """
        all_wc_win = list() # 存放所有微信窗口
        homonymous_wc_win = list()  # 存放同名的微信窗口
        desktop_wins = uiautomation.GetRootControl().GetChildren()  # 获取当前桌面对象
        for win in desktop_wins:
            # 考虑到上百个微信，这里这种方法处理
            if win.Name != "微信" or win.ClassName != "WeChatMainWndForPC":
                continue    # 跳过
            else:   # 把单个或多个微信窗口控件加入列表
                all_wc_win.append(win)
        if len(all_wc_win) == 0:     # 没有找到任何的微信窗口
            raise EnvironmentError("请检查是否已经登录并打开微信了")
        elif len(all_wc_win) == 1:   # 仅仅有一个微信代表仅仅开了一个微信
            self.hwnd, self.wc_win = all_wc_win[0].NativeWindowHandle, all_wc_win[0]  # 录入窗口对象（这个必须在前）
            self.wc_name, self.wc_id, self.wc_area = self.get_user_info(True)  # 录入用户属性
            return all_wc_win[0]  # 拿到微信窗口后返回
        elif len(all_wc_win) >= 2:   # 多个微信窗口
            if not wc_name:     # 微信名为空或没填就触发警告(以下需要用到微信名)
                raise ValueError("请填写微信名，检测到微信多开需要微信名进行判断")
            for wc_win in all_wc_win:    # 遍历多个微信的窗口
                # 过滤掉了非微信窗口后，开始过滤非指定账号(微信-最后控件-控件0-控件1(工具栏)-头像按钮(名称是微信名))
                if wc_win.GetChildren()[-1].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().Name == wc_name:
                    homonymous_wc_win.append(wc_win)    # 把符合用户微信名的窗口添加到同名列表
            if len(homonymous_wc_win) == 0:     # 没有这个窗口
                raise EnvironmentError(f"没有找到微信名：{wc_name} 的微信窗口，请检查是否已经登录并打开此微信")
            elif len(homonymous_wc_win) == 1:     # 同名窗口列表为1 代表没有其他同名窗口
                self.hwnd, self.wc_win = homonymous_wc_win[0].NativeWindowHandle, homonymous_wc_win[0] # 录入非同名窗口对象（这个必须在前）
                self.wc_name, self.wc_id, self.wc_area = self.get_user_info(True)   # 录入用户属性
                return all_wc_win[0]  # 拿到微信窗口后返回
            elif len(homonymous_wc_win) >= 2:   # 有2个微信名相同的微信窗口
                if not wc_id:       # 检测微信号是否填写
                    raise ValueError("请填写微信号，检测到微信多开且有同名需要微信号进行判断")
                for wc_win in homonymous_wc_win:    # 从同微信名的微信窗口中找
                    self.hwnd, self.wc_win = wc_win.NativeWindowHandle, wc_win    # 窗口属性临时传入可疑窗口控件对象(为了下面的方法调用)
                    self.wc_name, self.wc_id, self.wc_area = self.get_user_info(True)  # 获得用户信息(最小化窗口)
                    if wc_id == self.wc_id: # 调用方法拿到微信号进行对比
                        return wc_win
                raise EnvironmentError(f"请检查微信号是否填写正确，没有找到微信号对得上的窗口，")
        return None # 其他情况就放回空值

    # 导航栏(按钮多少可变)分析
    def toolbar_button(self):
        """获得导航栏的按钮控件"""
        toolbar_button_dict = dict()    # 控件字典(可变控件)
        def find_deepest_child(control):
            """递归存储最终的按钮控件（导航栏拿到的是最终按钮）
            参数： control ： 控件
            """
            # 如果有子控件就递归遍历
            if len(control.GetChildren()) != 0:
                for child_control in control.GetChildren():
                    find_deepest_child(child_control)    # 传入子控件继续遍历
                    if child_control.Name != "" and child_control.LocalizedControlType == "按钮": # 名字不为空以及是按钮类型
                        toolbar_button_dict[child_control.Name] = child_control   # 传入键值
            else:   # 这里一般为单个控件，即为之开启一个功能
                toolbar_button_dict[control.Name] = control  # 传入键值

        # 微信-最后控件-控件0-控件0(工具栏)[获得所有控件的孩子]
        for control in self.navigation_bar[5:-3]:    # 遍历导航栏控件孩子(跳过前5[第6个开始]和后3控件按钮，因为是固定按钮)
            # 不用担心没有控件导致溢出，没有控件直接不执行for
            find_deepest_child(control) # 导航栏的控件扔进递归函数里面解析
        print(toolbar_button_dict)

        if "更多功能" in toolbar_button_dict:       # 解析出了更多按钮这个控件
            self.max_win(self.hwnd)  # 最大化窗口
            self.min_win(self.hwnd) #  最小化窗口



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

    @staticmethod
    def max_win(hwnd):
        """最大化窗口
        参数：hwnd ： 需要关闭的窗口的句柄
        """
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    @staticmethod
    def min_win(hwnd):
        """最小化窗口
        参数：hwnd ： 需要关闭的窗口的句柄
        """
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    @staticmethod
    def close_win(hwnd):
        """关闭窗口（如果输入的不是父窗口则关闭的是子窗口）
        参数：hwnd ： 需要关闭的窗口的句柄
        """
        # 发送 WM_CLOSE 消息来请求关闭窗口
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    @staticmethod
    def hide_win(hwnd):
        """通过窗口句柄隐藏窗口
        参数：
        hwnd ： 需要隐藏的窗口的句柄
        """
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)  # 隐藏

    @staticmethod
    def show_win(hwnd):
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
        return bool(self.Chats.GetLegacyIAccessiblePattern().Value)  # LegacyIAccessible.Value

    def is_new_friend(self):
        """判断通讯录是否有新消息(新好友)"""
        return bool(self.Contacts.GetLegacyIAccessiblePattern().Value)

    def is_friends_circle(self):
        """朋友圈是否有新的消息"""
        return bool(self.Moments.GetLegacyIAccessiblePattern().Value)


if __name__ == '__main__':
    wc = WeChatBackgroundOperation("","")
    print(f"实验微信名：{wc.wc_name}\n实验微信ID：{wc.wc_id}\n实验微信地区：{wc.wc_area}")
    print(f"是否有新消息：{"有" if wc.is_new_messages() else "无"}")
    print(f"是否有新朋友：{"有" if wc.is_new_friend() else "无"}")
    # wc.back_click(wc.top_button)
    wc.toolbar_button()