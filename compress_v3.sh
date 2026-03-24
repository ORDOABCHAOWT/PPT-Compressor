#!/bin/bash
# PPT现代化无损压缩工具 v3.0 - Mac版（动态菜单版本）

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 压缩预设配置（从Python代码中读取）
PRESETS=("lossless" "high" "balanced" "aggressive" "small" "mini")
PRESET_NAMES=("完全无损" "高质量" "平衡模式" "激进PNG压缩" "小体积" "极小体积")

clear_screen() {
    clear
}

show_menu() {
    clear_screen
    echo -e "${CYAN}========================================${NC}"
    echo -e "${GREEN}  PPT现代化无损压缩工具 v3.0 (Mac)${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
    echo -e "${YELLOW}🔥 完全保留PNG透明度！${NC}"
    echo ""
    echo "请选择压缩档位："
    echo ""

    # 动态显示预设选项
    for i in "${!PRESETS[@]}"; do
        num=$((i + 1))
        preset="${PRESETS[$i]}"
        name="${PRESET_NAMES[$i]}"

        # 从Python获取该档位的描述
        desc=$($PYTHON_CMD ppt_compressor_v3.py --help 2>/dev/null | grep -A 1 "^\s*${preset}\s*-" | tail -1 | sed 's/^[[:space:]]*//')

        if [ $num -eq 1 ]; then
            echo -e "${GREEN}${num}. ${name}${NC} (推荐⭐)"
        elif [ "$preset" = "aggressive" ]; then
            echo -e "${CYAN}${num}. ${name}${NC} 🆕"
        else
            echo "${num}. ${name}"
        fi

        if [ -n "$desc" ]; then
            echo "   ${desc}"
        fi
        echo ""
    done

    echo "---"
    echo "7. 批量压缩文件夹"
    echo "8. 安装/检查依赖（包括oxipng）"
    echo "0. 退出"
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${YELLOW}💡 提示: 选项1完全无损，保留所有透明度${NC}"
    echo ""
}

check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        return 0
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        return 0
    else
        echo -e "${RED}错误: 未找到Python，请先安装Python 3${NC}"
        return 1
    fi
}

check_dependencies() {
    clear_screen
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}检查并安装依赖${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    if ! check_python; then
        echo ""
        echo "请访问 https://www.python.org/downloads/ 安装Python"
        read -p "按回车键继续..."
        return 1
    fi

    echo -e "${GREEN}✓ Python已安装: $($PYTHON_CMD --version)${NC}"
    echo ""

    # 检查Pillow
    if $PYTHON_CMD -c "import PIL" 2>/dev/null; then
        echo -e "${GREEN}✓ Pillow已安装${NC}"
    else
        echo -e "${YELLOW}⚠ Pillow未安装${NC}"
        echo ""
        read -p "是否现在安装Pillow? (y/n): " install_choice
        if [ "$install_choice" = "y" ] || [ "$install_choice" = "Y" ]; then
            echo ""
            echo "正在安装Pillow..."
            $PYTHON_CMD -m pip install Pillow
            echo ""
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ Pillow安装成功！${NC}"
            else
                echo -e "${RED}✗ Pillow安装失败${NC}"
            fi
        fi
    fi

    echo ""

    # 检查oxipng（关键！）
    if command -v oxipng &> /dev/null; then
        echo -e "${GREEN}✓ oxipng已安装: $(oxipng --version)${NC}"
        echo -e "  ${CYAN}可以使用真正的PNG无损压缩！${NC}"
    else
        echo -e "${YELLOW}⚠ oxipng未安装${NC}"
        echo -e "  ${CYAN}oxipng是PNG无损压缩神器，强烈推荐安装！${NC}"
        echo ""

        # 检查Homebrew
        if command -v brew &> /dev/null; then
            read -p "是否使用Homebrew安装oxipng? (y/n): " install_oxipng
            if [ "$install_oxipng" = "y" ] || [ "$install_oxipng" = "Y" ]; then
                echo ""
                echo "正在安装oxipng..."
                brew install oxipng
                if [ $? -eq 0 ]; then
                    echo ""
                    echo -e "${GREEN}✓ oxipng安装成功！${NC}"
                else
                    echo ""
                    echo -e "${RED}✗ oxipng安装失败${NC}"
                fi
            fi
        else
            echo -e "${YELLOW}未检测到Homebrew，请先安装Homebrew：${NC}"
            echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            echo ""
            echo "然后运行: brew install oxipng"
        fi
    fi

    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo ""
    read -p "按回车键继续..."
}

