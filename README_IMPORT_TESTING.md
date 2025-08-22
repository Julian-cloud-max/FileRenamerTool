# Import Validation Scripts for FileRenamerTool

这些脚本帮助你在打包前验证所有依赖项，避免打包后出现导入错误。

## 文件说明

### 1. `quick_import_test.py`
- **用途**: 快速验证关键依赖
- **运行时间**: 1-2秒
- **检查内容**: 
  - customtkinter 核心模块
  - tkinter 相关模块
  - 标准库模块
  - 应用程序模块

### 2. `import_validator.py`
- **用途**: 全面验证所有可能的依赖
- **运行时间**: 3-5秒
- **检查内容**:
  - 所有 quick_import_test.py 的内容
  - customtkinter 的所有子模块
  - 资源文件检查
  - 运行时依赖检查
  - PyInstaller 建议生成

### 3. `test_imports.bat` / `test_imports.ps1`
- **用途**: 自动化测试脚本
- **功能**: 按顺序运行所有测试并提供清晰的反馈

## 使用方法

### 方法1: 使用自动化脚本 (推荐)

**Windows PowerShell:**
```powershell
.\test_imports.ps1
```

**Windows CMD:**
```cmd
test_imports.bat
```

### 方法2: 手动运行

**快速测试:**
```bash
python quick_import_test.py
```

**完整验证:**
```bash
python import_validator.py
```

## 测试结果解读

### ✅ 成功情况
```
🎉 All tests passed! Ready for packaging.
```

### ⚠️ 失败情况
```
⚠️  Some imports failed. Please fix the issues before packaging.
```

失败时会显示具体的错误信息和 PyInstaller 建议。

## 常见问题解决

### 1. customtkinter 导入失败
```bash
pip install --upgrade customtkinter
```

### 2. 资源文件缺失
确保 customtkinter 安装完整，包含 assets 目录。

### 3. 应用程序导入失败
检查 `app_ui.py` 和 `main.py` 文件是否存在且语法正确。

## PyInstaller 建议

测试完成后，脚本会提供 PyInstaller 命令建议，例如：

```bash
pyinstaller --onefile --windowed --collect-all customtkinter main.py
```

## 工作流程

1. **开发阶段**: 每次修改代码后运行 `quick_import_test.py`
2. **打包前**: 运行 `import_validator.py` 进行全面检查
3. **问题排查**: 根据错误信息修复依赖问题
4. **打包**: 使用建议的 PyInstaller 命令

## 优势

- **提前发现问题**: 在打包前就发现导入错误
- **节省时间**: 避免重复打包-测试-修改的循环
- **自动化**: 一键运行所有测试
- **详细反馈**: 提供具体的错误信息和解决建议

## 注意事项

- 确保在正确的 Python 环境中运行测试
- 如果使用虚拟环境，请先激活环境
- 测试脚本会检查当前目录下的文件，确保在项目根目录运行 