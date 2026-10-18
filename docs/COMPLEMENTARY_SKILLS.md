# 互补技能库：Awesome QA Skills

本仓库是一个**确定性 QA 引擎 + 编排控制器 + 6 份专业指南**，覆盖测试的经典主干；[awesome-qa-skills](https://github.com/naodeng/awesome-qa-skills) 是一个 **165-skill 的广度技能库**，覆盖大量长尾专类测试方法与技巧。二者定位不同、彼此互补，不是替代关系。

> 本文说明：①两者各是什么、②我当前覆盖什么、③哪些由互补库提供、④如何安装互补库、⑤何时用哪个、⑥逐步补齐路线图。

---

## 一、两者各是什么

| | QA Master Skill（本仓库） | awesome-qa-skills（互补库） |
| --- | --- | --- |
| 本质 | 单个技能 + 确定性引擎 | 技能库：330 目录（165 中文 + 165 英文） |
| 组成 | 6 指南 + 确定性引擎(3 方法) + 13 维度 + Campaign 状态机 | 10 workflow + 150 testing-type + 5 skill-engineering |
| 每个 skill 形态 | 指南是 markdown，背后有真实 Python 引擎（离线确定性合成） | 纯 markdown 提示词（`SKILL.md`+`prompts/`+`references/`+`output-templates/`） |
| 核心价值 | 深度 + 确定性 + 编排 + 来源可追溯 | 广度：可单独安装某个测试类型 skill |
| 典型用途 | 需求评审 → 设计 → 分阶段执行/回归的**受人类门控**闭环 | 某个具体测试类型/工具的**单点**提示词工作流 |

**一句话**：本仓库是一把「带引擎的瑞士军刀」；awesome-qa-skills 是一面「150 个专类工具的货架」。

---

## 二、我当前覆盖什么（原生）

### 6 份专业指南（`qa_master/skills/professional/`）

| 指南 | 覆盖（经典主干） |
| --- | --- |
| `requirements-review` | 需求评审、多源冲突、边界、人工基线复核 |
| `functional-api` | 功能流程、API 契约/鉴权/负向、等价类、边界值、状态迁移、决策表 |
| `structural-integration` | 白盒分支/条件覆盖、集成契约（超时/重试/重复/乱序/部分副作用） |
| `nonfunctional-compatibility` | 性能/负载/压力/稳定性、兼容性 |
| `security-recovery` | 安全证明、恢复演练、威胁边界 |
| `regression-evidence` | 回归影响、缺陷与证据报告 |

### 确定性测试设计引擎（`qa_master/design_methods.py`）

离线、无需模型、可审计的有限合成：`boundary`（边界值）、`decision_table`（决策表）、`state_transition`（状态迁移）。

### 13 个测试维度

`functional` · `api` · `whitebox` · `integration` · `performance` · `load` · `stress` · `stability` · `compatibility` · `negative` · `security` · `recovery` · `regression`

---

## 三、我当前不覆盖、由互补库提供的（真实缺口）

以下专类方法与技巧，本仓库**尚未原生实现**；需要时直接安装 awesome-qa-skills 对应 skill（目录名见右列）。

| 缺口类别 | 由互补库提供（代表性 skill 目录） |
| --- | --- |
| **更多设计方法** | `pairwise-testing` · `combinatorial-testing` · `model-based-testing` · `property-based-testing` · `metamorphic-testing` |
| **工具类自动化** | `ui-test-playwright` · `ui-test-selenium` · `ui-test-cypress` · `ui-test-puppeteer` · `ui-test-webdriverio` · `ui-test-testcafe` · `api-test-postman` · `api-test-bruno` · `api-test-pytest` · `api-test-restassure` · `api-test-supertest` · `performance-test-k6` · `performance-test-gatling` · `performance-test-jmeter` |
| **UI/视觉/移动/可访问性** | `visual-regression-testing` · `cross-browser-testing` · `mobile-testing` · `accessibility-testing` |
| **可靠性工程** | `chaos-testing` · `failover-testing` · `circuit-breaker-testing` · `dependency-failure-testing` · `retry-testing` · `timeout-testing` · `resilience-testing` |
| **AI 原生测试** | `ai-feature-testing` · `llm-testing` · `llm-evaluation-design` · `prompt-testing` · `rag-quality-testing` · `rag-retrieval-testing` · `llm-hallucination-testing` · `ai-agent-testing` · `agent-tool-testing` · `prompt-injection-testing` · `agent-loop-testing` · `agent-memory-testing` · `agent-permission-testing` · `multi-agent-testing` · `ai-safety-testing` |
| **质量工程 / 生产运维** | `quality-gate-design` · `quality-metrics-design` · `quality-debt-analysis` · `automation-roi-analysis` · `production-verification` · `production-incident-analysis` · `distributed-trace-analysis` · `metrics-anomaly-analysis` · `root-cause-analysis` · `log-analysis` |
| **Skill 工程治理** | `skill-change-verification` · `skill-quality-review` · `skill-evaluation` · `skill-prose-review` · `skill-prose-trim` |

---

## 四、如何安装互补库

awesome-qa-skills 通过 `npx skills`（Agent Skills CLI）安装，也可一键安装、clone 或手动复制。英文 skill 是默认源，中文需显式指定 `skills/zh`。

```bash
# 装单个英文 skill（如 pairwise 设计方法）
npx skills add naodeng/awesome-qa-skills --skill pairwise-testing

# 装整个英文集合
npx skills add naodeng/awesome-qa-skills

# 装单个中文 skill
npx skills add https://github.com/naodeng/awesome-qa-skills/tree/main/skills/zh --skill pairwise-testing
```

其它方式：

```bash
# 一键安装（macOS/Linux，装英文到 Codex）
bash ./install-skills-mac.sh --tool codex --lang en

# 一键安装（Windows）
powershell -ExecutionPolicy Bypass -File .\install-skills-windows.ps1 -Tool codex -Lang en

# 完整克隆 / 子模块
git clone https://github.com/naodeng/awesome-qa-skills.git .skills/awesome-qa-skills
git submodule add https://github.com/naodeng/awesome-qa-skills.git .skills/awesome-qa-skills

# 手动复制单个 skill
cp -r skills/en/testing-types/pairwise-testing ~/.cursor/skills/
```

完整安装说明见对方仓库 `scripts/INSTALL_SKILLS.md`。

---

## 五、何时用哪个

| 场景 | 用本仓库 | 用互补库 |
| --- | --- | --- |
| 需求评审、冲突、基线复核 | ✅ 原生 | — |
| 边界值 / 决策表 / 状态迁移（离线确定性） | ✅ 确定性引擎 | — |
| 等价类 / 分支条件 / 场景法设计 | ✅ 6 指南 | — |
| 分阶段 QA/回归编排（受人类门控、可暂停恢复） | ✅ Campaign 状态机 | — |
| pairwise / combinatorial / model-based / property-based / metamorphic | 规划中（见路线图） | ✅ 直接用 |
| Playwright/Selenium/Cypress 等 UI 自动化脚本设计 | — | ✅ 直接用 |
| k6/JMeter/Gatling 性能压测 | — | ✅ 直接用 |
| LLM/RAG/Agent 测试、提示词注入 | 规划中（见路线图） | ✅ 直接用 |
| chaos / failover / circuit-breaker 可靠性测试 | 规划中（见路线图） | ✅ 直接用 |

---

## 六、逐步补齐路线图

目标是「把高价值方法逐步原生化」，而不是长期依赖互补库。计划如下（按优先级）：

| 阶段 | 内容 | 落点 |
| --- | --- | --- |
| **P1 设计方法** | `pairwise`、`combinatorial`（可确定性合成）→ 进引擎；`model-based`、`property-based`、`metamorphic` → 指南方法 | `design_methods.py` + 新参考/指南 |
| **P2 可靠性** | chaos / failover / circuit-breaker / dependency-failure / retry / timeout / resilience | 新指南 `reliability-engineering`（或扩展 `security-recovery`） |
| **P3 AI 原生** | LLM / RAG / prompt-injection / agent 测试 | 新指南 `ai-native-testing` |
| **P4 工具自动化** | Playwright/Selenium 等框架 + UI/视觉/跨浏览器/可访问性 | 新参考 `automation-tools` |
| **P5 质量工程/生产运维** | quality-gate / metrics / incident / trace / anomaly | 新指南 `quality-engineering` |

> 路线图反映的是「逐步原生化」的方向，不构成已交付能力的承诺。当前未原生实现的方法，均以上文「互补库」为准，并在 README「测试设计方法」表中如实标注来源，绝不虚标。
