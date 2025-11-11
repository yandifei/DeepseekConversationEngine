import os

from openai import OpenAI # 从 'openai' 库中导入 'OpenAI' 类，用于与 DeepSeek API 进行交互。

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

tools = [ # 定义一个工具列表，供模型在对话中使用。
    { # 列表中的第一个 (也是唯一的) 工具定义。
        "type": "function", # 指定工具类型为 'function' (函数)。
        "function": { # 函数的详细定义。
            "name": "get_weather", # 函数的名称。
            "description": "获取某个位置的天气，用户应该首先提供一个位置。", # 函数的描述，告诉模型何时使用此函数。
            "parameters": { # 函数所需的参数定义。
                "type": "object", # 参数类型为对象 (表示参数集合)。
                "properties": { # 对象的属性 (即函数的参数)。
                    "location": { # 定义 'location' 参数。
                        "type": "string", # 'location' 参数的类型是字符串。
                        "description": "城市和州，例如加利福尼亚州旧金山", # 'location' 参数的描述和示例。
                    }
                },
                "required": ["location"] # 指定 'location' 参数是必需的。
            },
        }
    },
]

messages = [{"role": "user", "content": "浙江杭州的天气怎么样？"}] # 初始化对话历史列表，包含用户的第一个问题。
print(f"User>\t {messages[0]['content']}") # 打印用户发送的原始消息。

message = send_messages(messages) # 第一次调用 API，发送用户消息。模型会决定是否调用工具。
print(message)  # 打印返回选项

tool = message.tool_calls[0] # 从模型返回的消息中提取第一个工具调用对象。
print(message.tool_calls)
print(tool)

def get_weather(location):
    # 这里需要写代码来调用一个真实的天气API
    # 假设我们成功获取了数据
    if "杭州" in location:
        return "晴，24℃，微风"
    elif "北京" in location:
        return "多云，15℃"
    else:
        return "对不起，无法获取该地的天气信息。"


# 遍历模型请求调用的所有工具
for tool_call in message.tool_calls: # message 此时包含模型请求的 tool_calls
    if tool_call.function.name == "get_weather":
        # 1. 解析模型给出的参数
        location = eval(tool_call.function.arguments)['location']

        # 2. 调用我们自己写的实际函数 (例如上面的 get_weather)
        tool_output = get_weather(location)

        # 3. 将结果格式化为 tool 消息并添加到 messages
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_output  # 注意：这里 now 是真实函数的输出！
        })



messages.append(message) # 将模型返回的包含工具调用的消息添加到对话历史中。
print(f"将模型返回的包含工具调用的消息添加到对话历史中:\n{messages}")

# messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"}) # 模拟执行工具（get_weather）并将其结果添加到对话历史中。
# message = send_messages(messages) # 第二次调用 API，将工具执行结果发回模型，模型基于此结果生成最终答案。
# print(f"Model>\t {message.content}") # 打印模型基于工具结果生成的最终回答。