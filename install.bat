@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==========================================
echo 🎬 ComfyUI-VibeCoding-Sora 安装脚本
echo ==========================================
echo.

rem 检测 ComfyUI 目录
set "COMFYUI_DIR="

rem 如果用户提供了参数，使用参数作为路径
if not "%~1"=="" (
    if exist "%~1" (
        set "COMFYUI_DIR=%~1"
        echo ✅ 使用指定路径: !COMFYUI_DIR!
    ) else (
        echo ❌ 错误：指定的路径不存在：%~1
        exit /b 1
    )
) else (
    rem 自动检测常见的 ComfyUI 安装位置
    echo 🔍 正在检测 ComfyUI 安装位置...
    echo.

    rem 检查常见位置
    if exist "%USERPROFILE%\Documents\ComfyUI" (
        set "COMFYUI_DIR=%USERPROFILE%\Documents\ComfyUI"
        echo    找到：!COMFYUI_DIR!
        goto :found
    )
    if exist "%USERPROFILE%\ComfyUI" (
        set "COMFYUI_DIR=%USERPROFILE%\ComfyUI"
        echo    找到：!COMFYUI_DIR!
        goto :found
    )
    if exist "C:\ComfyUI" (
        set "COMFYUI_DIR=C:\ComfyUI"
        echo    找到：!COMFYUI_DIR!
        goto :found
    )
    if exist ".\ComfyUI" (
        set "COMFYUI_DIR=.\ComfyUI"
        echo    找到：!COMFYUI_DIR!
        goto :found
    )
    if exist "..\ComfyUI" (
        set "COMFYUI_DIR=..\ComfyUI"
        echo    找到：!COMFYUI_DIR!
        goto :found
    )

    rem 未找到，提示用户输入
    echo ❌ 未能自动检测到 ComfyUI 目录
    echo.
    echo 已检查以下位置：
    echo    - %USERPROFILE%\Documents\ComfyUI
    echo    - %USERPROFILE%\ComfyUI
    echo    - C:\ComfyUI
    echo    - .\ComfyUI
    echo    - ..\ComfyUI
    echo.
    echo 💡 请提供 ComfyUI 安装路径：
    echo    方法1: install.bat C:\path\to\ComfyUI
    echo    方法2: 手动输入（按 Enter 继续）
    echo.
    set /p "COMFYUI_DIR=请输入 ComfyUI 路径: "

    if "!COMFYUI_DIR!"=="" (
        echo ❌ 路径不能为空
        exit /b 1
    )
    if not exist "!COMFYUI_DIR!" (
        echo ❌ 路径无效或不存在
        exit /b 1
    )

    :found
    echo.
    echo ✅ 找到 ComfyUI 目录：!COMFYUI_DIR!
)

echo.

rem 节点目标目录
set "NODE_DIR=!COMFYUI_DIR!\custom_nodes\ComfyUI-VibeCoding-Sora"

rem 检查节点是否已存在
if exist "!NODE_DIR!" (
    echo ⚠️  检测到已存在的节点目录
    echo    位置：!NODE_DIR!
    echo.
    set /p "CONFIRM=是否覆盖安装？[y/N] "
    if /i not "!CONFIRM!"=="y" (
        echo ❌ 安装已取消
        exit /b 1
    )
    echo 🗑️  删除旧版本...
    rmdir /s /q "!NODE_DIR!"
)

rem 复制节点文件
echo 📦 安装节点文件...
mkdir "!NODE_DIR!" 2>nul
xcopy /s /y /q "node_files\*" "!NODE_DIR!\" >nul

echo ✅ 节点文件已复制
echo.

rem 安装 Python 依赖
echo 📦 安装 Python 依赖（opencv-python）...

rem 检测 Python 环境
set "PYTHON_PIP="
if exist "!COMFYUI_DIR!\.venv\Scripts\pip.exe" (
    set "PYTHON_PIP=!COMFYUI_DIR!\.venv\Scripts\pip.exe"
    echo    使用 ComfyUI 虚拟环境：!PYTHON_PIP!
) else if exist "!COMFYUI_DIR!\python_embeded\python.exe" (
    set "PYTHON_PIP=!COMFYUI_DIR!\python_embeded\python.exe -m pip"
    echo    使用 ComfyUI 内置 Python
) else (
    where pip >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON_PIP=pip"
        echo    使用系统 pip
    ) else (
        echo ⚠️  警告：未找到 pip，跳过依赖安装
        echo    请手动安装：pip install opencv-python
        goto :skip_pip
    )
)

echo    正在安装 opencv-python...
!PYTHON_PIP! install opencv-python --quiet

echo ✅ Python 依赖已安装
:skip_pip
echo.

echo ==========================================
echo ✅ 安装完成！
echo ==========================================
echo.
echo 📋 已安装：
echo    • CustomSoraVideo 节点
echo    • opencv-python 依赖
echo.
echo 📍 节点位置：
echo    !NODE_DIR!
echo.
echo 🚀 下一步操作：
echo    1. ⚠️  完全重启 ComfyUI（不要只刷新浏览器）
echo    2. 📂 在 ComfyUI 中加载 vibecoding_sora-2.json
echo    3. 🔑 填入您的 API Key
echo    4. ▶️  开始生成视频！
echo.
echo ==========================================

pause