compress_file() {
    local preset=$1
    local preset_name=$2
    clear_screen
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}压缩PPT文件 - $preset_name${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    read -p "请输入PPT文件路径（或拖拽文件到此窗口）: " pptfile

    pptfile=$(echo "$pptfile" | sed "s/^[[:space:]]*//;s/[[:space:]]*$//;s/^'//;s/'$//")

    if [ -z "$pptfile" ]; then
        echo -e "${RED}错误: 未输入文件路径${NC}"
        read -p "按回车键继续..."
        return
    fi

    if [ ! -f "$pptfile" ]; then
        echo -e "${RED}错误: 文件不存在: $pptfile${NC}"
        read -p "按回车键继续..."
        return
    fi

    echo ""
    echo "开始压缩..."
    echo ""
    $PYTHON_CMD ppt_compressor_v3.py "$pptfile" --preset $preset

    echo ""
    read -p "按回车键继续..."
}

batch_compress_files() {
    clear_screen
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}批量压缩文件夹中的所有PPT${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    read -p "输入文件夹路径（包含PPT文件）: " input_dir
    input_dir=$(echo "$input_dir" | sed "s/^[[:space:]]*//;s/[[:space:]]*$//;s/^'//;s/'$//")

    if [ -z "$input_dir" ]; then
        echo -e "${RED}错误: 未输入文件夹路径${NC}"
        read -p "按回车键继续..."
        return
    fi

    read -p "输出文件夹路径: " output_dir
    output_dir=$(echo "$output_dir" | sed "s/^[[:space:]]*//;s/[[:space:]]*$//;s/^'//;s/'$//")

    if [ -z "$output_dir" ]; then
        echo -e "${RED}错误: 未输入输出路径${NC}"
        read -p "按回车键继续..."
        return
    fi

    echo ""
    echo "选择压缩档位："
    for i in "${!PRESETS[@]}"; do
        num=$((i + 1))
        echo "${num}) ${PRESETS[$i]} (${PRESET_NAMES[$i]})"
    done
    read -p "请选择(1-${#PRESETS[@]}): " preset_choice

    # 验证输入并设置preset
    if [[ "$preset_choice" =~ ^[0-9]+$ ]] && [ "$preset_choice" -ge 1 ] && [ "$preset_choice" -le "${#PRESETS[@]}" ]; then
        preset="${PRESETS[$((preset_choice - 1))]}"
    else
        preset="balanced"
        echo "无效选择，使用默认档位: balanced"
    fi

    echo ""
    echo "开始批量压缩（使用 $preset 档位）..."
    echo ""

    for file in "$input_dir"/*.pptx "$input_dir"/*.ppt; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            echo "处理: $filename"
            $PYTHON_CMD ppt_compressor_v3.py "$file" -o "$output_dir/$filename" --preset $preset
            echo ""
        fi
    done

    echo "批量压缩完成！"
    read -p "按回车键继续..."
}

main() {
    if ! check_python; then
        echo "请先安装Python 3，然后重新运行此脚本"
        exit 1
    fi

    while true; do
        show_menu
        read -p "请输入选项(0-8): " choice

        case $choice in
            1)
                compress_file "${PRESETS[0]}" "${PRESET_NAMES[0]}"
                ;;
            2)
                compress_file "${PRESETS[1]}" "${PRESET_NAMES[1]}"
                ;;
            3)
                compress_file "${PRESETS[2]}" "${PRESET_NAMES[2]}"
                ;;
            4)
                compress_file "${PRESETS[3]}" "${PRESET_NAMES[3]}"
                ;;
            5)
                compress_file "${PRESETS[4]}" "${PRESET_NAMES[4]}"
                ;;
            6)
                compress_file "${PRESETS[5]}" "${PRESET_NAMES[5]}"
                ;;
            7)
                batch_compress_files
                ;;
            8)
                check_dependencies
                ;;
            0)
                echo ""
                echo -e "${GREEN}感谢使用！${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}无效选项，请重新选择${NC}"
                sleep 1
                ;;
        esac
    done
}

main
