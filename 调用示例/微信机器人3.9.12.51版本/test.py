import uiautomation as auto

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
formats = auto.GetClipboardFormats()
for k, v in formats.items():
    if k == auto.ClipboardFormat.CF_UNICODETEXT:
        print("文本格式：",auto.GetClipboardText())
    elif k == auto.ClipboardFormat.CF_HTML:
        htmlText = auto.GetClipboardHtml()
        print("富文本格式：", htmlText)
    elif k == auto.ClipboardFormat.CF_BITMAP:
        bmp = auto.GetClipboardBitmap()
        print("位图：", bmp)
    # elif k == auto.ClipboardFormat.
    # else:
    #     other = auto.GetClipboardFormats()
    #     print(other)

