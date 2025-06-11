import psutil
import uiautomation as auto
import win32gui

# treeScrollPattern = tree.GetScrollPattern()
# treeScrollPattern.SetScrollPercent(-1,0)
# SetScrollPercent传入的两个参数表示将滚动条移动到指定百分比位置：
# horizontalPercent: 横向位置百分比
# verticalPercent: 纵向位置百分比
# SetScrollPercent(horizontalPercent, verticalPercent)

# 设置文本到剪切板：
# auto.SetClipboardText('Hello World')
# 设置富文本到剪切板：
# auto.SetClipboardHtml('<h1>Title</h1><br><h3>Hello</h3><br><p>test html</p><br>')
# 设置图片到剪切板，只需要将Bitmap设置到剪切板即可，下面演示通过图片文件路径构造Bitmap并设置到剪切板：
# with auto.Bitmap.FromFile(path)as bmp:
#     auto.SetClipboardBitmap(bmp)

# 获取当前剪切板的内容格式：
# formats = auto.GetClipboardFormats()
# print(formats)

# 读取剪切板时，我们可以根据当前剪切板的格式分别作不同的处理：
# formats = auto.GetClipboardFormats()
# for k, v in formats.items():
#     if k == auto.ClipboardFormat.CF_UNICODETEXT:
#         print("文本格式：",auto.GetClipboardText())
#     elif k == auto.ClipboardFormat.CF_HTML:
#         htmlText = auto.GetClipboardHtml()
#         print("富文本格式：", htmlText)
#     elif k == auto.ClipboardFormat.CF_BITMAP:
#         bmp = auto.GetClipboardBitmap()
#         print("位图：", bmp)
    # elif k == auto.ClipboardFormat.
    # else:
    #     other = auto.GetClipboardFormats()
    #     print(other)

# def merge_lists(lists):
#     if not lists:
#         return []
#     result = lists[0][:]  # 复制第一个列表
#     for i in range(1, len(lists)):
#         current_list = lists[i]
#         if not current_list:  # 跳过空列表
#             continue
#         # 计算最大可能的重叠长度
#         max_overlap = min(len(result), len(current_list))
#         overlap = 0
#         # 检查实际重叠长度
#         for j in range(1, max_overlap + 1):
#             if result[-j] != current_list[j - 1]:
#                 break
#             overlap = j  # 更新重叠长度
#         # 添加非重叠部分
#         result.extend(current_list[overlap:])
#     return result
#
# # 测试用例
# list1 = [1, 2, 3, 4, 4, 4]
# list2 = [4, 4, 5, 6, 7, 8, 9]
# list3 = [9, 10, 11, 12]
# lists = [list1, list2, list3]
# merged = merge_lists(lists)
# print(merged)  # 输出: [1, 2, 3, 4, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# a = [1,2,3,4,5,6,6,7,8,9,9,9]
# a = set(a)
# for i in range(2):
#     print(i)
# print(a.index(9))
# def find_pid(process_name):
#     """提供进程名找到进程号"""
#     for proc in psutil.process_iter(['pid', 'name']):
#         if proc.info['name'] == process_name:
#             return proc.info['pid']
#     return False
# a = find_pid("WeChat.exe")
# print(a)


from datetime import datetime

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))