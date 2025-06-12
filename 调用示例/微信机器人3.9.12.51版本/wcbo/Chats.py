"""Chats.py
聊天管理相关
消息接收和发送
"""
import os
from operator import length_hint
# 系统自带库
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
        self.wc = wechat_client  # 接收微信这个对象
        # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0-控件0-控件0(会话列表里面的子控件就是可滚动的列表了)
        self.chats_list_control: uiautomation.ListControl = None  # 聊太列表控件
        self.message_list_control : uiautomation.ListControl = None # 消息列表控件
        self.message_list : uiautomation.ListControl = None # 消息列表
        """文件记录路径相关"""
        self.message_path = os.path.join(os.getcwd(), f"{self.wc.id}")  # 创建文件夹用来放置当前绑定账号的聊天记录
        # self.file_path = os.path.join(self.message_path, "微信文件")   # 保存文件的路径
        # self.text_path = os.path.join(self.message_path, "聊天记录.txt")   # 文本消息的文本文件路径
        # self.json_path = os.path.join(self.message_path, "聊天记录.json")   # json格式消息的文本文件路径
        """聊天对象相关"""
        self.friends_or_group : None   # 聊天对象标志位，判断是好友聊天还是群聊聊天(0为好友，1为群聊0，如果不是则为False)

    """控件获取点击操作"""
    def click(self, render_time = 1):
        """点击和获得(刷新)会话列表控件
        参数 ： render_time ： 等待微信控件渲染的时间，默认1秒
        """
        # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0-控件0-控件0(会话列表里面的子控件就是可滚动的列表了)
        self.wc.back_click(self.wc.chats_button)  # 点击聊天按钮
        self.chats_list_control = self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[1].GetLastChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl()
        self.message_list = self.get_message_list   # 尝试获取消息列表
        sleep(render_time)    # 停顿1秒用来微信渲染

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
    def get_message_list(self, out = False):
        """获得或刷新消息列表(判断当前聊天窗口是否存在消息)
        注意：如果没有消息，消息列表是没有子控件的
        参数：
        out : 是否打印提示
        返回值：
        没有消息体返回False，有消息体返回True
        """
        # 判断是否有消息控件
        if len(self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[2].GetFirstChildControl().GetChildren()) != 1:
            if out: print("\033[93m当前聊天窗口没有任何消息\033[0m")
            return False
        # 这里不能指定类型不然会报错
        # 微信-最后控件-控件0-控件2-控件0-控件0-控件0-控件0-最后一个控件-控件0-控件0-消息列表控件-消息列表底下的所有子孩子
        self.message_list = self.wc.win.GetLastChildControl().GetFirstChildControl().GetChildren()[2].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetLastChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetChildren()
        return True

    @staticmethod
    def split_ont_message(message_control : uiautomation.Control, out = False):
        """单条消息解析(消息体解析)，消息解析的过程会被打需要做try的处理
        message_control : 消息体控件(消息列表里面的一个子控件)
        out : 是否打印提示
        """
        one_message = ""    # 构造消息体
        def tree_message(message_body_control: uiautomation.Control):
            """递归遍历消息体（非时间消息，浪费资源）
            参数： message_body_control ： 消息体控件(一条消息的组成)
            """
            nonlocal one_message    # 确定作用域
            for control in message_body_control.GetChildren():  # 解析子控件
                if control.GetChildren():   # 有子控件
                    tree_message(control)   # 递归解析
                    return True
                elif control.Name != "":    # 消息组合控件有效
                    one_message += control.Name
            return True

        message_control = message_control.GetFirstChildControl()    # 进入消息体（解析没用的消息控件）
        # 先判断是否是时间控件(时间)
        if not message_control.GetChildren():    # 时间控件（没有子孩子）
            return message_control.Name # 返回时间
        else:
            tree_message(message_control)  # 非时间的消息体(3个基础控件)
            if out: print(one_message)
        return one_message

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
        messages = dict()   # 消息字典(时间、发送者、发送消息)
        for  one_message in self.message_list:    # 读取消息列表列表的消息体
            if  one_message.GetFirstChildControl().LocalizedControlType == 50020:   # 文本控件(时间)
                print({"system:": one_message.GetFirstChildControl().Name})
            elif len(one_message.GetFirstChildControl().GetChildren()) == 3:     # 系统的“加入群聊消息”、好友的消息、我的消息
                one_message.GetChildren()
                if one_message.GetChildren()
            elif len(one_message.GetFirstChildControl().GetChildren()) == 5:    # 系统的“以下为新消息”

        return messages




