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