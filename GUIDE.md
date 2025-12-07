# 🎯 PPT Compressor - 快速上手指南

## 🚀 立即开始

### 方法一：使用 macOS 应用（推荐）

```bash
# 1. 构建并安装到 Applications
./build_app.sh

# 2. 在启动台或 Applications 文件夹中找到并打开 "PPT Compressor"
# 3. 浏览器会自动打开 Web 界面
# 4. 拖放 PPT 文件到界面中即可压缩
```

### 方法二：开发模式运行

```bash
# 直接运行服务器
./run.sh

# 或者
python3 server.py
```

## 🔄 日常开发流程

### 1. 修改代码后快速更新

```bash
# 快速更新 Applications 中的应用（推荐）
./update_app.sh

# 完整重新构建（修改了图标或配置时使用）
./build_app.sh
```

### 2. 测试修改

```bash
# 开发模式运行服务器
./run.sh

# 访问 http://127.0.0.1:5001 测试
```

## 📁 项目文件说明

### 核心文件

- **server.py** - Flask Web 服务器，自动打开浏览器
- **ppt_compressor_v3.py** - 压缩引擎，支持 6 种压缩档位
- **templates/index.html** - Web UI 界面
- **static/style.css** - macOS Sequoia 风格样式
- **static/script.js** - 前端交互逻辑

### 工具脚本

- **build_app.sh** - 完整构建并部署到 Applications
- **update_app.sh** - 快速更新 Applications 中的应用
- **run.sh** - 开发模式快速启动服务器
- **create_icon.py** - 生成应用图标

### 文档

- **README.md** - 完整文档
- **GUIDE.md** - 本快速上手指南

## 🎨 UI 界面特性

1. **拖放上传** - 支持拖拽 PPT 文件到界面
2. **4 种压缩档位** - 完全无损、高质量、平衡、激进
3. **实时反馈** - 显示压缩进度和结果
4. **动画效果** - 流畅的 macOS Sequoia 风格动画
5. **响应式设计** - 适配不同屏幕尺寸

## ⚙️ 配置选项

### 服务器端口

默认端口：`5001`

修改 `server.py` 中的 `port` 变量：

```python
def main():
    port = 5001  # 修改为你想要的端口
    ...
```

### 压缩档位

在 Web 界面中选择，或修改 `ppt_compressor_v3.py` 中的 `PRESETS` 配置：

```python
PRESETS = {
    'lossless': {...},
    'high': {...},
    'balanced': {...},
    'aggressive': {...}
}
```

## 🐛 故障排除

### 应用打不开

1. 右键点击应用 → "打开"
2. 在"系统偏好设置 > 安全性与隐私"中允许运行

### 浏览器没有自动打开

手动访问：`http://127.0.0.1:5001`

### 依赖缺失

```bash
pip3 install flask pillow werkzeug
brew install oxipng  # 可选，用于更好的 PNG 压缩
```

### 应用更新后没有变化

```bash
# 方法 1: 使用快速更新脚本
./update_app.sh

# 方法 2: 完整重新构建
./build_app.sh

# 方法 3: 手动刷新
killall Finder
killall Dock
```

## 💡 开发技巧

### 1. 实时预览修改

```bash
# 运行开发服务器
./run.sh

# 修改 CSS/JS 后刷新浏览器即可看到效果
# 修改 Python 代码后需要重启服务器
```

### 2. 快速部署流程

```bash
# 开发 → 测试 → 部署
./run.sh           # 1. 开发测试
# 按 Ctrl+C 停止
./update_app.sh    # 2. 快速更新到 Applications
```

### 3. 调试技巧

```bash
# 查看服务器日志
./run.sh

# 浏览器开发者工具
# 打开浏览器 → F12 → Console 标签
```

## 🎯 常用命令速查

```bash
# 完整构建
./build_app.sh

# 快速更新
./update_app.sh

# 开发运行
./run.sh

# 生成图标
python3 create_icon.py

# 打开应用位置
open /Applications/"PPT Compressor.app"

# 查看应用信息
ls -lah "/Applications/PPT Compressor.app/Contents/"
```

## 📊 性能优化建议

1. **安装 oxipng** - 获得更好的 PNG 压缩效果
   ```bash
   brew install oxipng
   ```

2. **选择合适的压缩档位** - 根据需求平衡质量和文件大小

3. **批量处理** - Web 界面支持连续压缩多个文件

## 🔐 安全提示

- 应用只在本地运行（127.0.0.1）
- 临时文件会在 1 小时后自动清理
- 不会上传任何数据到互联网

## 📝 版本历史

- **v4.0** - macOS Sequoia 风格重构
  - 全新 Web UI 界面
  - 自动打包和部署系统
  - 热更新支持
  - 现代化图标设计

- **v3.0** - 核心压缩引擎
  - 完全保留 PNG 透明度
  - 6 种压缩档位
  - oxipng 支持

---

🎉 享受你的全新 PPT Compressor！
