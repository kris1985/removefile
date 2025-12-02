@echo off
chcp 65001 >nul
echo ========================================
echo 文件清理工具 - Windows打包脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

echo [1/4] 检查并安装依赖...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo.
echo [2/4] 生成应用图标...
python generate_icon.py

if errorlevel 1 (
    echo [警告] 图标生成失败，将使用默认图标
)

echo.
echo [3/4] 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo [4/4] 开始打包...
python -m PyInstaller file_cleaner.spec --clean

if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo 可执行文件位置: dist\文件清理工具.exe
echo.
echo 提示：
echo - 可以将 dist\文件清理工具.exe 复制到任何Windows电脑上使用
echo - 首次运行可能会被杀毒软件拦截，请添加信任
echo.
pause

