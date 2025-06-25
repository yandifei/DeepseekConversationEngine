# 自己写的库
import timeit
from time import sleep

import uiautomation
import win32con
import win32gui

from wcbo import WeChatBackgroundOperation, Chats, Contacts

# wc = WeChatBackgroundOperation()
wc = WeChatBackgroundOperation("","",False)
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
# wc.back_double_click(wc.chats_button)  # 再次点击聊天按钮(双击)定位到新消息的对话列表
# 点击新消息的发送者并将返回值进行判断，2是点击后等待时间，True是打印检查新消息的结果
# if cs.select_new_message(2,True):
#     cs.get_all_message(True)    # 有新信息就深度解析消息体，True打印解析的消息
# wc.click(cs.edit_box2)
# sleep(1)


# cs.edit_box2.EditControl().GetValuePattern().SetValue("新内容")  #

# edit = cs.edit_box2.EditControl()
# if edit.GetPattern(uiautomation.PatternId.ValuePattern):
#     print(edit.IsEnabled, edit.IsKeyboardFocusable)
#     edit.SetFocus()
#     edit.GetLegacyIAccessiblePattern().SetValue("1111")
#     print("直接设置文本成功")
# else:
#     edit.SendKeys("中文内容", waitTime=0)  # waitTime=0 立即输入

# edit = cs.edit_box2.EditControl()
# if edit.IsEnabled and not edit.GetValuePattern().IsReadOnly:
#             edit.GetValuePattern().SetValue("新内容")
#             print("直接修改成功！")
#
# if edit.Exists(0, 0):
#         pattern = edit.GetLegacyIAccessiblePattern()
#         pattern.SetValue("新内容")
#         print("Legacy方式修改成功！")

# print(edit.NativeWindowHandle)
# new_text = "新内容"
# win32gui.SendMessage(wc.hwnd, win32con.WM_SETTEXT, 0, new_text)
# win32gui.SendMessage(wc.hwnd, win32con.EM_SETSEL, 0, -1)  # 全选文本
# win32gui.SendMessage(wc.hwnd, win32con.EM_REPLACESEL, True, new_text)  # 替换文本
# 方法2：模拟键盘操作（通用）
# else:
# edit.SetFocus()          # 聚焦到输入框
# edit.SendKeys("{Ctrl}a") # 全选
# edit.SendKeys("{DEL}")   # 删除
# edit.SendKeys("新内容")   # 输入新文本
# print("通过键盘模拟修改成功")
edit = cs.edit_box2.EditControl()
new_text = """
# edit = cs.edit_box2.EditControl()
# if edit.GetPattern(uiautomation.PatternId.ValuePattern):
#     print(edit.IsEnabled, edit.IsKeyboardFocusable)
#     edit.SetFocus()
#     edit.GetLegacyIAccessiblePattern().SetValue("1111")
#     print("直接设置文本成功")
# else:
#     edit.SendKeys("中文内容", waitTime=0)  # waitTime=0 立即输入

# edit = cs.edit_box2.EditControl()
# if edit.IsEnabled and not edit.GetValuePattern().IsReadOnly:
#             edit.GetValuePattern().SetValue("新内容")
#             print("直接修改成功！")
#
# if edit.Exists(0, 0):
#         pattern = edit.GetLegacyIAccessiblePattern()
#         pattern.SetValue("新内容")
#         print("Legacy方式修改成功！")

# print(edit.NativeWindowHandle)
# new_text = "新内容"
# win32gui.SendMessage(wc.hwnd, win32con.WM_SETTEXT, 0, new_text)
# win32gui.SendMessage(wc.hwnd, win32con.EM_SETSEL, 0, -1)  # 全选文本
# win32gui.SendMessage(wc.hwnd, win32con.EM_REPLACESEL, True, new_text)  # 替换文本
# 方法2：模拟键盘操作（通用）
# else:
# edit.SetFocus()          # 聚焦到输入框
# edit.SendKeys("{Ctrl}a") # 全选
# edit.SendKeys("{DEL}")   # 删除
# edit.SendKeys("新内容")   # 输入新文本
# print("通过键盘模拟修改成功")
edit = cs.edit_box2.EditControl()
edit.SendKeys("{Ctrl}a{Delete}sdfasdf", waitTime=0.1,interval=0)
"""
edit.SendKeys("{Ctrl}a{Delete}" + f"{new_text}", waitTime=0,interval=0)
