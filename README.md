# PPT Compressor

现代化的 PowerPoint 压缩工具，完全保留 PNG 透明度，支持真正的无损压缩。

## 特性

- 🎨 **完全保留 PNG 透明度** - 所有档位均支持
- 🚀 **真正的无损压缩** - 使用 oxipng 进行 PNG 优化
- 📦 **6 个压缩档位** - 压缩率 15%-95%
- 🖥️ **macOS 原生应用** - 双击即用
- ⚡ **高性能** - 多线程压缩

## 快速开始

```bash
# 安装依赖
pip3 install Pillow
brew install oxipng  # 强烈推荐

# 命令行使用
python3 ppt_compressor_v3.py input.pptx --preset lossless

# 或者双击打开应用
open "PPT Compressor.app"
```

## 压缩档位

| 档位 | 压缩率 | 说明 |
|------|--------|------|
| **lossless** | 15-30% | 完全无损，oxipng 最大压缩 |
| **high** | 30-50% | 高质量，视觉无损 |
| **balanced** | 50-70% | 平衡模式（默认） |
| **aggressive** | 70-85% | 激进压缩，降低颜色+限制尺寸 1280px |
| **small** | 70-85% | 小体积，降低颜色+限制尺寸 1920px |
| **mini** | 85-95% | 极小体积，激进压缩+限制尺寸 1280px |

**所有档位都保留 PNG 格式和透明度！**

## 使用示例

```bash
# 完全无损压缩
python3 ppt_compressor_v3.py file.pptx --preset lossless

# 激进压缩
python3 ppt_compressor_v3.py file.pptx --preset aggressive

# 指定输出路径
python3 ppt_compressor_v3.py input.pptx -o output.pptx --preset balanced
```

## 技术栈

- Python 3.7+
- Pillow (图像处理)
- oxipng (PNG 无损压缩)

## 许可证

MIT License
