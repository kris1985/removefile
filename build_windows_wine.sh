#!/bin/bash
# 使用Wine在Mac上打包Windows应用
# 需要先安装Wine: brew install --cask wine-stable

set -e

echo "========================================"
echo "文件清理工具 - Mac上打包Windows应用"
echo "使用Wine + PyInstaller"
echo "========================================"
echo ""

# 检查Wine是否安装
if ! command -v wine &> /dev/null; then
    echo "❌ 未找到Wine"
    echo ""
    echo "请先安装Wine:"
    echo "  brew install --cask wine-stable"
    echo ""
    echo "或者使用GitHub Actions自动构建（推荐）:"
    echo "  1. 推送代码到GitHub"
    echo "  2. 创建tag: git tag v1.0.0 && git push origin v1.0.0"
    echo "  3. 在GitHub Actions页面下载构建好的exe"
    exit 1
fi

echo "✅ 找到Wine: $(wine --version)"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python"
    exit 1
fi

echo "✅ 找到Python: $(python3 --version)"
echo ""

# 安装依赖
echo "[1/4] 安装Python依赖..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

# 生成图标
echo ""
echo "[2/4] 生成应用图标..."
python3 generate_icon.py

if [ $? -ne 0 ]; then
    echo "⚠️  图标生成失败，将使用默认图标"
fi

# 清理旧的构建文件
echo ""
echo "[3/4] 清理旧的构建文件..."
rm -rf build dist __pycache__ *.spec.bak

# 下载Windows版PyInstaller（如果不存在）
PYINSTALLER_DIR="$HOME/.wine/drive_c/PyInstaller"
PYINSTALLER_ZIP="$HOME/.wine/drive_c/pyinstaller.zip"

if [ ! -d "$PYINSTALLER_DIR" ]; then
    echo ""
    echo "[4/5] 下载Windows版PyInstaller..."
    mkdir -p "$(dirname "$PYINSTALLER_DIR")"
    
    # 下载PyInstaller
    PYINSTALLER_URL="https://github.com/pyinstaller/pyinstaller/releases/download/v5.13.0/pyinstaller-5.13.0.zip"
    curl -L -o "$PYINSTALLER_ZIP" "$PYINSTALLER_URL" || {
        echo "❌ 下载PyInstaller失败"
        echo "请手动下载并解压到: $PYINSTALLER_DIR"
        exit 1
    }
    
    # 使用Wine解压
    wine unzip -q "$PYINSTALLER_ZIP" -d "$(dirname "$PYINSTALLER_DIR")" || {
        echo "❌ 解压PyInstaller失败"
        exit 1
    }
    
    rm -f "$PYINSTALLER_ZIP"
fi

# 创建临时Python脚本用于Wine环境
echo ""
echo "[5/5] 使用Wine打包Windows应用..."
echo "⚠️  这可能需要几分钟时间..."

# 创建Windows批处理脚本
cat > build_wine.bat << 'EOF'
@echo off
chcp 65001 >nul
cd /d %~dp0
python -m pip install -r requirements.txt
python generate_icon.py
pyinstaller file_cleaner.spec --clean
EOF

# 使用Wine运行
wine cmd /c build_wine.bat

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✅ 打包完成！"
    echo "========================================"
    echo ""
    echo "可执行文件位置: dist/文件清理工具.exe"
    echo ""
    echo "注意：由于在Mac上使用Wine打包，"
    echo "建议在Windows系统上测试exe文件是否正常运行。"
    echo ""
else
    echo ""
    echo "❌ 打包失败"
    echo ""
    echo "建议使用GitHub Actions自动构建（更可靠）:"
    echo "  1. 推送代码到GitHub"
    echo "  2. 创建tag: git tag v1.0.0 && git push origin v1.0.0"
    echo "  3. 在GitHub Actions页面下载构建好的exe"
    exit 1
fi

# 清理临时文件
rm -f build_wine.bat

