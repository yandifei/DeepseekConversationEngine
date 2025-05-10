from setuptools import setup, find_packages

with open("README.md","r",encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="DeepseekConversationEngine",               # 包名(PyPI注册名)
    version="1.1.1",                                 # 版本号
    author="雁低飞",                                  # 作者
    author_email="3058439878@qq.com",                # 邮箱
    description="多人设、多场景、多论对话自动化管理",    # 简短描述
    long_description=long_description,               # 详细说明
    long_description_content_type="text/markdown",   # 详细说明使用标记类型
    url="https://github.com/yandifei/DeepseekConversationEngine", # 项目主页
    packages=find_packages(exclude=["调用示例"]),# 需要打包的部分，自动发现包目录(排除不需要打包的文件)
    # package_dir={"": "DeepseekConversationEngine"},  # 设置DeepseekConversationEngine目录为根目录
    package_data={
            "DeepseekConversationEngine": [
                "deepseek_v3_tokenizer/*",  # 分词必要的文件
                "提示库/*",    # 提示库文件
            ]
    },
    classifiers=[               # 分类标签（可选）
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 11"
    ],
    python_requires=">=3.13.1",                      # 项目支持的Python版本
    install_requires=[
        "requests",
        "transformers>=4.51.3",
        "openai>=1.60.1"
    ],               # 项目必须的依赖
    include_package_data=True                       # 是否包含非Python文件（如资源文件）
)