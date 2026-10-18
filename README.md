<div align="center">

# QA Master Skill

**一个受人类门控、可恢复的 QA 工作流控制器，外加一个 Codex QA 技能（Agent Skill）。**

评审需求、设计来源可链接的软件测试，并在 Codex 中协调分阶段 QA。

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.1.0-blue)](./pyproject.toml)
[![Status](https://img.shields.io/badge/status-pre--release-orange)]()
[![CI](https://github.com/leongibhub/QA-Master-Skill/actions/workflows/test.yml/badge.svg)](https://github.com/leongibhub/QA-Master-Skill/actions/workflows/test.yml)

</div>

> ⚠️ **当前是 V1 开发版，不是已验收的正式版。** 无需另装其它 QA Skill 仓库。

**快速链接：** [安装](#快速开始) · [用法](#用法) · [专业能力指南](#专业能力指南) · [入口点](#入口点) · [文档地图](#文档地图) · [验证证据](docs/verification/)

---

## 能做什么

一个仓库、一个 QA Master 入口。每个专业指南可单独路由，也可按「需求分析 → 测试设计 → 企业接入 → 本地执行」组成一条质量工作流。

| 场景 | 入口 | 帮助 |
| --- | --- | --- |
| 需求评审与测试计划 | 需求评审指南 · `qa-master plan` | 多源需求冲突、功能边界与状态、风险 → 可追踪的测试计划与用例 |
| 功能 / API / 白盒 / 集成测试设计 | 功能/API、结构/集成指南 · `campaign_cli` | 生成可审查的草稿用例、追踪、覆盖与缺口 |
| 确定性测试方法 | 边界值 · 决策表 · 状态迁移 | 从模型导出可审计的用例组合 |
| 企业工具接入 | Jira · Confluence · SynapseRT · GitLab CI | 读取、受控写入、JUnit 制品核验 |
| 本地受控执行 | 本机 Runner · 任务调度核心 | 可信宿主授权、环境隔离、超时清理 |

内置指南覆盖需求冲突、功能边界/状态、API、白盒、集成、性能/负载/压力/稳定性、兼容性、安全/恢复、回归与证据报告。详见 [专业能力](docs/SKILL_CAPABILITIES.md)。

## 快速开始

需要 Python 3.10 或以上；Windows 与 Linux 使用相同的 Python 命令。

```sh
git clone https://github.com/leongibhub/QA-Master-Skill.git
cd QA-Master-Skill

python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux:   source .venv/bin/activate

python -m pip install .
python -m qa_master install-codex --user
```

安装器把入口、专业指南、领域参考和本地助手一起装到 `~/.agents/skills/qa-master`。在 Codex 中打开待测项目，直接描述目标即可：

> `$qa-master 评审这份需求并生成测试用例，开发还未完成，不执行测试`

只供单个项目使用时，改用 `python -m qa_master install-codex --project <项目目录>`，装到该项目的 `.agents/skills/qa-master`。安装后的 Skill 不依赖原始源码目录或另一个 QA Skills 仓库；本地助手需要 Python 3.10+，没有 Python 时仍可只按指南由 Codex 完成分析设计。详细交付边界见 [Codex 核心版](docs/CODEX_CORE.md)。

## 用法

在支持 Agent Skills 标准自动发现的工具里，用自然语言描述目标即可；需要显式调用时直接点名入口。

| 你可以说 | 推荐入口 |
| --- | --- |
| 「评审这份需求，列出冲突和测试点」 | 需求评审指南 / `qa-master plan` |
| 「为这个登录流程生成测试用例」 | 功能/API 指南 / `campaign_cli` |
| 「给这个状态机补非法迁移用例」 | 状态迁移（`references/design-methods.md`） |
| 「读 Jira 需求并做核验」 | [企业接口](docs/ENTERPRISE_ADAPTERS.md) |
| 「在本机受控跑这份测试」 | [本机 Runner](docs/LOCAL_RUNNER.md) |

不知道从哪开始时，先跑 `qa-master plan`，它会输出规划阶段、信息缺口和匹配的专业指南。

## 专业能力指南

6 份原创、可被注册表发现的审查与设计指南（`qa_master/skills/professional/`）：

| 指南 | 覆盖维度 |
| --- | --- |
| `requirements-review` | 多源需求冲突、边界、人工复核 |
| `functional-api` | 功能流程、API 合约/鉴权/负向 |
| `structural-integration` | 白盒分支与路径、集成 |
| `nonfunctional-compatibility` | 性能/负载/压力/稳定性、兼容性 |
| `security-recovery` | 安全、恢复 |
| `regression-evidence` | 回归、缺陷与证据报告 |

注册表只返回本地包中已验证存在的文件，绝不把「选择某一指南」说成已调用模型、已运行测试或已产生结论。这些指南和确定性生成器不等于完整语义 Agent。

## 入口点

| 命令 | 能做什么 | 边界 |
| --- | --- | --- |
| `qa-master plan "任务"` | 规划阶段、信息缺口、专业指南，保存禁止执行的任务范围 | 保守规则解析，不授权执行 |
| `qa-master pause` / `resume` | 保存暂停状态，恢复后重查流程条件 | 暂停期间拒绝推进；恢复不增加授权 |
| `python -m qa_master.campaign_cli --input examples/campaign.json --output .qa-master/design.json` | 结构化需求草稿、追踪、覆盖与缺口 | 草稿，不能代替人类批准 |
| `qa-master-paired-eval` | 同题、同模型、同设置的双边评测资料校验 | 缺少双方实际输出时不能得出优劣 |
| `python -m qa_master.config_ui --config .qa-master/config.json` | 本机配置页面（默认 `http://127.0.0.1:8765`） | 仅非秘密配置与凭据环境变量引用 |

## 仓库结构

```text
QA-Master-Skill/
├── qa_master/                # Python 包：CLI、生成器、企业适配、评测运行时
│   └── skills/
│       ├── codex/            # Codex 技能入口 + references + examples
│       └── professional/     # 6 份专业能力指南
├── skills/qa-master/         # 源树入口（非独立安装包）
├── examples/                 # 教学模型（边界、决策表、状态迁移）
├── docs/                     # 交付边界、验收、评测与验证证据
├── tests/                    # unittest 套件
├── .github/workflows/        # CI（ubuntu/windows × py3.10/3.12）
├── pyproject.toml
└── README.md
```

## 设计原则

- **受人类门控：** 不提供默认放行器；单独填写 `approved_by`、设置环境变量或调用旧版 `approve` 命令都不能获得实际执行权限。
- **证据可核验：** 执行回执和结果来源由宿主验证，默认拒绝；任何 JSON 布尔值或审批人文本均不能证明真实身份。
- **来源可链接：** 用例与结论链接到需求来源，区分草稿、观察与已执行证据。
- **可恢复：** 状态在 schema v2 下保存，暂停/恢复/迁移都有明确边界。
- **独立安装：** 安装后的 Skill 不依赖源码目录；企业写入与执行仍需可信集成方实现宿主验证。
- **安全默认：** 不要把真实 Token、密码、Cookie、私钥、公司测试资料提交到这个 Public 仓库。

## 验证与质量

提交改动前，从仓库根目录运行：

```sh
python -W error::ResourceWarning -m unittest discover -s tests
```

CI 在 `ubuntu-latest` / `windows-latest` × Python 3.10 / 3.12 上执行同一命令。

- 复测证据位于 [docs/verification/](docs/verification/)，原始基线失败与修复记录均保留；历史 README 已归档至 [docs/history/](docs/history/)。
- 双边评测资料校验与协议见 [docs/BENCHMARK.md](docs/BENCHMARK.md) 和 [docs/PAIRED_EVALUATION.md](docs/PAIRED_EVALUATION.md)。
- 验证轨迹汇总见 [docs/verification/verification-trajectory-summary.md](docs/verification/verification-trajectory-summary.md)。

真实企业环境 E2E 为 `NOT_EXECUTED`；尚无证据证明总体优于 Awesome QA Skills，也不发布 V1.0 正式标签。

## 文档地图

| 文档 | 用途 |
| --- | --- |
| [CODEX_CORE.md](docs/CODEX_CORE.md) | Codex 核心版交付边界 |
| [SKILL_CAPABILITIES.md](docs/SKILL_CAPABILITIES.md) | 专业能力层设计与验收范围 |
| [ENTERPRISE_ADAPTERS.md](docs/ENTERPRISE_ADAPTERS.md) | Jira / Confluence / SynapseRT 接口 |
| [GITLAB_CI_ATTESTATION.md](docs/GITLAB_CI_ATTESTATION.md) | GitLab CI 制品核验 |
| [LOCAL_RUNNER.md](docs/LOCAL_RUNNER.md) | 本机 Runner 授权与隔离 |
| [JOB_SCHEDULER.md](docs/JOB_SCHEDULER.md) | 本地任务生命周期核心 |
| [SECURITY_CONTINUATION.md](docs/SECURITY_CONTINUATION.md) | 安全约束与身份边界 |
| [V1_ACCEPTANCE.md](docs/V1_ACCEPTANCE.md) | V1 验收范围 |
| [BENCHMARK.md](docs/BENCHMARK.md) | 评测协议 |
| [PAIRED_EVALUATION.md](docs/PAIRED_EVALUATION.md) | 双边评测运行时 |
| [CAMPAIGN_CLI.md](docs/CAMPAIGN_CLI.md) | Campaign CLI 用法 |
| [CONFIGURATION.md](docs/CONFIGURATION.md) | 配置页面与凭据引用 |
| [requirement-traceability-matrix.md](docs/03-requirements/requirement-traceability-matrix.md) | 需求追踪矩阵 |
| [verification/](docs/verification/) | 验证与复测证据 |

## 尚未交付

完整多语言语义 Agent、远程 SSH/WinRM 执行与资源调度、生产身份/密钥库、具体 SynapseRT 部署的全部业务操作与缺陷回归自动闭环、双方完整行为对照评测。

## 贡献

Issues 和 PR 欢迎：专业指南、生成器、企业适配、评测与文档改进。提交前请先跑测试套件，并把改动与对应需求/验证证据关联。

## 许可证

本项目当前**尚未附加开源许可证**；在明确许可证之前，请默认按保留所有权利处理。
