# 系统库
import sys
import traceback
# 第三方库

# 自己写的库
from wcbo import WeChatBackgroundOperation, Contacts, Chats

# wc = WeChatBackgroundOperation()
wc = WeChatBackgroundOperation("","", False)
print(f"实验微信名：{wc.wc_name}\n实验微信ID：{wc.wc_id}\n实验微信地区：{wc.wc_area}")

# cts = Contacts(wc)  # 创建通讯录对象，传入整个微信客户端对象
# a = cts.is_same_remark_name(0.02,True)

cs = Chats(wc)   # 创建聊天对象，传入整个微信客户端对象







































def exception_hook(all_excepts, value, traceback_obj):
    """捕获未处理的异常
    参数： all_excepts ： 所有的异常类型
    value ： 值
    traceback_obj ： 目标追踪
    """
    # 格式化异常信息
    error_msg = ''.join(traceback.format_exception(all_excepts, value, traceback_obj))
    print("\033[92m=============================以下为错误信息=============================\033[0m")
    print(f"\033[91m{error_msg}\033[0m")
    with open('error.log', 'w') as error_file:   # 写入错误信息
        error_file.write(f"发生错误：\n{error_msg}\n")
    # 退出程序
    input("\033[93m程序发生异常，优先尝试自行解决，如看不懂错误请把目录下的error.log文件内容给AI或发给作者(QQ邮箱：3058439878@qq.com)。按回车键关闭窗口\033[0m")

# sys.excepthook = exception_hook # 启动报错遍历
# input("测试结束，回车退出")
