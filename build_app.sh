#!/bin/bash

# PPT Compressor - 自动打包和部署脚本
# macOS Sequoia Style - 自动化构建并部署到 Applications 文件夹

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 项目配置
APP_NAME="PPT Compressor"
BUNDLE_ID="com.whitney.pptcompressor"
VERSION="4.0"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_PATH="$CURRENT_DIR/${APP_NAME}.app"
APPLICATIONS_PATH="/Applications/${APP_NAME}.app"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}  🎨 PPT Compressor - macOS Sequoia Style Builder        ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 步骤 1: 清理旧版本
echo -e "${BLUE}[1/7]${NC} 🧹 清理旧版本..."
if [ -d "$APP_PATH" ]; then
    rm -rf "$APP_PATH"
    echo -e "${GREEN}      ✓ 已删除临时构建目录${NC}"
fi

# 步骤 2: 创建应用包结构
echo -e "${BLUE}[2/7]${NC} 📦 创建应用包结构..."
mkdir -p "$APP_PATH/Contents/MacOS"
mkdir -p "$APP_PATH/Contents/Resources"
mkdir -p "$APP_PATH/Contents/Resources/templates"
mkdir -p "$APP_PATH/Contents/Resources/static"
echo -e "${GREEN}      ✓ 应用包结构已创建${NC}"

# 步骤 3: 创建 .icns 图标文件
echo -e "${BLUE}[3/7]${NC} 🎨 生成应用图标..."

# 如果 icon_1024.png 不存在，先生成它
if [ ! -f "$CURRENT_DIR/icon_1024.png" ]; then
    echo -e "${YELLOW}      ⚠️  图标文件不存在，正在生成...${NC}"
    python3 "$CURRENT_DIR/create_icon.py"
fi

# 创建 iconset
ICONSET_DIR="$CURRENT_DIR/PPTCompressor.iconset"
mkdir -p "$ICONSET_DIR"

cp "$CURRENT_DIR/icon_16.png" "$ICONSET_DIR/icon_16x16.png"
cp "$CURRENT_DIR/icon_32.png" "$ICONSET_DIR/icon_16x16@2x.png"
cp "$CURRENT_DIR/icon_32.png" "$ICONSET_DIR/icon_32x32.png"
cp "$CURRENT_DIR/icon_64.png" "$ICONSET_DIR/icon_32x32@2x.png"
cp "$CURRENT_DIR/icon_128.png" "$ICONSET_DIR/icon_128x128.png"
cp "$CURRENT_DIR/icon_256.png" "$ICONSET_DIR/icon_128x128@2x.png"
cp "$CURRENT_DIR/icon_256.png" "$ICONSET_DIR/icon_256x256.png"
cp "$CURRENT_DIR/icon_512.png" "$ICONSET_DIR/icon_256x256@2x.png"
cp "$CURRENT_DIR/icon_512.png" "$ICONSET_DIR/icon_512x512.png"
cp "$CURRENT_DIR/icon_1024.png" "$ICONSET_DIR/icon_512x512@2x.png"

iconutil -c icns "$ICONSET_DIR" -o "$APP_PATH/Contents/Resources/AppIcon.icns"
rm -rf "$ICONSET_DIR"
echo -e "${GREEN}      ✓ 应用图标已生成${NC}"

# 步骤 4: 复制应用文件
echo -e "${BLUE}[4/7]${NC} 📋 复制应用文件..."
cp "$CURRENT_DIR/server.py" "$APP_PATH/Contents/Resources/"
cp "$CURRENT_DIR/ppt_compressor_v3.py" "$APP_PATH/Contents/Resources/"
cp "$CURRENT_DIR/templates/index.html" "$APP_PATH/Contents/Resources/templates/"
cp "$CURRENT_DIR/static/style.css" "$APP_PATH/Contents/Resources/static/"
cp "$CURRENT_DIR/static/script.js" "$APP_PATH/Contents/Resources/static/"

# 复制 icon_128.png 用于 UI
cp "$CURRENT_DIR/icon_128.png" "$APP_PATH/Contents/Resources/static/"

echo -e "${GREEN}      ✓ 应用文件已复制${NC}"

# 步骤 5: 创建启动脚本
echo -e "${BLUE}[5/7]${NC} 🚀 创建启动脚本..."

cat > "$APP_PATH/Contents/MacOS/launcher" << 'LAUNCHER_EOF'
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

# 检查依赖（静默安装）
if ! $PYTHON -c "import flask" 2>/dev/null; then
    $PYTHON -m pip install --user flask pillow werkzeug &>/dev/null
fi

# 清理旧进程（避免端口冲突）
pkill -f "server.py" 2>/dev/null
sleep 1

# 启动服务器（后台运行）
nohup $PYTHON "$RESOURCES_DIR/server.py" > /tmp/ppt_compressor.log 2>&1 &

# 等待服务器启动
sleep 2

# 退出，让应用停止
exit 0
LAUNCHER_EOF

chmod +x "$APP_PATH/Contents/MacOS/launcher"
echo -e "${GREEN}      ✓ 启动脚本已创建${NC}"

# 步骤 6: 创建 Info.plist
echo -e "${BLUE}[6/7]${NC} 📝 创建 Info.plist..."

cat > "$APP_PATH/Contents/Info.plist" << PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>${BUNDLE_ID}</string>
    <key>CFBundleName</key>
    <string>${APP_NAME}</string>
    <key>CFBundleDisplayName</key>
    <string>${APP_NAME}</string>
    <key>CFBundleVersion</key>
    <string>${VERSION}</string>
    <key>CFBundleShortVersionString</key>
    <string>${VERSION}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <string>0</string>
    <key>NSAppleScriptEnabled</key>
    <true/>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>pptx</string>
                <string>ppt</string>
            </array>
            <key>CFBundleTypeName</key>
            <string>PowerPoint Presentation</string>
            <key>CFBundleTypeRole</key>
            <string>Viewer</string>
        </dict>
    </array>
</dict>
</plist>
PLIST_EOF

echo -e "${GREEN}      ✓ Info.plist 已创建${NC}"

# 步骤 7: 部署到 Applications 文件夹
echo -e "${BLUE}[7/7]${NC} 🚚 部署到 Applications 文件夹..."

# 删除旧版本
if [ -d "$APPLICATIONS_PATH" ]; then
    echo -e "${YELLOW}      ⚠️  检测到旧版本，正在更新...${NC}"
    rm -rf "$APPLICATIONS_PATH"
fi

# 复制到 Applications
cp -R "$APP_PATH" "$APPLICATIONS_PATH"

# 清理临时构建文件
rm -rf "$APP_PATH"

echo -e "${GREEN}      ✓ 已部署到 Applications 文件夹${NC}"

# 完成
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}  ✅ 构建和部署完成！                                     ${GREEN}║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📍 应用位置:${NC} ${APPLICATIONS_PATH}"
echo -e "${BLUE}🎨 版本:${NC} ${VERSION}"
echo ""
echo -e "${YELLOW}💡 使用方法:${NC}"
echo -e "   1. 在启动台或 Applications 文件夹中找到 '${APP_NAME}'"
echo -e "   2. 双击打开，浏览器会自动打开 Web 界面"
echo -e "   3. 拖放 PPT 文件到界面中即可压缩"
echo ""
echo -e "${YELLOW}🔄 更新应用:${NC}"
echo -e "   每次修改代码后，运行 ${BLUE}./build_app.sh${NC} 即可自动更新"
echo ""
