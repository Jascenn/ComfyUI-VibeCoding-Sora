# ComfyUI-VibeCoding-Sora 发行包

ComfyUI 自定义节点，用于通过 VibeCoding API 生成 Sora-2 视频。

## ✨ 特性

- 🎬 支持 3 个 Sora 模型：sora-2 / sora-2-pro / sora-2-hd
- 🎥 双模式：文生视频 (Text-to-Video) 和 图生视频 (Image-to-Video)
- 📤 4个输出：文本结果、缩略图、视频元数据、文件路径
- 🖼️ 自动生成视频缩略图（第一帧）
- 💾 自动下载视频到 output 目录
- 🎯 开箱即用的工作流

## 📦 包含文件

```
ComfyUI-VibeCoding-Sora-发行包/
├── install.sh                    # 一键安装脚本 (macOS/Linux)
├── install.bat                   # 一键安装脚本 (Windows)
├── vibecoding_sora-2.json       # 工作流文件
├── node_files/                   # 节点源码
│   ├── __init__.py
│   └── custom_sora_node.py
└── README.md                     # 本文件
```

## 🚀 快速开始

### 前提条件

1. ✅ 已安装 **ComfyUI** (支持桌面版/源码版)
2. ✅ 拥有 **VibeCoding API Key**

### 安装步骤

#### Step 1: 安装 ComfyUI（如果还没有）

下载并安装 ComfyUI.app：
- 官方下载：https://github.com/comfyanonymous/ComfyUI
- 安装后首次启动 ComfyUI

#### Step 2: 安装依赖节点

1. 在 ComfyUI 中加载 `vibecoding_sora-2.json`
2. 会提示缺失节点，点击 **"Manager"** 按钮
3. 使用 **"Install Missing Nodes"** 自动安装：
   - ComfyUI-Custom-Scripts
   - ComfyUI-VideoHelperSuite
4. 安装完成后点击 **"Restart"** 重启

#### Step 3: 安装 CustomSoraVideo 节点

**macOS / Linux:**
```bash
cd /path/to/ComfyUI-VibeCoding-Sora-发行包
bash install.sh
```

**Windows:**
```cmd
cd C:\path\to\ComfyUI-VibeCoding-Sora-发行包
install.bat
```

**脚本功能：**
- ✅ 自动检测 ComfyUI 安装位置
- ✅ 如果检测失败，可手动输入路径
- ✅ 支持参数指定路径
  - macOS/Linux: `bash install.sh /path/to/ComfyUI`
  - Windows: `install.bat C:\path\to\ComfyUI`
- ✅ 自动复制节点文件到 custom_nodes 目录
- ✅ 自动安装 opencv-python 依赖

#### Step 4: 重启 ComfyUI

**⚠️ 重要：必须完全重启 ComfyUI！**

- **终端运行**：按 `Ctrl+C` 停止，然后重新运行
- **macOS 应用**：`Command+Q` 完全退出，重新打开
- **Windows 应用**：关闭窗口或任务管理器结束进程，重新打开

#### Step 5: 使用工作流

1. 在 ComfyUI 中重新加载 `vibecoding_sora-2.json`
2. 所有节点应该正常显示（无红色缺失提示）
3. 在 **CustomSoraVideo** 节点填入你的 API Key
4. 点击 **"Queue Prompt"** 开始生成！

## 📋 使用说明

### 节点参数对照表

| 参数名称 | 说明 |
|---------|------|
| **api_url** | API 端点地址（默认即可） |
| **api_key** | API 密钥（可留空使用环境变量 VIBECODING_API_KEY） |
| **model** | 选择模型<br>• sora-2: 标准模型 (4-15秒)<br>• sora-2-pro: 专业版 (4-25秒)<br>• sora-2-hd: 高清版 (4-12秒) |
| **size** | 视频尺寸<br>• 1280x720 (推荐)<br>• 1920x1080<br>• 720x1280 (竖屏) |
| **duration** | 视频时长（秒），取决于选择的模型 |
| **prompt** | 视频描述（**必须英文**） |
| **seed** | 随机种子（任意数字） |
| **control** | 种子控制<br>• fixed: 固定种子<br>• randomize: 随机生成 |
| **image** | 可选图片输入（图生视频模式） |

