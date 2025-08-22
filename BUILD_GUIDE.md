# FileRenamerTool 构建指南

## 🚀 快速开始

### 方法1: 一键构建 (推荐)
```powershell
# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 运行构建脚本
.\build_package.ps1
```

### 方法2: 分步构建
```powershell
# 1. 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 2. 验证导入
python quick_import_test.py

# 3. 构建包
pyinstaller FileRenamerTool_optimized.spec
```

## 📋 构建选项

### 基本构建
```powershell
.\build_package.ps1
```

### 调试模式构建
```powershell
.\build_package.ps1 -Debug
```

### 控制台模式构建 (便于调试)
```powershell
.\build_package.ps1 -Console
```

### 跳过验证构建
```powershell
.\build_package.ps1 -SkipValidation
```

### 带图标的构建
```powershell
.\build_package.ps1 -Icon "path\to\icon.ico"
```

## 🔧 故障排除

### 1. 导入验证失败
```powershell
# 运行详细验证
python import_validator.py

# 查看具体错误信息
python -c "import customtkinter; print('CustomTkinter OK')"
```

### 2. 构建失败
```powershell
# 清理并重新构建
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
pyinstaller --clean FileRenamerTool_optimized.spec
```

### 3. 可执行文件无法启动
```powershell
# 使用控制台模式查看错误
.\build_package.ps1 -Console
```

## 📁 文件说明

- `quick_import_test.py` - 快速导入验证
- `import_validator.py` - 完整导入验证
- `FileRenamerTool_optimized.spec` - 优化的PyInstaller配置
- `build_package.ps1` - 自动化构建脚本
- `test_imports.ps1` - 导入测试脚本

## ✅ 验证清单

构建前请确认：
- [ ] 虚拟环境已激活
- [ ] 所有依赖已安装 (`pip install -r requirements.txt`)
- [ ] 导入验证通过 (`python quick_import_test.py`)
- [ ] 应用程序可以正常运行 (`python main.py`)

## 🎯 预期结果

成功构建后：
- 可执行文件位置: `dist\FileRenamerTool.exe`
- 文件大小: 约 20-50 MB
- 启动时间: 2-5 秒

## 🐛 常见问题

### Q: 构建的可执行文件很大？
A: 这是正常的，包含了Python运行环境和所有依赖。

### Q: 启动时出现错误？
A: 使用 `-Console` 参数重新构建以查看错误信息。

### Q: 某些功能不工作？
A: 运行 `python import_validator.py` 检查是否缺少依赖。

### Q: 构建很慢？
A: 首次构建较慢，后续构建会使用缓存。

## 📞 获取帮助

如果遇到问题：
1. 运行 `python import_validator.py` 查看详细错误
2. 使用 `-Console` 参数重新构建查看错误信息
3. 检查是否在正确的虚拟环境中
4. 确认所有依赖都已正确安装 