#!/bin/bash

# PPT Compressor - 清理脚本
# 清理所有运行中的服务器进程

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${BLUE}🧹 清理 PPT Compressor 进程...${NC}"
echo ""

# 清理所有相关进程
pkill -f "server.py" 2>/dev/null
pkill -f "ppt_compressor" 2>/dev/null

# 清理端口
lsof -ti:5001 | xargs kill -9 2>/dev/null

sleep 1

echo -e "${GREEN}✅ 清理完成！${NC}"
echo ""
echo -e "${YELLOW}💡 提示:${NC}"
echo -e "   - 所有 PPT Compressor 进程已停止"
echo -e "   - 端口 5001 已释放"
echo -e "   - 现在可以重新启动应用"
echo ""
