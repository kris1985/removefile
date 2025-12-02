# 文件清理工具

一个基于Python和tkinter的可视化文件清理工具，用于根据主图目录和副图目录，自动删除找不到对应主图的副图文件。

## 功能特点

- 🖼️ 可视化图形界面，操作简单
- 📁 支持递归遍历子目录
- 🔍 智能匹配主图和副图文件
- 🗑️ 自动删除找不到主图的副图
- 📂 自动清理空文件夹
- 📝 详细的操作日志

## 文件匹配规则

副图文件名规则：`文件名_副图.扩展名`

主图文件名：从副图文件名中提取 `_副图` 之前的部分，加上原扩展名

**示例：**
- 副图：`图片_副图.jpg` → 主图：`图片.jpg`
- 副图：`photo_副图.png` → 主图：`photo.png`

## 使用方法

### 方式一：直接运行Python脚本

1. 确保已安装Python 3.7或更高版本
2. 运行程序：
```bash
python file_cleaner.py
```

### 方式二：使用打包后的Windows可执行文件

1. 运行 `dist\文件清理工具.exe`
2. 无需安装Python环境

## Windows打包说明

### 在Windows上打包

### 打包步骤

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **执行打包脚本**
   
   **方法A：使用批处理脚本（推荐）**
   ```bash
   build_windows.bat
   ```
   
   **方法B：使用PowerShell脚本**
   ```powershell
   .\build_windows.ps1
   ```
   
   **方法C：手动打包**
   ```bash
   pyinstaller file_cleaner.spec --clean
   ```

3. **打包结果**
   - 打包完成后，可执行文件位于 `dist\文件清理工具.exe`
   - 可以将此exe文件复制到任何Windows电脑上使用，无需安装Python

### 在Mac上打包Windows应用

在Mac电脑上也可以打包Windows应用，有两种方法：

#### 方法一：使用GitHub Actions（推荐）⭐

**最简单的方法，无需本地配置：**

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

**或者手动触发：**
- 在GitHub仓库页面 → Actions → "Build Windows Application" → "Run workflow"

#### 方法二：使用Wine

**本地构建，需要安装Wine：**

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

**注意：** Wine打包的exe建议在Windows系统上测试。如果遇到问题，建议使用GitHub Actions方法。

详细说明请查看 [BUILD_MAC.md](BUILD_MAC.md)

### 打包选项说明

- `console=False`: 不显示控制台窗口，纯GUI应用
- `upx=True`: 启用UPX压缩，减小文件体积
- `name='文件清理工具'`: 生成的可执行文件名称

### 应用图标

程序已包含自动生成的应用图标，体现"文件清理"主题：
- 🎨 蓝色圆形背景，现代简洁设计
- 📄 文件图标配合红色删除标记
- ➡️ 箭头表示清理过程
- 自动生成多种尺寸适配Windows系统

图标会在打包过程中自动生成（`generate_icon.py`），无需手动操作。

如果需要自定义图标：
1. 准备一个 `.ico` 格式的图标文件（如 `custom_icon.ico`）
2. 在 `file_cleaner.spec` 文件中修改图标路径
3. 重新打包

## 系统要求

- **开发环境**：Python 3.7+
- **运行环境（打包后）**：Windows 7/8/10/11
- **依赖库**：
  - tkinter（Python标准库，通常已包含）
  - PyInstaller（仅打包时需要）
  - Pillow（仅打包时用于生成图标）

## 注意事项

1. ⚠️ **数据安全**：此工具会删除文件，操作前请确保已备份重要数据
2. ⚠️ **杀毒软件**：首次运行打包后的exe可能会被杀毒软件拦截，需要添加信任
3. ⚠️ **文件匹配**：确保副图文件名包含 `_副图` 标识，否则可能无法正确匹配

## 操作流程

1. 启动程序
2. 点击"选择"按钮选择主图目录
3. 点击"选择"按钮选择副图目录
4. 点击"开始清理"按钮
5. 确认操作后，程序会自动：
   - 遍历副图目录中的所有文件
   - 查找对应的主图文件
   - 删除找不到主图的副图文件
   - 清理空的子文件夹
6. 查看日志了解操作详情

## 许可证

MIT License

