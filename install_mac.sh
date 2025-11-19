#!/bin/bash
# PPT压缩工具 v3.0 - Mac一键安装脚本

echo "🚀 PPT现代化无损压缩工具 v3.0 - 安装向导"
echo "========================================="
echo ""

# 检查Homebrew
if ! command -v brew &> /dev/null; then
    echo "📦 未检测到Homebrew，正在安装..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew已安装"
fi

# 检查Python
if command -v python3 &> /dev/null; then
    echo "✅ Python已安装: $(python3 --version)"
else
    echo "📦 正在安装Python3..."
    brew install python3
fi

# 安装Pillow
echo ""
echo "📦 安装Python依赖..."
pip3 install Pillow

# 安装oxipng（关键！）
echo ""
echo "🔥 安装oxipng（PNG无损压缩神器）..."
if command -v oxipng &> /dev/null; then
    echo "✅ oxipng已安装: $(oxipng --version)"
else
    brew install oxipng
    if [ $? -eq 0 ]; then
        echo "✅ oxipng安装成功！"
    else
        echo "⚠️  oxipng安装失败，将使用Pillow进行PNG压缩"
    fi
fi

# 添加执行权限
echo ""
echo "🔧 设置文件权限..."
chmod +x compress_v3.sh
chmod +x ppt_compressor_v3.py

echo ""
echo "========================================="
echo "✅ 安装完成！"
echo ""
echo "现在可以使用以下方式运行："
echo "1. 运行图形界面: ./compress_v3.sh"
echo "2. 命令行使用: python3 ppt_compressor_v3.py 文件.pptx --preset lossless"
echo ""
echo "推荐使用 lossless 档位，完全保留PNG透明度！"
echo "========================================="
