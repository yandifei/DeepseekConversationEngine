"""---------------------------------------------------程序启动动画-----------------------------------------------------"""
try:
    import pyi_splash
    pyi_splash.close()
except ImportError:
    pass
"""---------------------------------------------------导包和导库-----------------------------------------------------"""
# 内置库
import sys
import types
# 第三方库
# 自己的库
from QQMessageMonitor import * # 导包
from deepseek_conversation_engine import DeepseekConversationEngine
uiautomation.SetClipboardText("") # 设置剪切板内容为空避免出现问题(第一次粘贴可能导致大量的文本出现)
all_role_name = "、".join([filename.replace(".txt", "") for filename in os.listdir("提示库/") if filename.endswith(".txt")])     #遍历有效文件
"""--------------------------------------------------需要修改的参数----------------------------------------------------"""
qq_group_name = input("请输入监听的群聊名称(如果有群备注请填备注名):")
qq_monitor_name = input("请输入你的身份(你在QQ群的名称):")
qq_administrator = input("请输入管理员名称(自己是超管，不输入则不设置):")
role = input(f"请输入自动回复的人设(提示库人设:{all_role_name}):")
win_xy = input("请输入QQ窗口窗口的位置(可以不填，默认最左上角[-579,2、-579,582、1919,-579、1919,2、1919,582]):")
win_xy = win_xy.replace("，",",") # 转换，字符
if not win_xy:  # 输入为空
    win_x = win_y = None
else:
    win_x, win_y = win_xy.split(",")
    win_x, win_y = int(win_x), int(win_y)
# qq_group_name = "1"
# qq_monitor_name = "雁低飞"
# qq_administrator = "雁低飞"
# role = "变态猫娘"
# win_x, win_y = 1919,-579
administrator = [qq_monitor_name]  # 设置超级管理员("雁低飞","yandifei")
administrator.append(qq_administrator) if qq_administrator != "" else print("未设置管理员")
"""----------------------------------------------------实例化对象------------------------------------------------------"""
chat_win1 = QQMessageMonitor(qq_group_name, qq_monitor_name)    # 会自动置顶和自动展示(最小化显示)
deepseek = DeepseekConversationEngine(role)  # 实例化对象
"""--------------------------------------------------QQ窗口绑定处理----------------------------------------------------"""
chat_win1.show_win()    # 展示窗口
chat_win1.top_win()     # 置顶窗口
chat_win1.move(win_x, win_y)        # 把窗口移动到最上角 0,1010
print("窗口已放置最左上角并置顶，可通过鼠标拖拽拉伸")
print(f"数据存放路径:\t{chat_win1.message_data_txt}")
for one_message in chat_win1.message_list:  # 打印初次绑定后的消息
    print(one_message)
