from wcbo import WeChatBackgroundOperation
from wcbo import Contacts

wc = WeChatBackgroundOperation("","", False)
print(f"实验微信名：{wc.wc_name}\n实验微信ID：{wc.wc_id}\n实验微信地区：{wc.wc_area}")




cts = Contacts(wc)  # 创建通讯录对象，传入整个微信客户端对象

# wc.is_wheel(wc.wc_win)
# wc.is_wheel(cts.contacts_list_control)  # 传入通讯录滚动列表控件

# # 获取滚动模式接口

# 设置滚动
wc.percent_wheel(cts.contacts_list_control,-1,1)
cts.contacts_list_control.WheelDown(waitTime=0.01)