# 在Mac上打包Windows应用

在Mac电脑上打包Windows应用有以下几种方法：

## 方法一：GitHub Actions（推荐）⭐

**优点：**
- ✅ 最简单，无需本地配置
- ✅ 自动构建，无需安装任何工具
- ✅ 构建环境稳定可靠
- ✅ 完全免费

**步骤：**

1. **推送代码到GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **创建tag触发构建**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **下载构建好的exe**
   - 打开GitHub仓库页面
   - 点击 "Actions" 标签
   - 选择最新的构建任务
   - 在 "Artifacts" 部分下载 `文件清理工具-windows`

4. **或者手动触发构建**
   - 打开GitHub仓库页面
   - 点击 "Actions" 标签
   - 选择 "Build Windows Application" 工作流
   - 点击 "Run workflow" 按钮

## 方法二：使用Wine

**优点：**
- ✅ 本地构建，无需网络
- ✅ 可以立即测试

**缺点：**
- ⚠️ 需要安装Wine
- ⚠️ 构建过程较慢
- ⚠️ 可能遇到兼容性问题

**步骤：**

1. **安装Wine**
   ```bash
   brew install --cask wine-stable
   ```

2. **运行打包脚本**
   ```bash
   chmod +x build_windows_wine.sh
   ./build_windows_wine.sh
   ```

3. **等待构建完成**
   - 首次运行需要下载Windows版PyInstaller
   - 构建完成后，exe文件在 `dist/文件清理工具.exe`

**注意事项：**
- Wine打包的exe建议在Windows系统上测试
- 如果遇到问题，建议使用GitHub Actions方法

## 方法三：使用虚拟机

如果以上方法都不适合，可以使用虚拟机：

1. 安装Parallels Desktop或VMware Fusion
2. 在虚拟机中安装Windows系统
3. 在Windows虚拟机中运行打包脚本

## 推荐方案

**强烈推荐使用GitHub Actions**，因为：
- 无需本地配置
- 构建环境稳定
- 完全自动化
- 可以生成发布版本

## 快速开始（GitHub Actions）

```bash
# 1. 初始化Git仓库（如果还没有）
git init
git add .
git commit -m "Add file cleaner app"

# 2. 创建GitHub仓库并推送
# （在GitHub上创建新仓库，然后）
git remote add origin <your-repo-url>
git push -u origin main

# 3. 创建tag触发构建
git tag v1.0.0
git push origin v1.0.0

# 4. 等待几分钟，在GitHub Actions页面下载exe
```

## 故障排除

### GitHub Actions构建失败

1. 检查 `.github/workflows/build-windows.yml` 文件是否存在
2. 确保所有依赖都在 `requirements.txt` 中
3. 查看Actions页面的错误日志

### Wine打包失败

1. 确保Wine正确安装：`wine --version`
2. 尝试更新Wine：`brew upgrade --cask wine-stable`
3. 如果问题持续，建议使用GitHub Actions

## 相关文件

- `.github/workflows/build-windows.yml` - GitHub Actions工作流配置
- `build_windows_wine.sh` - Wine打包脚本
- `file_cleaner.spec` - PyInstaller配置文件

