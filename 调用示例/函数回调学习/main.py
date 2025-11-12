import json
import os

from openai import OpenAI # 从 'openai' 库中导入 'OpenAI' 类，用于与 DeepSeek API 进行交互。
# 导入工具列表，供模型在对话中使用。# 定义一个工具列表，供模型在对话中使用。
from tools_manage import tools, tools_map


def send_messages(messages): # 定义一个名为 'send_messages' 的函数，接受一个参数 'messages' (对话历史列表)。
    response = client.chat.completions.create( # 调用 'client' 对象的 chat.completions.create 方法发送 API 请求。
        model="deepseek-chat", # 指定要使用的模型名称，这里是 DeepSeek 的聊天模型。
        messages=messages, # 传递对话历史列表。
        tools=tools # 传递定义好的工具列表，让模型可以决定是否调用工具。
    )
    return response.choices[0].message # 返回响应中第一个选项 (通常是唯一的选项) 的消息对象。

key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI( # 创建一个 OpenAI 客户端实例。
    api_key=key, # 设置 API 密钥。注意：这里应该替换成你自己的实际密钥。
    base_url="https://api.deepseek.com", # 设置 DeepSeek API 的基础 URL。
)



messages = [{"role": "user", "content": "来张黑丝"}] # 初始化对话历史列表，包含用户的第一个问题。
print(f"我：{messages[0]['content']}") # 打印用户发送的原始消息。

# 第一次调用 API，发送用户消息。模型会决定是否调用工具。
message = send_messages(messages)



# 判断模型是否会调用工具
if message.tool_calls:  # 工具列表有需要工具

    # 将模型的工具调用消息添加到对话历史中（这是关键的一步！）
    messages.append({
        "role": "assistant",
        "content": message.content,
        "tool_calls": message.tool_calls})

    # 遍历工具列表
    for tool_call in message.tool_calls:
        # 解析函数调用的参数
        function_args = json.loads(tool_call.function.arguments) or {}
        # 获取函数
        if tool_call.function.name in tools_map: # 调用的工具在映射表中
            # 调用函数并拿到返回的结果
            result: str = tools_map[tool_call.function.name](**function_args)
            # print(f"\033[91m函数执行结果：{result}\033[0m")
            # 将模型返回的包含工具调用的消息添加到对话历史中。
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
        else:
            print(f"遇到了其他需要调用的工具{tool_call.function.name}")

    # 第二次调用 API，将工具执行结果发回模型，模型基于此结果生成最终答案。
    message = send_messages(messages)


# 打印模型基于工具结果生成的最终回答。
print(f"AI:{message.content}")