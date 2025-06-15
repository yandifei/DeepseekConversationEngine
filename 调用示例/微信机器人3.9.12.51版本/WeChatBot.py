# 自己写的库
import timeit
from time import sleep
from wcbo import WeChatBackgroundOperation, Chats, Contacts

# wc = WeChatBackgroundOperation()
wc = WeChatBackgroundOperation()
print(f"微信名：{wc.name}\n微信ID：{wc.id}")

# cts = Contacts(wc)  # 创建通讯录对象，传入整个微信客户端对象

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

# wc.back_click(wc.chats_button)  # 点击聊天按钮
cs = Chats(wc)   # 创建聊天对象，传入整个微信客户端对象
cs.click() # 点击聊天控件并获得会话列表
wc.back_double_click(wc.chats_button)  # 再次点击聊天按钮(双击)定位到新消息的对话列表
# 点击新消息的发送者并将返回值进行判断，2是点击后等待时间，True是打印检查新消息的结果
if cs.select_new_message(2,True):
    cs.get_all_message(True)    # 有新信息就深度解析消息体，True打印解析的消息
