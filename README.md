# ComfyUI-VibeCoding-Sora

ComfyUI 自定义节点，用于通过 VibeCoding API 生成 Sora-2 视频。

---

## 🚀 快速安装（3 步完成）

### 1️⃣ 安装依赖节点

在 ComfyUI 中加载 `vibecoding_sora-2.json`，会提示缺失节点：
1. 点击 **"Manager"** 按钮
2. 点击 **"Install Missing Nodes"**
3. 安装完成后点击 **"Restart"**

### 2️⃣ 运行安装脚本

**macOS / Linux:**
```bash
bash install.sh
```

**Windows:**
```cmd
双击运行 install.bat
```

### 3️⃣ 重启 ComfyUI

**完全退出并重新打开 ComfyUI**

---

## ✅ 开始使用

1. 在 ComfyUI 中加载 `vibecoding_sora-2.json`
2. 在 **CustomSoraVideo** 节点填入 API Key
3. 点击 **"Queue Prompt"**

视频会自动保存到：`~/Documents/ComfyUI/output/`

---

## 📚 文档

- **快速开始**: 查看 `快速开始.md`
- **完整文档**: 查看 `README-详细文档.md`

---

## ✨ 功能特性

- 🎬 支持 3 个模型：sora-2 / sora-2-pro / sora-2-hd
- 🎥 文生视频 + 图生视频
- 🖼️ 自动生成缩略图
- 💾 自动下载视频

---

**就这么简单！🎉**

## 贡献与安全

- 参与开发前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 安全问题请按 [SECURITY.md](SECURITY.md) 私下报告，不要开公开 Issue。

## 许可证

本项目原创代码采用 [MIT License](LICENSE)。第三方依赖、上游项目与外部素材继续遵循各自许可证。
