"""Chats.py
聊天管理相关
消息接收和发送
"""
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
        self.message_list = None # 消息列表



    def click(self, render_time = 1):
        """点击和获得(刷新)会话列表控件
        参数 ： render_time ： 等待微信控件渲染的时间，默认1秒
        """
        # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0-控件0-控件0(会话列表里面的子控件就是可滚动的列表了)
        self.wc.back_click(self.wc.chats_button)  # 点击聊天按钮
        self.chats_list_control = self.wc.wc_win.GetLastChildControl().GetFirstChildControl().GetChildren()[1].GetLastChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl()
        self.message_list = self.chats_list_control.GetChildren()   # 消息列表
        sleep(render_time)    # 停顿1秒用来微信渲染

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
        if len(self.wc.wc_win.GetLastChildControl().GetFirstChildControl().GetChildren()[2].GetFirstChildControl().GetChildren()) != 1:
            if out: print("\033[93m当前聊天窗口没有任何消息\033[0m")
            return False
        # 这里不能指定类型不然会报错
        # 微信-最后控件-控件0-控件2-控件0-控件0-控件0-控件0-最后一个控件-控件0-控件0-消息列表控件-消息列表底下的所有子孩子
        self.message_list = self.wc.wc_win.GetLastChildControl().GetFirstChildControl().GetChildren()[2].GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetLastChildControl().GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().GetChildren()
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

    def get_message(self):
        """获得消息列表的所有消息(不进行深入解析)"""