"""------------------------------------------------------快捷指令------------------------------------------------------"""
# 用来放置参数(必须存在,需要用来判断是否需要参数)
args = None
# 函数映射表(使用lambda来匿名函数)，直接把指点放到环境变量外，防止每次加载的时候都是
function_map = {
    # 特殊指令
    "#兼容": [lambda : deepseek.compatible_openai(),"已经切换至兼容OpenAI的接口","切换中途发生异常"],
    "#测试接口": [lambda : deepseek.use_beat(),"已切换至测试接口","切换中途发生异常"],
    "#初始化": [lambda : deepseek.reset(),"已格式化deepseek对话引擎","初始化中途发生异常"],  # 恢复最开始设置的参数（创建对象时的默认参数）
    # 对话参数调节指令
    "#模型切换": [lambda : deepseek.switch_model(True),lambda : "已切换至V3模型" if deepseek.model_choice == "deepseek-chat" else "已切换至R1模型", "切换中途发生异常"],
    "#V3模型": [lambda : deepseek.set_model("V3"),"已切换至V3模型", "切换中途发生异常"],
    "#R1模型": [lambda : deepseek.set_model("R1"),"已切换至R1模型", "切换中途发生异常"],
    "#评分": [lambda score=50 : deepseek.score_answer(score),"评分成功", "超出打分范围([0-100]分,默认50分)"],
    "#最大token数": [lambda max_tokens=4096 : deepseek.set_max_tokens(max_tokens),lambda : f"已修改最大token数为{deepseek.max_tokens}", "超出最大token数范围([1-8192]分,默认4096)"],
    "#输出格式": [lambda response_format : deepseek.set_response_format(response_format),lambda : f"已修改为{deepseek.response_format}格式", "格式有误，指定模型必须输出的格式为\"text\"或\"json\""],    # input("请输入指定输出格式(text或json,],默认text):")
    "#敏感词": [lambda stop : deepseek.set_stop(stop),lambda : f"添加敏感词 {args} 成功","添加失败"],    # input("设置敏感词(默认为None):")
    "#删除敏感词": [lambda stop: deepseek.del_stop(stop),"删除成功","敏感词不存在"],
    "#流式": [lambda : deepseek.set_stream(True),"已切换至流式输出","切换中途发生异常"],
    "#非流式": [lambda : deepseek.set_stream(),"已切换至流式输出", "切换中途发生异常"],
    "#开启请求统计": [lambda : deepseek.set_stream_options(True),"已开启请求统计", "必须先开启流式(stream)才能开启修改开启这个字段"],
    "#关闭请求统计": [lambda : deepseek.set_stream_options(),"已关闭请求统计", "关闭请求统计途中发生异常"],
    "#温度": [lambda temperature : deepseek.set_temperature(temperature),lambda : f"已修改温度为{deepseek.temperature}", "超出温度范围([0.0-2.0,]默认1.0)"],
    "#核采样": [lambda top_p : deepseek.set_top_p(top_p), lambda : f"已修改核采样为{deepseek.top_p}", "超出核采样范围([0.0-1.0]分,默认1.0)"],   # float(input("请输入核采样,],数值越小内容部分逻越严谨(0.0-1.0,],默认1.0):"))
    "#工具列表": [lambda : deepseek.set_tools(),"修改成功", "修改未成功"],  # input("请输入模型可能会调用的 tool 的列表(默认为None):")
    "#工具开关": [lambda : deepseek.switch_tool_choice(),"已开启工具调用", "已关闭工具调用"],
    "#开启对数概率输出": [lambda : deepseek.set_logprobs(True), "已开启对数概率输出", "开启对数概率失败"],
    "#关闭对数概率输出": [lambda : deepseek.set_logprobs, "已关闭对数概率输出", "关闭对数概率失败"],
    "#位置输出概率": [lambda top_logprobs : deepseek.set_top_logprobs(top_logprobs), lambda : f"已修改概率输出个数为{deepseek.top_logprobs}", "未开启对数概率输出或参数不在调用范围(0-20)"],  # int(input("请指定的每个输出位置返回输出概率top为几的token(0-20，默尔为None):"))
    # FIM对话参数
    "#FIM对话": [True, lambda : deepseek.fill_in_the_middle_ask(), "调用失败"],  # 使用FIM对话补全
    "#FIM补全开头": [lambda prompt : deepseek.set_prompt(prompt),"已补全开头", "补全开头失败"],
    "#FIM完整输出": [lambda : deepseek.set_echo(),"因为服务器那边不接受True，只接受False和None,所以这个功能无效", "因为服务器那边不接受True，只接受False和None,所以这个功能无效"],  # 这个参数就只有False和None了，改不了一点
    "#FIM对数概率输出": [lambda FIM_logprobs : deepseek.set_FIM_logprobs(FIM_logprobs),lambda : f"已制定输出中保留{deepseek.FIM_logprobs}个最可能输出token的对数概率", "参数不在调用范围[0-20]"],  # int(input("请输入需要多少个候选token数量输出对数概率(默认0):"))
    "#FIM补全后缀": [lambda suffix : deepseek.set_suffix(suffix),"已补全后缀", "后缀补全失败"], # input("请输入需要补全的后缀(默认为None):")
    # 上下文参数
    "#思维链": [lambda : deepseek.reasoning_content_output(), lambda : deepseek.reasoning_content,"思维链为空"],  # 会返回False或字符串
    "#对话轮次": [lambda dialog_round : deepseek.set_dialog_history(dialog_round), lambda : "已解除对话轮次限制，注意最大token数和高额消费" if deepseek.clear_flag == -1 else f"已设置对话轮次为{deepseek.clear_flag}轮", "无法设置对话轮次为负数"], # int(input("请输入最大对话轮数，超过自动删除(默认值为5):"))
    "#聊天记录": [lambda : deepseek.print_dialog_history(), lambda : "\n".join(deepseek.print_dialog_history()),"聊天记录为空"],
    "#清空对话历史": [lambda : deepseek.clear_dialog_history(),"已清空对话历史(人设除外)","对话历史为空无需清空"],
    # 多人设管理
    "#人设切换": [lambda role_name : deepseek.role_switch(role_name),lambda : f"已切换人设为：{args}","提示库不存在该人设"],    # input("请输入切换的人设:")
    "#所有人设": [lambda : deepseek.role_list(),lambda : "提示库的所有人设:" + "、".join(deepseek.role_list()), "提示库中为空，不存在任何人设"],  # 人设做了处理
    "#人设查询": [lambda role_name : deepseek.select_role_content(role_name),lambda : deepseek.select_role_content(args), "不存在该人设，无法进行打印"],    # input("请输入要查询的人设:")
    "#当前人设": [lambda : deepseek.print_role_content(),lambda : f"当前人设:{deepseek.role}","当前人设为空"],
    "#人设自定": [lambda role_txt : deepseek.set_role(role_txt),"自定义人设成功", "自定义人设失败"],# input("请输入人设内容:")
    "#删除人设": [lambda : deepseek.remove_role(),"成功删除人设", "未设置人设，不需要进行删除"],
    # 场景关键词自动调控参数
    "#代码": [lambda : deepseek.scene_switch("代码"),"已切换至代码场景","切换场景失败"],
    "#数学": [lambda : deepseek.scene_switch("代码"),"已切换至数学场景","切换场景失败"],
    "#数据": [lambda : deepseek.scene_switch("数据"),"已切换至数据场景","切换场景失败"],
    "#分析": [lambda : deepseek.scene_switch("分析"),"已切换至分析场景","切换场景失败"],
    "#对话": [lambda : deepseek.scene_switch("对话"),"已切换至对话场景","切换场景失败"],
    "#翻译": [lambda : deepseek.scene_switch("翻译"),"已切换至翻译场景","切换场景失败"],
    "#创作": [lambda : deepseek.scene_switch("创作"),"已切换至创作场景","切换场景失败"],
    "#写作": [lambda : deepseek.scene_switch("写作"),"已切换至写作场景","切换场景失败"],
    "#作诗": [lambda : deepseek.scene_switch("作诗"),"已切换至作诗场景","切换场景失败"],
    # 余额和token数查询
    "#余额": [True, lambda : deepseek.return_balance(), "无法查询"],
    "#token": [True, lambda : deepseek.return_token(), lambda : deepseek.return_balance(), "无法查询"]
}
def qq_quick_order(order: str):
    """qq快捷指令（调用此方法后自动分割后通过关键字快速找到其他方法）
    参数： order ： 收到的消息(#R1模型)
    返回值：如果指令存在则执行对应的函数后返回True，如果指令不存在返回False
    """
    global args #使用外面的全局变量
    def execute_function(true_false_result):
        """是否执行返回值的函数
        参数 : true_false_result  ；执行结果
        """
        if true_false_result:  # 执行结果有效果
            if function_check(function_map[order][1]):  # 真值是一个函数
                chat_win1.send_message(function_map[order][1]())  # 执行真值的函数并发送
            else:
                chat_win1.send_message(function_map[order][1])  # 直接发送真值
        else:
            if function_check(function_map[order][2]):  # 假值是一个函数
                chat_win1.send_message(function_map[order][2]())  # 执行假值的函数并发送
            else:
                chat_win1.send_message(function_map[order][2])  # 直接发送假值

    function_check = lambda def_function: True if isinstance(def_function, (types.LambdaType,types.FunctionType,types.MethodType)) else False   # 检查是否为匿名函数
    # 检查指令是否包含参数并做处理
    if ":" in order:  # 如何指令中存在:代表的是参数
        if not order.split(":",1)[1]:     # 参数为空
            chat_win1.send_message("参数为空")  # 有:却不填
            return False
        order, args = order.split(":",1)[0], order.split(":",1)[1]  # 分割指令和参数
    # 检查指令是否在函数映射字典中
    if order not in function_map:   # 指令不在字典里面
        chat_win1.send_message("不存在该指令")
        print("\033[93m接收到了不存在的指令\033[0m")
        return False  # 没有这个指令
    else:
        if function_check(function_map[order][0]) and args is None:   # 是一个无参函数
            # print("\033[92m无参函数执行了\033[0m")
            try:    # 假设没有:却必须要填入参数没有填
                result = function_map[order][0]()    # 执行函数并拿到返回结果
                execute_function(result)
            except TypeError:
                if function_check(function_map[order][2]):  # 假值是一个函数
                    chat_win1.send_message("请在指令中附带必要参数:\n" + function_map[order][2]())  # 执行假值的函数并发送
                else:
                    chat_win1.send_message("请在指令中附带必要参数:\n" + function_map[order][2])  # 直接发送假值
        elif function_check(function_map[order][0]) and args is not None:    # 是有参函数
            # print("\033[92m有参函数执行了\033[0m")
            result = function_map[order][0](args)  # 传入参数并执行函数并拿到返回结果
            execute_function(result)
        else:   # 不是一个函数(可能是None、True、False)
            # print("\033[92m不是函数执行了\033[0m")
            result = function_map[order][0]     # 传入的不是一个函数不执行，仅仅拿到值
            execute_function(result)
    return True  # 存在指令且执行即返回True

