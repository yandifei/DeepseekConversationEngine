"""download_images_for_a_specific_topic.py
下载特定主题的图片
"""
# 内置库
import io
import json
# 第三方库
import requests
from PIL import Image               # 图片格式转换处理(pip install Pillow)
# 自己的模块
from tools_manage.base_tool import BaseTool # 工具的顶层设计类


class DownloadImagesForASpecificTopic(BaseTool):
    def __init__(self):
        # 图片保存路径
        self.path = "./temp"
        # 这个必须优于get_description存在
        self.picture_map = dict()  # 图片映射表
        self.picture_map_read()  # 录入图片映射表数据
        self.name = "download_images_for_a_specific_topic"
        print(__name__)
        self.description = self.get_description()
        self.parameters = {
            "type": "object",
            "properties": {
                "theme": {
                    "type": "string",
                    "description": "你必须选择其中一个主题：" + "、".join(name for name in self.picture_map.keys()),
                    "enum": list(self.picture_map.keys())  # 明确列出所有可选值
                },
                "quantity": {
                    "type": "integer",
                    "description": "图片数量：0=确认能力，默认3",
                    "minimum": 0,  # 最小值为0
                    "maximum": 20  # 最大值为20
                }
            },
            "required": ["theme", "quantity"]
        }
        super().__init__(self.name, self.description, self.parameters)
        # 请求超时时间
        self.requests_timeout = 10
        # 请求头构造
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
        }

    def get_description(self):
        return "发送一张图片，图片主题：" + "、".join(name for name in self.picture_map.keys())

    def picture_map_read(self):
        """图片映射表读取"""
        try:
            with open("用户设置/关键词回复/图片映射表.json", "r", encoding="utf-8") as json_file:
            # with open("../用户设置/关键词回复/图片映射表.json", "r", encoding="utf-8") as json_file:
                self.picture_map = json.load(json_file)  # 监测指定的人和关键字
        except json.JSONDecodeError as e:
            print(f"\033[91m图片映射表.json 文件的格式错误或json没有任何内容\033[0m")
            return False
        return True

    def execute(self, **kwargs) -> str:
        # 从 kwargs 字典中获取 'theme' 参数的值
        theme = kwargs.get('theme')
        quantity = kwargs.get('quantity')
        # 检查参数有效性
        if not theme or not isinstance(theme, str):
            return "错误：请提供有效的图片主题参数。"
        # 检查主题是否存在
        if theme not in self.picture_map:
            return f"没有找到主题为 '{theme}' 的图片。"
        for i in range(quantity):
            # 只有通过所有检查后才执行下载
            # 下载图片（这里这么做是为了分离消息发送）
            try:
                # 请求超过10秒为超时
                with Image.open(io.BytesIO(
                        requests.get(self.picture_map[theme], headers=self.headers, timeout=self.requests_timeout).content)) as img:
                    img.save(f"{self.path}/网页请求图片{i}.png", "PNG")
            except Exception as e:
                return f"图片下载失败，出现异常错误:{e}"
        return f"已发送{quantity}张{theme}主题的图片"

# if __name__ == '__main__':
    # print(a.picture_map)
    # print(a.description)
