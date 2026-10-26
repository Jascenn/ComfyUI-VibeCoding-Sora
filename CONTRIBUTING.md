# 贡献指南 Contributing

`ComfyUI-VibeCoding-Sora`：通过 VibeCoding API 在 ComfyUI 中生成 Sora-2 视频的自定义节点。 小改动可以直接提 PR；涉及对外行为、数据结构、发布流程或批量重构时，请先开 Issue 对齐范围。

## 本地验证

```bash
python3 -m py_compile node_files/*.py
bash -n install.sh
```

如果 README 的安装步骤无法照做，请把它当作 bug 提交。不要把“在我机器上能跑”当作验证完成。

## 分支与提交

- 分支名使用 `feat/`、`fix/`、`docs/`、`refactor/`、`chore/` 前缀和 kebab-case 描述。
- `main` 只接受 PR；不要直接推送，也不要 force push 已共享的分支。
- 提交标题使用 Conventional Commits，例如 `fix(cli): preserve backup before overwrite`。
- 一个 PR 只解决一个问题。行为变化、格式化、依赖升级不要混在同一次提交里。
- 默认建议 squash merge，让一个 PR 对应 `main` 上的一条可回溯记录。

## 本项目的安全边界

- 不要提交 `VIBECODING_API_KEY`、请求日志、生成结果、下载视频或包含个人路径的工作流快照。
- 默认工作流不得预填真实 API Key；示例必须使用环境变量或空白占位值。
- 修改节点输入输出、模型参数或下载路径时，同时验证文生视频、图生视频和接口失败三条路径。
- 本仓库的 MIT 许可证只覆盖仓库原创代码；ComfyUI、工作流依赖的第三方节点和其他外部素材继续遵循各自许可证。

## PR 最少要写什么

1. 为什么需要改，关联的 Issue 或具体问题。
2. 改了什么，以及明确没有改什么。
3. 陌生人能照着执行的验证命令和结果。
4. 影响面与回滚方式；涉及页面时附桌面和移动端截图。

## 审查与合并

单人维护时，PR 的价值是给未来的自己留下“当时为什么这样做”。评论建议标注 `【阻塞】`、`【建议】` 或 `【nit】`。安全漏洞不要开公开 Issue，请按 [SECURITY.md](SECURITY.md) 私下报告。

## 范围

本项目主要覆盖：ComfyUI 自定义节点、安装脚本、示例工作流、API 调用和视频下载。
