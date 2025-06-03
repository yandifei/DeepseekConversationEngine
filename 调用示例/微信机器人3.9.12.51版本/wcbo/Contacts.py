"""contacts.py
用来管理通讯录的属性和方法
添加好友，好友遍历等方法
"""

# 自己的库
from wcbo import WeChatBackgroundOperation  # 导入微信这个类


# 导包

class Contacts:
    def __init__(self, wechat_client : WeChatBackgroundOperation):
        """通讯录管理
        wechat_client : 微信对象
        """
        self.wc = wechat_client  # 接收微信这个对象调用里面最基础的方
        # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0(联系人列表,子控件就是人了)
        self.contacts_list_control = self.wc.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[1].GetChildren()[-1].GetFirstChildControl().GetFirstChildControl()

    def record_all_friends(self,path):
        """记录所有的好友
        path : 保存记录文件的路径
        """
        self.wc.back_click(self.wc.contacts_button) # 点击通讯录按钮


