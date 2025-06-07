import win32con

from wcbo import WeChatBackgroundOperation
from wcbo import Contacts

wc = WeChatBackgroundOperation("","", False)
print(f"实验微信名：{wc.wc_name}\n实验微信ID：{wc.wc_id}\n实验微信地区：{wc.wc_area}")

cts = Contacts(wc)  # 创建通讯录对象，传入整个微信客户端对象


a = cts.is_same_remark_name(True)
# for i in a:
#     print(i)
# cts.get_contacts_controls()   # 获得好友列表控件(获得好友列表按钮)
# for i in cts.contacts_list_control.GetChildren():
#     print(i.GetLegacyIAccessiblePattern().State)
