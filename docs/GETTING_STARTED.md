# 安装与第一次任务

## Windows 安装

需要 Git、支持加载 Skill 的 Agent，以及 Python 3.10+ 或 `uv`。不需要手工创建或激活 `.venv`。先克隆仓库：

```cmd
git clone https://github.com/leongibhub/QA-Master-Skill.git
cd QA-Master-Skill
```

仅克隆源码不会把 `qa-master` 安装为命令。以下两条路径任选其一。

### 已有 Python 3.10+

运行 `py -3 --version` 确认版本。版本为 3.10 或更高时，可直接在克隆后的仓库根目录运行模块：

```cmd
py -3 -m qa_master --help
```

这条路径不依赖虚拟环境，也不依赖 `qa-master` 是否在 PATH 中。后续所有 `qa-master ...` 命令都可以替换成 `py -3 -m qa_master ...`。

如果 `py` 启动器不可用而 `python --version` 显示 3.10+，使用等价的 `python -m qa_master ...`，例如 `python -m qa_master install-codex --user`。想把命令安装到用户环境、方便以后直接输入 `qa-master` 时，可选运行：

```cmd
py -3 -m pip install --user .
```

若终端仍提示找不到 `qa-master`，重新打开终端，或继续使用不受 PATH 影响的 `py -3 -m qa_master ...`。

### 没有 Python 或版本低于 3.10

先安装 uv。可以使用 Windows 包管理器：

```cmd
winget install --id=astral-sh.uv -e
```

