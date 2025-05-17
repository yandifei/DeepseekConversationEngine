# -*- mode: python ; coding: utf-8 -*-

# 分析主脚本和依赖项
a = Analysis(
    ['QQ聊天AI.py'],          # 主入口脚本文件
    pathex=[],                # 额外搜索路径（可添加自定义路径，如['./src']）
    binaries=[],              # 需要包含的二进制文件（如.dll/.so）
    datas=[],                 # 需要包含的非代码文件（如图片、配置文件）
    hiddenimports=[],         # 显式声明隐式导入的库（如某些动态加载的模块）
    hookspath=[],            # 自定义钩子脚本路径
    hooksconfig={},          # 钩子配置参数
    runtime_hooks=[],        # 运行时钩子脚本（处理特殊依赖）
    excludes=[],             # 排除不需要的模块（减小体积）
    noarchive=False,         # 是否禁用归档模式（True会解压文件到临时目录）
    optimize=0,              # Python优化级别（0-2）
)

# 将Python字节码打包成ZIP文件（PYZ）
pyz = PYZ(a.pure)            # a.pure表示所有纯Python模块

# 启动画面配置（需安装 pyinstaller-splash）
splash = Splash(
    '.\\文档\\QQ_chat_AI.png', # 启动图片路径（注意Windows路径需转义或使用r''）
    binaries=a.binaries,     # 继承Analysis的二进制文件
    datas=a.datas,           # 继承Analysis的数据文件
    text_pos=None,           # 文本位置坐标（(x,y)格式）
    text_size=12,            # 加载进度文本字号
    minify_script=True,      # 压缩JavaScript代码
    always_on_top=True,      # 启动画面置顶显示
)

# 生成可执行文件配置
exe = EXE(
    pyz,                      # 包含所有Python模块的ZIP
    a.scripts,                # 主脚本信息
    splash,                   # 添加启动画面组件
    [],                       # 其他扩展模块（如加密模块）
    exclude_binaries=True,    # 是否排除二进制文件
    name='QQ聊天AI',           # 生成的可执行文件名
    debug=False,              # 是否包含调试信息
    bootloader_ignore_signals=False,  # 是否忽略系统信号
    strip=False,              # 是否去除符号信息（Linux/macOS）
    upx=True,                 # 是否使用UPX压缩可执行文件
    console=True,             # 是否显示控制台窗口（True=显示）
    disable_windowed_traceback=False,
    argv_emulation=False,     # macOS参数模拟（如文件拖拽）
    target_arch=None,         # 目标架构（如x86/x64）
    uac_admin=True,          # 是否请求管理员权限（Windows）
    icon=['文档\\QQ_chat_AI.ico'],  # 程序图标路径
)

# 收集所有文件到输出目录（单文件夹发布模式）
coll = COLLECT(
    exe,                      # 包含可执行文件配置
    a.binaries,               # 二进制文件集合
    a.datas,                  # 数据文件集合
    splash.binaries,          # 启动画面的二进制依赖
    strip=False,
    upx=True,                 # 对二进制文件使用UPX压缩
    name='QQ聊天AI',           # 输出文件夹名称
)