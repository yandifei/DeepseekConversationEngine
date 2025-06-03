from wcbo import WeChatBackgroundOperation
from wcbo import Contacts

wc = WeChatBackgroundOperation("","", False)
print(f"实验微信名：{wc.wc_name}\n实验微信ID：{wc.wc_id}\n实验微信地区：{wc.wc_area}")

cts = Contacts(wc)  # 创建通讯录对象，传入整个微信客户端对象
# while 1:
#     cts.contacts_list_control.SetFocus()
# 获取滚动模式接口

scroll_pattern = cts.contacts_list_control.GetScrollPattern()
if not scroll_pattern:
    print("控件不支持滚动模式")
else:
    print(1)

# 检查垂直滚动是否可用
if not scroll_pattern.VerticallyScrollable:
    print("垂直滚动不可用")
else:
    print(1)

import uiautomation as auto
direction='down'
scroll_type = 'page'
# 执行滚动操作
# 执行滚动操作
for _ in range(1):
    if scroll_type == 'page':
        # 整页滚动
        if direction == 'down':
            scroll_pattern.Scroll(auto.ScrollAmount.LargeIncrement)
        else:  # up
            scroll_pattern.Scroll(auto.ScrollAmount.LargeDecrement)
    else:
        # 逐项滚动
        if direction == 'down':
            scroll_pattern.Scroll(auto.ScrollAmount.SmallIncrement)
        else:  # up
            scroll_pattern.Scroll(auto.ScrollAmount.SmallDecrement)

# wc.back_wheel(cts.contacts_list_control,5,"ip")
# wc.back_click(cts.contacts_list_control)
# cts.record_all_friends(1)