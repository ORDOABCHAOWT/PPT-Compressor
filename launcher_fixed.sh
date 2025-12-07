#!/bin/bash

# 获取 Resources 目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RESOURCES_DIR="$DIR/../Resources"

cd "$RESOURCES_DIR"

# 查找 Python3
if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif [ -x "/usr/local/bin/python3" ]; then
    PYTHON="/usr/local/bin/python3"
elif [ -x "/opt/homebrew/bin/python3" ]; then
    PYTHON="/opt/homebrew/bin/python3"
else
    osascript -e 'display dialog "错误: 未找到 Python 3\n\n请先安装 Python 3" buttons {"确定"} default button 1 with icon stop'
    exit 1
fi

# 检查依赖（静默检查，不弹窗）
if ! $PYTHON -c "import flask" 2>/dev/null; then
    $PYTHON -m pip install --user flask pillow werkzeug &>/dev/null
fi

# 启动服务器（后台运行，避免应用一直跳）
nohup $PYTHON "$RESOURCES_DIR/server.py" > /tmp/ppt_compressor.log 2>&1 &

# 等待服务器启动
sleep 2

# 退出，让应用停止跳动
exit 0
