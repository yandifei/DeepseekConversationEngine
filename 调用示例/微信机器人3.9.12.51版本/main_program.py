from wcbo import WeChatBackgroundOperation
from wcbo import Contacts

wc = WeChatBackgroundOperation("","", False)
print(f"实验微信名：{wc.wc_name}\n实验微信ID：{wc.wc_id}\n实验微信地区：{wc.wc_area}")




cts = Contacts(wc)  # 创建通讯录对象，传入整个微信客户端对象

# wc.is_wheel(wc.wc_win)
# wc.is_wheel(cts.contacts_list_control)  # 传入通讯录滚动列表控件

# # 获取滚动模式接口
# import time
# cts.contacts_list_control.SetFocus()    # 设置焦点
# time.sleep(1)
# # 设置滚动
# cts.contacts_list_control.GetScrollPattern().SetScrollPercent(-1, 50)

# wc.back_wheel(cts.contacts_list_control)
# wc.wheel(cts.contacts_list_control, 1)
# wc.percent_wheel(cts.contacts_list_control, -1, 50)
cts.find_same_name()