也可以按 [uv 官方 Windows 安装说明](https://docs.astral.sh/uv/getting-started/installation/) 安装。新开终端后，在仓库根目录运行：

```cmd
uv tool install --force --python 3.13 .
```

`uv` 会下载并管理 Python 3.13 和独立工具环境。若 `uv` 提示 hardlink 已回退为复制，安装仍然可用；可在更新时加 `--link-mode=copy` 消除提示。

若安装后仍提示找不到 `qa-master`，运行 `uv tool update-shell`，关闭并重新打开终端后再试。需要在当前终端立即运行时，使用：

```cmd
uv tool run --from . --python 3.13 qa-master --help
```

后续把 `qa-master` 及其参数放在该前缀之后即可。这条命令已经在本仓库验证，但首次构建完整工具包会比持久安装慢。

## Linux / macOS

已有 Python 3.10+ 时，在仓库根目录运行 `python3 -m qa_master install-codex --user`。没有合适 Python 时，按 [uv 官方安装说明](https://docs.astral.sh/uv/getting-started/installation/) 安装 uv，再运行：

```bash
uv tool install --force --python 3.13 .
qa-master install-codex --user
```

Claude Code 的用户级目标是 `$HOME/.claude/skills/qa-master`，项目级目标是 `<project>/.claude/skills/qa-master`；将 Windows 表格中的反斜杠改为 `/`。TRAE CN 的实际 Linux/macOS 发现路径未在本变更中验证，保持 `NOT_EXECUTED`。

## 选择 Agent 宿主和安装范围

请按下表选择真正使用的宿主。下表是已有 Python 用户可直接复制的 Windows `cmd` 命令；PowerShell 请把 `%USERPROFILE%` 改为 `$env:USERPROFILE`。已通过 uv 安装的用户，把每条 `py -3 -m qa_master` 替换为 `qa-master`；PATH 尚未刷新时替换为 `uv tool run --from . --python 3.13 qa-master`。

| 宿主 | 用户级命令 | 用户级目录 | 项目级命令 | 项目级目录 |
| --- | --- | --- | --- | --- |
| Codex / OpenCode | `py -3 -m qa_master install-codex --user` | `%USERPROFILE%\.agents\skills\qa-master` | `py -3 -m qa_master install-codex --project "<项目绝对路径>"` | `<项目>\.agents\skills\qa-master` |
| VS Code Claude Code | `py -3 -m qa_master install-codex --target "%USERPROFILE%\.claude\skills\qa-master"` | `%USERPROFILE%\.claude\skills\qa-master` | `py -3 -m qa_master install-codex --target "<项目绝对路径>\.claude\skills\qa-master"` | `<项目>\.claude\skills\qa-master` |
| TRAE CN | `py -3 -m qa_master install-codex --target "%USERPROFILE%\.trae-cn\skills\qa-master"` | `%USERPROFILE%\.trae-cn\skills\qa-master` | `py -3 -m qa_master install-codex --target "<项目绝对路径>\.trae\skills\qa-master"` | `<项目>\.trae\skills\qa-master` |

把 `<项目绝对路径>` 替换成真实路径，例如 `D:\work\demo`。不要在同一条命令中混用 `--user`、`--project` 和 `--target`。

VS Code 里的 Claude Code 和 TRAE CN 都是 Skill 宿主；DeepSeek 等模型继续由宿主的既有配置选择。QA Master 不读取、不设置模型端点、密码或 API Token。

`%USERPROFILE%\.trae-cn\skills` 和项目 `.trae\skills` 路径已按当前 TRAE CN 使用场景写入本指南；尚未在用户提供的实际 TRAE CN 会话中观察到加载和调用，因此宿主发现状态为 `NOT_EXECUTED`。目录复制或命令成功不代表聊天宿主已经加载 Skill。

## 检查安装后的内容

只检查刚才安装到的宿主目录。比如已安装到 TRAE CN 的 `%USERPROFILE%\.trae-cn\skills\qa-master`，就不要检查 Codex/OpenCode 的 `%USERPROFILE%\.agents\skills\qa-master`。

| 安装到的宿主 | 用户级 `SKILL.md` 检查命令 | 同一目录的本地助手自检 |
| --- | --- | --- |
| Codex / OpenCode | `dir "%USERPROFILE%\.agents\skills\qa-master\SKILL.md"` | `py -3 -I "%USERPROFILE%\.agents\skills\qa-master\scripts\qa.py" skills` |
| VS Code Claude Code | `dir "%USERPROFILE%\.claude\skills\qa-master\SKILL.md"` | `py -3 -I "%USERPROFILE%\.claude\skills\qa-master\scripts\qa.py" skills` |
| TRAE CN | `dir "%USERPROFILE%\.trae-cn\skills\qa-master\SKILL.md"` | `py -3 -I "%USERPROFILE%\.trae-cn\skills\qa-master\scripts\qa.py" skills` |

项目级安装时，将表格中的用户级目录替换成上表相应的项目级目录。`dir` 应列出 `SKILL.md`。本地助手自检从安装后的助手读取资料，而非从原仓库读取；JSON 中 `vendor.count` 应为 330，`en` / `zh` 各为 165。没有系统 Python、只安装了 uv 的机器，使用 `uv run --no-project --python 3.13 python -I "<skill>\scripts\qa.py" skills`，其中 `<skill>` 是实际安装目录。这些数量代表 165 个逻辑技能，分类合计为双语工作流 20、测试类型 300、技能工程 10。若数量为 0，不应继续假定安装完整；记录命令输出和安装版本后检查交付。

安装输出中 `"status": "INSTALLED"` 表示安装包已写入目标目录。`"execution": "NOT_EXECUTED"` 表示安装没有执行 QA 任务，不是安装失败；同样，它不证明宿主已发现或调用该 Skill。

安装目录也应含 `SKILL.md`、`references/`、`examples/` 和 `scripts/`。目录存在只是交付检查，不代表 Agent 已实际应用这些指南。

## 开始工作

关闭并新建目标宿主的聊天会话后，在项目内提供真实文件路径。Claude Code 可使用：

```text
/qa-master 阅读当前项目需求并生成测试用例；只做设计，不执行测试，不写入外部系统。
```

TRAE CN 使用自然语言，例如：

```text
使用 qa-master skill 阅读当前项目需求并生成测试用例；只做设计，不执行测试，不写入外部系统。
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

已通过 uv 安装的用户，更新 Python 包后对原目标使用安装器更新模式：

```cmd
uv tool install --force --reinstall --link-mode=copy --python 3.13 .
qa-master install-codex --user --update
```

已有 Python 的直接运行用户，先拉取仓库更新，然后在仓库根目录执行相同目标命令并加 `--update`，例如 `py -3 -m qa_master install-codex --target "%USERPROFILE%\.claude\skills\qa-master" --update`。TRAE CN 同理：`py -3 -m qa_master install-codex --target "%USERPROFILE%\.trae-cn\skills\qa-master" --update`。`py` 启动器不可用时，使用等价的 `python -m qa_master install-codex --target "%USERPROFILE%\.trae-cn\skills\qa-master" --update`。安装器仅更新未被手工修改的受管理安装并保留备份。遇到拒绝时先检查本地改动，不要删除目录来绕过保护。更新后再次运行安装助手的 `skills` 自检。

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
