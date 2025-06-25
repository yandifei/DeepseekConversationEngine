"""Chats.py
聊天管理相关
消息接收和发送
"""
# 系统自带库
import os
from datetime import datetime
from time import sleep
# 第三方库
import uiautomation
# 自己的库
from wcbo import WeChatBackgroundOperation  # 导入微信这个类

class Chats:
    def __init__(self, wechat_client: WeChatBackgroundOperation):
        """聊天管理
        wechat_client : 微信对象
        """
        """会话列表和消息列表"""
        self.wc = wechat_client  # 接收微信这个对象
        try:
            # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0-控件0-控件0(会话列表里面的子控件就是可滚动的列表了)
            # 会话列表控件
            self.chats_list_control = self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[1].GetLastChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl()
            self.chats_list = self.chats_list_control.GetChildren() # 聊天列表
        except AttributeError:
            # print("\033[91m未成功获取聊天列表控件\033[0m")
            pass
        try:
            # 微信-最后控件-控件0-控件2-控件0-控件0-控件0-控件0-最后一个控件-控件0-控件0-消息列表控件-消息列表底下的所有子孩子
            # 消息列表
            self.message_list = self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[2].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetLastChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetChildren()
        except AttributeError:
            # print("\033[91m未成功获取消息列表\033[0m")
            pass
        """编辑窗口"""
        try:    # 这些控件只有在有对话窗口是才会出现
            # 工具栏： 微信-最后控件-控件0-控件2-控件0-控件0-控件0-控件0-最后一个控件-最后一个控件-最后一个控件-控件0-控件0(工具栏)-子孩子(编辑窗口的所有控件)
            self.tool_bar = self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[2].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetLastChildControl().GetLastChildControl().GetLastChildControl().GetFirstChildControl().GetFirstChildControl().GetChildren()
            # 这里少了5、6是因为它们不是按钮而是空格
            self.emoji_button = self.tool_bar[0]        # 表情按钮，工具栏里面的控件0
            self.send_file_button = self.tool_bar[1]    # 发送文件按钮，工具栏里面的控件1
            self.screenshot_button = self.tool_bar[2]   # 截图按钮，工具栏里面的控件2
            self.screenshot_button2 = self.tool_bar[3]  # 截图按钮2，工具栏里面的控件3
            self.chat_history_button = self.tool_bar[4] # 聊天记录按钮，工具栏里面的控件4
            self.voice_chat_button = self.tool_bar[7]   # 语音聊天按钮，工具栏里面的控件5
            self.video_chat_button = self.tool_bar[8]   # 视频聊天按钮，工具栏里面的控件6
            # 发送按钮： 微信-最后控件-控件0-控件2-控件0-控件0-控件0-控件0-最后一个控件-最后一个控件-最后一个控件-控件0-最后一个控件-最后一个控件-控件0
            self.send_button = self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[2].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetLastChildControl().GetLastChildControl().GetLastChildControl().GetFirstChildControl().GetLastChildControl().GetLastChildControl().GetFirstChildControl()
            # 编辑框：微信-最后控件-控件0-控件2-控件0-控件0-控件0-控件0-最后一个控件-最后一个控件-最后一个控件-控件0-控件1(PaneControl)-控件0(编辑控件)
            self.edit_box = self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[2].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetLastChildControl().GetLastChildControl().GetLastChildControl().GetFirstChildControl().GetChildren()[1].GetFirstChildControl()
            self.edit_box2 = self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[2].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetLastChildControl().GetLastChildControl().GetLastChildControl().GetFirstChildControl().GetChildren()[1]
        except AttributeError:
            pass




        """文件记录路径相关"""
        self.message_path = os.path.join(os.getcwd(), f"{self.wc.id}")  # 创建文件夹用来放置当前绑定账号的聊天记录
        # self.file_path = os.path.join(self.message_path, "微信文件")   # 保存文件的路径
        # self.text_path = os.path.join(self.message_path, "聊天记录.txt")   # 文本消息的文本文件路径
        # self.json_path = os.path.join(self.message_path, "聊天记录.json")   # json格式消息的文本文件路径
        """聊天对象相关"""
        self.friends_or_group : None   # 聊天对象标志位，判断是好友聊天还是群聊聊天(0为好友，1为群聊0，如果不是则为False)

    """控件获取点击操作"""
    def click(self, render_time = 1, out = False):
        """点击和获得(刷新)会话列表、消息列表
        参数 ： render_time ： 等待微信控件渲染的时间，默认1秒
        out : 是否输出提示,默认False
        """
        # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0-控件0-控件0(会话列表里面的子控件就是可滚动的列表了)
        self.wc.back_click(self.wc.chats_button)  # 点击聊天按钮
        sleep(render_time)  # 停顿1秒用来微信渲染
        try:
            # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0-控件0-控件0(会话列表里面的子控件就是可滚动的列表了)
            # 聊天列表控件
            self.chats_list_control = self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[1].GetLastChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl()
            self.chats_list = self.chats_list_control.GetChildren()  # 聊天列表
        except AttributeError:
            if out: print("\033[91m未成功获取聊天列表控件\033[0m")
        try:
            # 微信-最后控件-控件0-控件2-控件0-控件0-控件0-控件0-最后一个控件-控件0-控件0-消息列表控件-消息列表底下的所有子孩子
            # 消息列表
            self.message_list = self.message_list = self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[2].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetLastChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetChildren()
        except AttributeError:
            if out: print("\033[91m未成功获取消息列表\033[0m")

    def refresh(self, out = False):
        """获得或刷新消息列表(判断当前聊天窗口是否存在消息)
        注意：如果没有消息，消息列表是没有子控件的
        参数：
        out : 是否打印提示
        返回值：
        没有消息体返回False，有消息体返回True
        """
        # 判断是否有消息控件
        if len(self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[2].GetFirstChildControl().GetChildren()) != 1:
            if out: print("\033[91m当前聊天窗口没有任何消息\033[0m")
            return False
        try:
            # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0-控件0-控件0(会话列表里面的子控件就是可滚动的列表了)
            # 聊天列表控件
            self.chats_list_control = self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[
                1].GetLastChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl()
            self.chats_list = self.chats_list_control.GetChildren()  # 聊天列表
        except AttributeError:
            print("\033[91m未成功获取聊天列表控件\033[0m")
        try:
            # 微信-最后控件-控件0-控件2-控件0-控件0-控件0-控件0-最后一个控件-控件0-控件0-消息列表控件-消息列表底下的所有子孩子
            # 消息列表
            self.message_list = self.message_list = \
            self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[
                2].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetLastChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetChildren()
        except AttributeError:
            print("\033[91m未成功获取消息列表\033[0m")
        return True

    def select_new_message(self, wait_time = 2, out = False):
        """选择回应的消息
        wait_time : 点击后的等待时间，等待渲染完成拿到消息控件，默认2秒
        out : 是否打印提示
        """
        if not self.wc.is_new_messages():   # 没有新的消息
            if out: print("\033[94m没有新消息\033[0m")
            return False
        for control in self.chats_list: # 读取对话列表(对话列表有好友、群聊、订阅号等其他元素)
            if len(control.GetFirstChildControl().GetChildren()) == 3:  # 有三个控件代表有消息(2个控件没消息)
                # 判断是否非好友或群聊(子控件的子控件0是"SessionListItem")
                if control.GetFirstChildControl().GetFirstChildControl().Name == "SessionListItem":
                    self.wc.back_click(control)   # 点击这个控件微信接收这个无效的消息
                    if out: print(f"\033[93m检测到非好友或群聊消息，已进行接收和废弃处理。消息来源：{control.Name}\033[0m")
                    return False    # 这个不是要处理的消息
                self.wc.back_click(control) # 点击有效控件
                if out: print(f"\033[93m接收到：{control.GetFirstChildControl().GetFirstChildControl().Name} 的{control.GetFirstChildControl().GetLastChildControl().Name}条消息\033[0m")
                sleep(wait_time)
                return control  # 返回有效控件
        return False    # 没早到新的消息(会话列表此时改变了就这样)

    """记录保存相关"""
    def create_record_directory(self, out = False):
        """创建文件夹路径
        out : 是否打印输出提示,默认False
        """
        # 以微信号创建文件夹放置聊天记录
        try:
            os.makedirs(self.message_path)
            if out: print(f"微信号:{self.wc.id} 的聊天记录保存在了\t{self.message_path}\t路径下")
        except FileExistsError:  # 路径一定存在且合法
            if out: print(f"{self.message_path}\t路径已存在，微信号: {self.wc.id} 聊天记录将继续存放到该目录中")
        # # 创建微信文件的聊天记录(下载后保存的位置)
        # try:
        #     os.makedirs(self.file_path)
        #     if out: print(f"聊天文件将保存在了\t{self.message_path}\t路径下")
        # except FileExistsError:  # 路径一定存在且合法
        #     if out: print(f"{self.message_path}\t路径已存在，聊天文件将继续存放到该目录中")
        # # 创建微信的聊天文本文件(txt和json文件，json是基础，txt是为了用户方便看)
        # with open(f"{self.text_path}", "w",encoding="utf8") as message_file:    # 创建txt文件
        #     message_file.write(f"微信名：{self.wc.wc_name}\n微信ID：{self.wc.id}")  # 写入信息
        # open(f"{self.json_path}", "w",encoding="utf8").close()  # 创建json文件不写入
        # if out: print("微信号:{self.wc.id} 的聊天记录保存在了\t{self.message_path}\t路径下")


    """消息相关"""
    # @staticmethod
    # def split_ont_message(message_control : uiautomation.Control, out = False):
    #     """单条消息解析(消息体解析)，消息解析的过程会被打需要做try的处理
    #     message_control : 消息体控件(消息列表里面的一个子控件)
    #     out : 是否打印提示
    #     """
    #     one_message = ""    # 构造消息体
    #     def tree_message(message_body_control: uiautomation.Control):
    #         """递归遍历消息体（非时间消息，浪费资源）
    #         参数： message_body_control ： 消息体控件(一条消息的组成)
    #         """
    #         nonlocal one_message    # 确定作用域
    #         for control in message_body_control.GetChildren():  # 解析子控件
    #             if control.GetChildren():   # 有子控件
    #                 tree_message(control)   # 递归解析
    #                 return True
    #             elif control.Name != "":    # 消息组合控件有效
    #                 one_message += control.Name
    #         return True
    #
    #     message_control = message_control.GetFirstChildControl()    # 进入消息体（解析没用的消息控件）
    #     # 先判断是否是时间控件(时间)
    #     if not message_control.GetChildren():    # 时间控件（没有子孩子）
    #         return message_control.Name # 返回时间
    #     else:
    #         tree_message(message_control)  # 非时间的消息体(3个基础控件)
    #         if out: print(one_message)
    #     return one_message

    def get_message(self, out = False):
        """获得消息列表的所有消息(不进行深入解析)
        out : 是否打印输出提示,默认False
        返回值：打印所有消息
        """
        messages = list()  # 所有消息
        for simple_message in self.message_list:    # 仅仅解析简单的消息
            if out : print(simple_message.Name)
            messages.append(simple_message.Name)
        return messages

    @staticmethod
    def tree_message(message_body_control: uiautomation.Control, simple_message):
        """递归遍历消息内容
        参数：
        simple_message : 消息列表表层的消息
        message_body_control ： 消息体控件(一条消息的组成)
        返回值：
        message_content ： 消息内容
        """
        message_content = ""  # 放置真正的消息内容(这里仅有深度解析的消息内容，不包括发送者等)

        # 判断语音消息("[语音]"文本和控件类型)
        # jude_control =  message_body_control.GetLastChildControl().GetFirstChildControl().GetChildren()  # 过滤没用控件，方便到达区别文本的结构（判断子孩子个数）
        if "[语音]" in simple_message and len(message_body_control.GetChildren()) == 2:   # 语音控件没有那么深(2个控件或1个控件)
            message_content += "语音:"
        # 判断引用消息(我的引用和别人的引用在结构上不同)
        elif "引用  的消息 : " in simple_message and (len(message_body_control.GetFirstChildControl().GetFirstChildControl().GetChildren()) == 2 or len(message_body_control.GetChildren()) == 2):   # 文本控件子控件的子控件的子控件没有2个控件
            message_content += "引用:"
        # 判断是否为动画表情
        elif simple_message == "[动画表情]" and len(message_body_control.GetFirstChildControl().GetFirstChildControl().GetChildren()) == 2:   # 文本控件子控件的子控件的子控件没有2个控件
            message_content += "表情:"
        # 判断是否为图片
        elif simple_message == "[图片]" and len(message_body_control.GetFirstChildControl().GetFirstChildControl().GetChildren()) == 2:   # 文本控件子控件的子控件的子控件没有2个控件
            message_content += "图片:"
        # 判断是否为视频
        elif simple_message == "[视频]" and len(message_body_control.GetFirstChildControl().GetFirstChildControl().GetChildren()) == 2:   # 文本控件子控件的子控件的子控件没有2个控件
            message_content += "视频:"
        # 判断是否为文件
        elif simple_message == "[文件]" and len(message_body_control.GetFirstChildControl().GetFirstChildControl().GetChildren()) == 3:   # 文本控件子控件的子控件的子控件没有2个控件
            message_content += "文件:"
        else:   # 其他的全部认为文本
            message_content += "文本:"

        def combine_message(split_message_controls):
            """组合拼接消息内容
            参数： split_message_controls ： 需要分割的消息体控件(一条消息的组成)
            """
            nonlocal message_content  # 确定作用域
            for control in split_message_controls.GetChildren():  # 解析子控件
                if control.GetChildren():  # 有子控件
                    combine_message(control)  # 递归解析
                elif control.Name != "":  # 消息组合控件有效
                    message_content += control.Name
        # 调用递归函数，传入解析控件
        combine_message(message_body_control)
        return message_content

    def get_all_message(self, out = False):
        """获得消息列表所有消息(深度解析，获得人名和分析消息体)
        out : 是否打印输出提示,默认False
        """
        # {
        #    {
        #     "timestamp": "2025-06-11 23:48:57"
        #     "role": "我"
        #     "content": "Hello World"
        #    },
        #    {
        #     "timestamp": "2025-06-11 23:48:57"
        #     "role": "好友"
        #     "content": "你好"
        #    }
        # }

        # 刷新消息列表
        self.message_list = self.message_list = self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[2].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetLastChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetChildren()
        messages = dict()   # 消息字典(时间、发送者、发送消息)
        for  one_message in self.message_list:    # 读取消息列表列表的消息体
            if  one_message.GetFirstChildControl().ControlType == 50020:   # 文本控件(时间)
                if out: print({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": "WeChat",
                    "content": "文本:" + one_message.GetFirstChildControl().Name
                })
            elif len(one_message.GetFirstChildControl().GetChildren()) == 3:     # 系统的“加入群聊消息”、好友的消息、我的消息
                simple_message = one_message.Name   # 拿到简单的消息(消息类型，可被文本消息欺骗)
                # 先判断发送者再详细分析发送的消息
                one_message = one_message.GetFirstChildControl() # 进入有效控件（3个控件）
                if one_message.GetFirstChildControl().ControlType == 50000: # 第一个子孩子为按钮控件(好友发送的消息)
                    # 好友
                    message_content = self.tree_message(one_message.GetChildren()[1].GetLastChildControl(), simple_message)  # 递归解析，跳过再次解析好友名字
                    if out: print({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "role": one_message.GetFirstChildControl().Name,
                        "content": message_content
                    })
                elif one_message.GetLastChildControl().ControlType == 50000:    # 最后一个子孩子为按钮控件(自己发送的消息)
                    # 自己
                    message_content = self.tree_message(one_message.GetChildren()[1].GetLastChildControl(), simple_message)  # 递归解析消息内容控件(为了上面的跳过统一格式)
                    if out: print({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "role": one_message.GetLastChildControl().Name,
                        "content": message_content
                    })
                elif one_message.GetChildren()[1].ControlType == 50020: # 中间为文本控件(系统的“加入群聊消息”)
                    # 系统(加入群聊)
                    if out: print({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "role": "WeChat",
                        "content": "文本:" + one_message.GetChildren()[1].Name
                    })   # 这里中间控件即为解析控件(特殊情况)
            elif len(one_message.GetFirstChildControl().GetChildren()) == 5:    # 系统的“以下是最近消息”
                if out: print({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": "WeChat",
                    "content": "文本:"+ one_message.GetFirstChildControl().GetChildren()[2].Name
                })  # “以下是最近消息”
        return messages




