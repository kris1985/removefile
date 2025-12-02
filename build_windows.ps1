# PowerShell打包脚本
# 文件清理工具 - Windows打包脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "文件清理工具 - Windows打包脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python是否安装
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[1/5] 检查Python..." -ForegroundColor Green
    Write-Host "找到: $pythonVersion" -ForegroundColor Gray
} catch {
    Write-Host "[错误] 未找到Python，请先安装Python 3.7或更高版本" -ForegroundColor Red
    Read-Host "按Enter键退出"
    exit 1
}

Write-Host ""
Write-Host "[2/5] 检查并安装依赖..." -ForegroundColor Green
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 依赖安装失败" -ForegroundColor Red
    Read-Host "按Enter键退出"
    exit 1
}

Write-Host ""
Write-Host "[3/5] 生成应用图标..." -ForegroundColor Green
python generate_icon.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "[警告] 图标生成失败，将使用默认图标" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[4/5] 清理旧的构建文件..." -ForegroundColor Green
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "__pycache__") { Remove-Item -Recurse -Force "__pycache__" }

Write-Host ""
Write-Host "[5/5] 开始打包..." -ForegroundColor Green
python -m PyInstaller file_cleaner.spec --clean

if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 打包失败" -ForegroundColor Red
    Read-Host "按Enter键退出"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "打包完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "可执行文件位置: dist\文件清理工具.exe" -ForegroundColor Yellow
Write-Host ""
Write-Host "提示：" -ForegroundColor Cyan
Write-Host "- 可以将 dist\文件清理工具.exe 复制到任何Windows电脑上使用" -ForegroundColor Gray
Write-Host "- 首次运行可能会被杀毒软件拦截，请添加信任" -ForegroundColor Gray
Write-Host ""
Read-Host "按Enter键退出"

