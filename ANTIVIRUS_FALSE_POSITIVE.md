# 🛡️ 杀毒软件误报说明

## ⚠️ 重要提示

**FileRenamerTool.exe 是安全的！** 如果杀毒软件报告病毒，这是**误报**。

## 🔍 为什么会出现误报？

### 技术原因
1. **代码打包技术**：PyInstaller将Python代码打包到exe中，杀毒软件可能误认为这是代码混淆
2. **动态模块加载**：CustomTkinter的动态导入可能触发启发式检测
3. **缺少数字签名**：未签名的可执行文件更容易被误报
4. **启发式检测**：杀毒软件基于行为模式判断，可能误判

### 常见误报场景
- Windows Defender 报告威胁
- 360安全卫士 报告病毒
- 腾讯电脑管家 报告风险
- 火绒 报告可疑文件

## ✅ 如何解决误报？

### 方法1：添加信任/白名单（推荐）

#### Windows Defender
1. 右键点击 `FileRenamerTool.exe` → "属性"
2. 勾选 "解除锁定"（如果有此选项）
3. 在 Windows 安全中心添加排除项：
   - 设置 → 更新和安全 → Windows 安全中心
   - 病毒和威胁防护 → 管理设置
   - 排除项 → 添加或删除排除项
   - 添加 `FileRenamerTool.exe`

#### 360安全卫士
1. 打开360安全卫士
2. 木马查杀 → 信任区
3. 添加 `FileRenamerTool.exe`

#### 腾讯电脑管家
1. 打开腾讯电脑管家
2. 病毒查杀 → 信任区
3. 添加 `FileRenamerTool.exe`

#### 火绒
1. 打开火绒安全
2. 防护中心 → 信任区
3. 添加 `FileRenamerTool.exe`

### 方法2：临时关闭实时保护
1. 临时关闭杀毒软件的实时保护
2. 下载并运行程序
3. 重新开启实时保护

### 方法3：使用源码版本
如果仍然担心，可以使用源码版本：
```bash
git clone https://github.com/Julian-cloud-max/FileRenamerTool.git
cd FileRenamerTool
pip install -r requirements.txt
python main.py
```

## 🔒 安全保证

### 开源透明
- 所有源代码都在GitHub上公开
- 任何人都可以审查代码
- 使用MIT开源协议

### 技术安全
- 纯Python代码，无恶意行为
- 不收集用户数据
- 不连接外部服务器
- 所有操作都在本地进行

### 社区验证
- 项目已获得多个Star
- 有活跃的Issues和讨论
- 代码经过社区审查

## 📋 验证步骤

### 1. 检查文件来源
- 确保从官方GitHub仓库下载
- 检查文件哈希值（如果提供）

### 2. 使用在线扫描
- [VirusTotal](https://www.virustotal.com/)
- [Jotti](https://virusscan.jotti.org/)
- [MetaDefender](https://metadefender.opswat.com/)

### 3. 本地测试
- 在虚拟机中测试
- 在隔离环境中运行

## 🆘 如果问题持续

### 联系支持
- 在GitHub上创建Issue
- 提供杀毒软件名称和版本
- 附上误报截图

### 替代方案
- 使用源码版本
- 等待杀毒软件更新病毒库
- 选择其他杀毒软件

## 📚 相关链接

- [GitHub仓库](https://github.com/Julian-cloud-max/FileRenamerTool)
- [Issues页面](https://github.com/Julian-cloud-max/FileRenamerTool/issues)
- [讨论页面](https://github.com/Julian-cloud-max/FileRenamerTool/discussions)

---

**记住：FileRenamerTool是100%安全的开源软件！** 🛡️✅ 