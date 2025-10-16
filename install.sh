#!/bin/bash

# ComfyUI-VibeCoding-Sora 一键安装脚本
# 使用方法：bash install.sh [ComfyUI路径]

set -e

echo "=========================================="
echo "🎬 ComfyUI-VibeCoding-Sora 安装脚本"
echo "=========================================="
echo ""

# 检测 ComfyUI 目录
COMFYUI_DIR=""

# 如果用户提供了参数，使用参数作为路径
if [ -n "$1" ]; then
    if [ -d "$1" ]; then
        COMFYUI_DIR="$1"
        echo "✅ 使用指定路径：$COMFYUI_DIR"
    else
        echo "❌ 错误：指定的路径不存在：$1"
        exit 1
    fi
else
    # 自动检测常见的 ComfyUI 安装位置
    echo "🔍 正在检测 ComfyUI 安装位置..."
    echo ""

    POSSIBLE_PATHS=(
        "$HOME/Documents/ComfyUI"
        "$HOME/ComfyUI"
        "/Applications/ComfyUI/ComfyUI"
        "$HOME/Applications/ComfyUI"
        "./ComfyUI"
        "../ComfyUI"
    )

    for path in "${POSSIBLE_PATHS[@]}"; do
        if [ -d "$path" ]; then
            echo "   找到：$path"
            COMFYUI_DIR="$path"
            break
        fi
    done

    if [ -z "$COMFYUI_DIR" ]; then
        echo "❌ 未能自动检测到 ComfyUI 目录"
        echo ""
        echo "已检查以下位置："
        for path in "${POSSIBLE_PATHS[@]}"; do
            echo "   - $path"
        done
        echo ""
        echo "💡 请提供 ComfyUI 安装路径："
        echo "   方法1: bash install.sh /path/to/ComfyUI"
        echo "   方法2: 手动输入（按 Enter 继续）"
        echo ""
        read -p "请输入 ComfyUI 路径: " user_path

        if [ -n "$user_path" ] && [ -d "$user_path" ]; then
            COMFYUI_DIR="$user_path"
        else
            echo "❌ 路径无效或不存在"
            exit 1
        fi
    fi

    echo ""
    echo "✅ 找到 ComfyUI 目录：$COMFYUI_DIR"
fi

echo ""

# 节点目标目录
NODE_DIR="$COMFYUI_DIR/custom_nodes/ComfyUI-VibeCoding-Sora"

# 检查节点是否已存在
if [ -d "$NODE_DIR" ]; then
    echo "⚠️  检测到已存在的节点目录"
    echo "   位置：$NODE_DIR"
    echo ""
    read -p "是否覆盖安装？[y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 安装已取消"
        exit 1
    fi
    echo "🗑️  删除旧版本..."
    rm -rf "$NODE_DIR"
fi

# 复制节点文件
echo "📦 安装节点文件..."
mkdir -p "$NODE_DIR"
cp -r node_files/* "$NODE_DIR/"

echo "✅ 节点文件已复制"
echo ""

# 安装 Python 依赖
echo "📦 安装 Python 依赖（opencv-python）..."

# 检测 Python 环境
if [ -f "$COMFYUI_DIR/.venv/bin/pip" ]; then
    PYTHON_PIP="$COMFYUI_DIR/.venv/bin/pip"
    echo "   使用 ComfyUI 虚拟环境：$PYTHON_PIP"
elif command -v pip3 &> /dev/null; then
    PYTHON_PIP="pip3"
    echo "   使用系统 pip3"
else
    PYTHON_PIP="pip"
    echo "   使用系统 pip"
fi

echo "   正在安装 opencv-python..."
$PYTHON_PIP install opencv-python --quiet

echo "✅ Python 依赖已安装"
echo ""

echo "=========================================="
echo "✅ 安装完成！"
echo "=========================================="
echo ""
echo "📋 已安装："
echo "   • CustomSoraVideo 节点"
echo "   • opencv-python 依赖"
echo ""
echo "📍 节点位置："
echo "   $NODE_DIR"
echo ""
echo "🚀 下一步操作："
echo "   1. ⚠️  完全重启 ComfyUI（不要只刷新浏览器）"
echo "   2. 📂 在 ComfyUI 中加载 vibecoding_sora-2.json"
echo "   3. 🔑 填入您的 API Key"
echo "   4. ▶️  开始生成视频！"
echo ""
echo "=========================================="
