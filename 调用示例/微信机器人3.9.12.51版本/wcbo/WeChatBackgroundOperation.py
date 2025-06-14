"""微信后台操作(WeChat background operation)
对微信窗口实现基本控制
对消息实现监听或收发
处理添加好友和问题回答
"""
from time import sleep

# 自带的库

# 导入第三方库
import uiautomation
import win32api
import win32gui
import win32con

class WeChatBackgroundOperation:
    """微信后台操作类"""
    def __init__(self, name = None, id = None, init_min_win = True):
        """初始化类
        参数：
        name ： 微信名，默认None(仅在控制多个微信时需要填写)
        id : 微信号，默认None(仅在控制多个微信时需要填写)
        init_min_win : 默认True初始化时最小化窗口(为了方便开发可以改为False)
        """
        """初始化属性定义"""
        self.name = None     # 用户微信名
        self.id = None       # 用户微信号
        self.wc_area = None     # 用户微信地区
        self.hwnd = None        # 窗口句柄
        self.win : uiautomation.WindowControl = None      # 窗口控件对象
        self.init_min_win = init_min_win # 最小化窗口标志位
        self.get_win(name, id)     # 使用方法绑定窗口并录入属性(获得当前微信或从多开的微信中找到指定的微信)
        """标题栏(title_bar)[窗口控制按钮]"""
        # 微信-最后控件-控件0-最后控件-最后控件(工具栏)[里面的子控件就是窗口控制按钮了]
        self.top_button = self.win.GetChildren()[-1].GetChildren()[0].GetChildren()[-1].GetChildren()[-1].GetFirstChildControl()  # 置顶（复合按钮）按钮
        self.min_button = self.top_button.GetNextSiblingControl()  # 最小化按钮
        self.max_button = self.min_button.GetNextSiblingControl()  # 最大化按钮
        self.close_button = self.max_button.GetNextSiblingControl()  # 关闭按钮
        """导航栏(按钮多少可变)"""
        # 微信-最后一格控件-1控件-导航(子控件就是导航栏的按钮了)[这里直接拿所有子控件]
        self.navigation_bar =  self.win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetChildren() # 导航栏
        # 固定控件
        self.avatar_button = self.navigation_bar[0]                                 # 头像按钮
        self.chats_button = self.navigation_bar[1]                                  # 聊天按钮
        self.contacts_button = self.navigation_bar[2]                               # 通讯录按钮
        self.favorites_button = self.navigation_bar[3]                              # 收藏按钮
        self.chat_files_button = self.navigation_bar[4]                             # 聊天文件按钮
        self.mini_programs_button = self.navigation_bar[-3].GetFirstChildControl()  # 小程序面板
        self.file_transfer_button = self.navigation_bar[-2].GetFirstChildControl()  # 手机(文件传输)
        self.settings_button = self.navigation_bar[-1].GetFirstChildControl()       # 设置及其他
        # 额外控件
        self.moments_button : uiautomation.Control = None                # 朋友圈按钮
        self.channels_button : uiautomation.Control = None     # "视频号"
        self.search_button : uiautomation.Control = None     # "搜一搜"
        self.news_button : uiautomation.Control = None # "看一看"
        # 调用方法获得额外的控件
        self.toolbar_button()   # 遍历导航栏额外的控件
        """搜索框(固定的控件按钮)"""
        # 微信-最后一格控件-控件0-控件1-控件0-控件0-最后一格控件-控件0
        self.search_box = self.win.GetLastChildControl().GetFirstChildControl().GetChildren()[1].GetFirstChildControl().GetFirstChildControl().GetLastChildControl().GetFirstChildControl()
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

    def get_win(self, name = None, id = None):
        """绑定获得微信窗口对象
        参数：
        name ： 微信名(默认None)，仅在多开微信时才能用上
        id : 微信号，默认None(仅在控制多个微信时需要填写)
        min_win : 是否最小化窗口,默认True，为了调试可以设置为False
        返回值： 微信窗口对象
        """
        all_win = list() # 存放所有微信窗口
        homonymous_win = list()  # 存放同名的微信窗口
        desktop_wins = uiautomation.GetRootControl().GetChildren()  # 获取当前桌面对象
        for win in desktop_wins:
            # 考虑到上百个微信，这里这种方法处理
            if win.Name != "微信" or win.ClassName != "WeChatMainWndForPC":
                continue    # 跳过
            else:   # 把单个或多个微信窗口控件加入列表
                all_win.append(win)
        if len(all_win) == 0:     # 没有找到任何的微信窗口
            raise EnvironmentError("请检查是否已经登录并打开微信了")
        elif len(all_win) == 1:   # 仅仅有一个微信代表仅仅开了一个微信
            self.hwnd, self.win = all_win[0].NativeWindowHandle, all_win[0]  # 录入窗口对象（这个必须在前）
            if self.init_min_win: win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)  # 是否调用win的api最小化窗口
            self.name, self.id, self.wc_area = self.get_user_info()  # 录入用户属性
            return all_win[0]  # 拿到微信窗口后返回
        elif len(all_win) >= 2:   # 多个微信窗口
            if not name:     # 微信名为空或没填就触发警告(以下需要用到微信名)
                raise ValueError("请填写微信名，检测到微信多开需要微信名进行判断")
            for win in all_win:    # 遍历多个微信的窗口
                # 过滤掉了非微信窗口后，开始过滤非指定账号(微信-最后控件-控件0-控件1(工具栏)-头像按钮(名称是微信名))
                if win.GetChildren()[-1].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().Name == name:
                    homonymous_win.append(win)    # 把符合用户微信名的窗口添加到同名列表
            if len(homonymous_win) == 0:     # 没有这个窗口
                raise EnvironmentError(f"没有找到微信名：{name} 的微信窗口，请检查是否已经登录并打开此微信")
            elif len(homonymous_win) == 1:     # 同名窗口列表为1 代表没有其他同名窗口
                self.hwnd, self.win = homonymous_win[0].NativeWindowHandle, homonymous_win[0] # 录入非同名窗口对象（这个必须在前）
                if self.init_min_win: win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)  # 是否调用win的api最小化窗口
                self.name, self.id, self.wc_area = self.get_user_info()   # 录入用户属性
                return all_win[0]  # 拿到微信窗口后返回
            elif len(homonymous_win) >= 2:   # 有2个微信名相同的微信窗口
                if not id:       # 检测微信号是否填写
                    raise ValueError("请填写微信号，检测到微信多开且有同名需要微信号进行判断")
                for win in homonymous_win:    # 从同微信名的微信窗口中找
                    self.hwnd, self.win = win.NativeWindowHandle, win    # 窗口属性临时传入可疑窗口控件对象(为了下面的方法调用)
                    if self.init_min_win: win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)  # 是否调用win的api最小化窗口
                    self.name, self.id, self.wc_area = self.get_user_info()  # 获得用户信息(最小化窗口)
                    if id == self.id: # 调用方法拿到微信号进行对比
                        return win
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
        # 控件超出基础范围需要最大化拿到所有控件
        if "更多功能" in toolbar_button_dict:       # 解析出了更多按钮这个控件
            self.max_win(self.hwnd)  # 最大化窗口
            if self.init_min_win: self.min_win(self.hwnd) #  最小化窗口(根据属性判断是否开启这个功能)
            toolbar_button_dict.clear() # 清空字典(必须清空，之前的控件录入已经改变了，尤其是更多功能按钮)
            # 重新遍历导航栏的控件
            for control in self.navigation_bar[5:-3]:
                find_deepest_child(control)  # 导航栏的控件扔进递归函数里面解析
        # print(toolbar_button_dict)  # 打印导航栏额外的控件
        if "朋友圈" in toolbar_button_dict:
            self.moments_button = toolbar_button_dict["朋友圈"]  # 朋友圈按钮
        if "视频号" in toolbar_button_dict:
            self.channels_button = toolbar_button_dict["视频号"]  # "视频号"
        if "看一看" in toolbar_button_dict:
            self.news_button = toolbar_button_dict["看一看"]  # "看一看"
        if "搜一搜" in toolbar_button_dict:
                self.search_button = toolbar_button_dict["搜一搜"]  # "搜一搜"

    def get_user_info(self):
        """获得用户信息(最小化窗口)
        参数：
        返回值：
        name ； 微信名
        id ： 微信号
        wc_area ： 地区名
        """
        # 微信-最后一格控件-1控件-导航-1控件(头像按钮avatar_button)
        self.back_click(self.win.GetChildren()[-1].GetChildren()[0].GetChildren()[0].GetChildren()[0])  # 后台点击头像这个按钮
        avatar_win = self.win.GetFirstChildControl() # 获得微信下的第一个窗口(小窗口有的的时候这个就有效)
        # 判断是否是头像窗口(通过类名和标题判断)
        if avatar_win.ClassName == "ContactProfileWnd" and avatar_win.Name == "微信":  # 怕渲染需要时间导致控件无法读取(应该不会吧，想改while)
            # 微信-控件1(微信小窗口)-控件0-控件0-控件0-控件0-控件1(里面的子控件就是需要提取的内容)
            infos_button = avatar_win.GetChildren()[1].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetChildren()[1]
            # 控件1(里面的子控件就是需要提取的内容)-控件0-名字文本控件
            name = infos_button.GetFirstChildControl().GetFirstChildControl().Name
            # 控件1(里面的子控件就是需要提取的内容)-控件1-控件0-有2个控件(2为微信名)
            id = infos_button.GetChildren()[1].GetFirstChildControl().GetChildren()[1].Name
            # 控件1(里面的子控件就是需要提取的内容)-控件1-控件1-有2个控件(2为地方名)
            wc_area = infos_button.GetChildren()[1].GetChildren()[1].GetChildren()[1].Name
            avatar_win.Hide()   # 隐藏头像小窗口
        else:   # 这里干个保险吧
            raise EnvironmentError("读取头像窗口控件失败(关掉窗口或失去焦点就会导致这样)")
        return name, id, wc_area

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
        screen_x, screen_y = control.BoundingRectangle.xcenter(),control.BoundingRectangle.ycenter()
        # 把屏幕坐标转换为客户端坐标（应用窗口的坐标）
        client_x, client_y = win32gui.ScreenToClient(self.hwnd, (screen_x, screen_y))
        # 坐标转换，16位的整数（通常是坐标值）合并成一个32位的长整型值
        long_position = win32api.MAKELONG(client_x, client_y)
        # 模拟鼠标移动到窗口上
        # win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, long_position)
        # 激活窗口
        # win32gui.SendMessage(self.hwnd, win32con.WM_SETFOCUS, 0, 0)
        control.SetFocus()  # 设置焦点(如果不设置焦点窗口就不接收消息)
        # 模拟鼠标按下(窗口句柄和客户端坐标)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        # 模拟鼠标弹起(窗口句柄和客户端坐标)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, long_position)

    def back_double_click(self, control, wait_time = 0.05):
        """向窗口发送双击消息
        参数：control：控件对象
        wait_time : 双机等待时间，默认0.1
        """
        # 获取控件中心x和y的绝对坐标
        screen_x, screen_y = control.BoundingRectangle.xcenter(),control.BoundingRectangle.ycenter()
        # 把屏幕坐标转换为客户端坐标（应用窗口的坐标）
        client_x, client_y = win32gui.ScreenToClient(self.hwnd, (screen_x, screen_y))
        # 坐标转换，16位的整数（通常是坐标值）合并成一个32位的长整型值
        long_position = win32api.MAKELONG(client_x, client_y)
        # 激活窗口
        win32gui.SendMessage(self.hwnd, win32con.WM_SETFOCUS, 0, 0)
        # control.SetFocus()  # 设置焦点激活窗口(如果不设置焦点窗口就不接收消息)
        # 鼠标模拟移动过去
        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, long_position)
        # 模拟鼠标双击(窗口句柄和客户端坐标)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDBLCLK, win32con.MK_LBUTTON, long_position)
        # 模拟鼠标弹起
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, long_position)  # 弹起



    def back_key(self, control, vk_code):
        """后台按键(向窗口发送按键)
        参数：control：控件对象
        vk_code  ： 虚拟按键码
        """
        # 先发送 WM_ACTIVATE 激活窗口再发送 WA_CLICKACTIVE 鼠标激活 (这是必要的一步)
        # win32api.SendMessage(self.hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE,0)
        """位范围	名称	            说明
            0-15	Repeat Count	    按键的重复次数（通常为0，表示首次按下）
            16-23	Scan Code	        按键的硬件扫描码（通过 MapVirtualKey(vk_code, 0) 获取）
            24	    Extended Key	    是否为扩展键（如方向键、功能键等，需设为 1）
            25-28	Reserved	        保留位（必须为0）
            29	    Context Code	    按键时是否按住 Alt 键（0=未按住，1=按住）
            30	    Previous State	    按键之前的状态（0=未按下，1=已按下；KEYUP消息必须设为1）
            31	    Transition State	按键状态转换（0=按下，1=释放；KEYDOWN=0, KEYUP=1）
        """
        # 构建lParam参数
        scan_code = win32api.MapVirtualKey(vk_code, 0)  # 获取扫描码
        # KEYDOWN消息的lParam(32位的消息参数（LONG_PTR类型）)
        lparam_down = (0 << 24) | (scan_code << 16) | 0x1
        # KEYUP消息的lParam（设置第31位表示释放）
        lparam_up = (0x3 << 24) | (scan_code << 16) | 0x1 | 0xC0000000
        control.SetFocus()  # 必须设置焦点(上面的用不了，估计是激活只是激活了整个窗口，没有激活控件)
        # 向微信窗口发送后台消息
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, vk_code, lparam_down)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, vk_code, lparam_up)



    @staticmethod
    def is_wheel(control):
        """判断控件是否支持滚动和滚动是否能用
        control：控件对象
        返回值 ：
        """
        # 50008是滚动控件
        if control.ControlType != 50008 or not control.GetScrollPattern():
            print("控件不支持滚动模式")
            return False
        # 获得滚动接口
        scroll_pattern = control.GetScrollPattern()
        if not scroll_pattern.VerticallyScrollable and not scroll_pattern.HorizontallyScrollable:
            print("垂直滚动和纵向滚动不可用")
            return False
        # 检查垂直滚动是否可用
        if scroll_pattern.VerticallyScrollable:
            print("垂直滚动可用")
        # 检查纵向滚动是否可用
        if scroll_pattern.HorizontallyScrollable:
            print("纵向滚动可用")
        return True

    @staticmethod
    def wheel(control, wheel_time=0.01, direction = "down"):
        """前台列表滚动
        control：控件对象
        wheel_time ： 滚动时间(默认滚动0.01秒)
        direction ： 滚动反向(默认为"down"，向下)，不区分大小写
        """
        if direction == "down".lower():
            control.WheelDown(waitTime=wheel_time)
        else:
            control.WheelUp(waitTime=wheel_time)

    @staticmethod
    def percent_wheel(control, horizontal_percent = -1, vertical_percent = -1):
        """列表百分比滚动（必须要确保控件支持滚动和滚动可用）-1代表不动
        control：控件对象
        horizontal_percent : 横向百分比(1-100)
        vertical_percent : 纵向百分比(1-100)
        """
        # bug就是vertical_percent是浮点数啊！！！！！50%是0.5(AI解答错的，我这里测试成功)
        # 从当前百分比开始位移
        control.GetScrollPattern().SetScrollPercent(horizontal_percent / 100, vertical_percent / 100)


    def back_wheel(self, control, scroll_times = 1, direction = "down"):
        """后台滚轮（ 120 是标准滚动单位）
        参数:
        control：控件对象
        scroll_times ： 滚动次数(默认为1)
        direction ： 滚动方向(默认为"down",向下)
        """
        # 获取控件中心x和y的绝对坐标(不需要转换，本身就是客户端坐标)
        client_x, client_y = control.BoundingRectangle.xcenter(), control.BoundingRectangle.ycenter()
        # 计算向下滚动量 (WHEEL_DELTA = 120 是标准滚动单位)
        scroll_amount = -scroll_times * win32con.WHEEL_DELTA
        # 坐标转换，16位的整数（通常是坐标值）合并成一个32位的长整型值
        long_position = win32api.MAKELONG(client_x, client_y)
        # 构造wParam (高位字是滚动量，低位字是虚拟键状态)
        if not direction.lower():   # 如果参数不是down(不区分大小写)
            scroll_amount = -scroll_amount  # 添加负号反转为正数
        keyboard_key = (scroll_amount << 16) | 0  # 0表示无按键（这个就是按住某个按键）
        control.SetFocus()  # 设置焦点(如果不设置焦点窗口就不接收消息)
        # 给窗口发送滚轮消息
        win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEWHEEL, keyboard_key, long_position)

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
    def min_win(hwnd):
        """最小化窗口
        参数：hwnd ： 需要关闭的窗口的句柄
        """
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    @staticmethod
    def max_win(hwnd):
        """最大化窗口
        参数：hwnd ： 需要关闭的窗口的句柄
        """
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

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
        return bool(self.chats_button.GetLegacyIAccessiblePattern().Value)  # LegacyIAccessible.Value

    def is_new_friend(self):
        """判断通讯录是否有新消息(新好友)
        返回值 ： 如果有消息则返回True，否则返回False
        """
        return bool(self.contacts_button.GetLegacyIAccessiblePattern().Value)

    def is_new_favorites(self):
        """收藏是否有新的消息
        返回值 ： 如果有消息则返回True，否则返回False
        """
        return bool(self.favorites_button.GetLegacyIAccessiblePattern().Value)

    def is_new_chat_files(self):
        """聊天文件是否有新的消息
        返回值 ： 如果有消息则返回True，否则返回False
        """
        return bool(self.chat_files_button.GetLegacyIAccessiblePattern().Value)

    def is_new_moments(self):
        """朋友圈是否有新的消息"""
        return bool(self.moments_button.GetLegacyIAccessiblePattern().Value)

    def is_new_channels(self):
        """视频号是否有新的消息
        返回值 ： 如果有消息则返回True，否则返回False
        """
        return bool(self.channels_button.GetLegacyIAccessiblePattern().Value)

    def is_new_news(self):
        """看一看是否有新的消息
        返回值 ： 如果有消息则返回True，否则返回False
        """
        return bool(self.news_button.GetLegacyIAccessiblePattern().Value)

    def is_new_search(self):
        """搜一搜是否有新的消息
        返回值 ： 如果有消息则返回True，否则返回False
        """
        return bool(self.search_button.GetLegacyIAccessiblePattern().Value)

    def is_new_mini_programs(self):
        """小程序面板是否有新的消息
        返回值 ： 如果有消息则返回True，否则返回False
        """
        return bool(self.mini_programs_button.GetLegacyIAccessiblePattern().Value)

    def is_new_file_transfer(self):
        """手机(文件传输)是否有新的消息
        返回值 ： 如果有消息则返回True，否则返回False
        """
        return bool(self.file_transfer_button.GetLegacyIAccessiblePattern().Value)

    def is_new_settings(self):
        """设置及其他是否有新的消息
        返回值 ： 如果有消息则返回True，否则返回False
        """
        return bool(self.settings_button.GetLegacyIAccessiblePattern().Value)

if __name__ == '__main__':
    wc = WeChatBackgroundOperation("","", False)
    print(f"实验微信名：{wc.name}\n实验微信ID：{wc.id}\n实验微信地区：{wc.wc_area}")












