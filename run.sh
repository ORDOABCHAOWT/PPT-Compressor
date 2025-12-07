#!/bin/bash

# PPT Compressor - 快速启动脚本
# 直接从项目目录启动 Web 服务器进行测试

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${BLUE}🚀 启动 PPT Compressor (开发模式)${NC}"
echo ""

# 检查依赖
python3 -c "import flask" 2>/dev/null || {
    echo -e "${YELLOW}📦 正在安装依赖...${NC}"
    pip3 install flask pillow werkzeug
    echo ""
}

# 启动服务器
echo -e "${GREEN}✅ 服务器正在启动...${NC}"
echo -e "${BLUE}📡 地址: http://127.0.0.1:5001${NC}"
echo -e "${YELLOW}💡 按 Ctrl+C 停止服务器${NC}"
echo ""

python3 server.py
