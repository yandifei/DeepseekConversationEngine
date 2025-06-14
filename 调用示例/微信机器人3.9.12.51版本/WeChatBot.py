# 自己写的库
from time import sleep

from numpy.testing.print_coercion_tables import print_new_cast_table

from wcbo import WeChatBackgroundOperation, Chats

# wc = WeChatBackgroundOperation()
wc = WeChatBackgroundOperation("","", False)
print(f"微信名：{wc.name}\n微信ID：{wc.id}")

# cts = Contacts(wc)  # 创建通讯录对象，传入整个微信客户端对象
# a = cts.find_same_remark_name(0.02,True)

cs = Chats(wc)   # 创建聊天对象，传入整个微信客户端对象
# cs.click() # 点击聊天控件并获得会话列表
# 自动回复逻辑
# while True:
#     if wc.is_new_messages():    # 如果微信有新的消息就处理
#         wc.back_click(wc.chats_button)  # 点击聊天按钮
#         sleep(0.01)
#         wc.back_click(wc.chats_button)  # 再次点击聊天按钮(双击)
#         cs.refresh()    # 刷新控件,点击后都得刷新
#         print(1)
#     else:
#         print("没有消息")

# sleep(1)

wc.back_click(wc.chats_button)  # 点击聊天按钮

wc.back_double_click(wc.chats_button,0.2)  # 再次点击聊天按钮(双击)

# cs.get_message(True)    # 简单获得所有消息，True打印输出
# cs.get_all_message(True)    # 如何不是好友或群聊会有红色警告和报错，参数True是把打印输出

# cs.split_ont_message(True)
# cs.create_record_directory(True)