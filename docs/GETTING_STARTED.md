# 安装与第一次任务

## 选择安装范围

先按 [README 的 Windows / Linux 命令](../README.md#快速开始) 安装 Python 包。以下命令中的 `python` 指该虚拟环境中的 Python。

```bash
# 仅安装到指定业务项目（路径有空格时加引号）
python -m qa_master install-codex --project "<项目绝对路径>"
# 或安装到当前用户
python -m qa_master install-codex --user
```

项目安装位置为 `<项目>/.agents/skills/qa-master`；用户安装位置为 `~/.agents/skills/qa-master`。不要在同一条命令中混用目标参数。重新打开目标项目的 Agent 会话，让宿主重新发现技能。

Windows 无需执行激活脚本：使用 `.\.venv\Scripts\python.exe`。Linux 使用 `.venv/bin/python`。若选择激活，PowerShell 命令为 `.\.venv\Scripts\Activate.ps1`，Bash 命令为 `source .venv/bin/activate`；激活受策略限制时直接使用完整解释器路径即可。

## 检查安装后的内容

将 `<skill>` 替换为安装目录的绝对路径，并在业务项目目录执行：

```bash
python -I "<skill>/scripts/qa.py" skills
```

这条命令从安装后的助手读取资料，而非从原仓库读取。检查返回的专业指南和 `vendor` 统计：双语资料应有 330 个目录，`en` / `zh` 各 165。它们代表 165 个逻辑技能，分类合计为双语工作流 20、测试类型 300、技能工程 10。若数量为 0，不应继续假定安装完整；记录命令输出和安装版本后检查交付。

安装目录也应含 `SKILL.md`、`references/`、`examples/` 和 `scripts/`。目录存在只是交付检查，不代表 Agent 已实际应用这些指南。

## 开始工作

在目标项目内提供真实文件路径：

```text
$qa-master 阅读 docs/requirements.md 和 openapi.yaml，评审需求并制定测试计划。
仅做设计，不执行、不导入；列出已知事实、冲突和需要我补充的信息。
```

建议说明：要完成哪些阶段、材料在哪里、希望得到哪些文件，以及允许哪些外部操作。缺少构建时仍可设计，并保留等待构建的交接说明。不要为了调用 Skill 而先把普通需求改写成工具专用格式。

若只需观察路由和状态，可使用安装助手：

```bash
python -I "<skill>/scripts/qa.py" init demo-login
python -I "<skill>/scripts/qa.py" plan "只评审用例，不要提交缺陷"
python -I "<skill>/scripts/qa.py" status
```

状态默认写入当前目录的 `.qa-master/campaign.json`。不同任务使用不同目录，或在子命令前传入 `--state <文件>`。`init` 用于新状态；已有任务先查看 `status`，避免把新建当成恢复。

## 更新与继续

更新 Python 包后，对原目标使用安装器更新模式：

```bash
python -m qa_master install-codex --project "<项目绝对路径>" --update
```

安装器仅更新未被手工修改的受管理安装并保留备份。遇到拒绝时先检查本地改动，不要删除目录来绕过保护。更新后再次运行安装助手的 `skills` 自检。

在任务目录中，可保存暂停原因和恢复状态：

```bash
python -I "<skill>/scripts/qa.py" pause "等待可测试构建"
python -I "<skill>/scripts/qa.py" resume
```

恢复不会批准需求、用例、外部写入或测试执行。由 Agent 读取先前产物和最新来源，确认变化后继续。

## 下一步

- 找到具体方法：[完整技能目录](SKILL_CATALOG.md)。
- 使用结构化有限模型：[设计方法契约](../qa_master/skills/codex/references/design-methods.md)。
- 连接企业系统：[配置中心](CONFIGURATION.md) 与 [企业接口](ENTERPRISE_ADAPTERS.md)。
- 开始真实执行前：[本机 Runner](LOCAL_RUNNER.md) 与 [证据绑定](EVIDENCE_BINDING.md)。
