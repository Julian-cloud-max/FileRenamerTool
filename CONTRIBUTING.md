# 🤝 贡献指南

感谢你考虑为 FileRenamerTool 做出贡献！我们欢迎所有形式的贡献，包括但不限于：

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- 🎨 改进用户界面

## 📋 贡献流程

### 1. 准备工作

1. **Fork 项目**
   - 在 GitHub 上 Fork 这个项目到你的账户
   - 克隆你的 Fork 到本地

2. **设置开发环境**
   ```bash
   git clone https://github.com/your-username/FileRenamerTool.git
   cd FileRenamerTool
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或者
   git checkout -b fix/your-bug-fix
   ```

### 2. 开发规范

#### 代码风格
- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) Python 代码规范
- 使用 4 个空格进行缩进
- 行长度不超过 120 字符
- 使用有意义的变量和函数名

#### 提交信息规范
使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

类型说明：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat: add regex support for text replacement
fix: resolve file sorting issue with numbers
docs: update installation instructions
```

#### 测试要求
- 确保你的代码能够正常运行
- 测试新功能或修复的 Bug
- 确保没有破坏现有功能

### 3. 提交贡献

1. **提交代码**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   git push origin feature/your-feature-name
   ```

2. **创建 Pull Request**
   - 在 GitHub 上创建 Pull Request
   - 填写详细的描述，说明你的更改
   - 如果解决了某个 Issue，请在描述中引用

3. **Pull Request 模板**
   ```markdown
   ## 更改类型
   - [ ] Bug 修复
   - [ ] 新功能
   - [ ] 文档更新
   - [ ] 代码重构
   - [ ] 其他

   ## 描述
   请详细描述你的更改...

   ## 测试
   - [ ] 我已经测试了这些更改
   - [ ] 没有破坏现有功能

   ## 相关 Issue
   修复 #123
   ```

### 4. 代码审查

- 所有 Pull Request 都会经过代码审查
- 请耐心等待维护者的反馈
- 根据反馈进行必要的修改

## 🐛 报告 Bug

### Bug 报告模板

```markdown
## Bug 描述
简要描述这个 Bug...

## 重现步骤
1. 打开程序
2. 选择文件夹
3. 执行操作
4. 出现错误

## 预期行为
应该发生什么...

## 实际行为
实际发生了什么...

## 环境信息
- 操作系统：Windows 10/11
- Python 版本：3.9+
- 程序版本：v1.0.0

## 附加信息
截图、日志文件等...
```

## 💡 功能建议

### 建议模板

```markdown
## 功能描述
详细描述你想要的功能...

## 使用场景
在什么情况下会用到这个功能...

## 实现建议
如果有的话，提供实现思路...

## 优先级
- [ ] 高
- [ ] 中
- [ ] 低
```

## 📝 文档贡献

我们欢迎文档改进，包括：

- 完善 README.md
- 添加使用示例
- 改进代码注释
- 翻译文档

## 🎯 开发重点

### 当前优先功能
- 正则表达式支持
- 子文件夹递归处理
- 更多主题选项
- 批量操作统计

### 技术债务
- 代码重构和优化
- 单元测试覆盖
- 性能优化
- 错误处理改进

## 📞 联系我们

如果你有任何问题或需要帮助：

- 在 [Issues](https://github.com/your-username/FileRenamerTool/issues) 中提问
- 在 [Discussions](https://github.com/your-username/FileRenamerTool/discussions) 中讨论
- 直接联系维护者

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！你的贡献让这个项目变得更好。

---

**记住：每一个贡献，无论大小，都是宝贵的！** 🌟 