### 双模式支持

**文生视频 (Text-to-Video)：**
- 断开 LoadImage 连接
- 仅使用 prompt 描述生成视频

**图生视频 (Image-to-Video)：**
- 连接 LoadImage 节点（默认已连接）
- 在 LoadImage 节点选择图片
- prompt 描述视频动作和风格
- 示例：`"The scene gradually comes to life with gentle motion"`

### 输出说明

工作流提供 4 个输出：

| 输出名称 | 类型 | 说明 |
|---------|------|------|
| **text_result** | STRING | 详细生成信息（任务ID、URL、路径等） |
| **thumbnail** | IMAGE | 视频第一帧缩略图 |
| **video** | VIDEO | 视频元数据（已自动下载） |
| **video_path** | STRING | 本地文件完整路径 |

## 🔑 API Key 配置

### 方法 1: 在节点中填写
直接在 `api_key` 字段填入你的密钥

### 方法 2: 环境变量（推荐）

**macOS/Linux:**
```bash
echo 'export VIBECODING_API_KEY="vb-proj-xxxxx"' >> ~/.zshrc
source ~/.zshrc
```

**Windows:**
```cmd
setx VIBECODING_API_KEY "vb-proj-xxxxx"
```

然后重启 ComfyUI

## 📁 输出位置

生成的视频自动保存到：
```
~/Documents/ComfyUI/output/custom_sora_[model]_[timestamp].mp4
```

## 🐛 故障排查

### 问题 1：节点未加载

**检查：**

macOS/Linux:
```bash
ls ~/Documents/ComfyUI/custom_nodes/ComfyUI-VibeCoding-Sora
```

Windows:
```cmd
dir %USERPROFILE%\Documents\ComfyUI\custom_nodes\ComfyUI-VibeCoding-Sora
```

应该看到 `__init__.py` 和 `custom_sora_node.py`

**解决：**
完全重启 ComfyUI（不是刷新页面）

### 问题 2：缩略图显示灰色

**原因：**opencv-python 未安装

**解决：**

macOS/Linux:
```bash
~/Documents/ComfyUI/.venv/bin/pip install opencv-python
```

Windows:
```cmd
%USERPROFILE%\Documents\ComfyUI\.venv\Scripts\pip.exe install opencv-python
```

### 问题 3：API 调用失败

**检查：**
1. API Key 是否正确
2. 网络连接是否正常
3. API 余额是否充足

### 问题 4：Read-only file system 错误

这是 macOS App Translocation 安全机制问题。

**解决：**
```bash
xattr -cr /Applications/ComfyUI.app
# 完全退出 ComfyUI.app，重新打开
```

## 💡 使用技巧

1. **首次使用**：建议 duration 设为 4-8 秒
2. **Prompt**：必须使用英文描述
3. **随机生成**：seed=0 + control="randomize"
4. **重复生成**：使用相同 seed + control="fixed"
5. **高清视频**：选择 sora-2-hd 模型

## 📊 参数推荐

### 快速测试
```
model: sora-2
size: 1280x720
duration: 8
```

### 中等时长视频
```
model: sora-2
size: 1280x720
duration: 12
prompt: (英文描述，适合有情节的短片)
```

### 长视频（专业版）
```
model: sora-2-pro
size: 1920x1080
duration: 20
```

### 图生视频
```
model: sora-2
size: 1280x720
duration: 8
image: [连接 LoadImage]
prompt: The scene gradually comes to life with gentle motion
```

## ⚠️ 重要提示

- Prompt 必须使用英文
- 视频自动保存到 output 目录
- 修改 seed 值可重新生成不同结果
- 文生视频模式：断开 LoadImage 连接即可

## 🔗 相关链接

- [VibeCoding API 文档](https://vibecodingapi.ai/docs)
- [ComfyUI 官方文档](https://github.com/comfyanonymous/ComfyUI)

## 📝 版本历史

### v1.2.0 (2025-10-16)
- ✅ 支持图片输入（Image-to-Video）
- ✅ 完整的工作流配置
- ✅ 一键安装脚本

---

**祝你使用愉快！🎉**
