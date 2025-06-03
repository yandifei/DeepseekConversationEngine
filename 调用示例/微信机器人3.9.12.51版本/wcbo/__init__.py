__author__ = "雁低飞"
__version__ = "1.0.0"
__url = "https://github.com/yandifei/DeepseekConversationEngine"

# 定义包的公共接口
__all__ = ["WeChatBackgroundOperation","Contacts"]
#  初始化导包
from .WeChatBackgroundOperation import WeChatBackgroundOperation    # 导入这个类
from .Contacts import Contacts  # 导入通讯录管理这个类
