# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['QQ聊天AI.py'],
    pathex=[],
    binaries=[],
    datas=[('B:/Pycharm/Anaconda3/envs/QQBot/Lib/site-packages/comtypes', 'comtypes'), ('B:/Pycharm/Anaconda3/envs/QQBot/Lib/site-packages/uiautomation/bin', 'uiautomation/bin')],
    hiddenimports=['comtypes'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
splash = Splash(
    '.\\文档\\QQ_chat_AI.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

exe = EXE(
    pyz,
    a.scripts,
    splash,
    [],
    exclude_binaries=True,
    name='QQ聊天AI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['文档\\QQ_chat_AI.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    splash.binaries,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='QQ聊天AI',
)
