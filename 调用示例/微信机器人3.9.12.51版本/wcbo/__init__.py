__author__ = "雁低飞"
__version__ = "1.0.0"



__url = "https://github.com/yandifei/DeepseekConversationEngine"

# 定义包的公共接口
__all__ = ["WeChatBackgroundOperation", "Contacts", "Chats"]
#  初始化导包
from .WeChatBackgroundOperation import WeChatBackgroundOperation    # 导入这个类
from .Contacts import Contacts  # 导入通讯录管理这个类
from .Chats import Chats    # 导入聊天这个类
# """静态方法"""
# import psutil
# def find_pid(process_name):
#     """提供进程名找到进程号
#     参数：
#     process_name ： 进程名
#     返回值：
#     如果有则返回进程ID，无则返回False
#     """
#     for proc in psutil.process_iter(['pid', 'name']):
#         if proc.info['name'] == process_name:
#             return proc.info['pid']
#     return False