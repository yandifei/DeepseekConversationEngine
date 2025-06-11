# 自己写的库
from wcbo import WeChatBackgroundOperation, Contacts, Chats

# wc = WeChatBackgroundOperation()
wc = WeChatBackgroundOperation("","", False)
print(f"实验微信名：{wc.wc_name}\n实验微信ID：{wc.wc_id}\n实验微信地区：{wc.wc_area}")

# cts = Contacts(wc)  # 创建通讯录对象，传入整个微信客户端对象
# a = cts.is_same_remark_name(0.02,True)

cs = Chats(wc)   # 创建聊天对象，传入整个微信客户端对象
cs.click() # 点击聊天控件并获得会话列表
cs.get_message_list(True)   # 获得消息列表)

cs.get_message(True)    # 获得所有消息，True打印输出

# cs.split_ont_message(True)