def exit_qq_auto_reply(administrator_name):
    """判断是否退出QQ自动回复
    参数 ： administrator_name ： 超级管理员的名字
    """
    if administrator_name in administrator:
        print("\033[31m已停止QQ监听回复和退出deepseek对话引擎\033[0m")
        chat_win1.send_message("已停止QQ自动回复\n已退出deepseek对话引擎")
        sys.exit()  # 优雅退出程序
    else:
        print("\033[31m此为高级操作，你无权执行该指令\033[0m")
        chat_win1.send_message("此为高级操作，你无权执行该指令")
"""-------------------------------------------------QQ消息回复处理-----------------------------------------------------"""
# try:
while True:
    sleep(1)  # 每1秒监测一次变化
    chat_win1.show_win()    # 展示窗口
    chat_win1.top_win()     # 置顶开窗口
    chat_win1.monitor_message() # 始监控
    """消息处理"""
    if len(chat_win1.message_processing_queues) > 0:    # 队列不为空，进行队列处理
        # 这里是发送者的名字，我接收它的名字
        sender = chat_win1.message_processing_queues[0]["发送者"]
        # 我接受的消息（这里的发送消息指的是对方的发送消息)
        accept_message = chat_win1.message_processing_queues[0]["发送消息"]
        accept_message = accept_message.replace(f"@{chat_win1.monitor_name} ", "")   # 去除（@自己的名字 ）这个部分
        if accept_message == "": accept_message = " "    # 确保消息体不为空
        # 对方的消息发送时间
        accept_time = chat_win1.message_processing_queues[0]["发送时间"]
        """===============快捷指令处理==========="""
        if "#" == accept_message[0]:   # 检测到指令的消息
            if "#退出" in accept_message:      # 消息中存在退出指令
                exit_qq_auto_reply(sender)     # 检查发送者的身份是否为管理员(内置优雅退出)
            else: qq_quick_order(accept_message)    # 把指令带进入分析
            chat_win1.message_processing_queues.pop(0)  # 清理收到的指令(出队)
            print(f"\033[94m已完成“{sender}”的指令\033[0m")
        else:       # 非退出指令操作
            # deepseek.conversation_engine(content)  # 调用对话引擎
            reply = deepseek.ask(f"{sender}:{accept_message}",False)  # 发出请求并回应(这里不打印到屏幕上)
            print(f"\033[96m{reply}\033[0m")    # 打印回应字体(青色)
            chat_win1.send_message(f"@{sender} "+ reply)                       # 把回应发送到qq
            deepseek.dialog_history_manage()    # 自动删除久远的对话历史
            chat_win1.message_processing_queues.pop(0)  # 清理回应的消息(出队)
            print(f"\033[94m已完成“{sender}”的消息处理\033[0m")
# except Exception as e:
#     print(f"捕获到异常: {e}")
#     # input("按Enter键退出...")  # 防止窗口立即关闭
# : 'comtypes==1.4.10', 'mkl-service==2.4.0', 'pywin32==310', 'setuptools==72.1.0', 'uiautomation==2.0.28', 'wheel==0.45.1'