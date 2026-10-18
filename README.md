<div align="center">

# QA Master Skill

**一个受人类门控、可恢复的 QA 工作流控制器，外加一个 Codex QA 技能（Agent Skill）。**

评审需求、设计来源可链接的软件测试，并在 Codex 中协调分阶段 QA。

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](./pyproject.toml)
[![Status](https://img.shields.io/badge/status-released-green)]()
[![CI](https://github.com/leongibhub/QA-Master-Skill/actions/workflows/test.yml/badge.svg)](https://github.com/leongibhub/QA-Master-Skill/actions/workflows/test.yml)
[![License: PolyForm Noncommercial 1.0.0](https://img.shields.io/badge/License-PolyForm%20Noncommercial%201.0.0-blue.svg)](./LICENSE)

</div>

> ⚠️ **已发布 1.0.0；企业 E2E、性能、远程执行等能力尚未验收，见下方「当前边界」。** 无需另装其它 QA Skill 仓库。

**快速链接：** [安装](#快速开始) · [用法](#用法) · [专业能力指南](#专业能力指南) · [入口点](#入口点) · [文档地图](#文档地图) · [验证证据](docs/verification/)

---

## 能做什么

一个仓库、一个 QA Master 入口。每个专业指南可单独路由，也可按「需求分析 → 测试设计 →（可选）企业接入 → 本地执行」组成一条质量工作流。企业接入不是必经步骤：默认不连任何企业系统，需要时先在配置页（`config_ui`）预配适配器并授权。

| 场景 | 入口 | 帮助 |
| --- | --- | --- |
| 需求评审与测试计划 | 需求评审指南 · `qa-master plan` | 多源需求冲突、功能边界与状态、风险 → 可追踪的测试计划与用例 |
| 功能 / API / 白盒 / 集成测试设计 | 功能/API、结构/集成指南 · `campaign_cli` | 生成可审查的草稿用例、追踪、覆盖与缺口 |
| 确定性测试方法 | 边界值 · 决策表 · 状态迁移 · 成对组合 · 组合测试 | 从模型导出可审计的用例组合 |
| 企业工具接入（可选） | Jira · Confluence · SynapseRT · GitLab CI | 先在配置页预配适配器，再读取 / 受控写入 / JUnit 制品核验 |
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

安装器把入口、专业指南、领域参考和本地助手一起装到 `~/.agents/skills/qa-master`。在 Codex 或 OpenCode 中打开待测项目，直接描述目标即可：

> `$qa-master 评审这份需求并生成测试用例，开发还未完成，不执行测试`

只供单个项目使用时，改用 `python -m qa_master install-codex --project <项目目录>`，装到该项目的 `.agents/skills/qa-master`。安装后的 Skill 不依赖原始源码目录或另一个 QA Skills 仓库；本地助手需要 Python 3.10+，没有 Python 时仍可只按指南由 Codex 完成分析设计。详细交付边界见 [Codex 核心版](docs/CODEX_CORE.md)。

## 支持的 Agent 工具

本 Skill 遵循 Agent Skills 开放标准（一个目录 + `SKILL.md` + frontmatter）。安装器把完整技能装到 `.agents/skills/qa-master`，凡是读取 `.agents/skills/` 的工具都能直接发现。

| 工具 | 安装位置 | 方式 |
| --- | --- | --- |
| Codex CLI | `~/.agents/skills/qa-master` | `python -m qa_master install-codex --user`（原生） |
| OpenCode | `~/.agents/skills/qa-master`（全局）· `.agents/skills/qa-master`（项目） | 同上——OpenCode 也读 `.agents/skills/`（agent-compatible） |
| Claude Code | `~/.claude/skills/qa-master` | 手动复制或软链（Claude Code 读 `.claude/skills/`） |
| WorkBuddy（腾讯云） | `.workbuddy/skills/qa-master` | 手动复制或软链（支持 Agent Skills 标准） |

- **全局**：`install-codex --user` → `~/.agents/skills/qa-master`，Codex CLI 与 OpenCode 都能发现。
- **项目**：`install-codex --project <项目目录>` → `<项目>/.agents/skills/qa-master`，在该项目内被 Codex CLI 与 OpenCode 发现。
- **Claude Code** 读 `~/.claude/skills/`，把装好的 `qa-master` 目录复制/软链过去即可；`SKILL.md` 的 frontmatter 只含 `name`/`description`，跨工具通用。

安装后若工具没刷新技能列表，重新打开会话。

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

## 最佳实践

一条质量工作流覆盖「需求 → 测试计划 → 测试用例 → 执行 → 报告」。以下每条都是本仓库真实命令与真实输出，在仓库根目录可直接复现。

**① 需求：先暴露信息缺口，再谈用例。** `plan` 是意图路由而非生成器，优先回答「缺什么」。

```sh
python -m qa_master init demo-login
python -m qa_master plan "评审用户上传文档功能的需求，列出冲突和测试点"
```

输出：`no_execution: true`、`questions` 列出信息缺口（例如「请提供需求文件 / Wiki / GitLab 仓库地址」）、`professional_guidance.selected` 自动选中 `requirements-review`。**先补齐来源再设计**——别让 Agent 在缺需求来源时凭空生成用例。

**② 测试计划：把需求写成结构化 bundle。** 结构化需求（`id` / `text` / `source` / `approved` / `dimension` / `acceptance` / `preconditions` / `test_data` / `priority`）让评审与追踪可核对，示例见 `examples/campaign.json`。

```sh
python -m qa_master.campaign_cli --input examples/campaign.json --output .qa-master/design.json
```

产出 JSON 里：`requirement_review.approval = PENDING_HUMAN`（不替人类拍板）、`requirement_findings` 列出冲突/阻断。**`approved` 只对已确认需求打 `true`，评审结论永远停在 `PENDING_HUMAN` 由人决定。**

**③ 测试用例：草稿与覆盖缺口一起看。** 生成的用例默认 `approval=DRAFT`，同时给出 13 维度的覆盖矩阵。

产出 JSON：`test_cases[]` 每条带 `trace`（回指需求）、`dimension`、`steps`、`expected`；`coverage.*` 中 `DRAFT` = 已生成、`UNASSESSED` = 未覆盖维度。**先扫 `coverage` 里的 `UNASSESSED`，那才是缺口，别只看用例数量。**

**④ 测试用例（进阶）：能结构化就用确定性方法。** 边界值 / 决策表 / 状态迁移 / 成对组合 / 组合测试不依赖模型猜测，直接从结构化模型导出可审计用例（示例 `examples/design-methods.json`）。

```sh
python -m qa_master design --input examples/design-methods.json --output .qa-master/methods.json
```

输出：`method_candidates = 14`、`status = DRAFT_UNAPPROVED`、`execution = NOT_EXECUTED`。**结构能明确时别交给语义模型猜，确定性引擎结果可复现、可审计。**

**⑤ 执行：默认拒绝，显式授权后才动。** 受人类门控是特性，不是 bug。

```sh
python -m qa_master check execution
# {"state": "DENIED_BY_TASK_SCOPE", "execution_authorized": false, ...}
```

**草稿停在 `DRAFT_UNAPPROVED`，只有显式授权（可信宿主 + 审批验证）才进入执行，没有默认放行器。**

**⑥ 报告：如实反映门控状态，不做「通过」宣称。**

```sh
python -m qa_master check report   # {"state": "PENDING", ...}
```

产出 JSON：`workflow.requirements_review = WAITING_HUMAN_APPROVAL`、`workflow.execution = NOT_AUTHORIZED`、`case_review.trace_matrix`（需求→用例追踪）。**报告是「追踪 + 门控状态」的证据，不是「测试通过」的结论——没有执行授权就没有执行结论。**

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

**13 个测试维度**（用于指南路由与覆盖判定）：`functional`、`api`、`whitebox`、`integration`、`performance`、`load`、`stress`、`stability`、`compatibility`、`negative`、`security`、`recovery`、`regression`。

**测试设计方法**（确定性引擎 + 专业指南共同覆盖）：

| 方法 | 确定性引擎 | 说明 |
| --- | --- | --- |
| 等价类划分 | — | 有效/无效等价类 + 边界（`functional-api` 指南） |
| 边界值分析 | `boundary` | 双侧端点 + 内侧步进点 + 越界邻域 |
| 决策表 / 判定表 | `decision_table` | 条件组合、约束排除、规则冲突/缺口 |
| 状态迁移 | `state_transition` | 状态、触发、守卫/效果、闭环非法迁移 |
| 成对组合 | `pairwise` | 固定强度 2，贪心覆盖数组覆盖所有参数对 |
| 组合测试 | `combinatorial` | 可选强度 2–3，贪心覆盖数组覆盖所有 t 元交互 |
| 分支 / 条件覆盖 | — | 复合谓词、决策/条件证据（`structural-integration` 指南） |
| 场景法 | — | 正常交付、契约不符、超时、重试耗尽、重复消息、乱序、部分副作用等 |

带 `boundary` / `decision_table` / `state_transition` / `pairwise` / `combinatorial` 的是 `qa_master.design_methods` 的**确定性有限合成方法**（无需模型，直接从结构化模型导出可审计用例）；等价类、场景法、分支/条件等由专业指南配合模型完成。详见 [设计方法契约](qa_master/skills/codex/references/design-methods.md)。

> 尚未原生实现的设计方法（model-based / property-based / metamorphic）以及工具自动化、可靠性、AI 原生测试等长尾专类，已随内置的 awesome-qa-skills vendor 广度库提供（见下方「广度技能库」）；`qa-master plan` 会把这些阶段路由到对应 skill。本仓库仍逐步把高价值方法原生化。

注册表只返回本地包中已验证存在的文件，绝不把「选择某一指南」说成已调用模型、已运行测试或已产生结论。这些指南和确定性生成器不等于完整语义 Agent。

## 广度技能库：内置 Awesome QA Skills（330 skill）

本仓库已把 [awesome-qa-skills](https://github.com/naodeng/awesome-qa-skills) 的 **330 个 skill（165 中文 + 165 英文）** 以 vendor 形式内置到 `qa_master/skills/vendor/awesome-qa-skills/`（10 workflow + 150 testing-type + 5 skill-engineering），作为本仓库的「广度叶子」，随包分发、开箱即用，无需再单独安装。

**路由整合（本仓库独有）**：`qa-master plan` 通过 `core.SKILLS` / `core.DIMENSION_SKILLS` 把规划阶段映射到 canonical skill 名，再在 vendor 里选中中英双语对应 skill，结果输出在 `vendor_skills` 字段。这是 awesome-qa-skills 本身没有的——它有广度，但没有意图路由、`no_execution` 门控、可暂停恢复状态机、来源追踪、企业适配，以及确定性覆盖数组引擎（`boundary` / `decision_table` / `state_transition` / `pairwise` / `combinatorial`）。

长尾专类（model-based / property-based / metamorphic、Playwright/Selenium/Cypress、k6/JMeter/Gatling、LLM/RAG/Agent 测试、chaos/circuit-breaker 等）现在随本仓库提供；同时本仓库继续把高价值方法原生化。完整的覆盖对照、缺口清单与路线图见 [广度技能库](docs/COMPLEMENTARY_SKILLS.md)。

## 入口点

| 命令 | 能做什么 | 边界 |
| --- | --- | --- |
| `qa-master plan "任务"` | 规划阶段、信息缺口、专业指南，保存禁止执行的任务范围 | 保守规则解析，不授权执行 |
| `qa-master pause` / `resume` | 保存暂停状态，恢复后重查流程条件 | 暂停期间拒绝推进；恢复不增加授权 |
| `python -m qa_master.campaign_cli --input examples/campaign.json --output .qa-master/design.json` | 结构化需求草稿、追踪、覆盖与缺口 | 草稿，不能代替人类批准 |
| `qa-master-paired-eval` | 同题、同模型、同设置的双边评测资料校验 | 缺少双方实际输出时不能得出优劣 |
| `python -m qa_master.config_ui --config .qa-master/config.json` | 本机配置页面（默认 `http://127.0.0.1:8765`）——预配企业适配器与测试机连接 | 仅非秘密配置与凭据环境变量引用 |

## 架构流程图

```mermaid
flowchart TD
    A([用户 · 自然语言]) --> B[Agent 工具<br/>Codex CLI · OpenCode · Claude Code · WorkBuddy]
    B --> C[qa-master SKILL.md<br/>总控入口]
    C --> D{意图路由<br/>qa-master plan}
    D -->|需求评审| E[需求评审指南<br/>冲突 · 边界 · 人工复核]
    D -->|测试设计| F{确定性方法?}
    D -->|企业接入?| G{已预配企业适配器?}
    D -->|受控执行| H[本机 Runner<br/>任务调度核心]
    D -->|长尾专类| V[Vendor 广度库<br/>330 skill · 中英双语]
    F -->|是 · 结构化模型| I[确定性引擎<br/>boundary · decision_table · state_transition · pairwise · combinatorial]
    F -->|否 · 需语义| J[专业指南 + 模型<br/>等价类 · 场景法 · 分支条件 · 安全 · 性能...]
    G -->|否 · 未预配| K[草稿产物<br/>用例 · 覆盖 · 缺口 · 追踪]
    G -->|是 · 已授权| G2[企业适配<br/>Jira · Confluence · SynapseRT · GitLab CI]
    E --> K
    I --> K
    J --> K
    G2 --> K
    V --> K
    K --> L{是否执行?}
    L -->|否| M([DRAFT_UNAPPROVED 交付])
    L -->|是 · 需授权| H
    H --> N[证据与验证<br/>attestation · paired-evaluation]
    K --> N
    N --> M
```

`SKILL.md` 是给 Agent 的入口；`qa_master` CLI 是本地确定性工具。关键分支：①意图路由（需求评审 / 测试设计 / 受控执行 / 长尾专类路由到 vendor 广度库；企业接入是可选分支，需先在配置页预配适配器，未预配则跳过）；②测试设计里「结构化模型走确定性引擎，语义类走专业指南 + 模型」；③长尾专类（model-based、工具自动化、AI 原生、可靠性等）由内置 330-skill vendor 广度库提供；④产出默认停在 `DRAFT_UNAPPROVED`，只有显式授权才进入受控执行并落到证据与验证。

## 仓库结构

```text
QA-Master-Skill/
├── qa_master/                # Python 包：CLI、生成器、企业适配、评测运行时
│   └── skills/
│       ├── codex/            # Codex 技能入口 + references + examples
│       ├── professional/     # 6 份专业能力指南
│       └── vendor/awesome-qa-skills/  # 内置广度库：330 skill（中英双语）
├── skills/qa-master/         # 源树入口（非独立安装包）
├── examples/                 # 教学模型（边界、决策表、状态迁移）
├── docs/                     # 交付边界、验收、评测与验证证据
├── tests/                    # unittest 套件
├── .github/workflows/        # CI（ubuntu/windows × py3.10/3.12）
├── pyproject.toml
├── LICENSE                   # PolyForm Noncommercial 1.0.0
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
python -m pip install ".[test]"      # 安装测试依赖（含 attestation 验签所需的 cryptography）
python -W error::ResourceWarning -m unittest discover -s tests
```

CI 在 `ubuntu-latest` / `windows-latest` × Python 3.10 / 3.12 上执行同一命令（先 `pip install ".[test]"` 再跑测试）。`cryptography` 是可选运行时依赖：只做需求评审/测试设计而不做 attestation 验签时，基础 `pip install .` 即可。

- 复测证据位于 [docs/verification/](docs/verification/)，原始基线失败与修复记录均保留；历史 README 已归档至 [docs/history/](docs/history/)。
- 双边评测资料校验与协议见 [docs/BENCHMARK.md](docs/BENCHMARK.md) 和 [docs/PAIRED_EVALUATION.md](docs/PAIRED_EVALUATION.md)。
- 验证轨迹汇总见 [docs/verification/verification-trajectory-summary.md](docs/verification/verification-trajectory-summary.md)。

真实企业环境 E2E 为 `NOT_EXECUTED`；尚无证据证明总体优于 Awesome QA Skills。

## 文档地图

| 文档 | 用途 |
| --- | --- |
| [CODEX_CORE.md](docs/CODEX_CORE.md) | Codex 核心版交付边界 |
| [SKILL_CAPABILITIES.md](docs/SKILL_CAPABILITIES.md) | 专业能力层设计与验收范围 |
| [COMPLEMENTARY_SKILLS.md](docs/COMPLEMENTARY_SKILLS.md) | 广度技能库对照、缺口清单与原生化路线图 |
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

## 当前边界

V1.0 的如实边界——以下能力因需要外部资源或超出本地工具范围而尚未交付（`NOT_AVAILABLE` / `NOT_EXECUTED`）：

- **完整多语言语义 Agent**：本技能是确定性控制器 + 指南，不是全自动 Agent。
- **远程 SSH/WinRM 执行与资源调度**：需要可信宿主与基础设施。
- **生产身份 / 密钥库**：需要企业级密钥管理。
- **SynapseRT 全量业务操作与缺陷回归闭环**：需要具体部署环境。
- **「优于 Awesome QA Skills」的正式结论**：REQ-011 需严格画像 + 人类评分 + 独立 holdout，均 `NOT_AVAILABLE`。

明确列出边界是为了不夸大能力、不做未经验证的宣称。

## 贡献

Issues 和 PR 欢迎：专业指南、生成器、企业适配、评测与文档改进。提交前请先跑测试套件，并把改动与对应需求/验证证据关联。

## 许可证

本仓库采用 [PolyForm Noncommercial License 1.0.0](./LICENSE)。您可以自由使用、修改和分发本软件，但仅限非商业目的（如个人学习、研究、实验、慈善机构、教育机构、公共研究组织、政府机构等用途）。
