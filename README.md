# 🎨 PPT Compressor - macOS Sequoia Style

现代化的 PowerPoint 压缩工具，采用 macOS Sequoia 设计风格，通过浏览器提供优雅的 Web 界面。

## ✨ 特性

- 🎨 **macOS Sequoia 风格** - 现代化的玻璃态设计，流畅的动画效果
- 🌐 **Web 界面** - 自动在浏览器中打开，无需命令行操作
- 🚀 **真正无损压缩** - 使用 oxipng 和 MozJPEG，完全保留 PNG 透明度
- 📦 **一键打包** - 自动构建和部署到 Applications 文件夹
- 🔄 **热更新支持** - 修改代码后快速更新应用
- 💎 **6 种压缩档位** - 从完全无损到极致压缩

## 📦 安装

### 自动安装（推荐）

直接运行构建脚本，应用会自动安装到 Applications 文件夹：

```bash
./build_app.sh
```

### 手动安装依赖

```bash
# 安装 Python 依赖
pip3 install flask pillow werkzeug

# 安装 oxipng（可选，用于更好的 PNG 压缩）
brew install oxipng
```

## 🚀 使用方法

### 方式 1: 使用 macOS 应用（推荐）

1. 运行 `./build_app.sh` 构建并安装应用
2. 在启动台或 Applications 文件夹中找到 "PPT Compressor"
3. 双击打开，浏览器会自动打开 Web 界面
4. 拖放 PPT 文件到界面中即可压缩

### 方式 2: 直接运行服务器

```bash
python3 server.py
```

浏览器会自动打开 `http://127.0.0.1:5001`

## 🔄 开发和更新

### 快速更新应用

修改代码后，运行快速更新脚本：

```bash
./update_app.sh
```

这会自动更新 Applications 文件夹中的应用，无需完整重新构建。

### 完整重新构建

如果需要完整重新构建（例如修改了图标或配置）：

```bash
./build_app.sh
```

### 开发模式

在开发过程中，可以直接运行服务器进行测试：

```bash
python3 server.py
```

## 📊 压缩档位

| 档位 | 描述 | 压缩率 | 特点 |
|------|------|--------|------|
| **完全无损** | PNG 透明度完整保留 | 15-30% | 使用 oxipng 真正无损压缩 |
| **高质量** | 视觉无损 | 30-50% | PNG 保留透明度，JPEG 高质量 |
| **平衡** | 轻微损失（默认） | 50-70% | PNG 保留透明度，适度压缩 |
| **激进** | 保留 PNG 和透明度 | 70-85% | 降低颜色数量，限制尺寸 1280px |

## 🎯 项目结构

```
PPT-compressor/
├── server.py                    # Flask Web 服务器
├── ppt_compressor_v3.py        # 核心压缩引擎
├── templates/
│   └── index.html              # Web UI 模板
├── static/
│   ├── style.css               # macOS Sequoia 风格样式
│   └── script.js               # 前端交互逻辑
├── create_icon.py              # 图标生成脚本
├── build_app.sh                # 自动构建和部署脚本
├── update_app.sh               # 快速更新脚本
└── README.md                   # 本文档
```

## 🛠 技术栈

- **后端**: Flask (Python 3)
- **前端**: HTML5 + CSS3 + Vanilla JavaScript
- **压缩**: Pillow + oxipng
- **设计**: macOS Sequoia Design Language

## 💡 核心功能

### 1. Web UI 界面

- 拖放上传 PPT 文件
- 实时选择压缩档位
- 动态显示压缩结果
- 一键下载压缩后的文件

### 2. 自动打包系统

- 自动生成应用图标（.icns）
- 创建标准的 macOS 应用包结构
- 自动部署到 Applications 文件夹
- 支持快速增量更新

### 3. 压缩引擎

- 完全保留 PNG 透明度
- 支持 oxipng 无损压缩
- 智能图片格式转换
- 多种压缩档位可选

## 🎨 设计特点

- **玻璃态效果** - backdrop-filter 实现的模糊背景
- **流畅动画** - CSS transitions 和 keyframes
- **动态背景** - 浮动的渐变色斑
- **响应式设计** - 适配不同屏幕尺寸
- **Apple 配色** - 使用 Apple 官方配色

## 🔧 常见问题

### Q: 应用打不开？

A: 首次运行可能需要在"系统偏好设置 > 安全性与隐私"中允许应用运行。

### Q: 如何卸载？

A: 直接删除 `/Applications/PPT Compressor.app` 即可。

### Q: 浏览器没有自动打开？

A: 手动访问 `http://127.0.0.1:5001` 即可。

### Q: 压缩率不理想？

A: 尝试不同的压缩档位，或安装 `oxipng` 获得更好的效果。

## 📄 许可证

本项目为个人工具，遵循 MIT 许可证。

## 🙏 致谢

- [Flask](https://flask.palletsprojects.com/) - Python Web 框架
- [Pillow](https://python-pillow.org/) - Python 图像处理库
- [oxipng](https://github.com/shssoichiro/oxipng) - PNG 无损压缩工具

---

Made with ❤️ for macOS Sequoia
