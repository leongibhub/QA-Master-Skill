# QA Master Skill

**单仓库、一套安装入口的原创 QA 总控工程（当前为 v0.2 开发版）。**

目标：对用户的一句话测试任务，自动判断需求评审、测试设计、代码分析、执行、回归、报告等阶段，按风险、审批与状态安全推进。测试技能以本项目自有模块实现，不要求用户另装其它 QA Skill。

## 当前已实现（V0.1）
- 任务意图和范围解析的基础规则
- 项目状态与确认答复持久化
- 需求/用例/执行审批门禁
- 缺少构建/环境时暂停
- 13 类测试覆盖检查
- 39 项本地单元测试：21 项工作流规则 + 18 项需求/用例/证据检查（详见 `docs/QUALITY_BASELINE.md`）

## V0.2 新增：可运行质量审计逻辑
- `qa_master/quality.py`：需求歧义/来源/确认检查、结构化用例字段和追踪审计、证据约束的执行结果汇总
- `tests/test_quality.py`：18 项新单元测试
- 尚不包含自动语义需求解析或完整用例生成，必须由 Agent/后续引擎负责。

## 尚未实现
完整的原创需求分析/白盒/API/性能/稳定性/安全 Skill 内容、运行时 AI Agent 分派、GitLab/Jira/SynapseRT/Wiki 接口、远程 Runner、自动生成可执行脚本及端到端闭环。**V0.1 不应视为可独立完成所有测试的成品。**

## 安装（Windows）
```powershell
git clone https://github.com/leongibhub/QA-Master-Skill.git
cd QA-Master-Skill
py -3.10 -m unittest discover -s tests -v
py -3.10 -m qa_master init "demo"
py -3.10 -m qa_master plan "只生成测试用例，不执行测试"
```

在 Codex/OpenCode 以当前目录为工程根目录，读取 `AGENTS.md` 与 `skills/qa-master/SKILL.md`。当前命令行工具是本地规则验证器，并不会自动访问外部平台。

## 统一产品化方向
`skills/qa-master` 为唯一入口；`skills/` 下逐步加入独立实现的需求评审、功能/API/白盒、性能/压力、可靠性、安全、回归及报告模块；`adapters/` 与 `runners/` 为后续内置集成。一次安装应包含已实现的全部模块，无需用户单独配置或安装第三方 QA Skill 包。

## 知识产权
项目以自主实现为原则。可以研究公开项目的功能思想，但不复制受许可证限制的实现，也不将他人代码篡改署名后作为原创发布。借鉴的第三方资料如需使用，应遵守其许可证及归属要求。

> 注意：这是 Public 仓库。不要提交 Token、密码、SSH 私钥或真实机器凭据。
