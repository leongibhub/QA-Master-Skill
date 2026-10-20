# 安装与第一次任务

## Windows 安装

需要 Python 3.10+、Git 和 `uv`。不需要手工创建或激活 `.venv`；`uv tool` 会管理自己的隔离环境。

```powershell
# 已克隆仓库时，在仓库根目录运行
uv tool install --force --python 3.13 .
```

随后按聊天宿主选择一个入口：

```powershell
# Codex 或 OpenCode 共用的用户级入口
qa-master install-codex --user

# VS Code 的 Claude Code 入口
qa-master install-codex --target "$HOME\.claude\skills\qa-master"
```

前者写入 `$HOME\.agents\skills\qa-master`，后者写入 `$HOME\.claude\skills\qa-master`。不要在同一条命令中混用 `--user`、`--project` 和 `--target`。

若只安装到一个项目：

```powershell
# Codex 或 OpenCode
qa-master install-codex --project "<项目绝对路径>"

# VS Code 的 Claude Code
qa-master install-codex --target "<项目绝对路径>\.claude\skills\qa-master"
```

项目级入口分别位于 `<项目>\.agents\skills\qa-master` 和 `<项目>\.claude\skills\qa-master`。Linux/macOS 使用相同命令，将路径分隔符改为 `/`；例如 Claude Code 用户级目标为 `$HOME/.claude/skills/qa-master`。

VS Code 里的 Claude Code 是 Skill 宿主；QA 使用的 DeepSeek 模型继续由 Claude Code 的既有配置选择。QA Master 不读取、不设置模型端点、密码或 API Token。

## 检查安装后的内容

以下是 Codex/OpenCode 的用户级安装检查；Claude Code 安装时将 `.agents` 替换为 `.claude`：

```powershell
Test-Path "$HOME\.agents\skills\qa-master\SKILL.md"
py -3 -I "$HOME\.agents\skills\qa-master\scripts\qa.py" skills
```

第一条应为 `True`。第二条从安装后的助手读取资料，而非从原仓库读取；JSON 中 `vendor.count` 应为 330，`en` / `zh` 各为 165。它们代表 165 个逻辑技能，分类合计为双语工作流 20、测试类型 300、技能工程 10。若数量为 0，不应继续假定安装完整；记录命令输出和安装版本后检查交付。

安装目录也应含 `SKILL.md`、`references/`、`examples/` 和 `scripts/`。目录存在只是交付检查，不代表 Agent 已实际应用这些指南。

## 开始工作

关闭并新建目标宿主的聊天会话后，在项目内提供真实文件路径。Claude Code 可使用：

```text
/qa-master 阅读当前项目需求并生成测试用例；只做设计，不执行测试，不写入外部系统。
```

建议说明：要完成哪些阶段、材料在哪里、希望得到哪些文件，以及允许哪些外部操作。缺少构建时仍可设计，并保留等待构建的交接说明。不要为了调用 Skill 而先把普通需求改写成工具专用格式。

若只需观察路由和状态，可使用安装助手；将 `<skill>` 替换为实际安装目录：

```powershell
py -3 -I "<skill>\scripts\qa.py" init demo-login
py -3 -I "<skill>\scripts\qa.py" plan "只评审用例，不要提交缺陷"
py -3 -I "<skill>\scripts\qa.py" status
```

状态默认写入当前目录的 `.qa-master/campaign.json`。不同任务使用不同目录，或在子命令前传入 `--state <文件>`。`init` 用于新状态；已有任务先查看 `status`，避免把新建当成恢复。

## 更新与继续

更新 Python 包后，对原目标使用安装器更新模式：

```powershell
uv tool install --force --link-mode=copy --python 3.13 .
qa-master install-codex --user --update
```

更新 Claude Code 入口时，对相同目标追加 `--update`：`qa-master install-codex --target "$HOME\.claude\skills\qa-master" --update`。安装器仅更新未被手工修改的受管理安装并保留备份。遇到拒绝时先检查本地改动，不要删除目录来绕过保护。`uv` 的 hardlink 失败提示仅表示已回退到复制，不影响安装；`--link-mode=copy` 可以避免该提示。更新后再次运行安装助手的 `skills` 自检。

在任务目录中，可保存暂停原因和恢复状态：

```powershell
py -3 -I "<skill>\scripts\qa.py" pause "等待可测试构建"
py -3 -I "<skill>\scripts\qa.py" resume
```

恢复不会批准需求、用例、外部写入或测试执行。由 Agent 读取先前产物和最新来源，确认变化后继续。

## 下一步

- 找到具体方法：[完整技能目录](SKILL_CATALOG.md)。
- 使用结构化有限模型：[设计方法契约](../qa_master/skills/codex/references/design-methods.md)。
- 连接企业系统：[配置中心](CONFIGURATION.md) 与 [企业接口](ENTERPRISE_ADAPTERS.md)。
- 开始真实执行前：[本机 Runner](LOCAL_RUNNER.md) 与 [证据绑定](EVIDENCE_BINDING.md)。
