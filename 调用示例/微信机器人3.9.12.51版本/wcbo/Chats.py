"""Chats.py
聊天管理
消息接收和发送
"""
# 系统自带库
from time import sleep
# 第三方库
import uiautomation
# 自己的库
from wcbo import WeChatBackgroundOperation  # 导入微信这个类

class Chats:
    def __init__(self, wechat_client: WeChatBackgroundOperation):
        """通讯录管理
        wechat_client : 微信对象
        """
        self.wc = wechat_client  # 接收微信这个对象
        # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0(联系人列表,子控件就是人了)
        self.chats_list_control: uiautomation.ListControl = None  # 聊太列表控件

    def get_chats_list_control(self):
        


