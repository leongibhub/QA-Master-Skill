# 广度技能库：Awesome QA Skills（已内置）

本仓库是一个**确定性 QA 引擎 + 编排控制器 + 6 份专业指南**，覆盖测试的经典主干；同时已把 [awesome-qa-skills](https://github.com/naodeng/awesome-qa-skills) 的 **330 个 skill（165 中文 + 165 英文）** 以 vendor 形式内置，作为本仓库的「广度叶子」。二者不再是「两个库」的关系，而是「一个库 + 内置广度 + 路由整合」。

> 本文说明：①两者各是什么、②我原生覆盖什么、③内置 vendor 提供什么、④路由如何整合、⑤何时用哪个、⑥逐步原生化路线图。

---

## 一、两者各是什么（现在的关系）

| | 本仓库原生能力 | 内置 vendor（awesome-qa-skills） |
| --- | --- | --- |
| 本质 | 确定性引擎 + 编排/门控 + 6 指南 | 广度技能库：330 目录（165 中文 + 165 英文） |
| 组成 | 6 指南 + 确定性引擎(5 方法) + 13 维度 + Campaign 状态机 | 10 workflow + 150 testing-type + 5 skill-engineering |
| 每个 skill 形态 | 指南是 markdown，背后有真实 Python 引擎（离线确定性合成） | 纯 markdown 提示词（`SKILL.md`+`prompts/`+`references/`+`output-templates/`） |
| 位置 | `qa_master/skills/professional/` | `qa_master/skills/vendor/awesome-qa-skills/` |
| 核心价值 | 深度 + 确定性 + 编排 + 来源可追溯 + 门控 | 广度：覆盖大量长尾专类测试方法与技巧 |

**一句话**：本仓库是一把「带引擎的瑞士军刀」，货架上内置了「150 个专类工具」；而意图路由、`no_execution` 门控、状态机、来源追踪、企业适配、确定性引擎——这些是 awesome-qa-skills 本身没有的。

---

## 二、我原生覆盖什么

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

离线、无需模型、可审计的有限合成：`boundary`（边界值）、`decision_table`（决策表）、`state_transition`（状态迁移）、`pairwise`（成对组合）、`combinatorial`（组合测试）。

### 13 个测试维度

`functional` · `api` · `whitebox` · `integration` · `performance` · `load` · `stress` · `stability` · `compatibility` · `negative` · `security` · `recovery` · `regression`

---

## 三、内置 vendor 提供什么（广度叶子）

以下专类方法由内置 vendor 提供，随包分发、开箱即用，**无需再外部安装**。原生引擎未实现它们（见第六节路线图），但 `qa-master plan` 已能把对应阶段路由到这些 skill。

| 缺口类别 | 内置 vendor 提供（代表性 skill 目录） |
| --- | --- |
| **更多设计方法** | `model-based-testing` · `property-based-testing` · `metamorphic-testing` |
| **工具类自动化** | `ui-test-playwright` · `ui-test-selenium` · `ui-test-cypress` · `ui-test-puppeteer` · `ui-test-webdriverio` · `ui-test-testcafe` · `api-test-postman` · `api-test-bruno` · `api-test-pytest` · `api-test-restassure` · `api-test-supertest` · `performance-test-k6` · `performance-test-gatling` · `performance-test-jmeter` |
| **UI/视觉/移动/可访问性** | `visual-regression-testing` · `cross-browser-testing` · `mobile-testing` · `accessibility-testing` |
| **可靠性工程** | `chaos-testing` · `failover-testing` · `circuit-breaker-testing` · `dependency-failure-testing` · `retry-testing` · `timeout-testing` · `resilience-testing` |
| **AI 原生测试** | `ai-feature-testing` · `llm-testing` · `llm-evaluation-design` · `prompt-testing` · `rag-quality-testing` · `rag-retrieval-testing` · `llm-hallucination-testing` · `ai-agent-testing` · `agent-tool-testing` · `prompt-injection-testing` · `agent-loop-testing` · `agent-memory-testing` · `agent-permission-testing` · `multi-agent-testing` · `ai-safety-testing` |
| **质量工程 / 生产运维** | `quality-gate-design` · `quality-metrics-design` · `quality-debt-analysis` · `automation-roi-analysis` · `production-verification` · `production-incident-analysis` · `distributed-trace-analysis` · `metrics-anomaly-analysis` · `root-cause-analysis` · `log-analysis` |
| **Skill 工程治理** | `skill-change-verification` · `skill-quality-review` · `skill-evaluation` · `skill-prose-review` · `skill-prose-trim` |

---

## 四、路由如何整合（本仓库独有）

`qa-master plan` 的整合路径：

1. `intent.py` 把自然语言保守解析为规划阶段（`requirements`/`review`/`design`/`execution`/…），识别 `no_execution` 与信息缺口。
2. `skill_registry.select_skills` 按阶段/维度选出**原生指南**，输出在 `professional_guidance`。
3. `skill_registry.select_vendor_skills` 通过 `core.SKILLS` / `core.DIMENSION_SKILLS` 把阶段映射到 canonical skill 名，再在 vendor 里选中**中英双语**对应 skill，输出在 `vendor_skills`。
4. 名字在 vendor 里不存在（如 `regression-testing` / `compatibility-testing`，对应已有原生指南的维度）会被**优雅跳过**，不报错。

```
qa-master plan "评审需求并设计测试用例"
# → stages: [review, design]
# → professional_guidance: requirements-review, functional-api, …
# → vendor_skills.wanted: requirements-analysis, test-strategy, test-case-writing, test-case-reviewer
# → vendor_skills.selected: 每个名字 × {en, zh}（共 8 个叶子）
```

验证在 `tests/test_vendor_skills.py`：330 发现、阶段/维度路由、双语、优雅跳过。

---

## 五、何时用哪个

| 场景 | 用原生 | 用内置 vendor |
| --- | --- | --- |
| 需求评审、冲突、基线复核 | ✅ 原生 | — |
| 边界值 / 决策表 / 状态迁移 / 成对组合 / 组合测试（离线确定性） | ✅ 确定性引擎 | — |
| 等价类 / 分支条件 / 场景法设计 | ✅ 6 指南 | — |
| 分阶段 QA/回归编排（受人类门控、可暂停恢复） | ✅ Campaign 状态机 | — |
| model-based / property-based / metamorphic | 规划中（见路线图） | ✅ vendor 直接路由 |
| Playwright/Selenium/Cypress 等 UI 自动化脚本设计 | — | ✅ vendor 直接路由 |
| k6/JMeter/Gatling 性能压测 | — | ✅ vendor 直接路由 |
| LLM/RAG/Agent 测试、提示词注入 | 规划中（见路线图） | ✅ vendor 直接路由 |
| chaos / failover / circuit-breaker 可靠性测试 | 规划中（见路线图） | ✅ vendor 直接路由 |

---

## 六、逐步原生化路线图

内置 vendor 让「拥有全部能力」立即成立；原生化的意义是把高价值方法从「markdown 提示词」升级为「确定性引擎 / 专业指南」，从而获得可审计、无需模型、可追踪的能力。计划如下（按优先级）：

| 阶段 | 内容 | 落点 |
| --- | --- | --- |
| **P1 设计方法** | ✅ `pairwise`、`combinatorial` 已进引擎；`model-based`、`property-based`、`metamorphic` → 指南方法 | `design_methods.py` + 新参考/指南 |
| **P2 可靠性** | chaos / failover / circuit-breaker / dependency-failure / retry / timeout / resilience | 新指南 `reliability-engineering`（或扩展 `security-recovery`） |
| **P3 AI 原生** | LLM / RAG / prompt-injection / agent 测试 | 新指南 `ai-native-testing` |
| **P4 工具自动化** | Playwright/Selenium 等框架 + UI/视觉/跨浏览器/可访问性 | 新参考 `automation-tools` |
| **P5 质量工程/生产运维** | quality-gate / metrics / incident / trace / anomaly | 新指南 `quality-engineering` |

> 路线图反映的是「逐步原生化」的方向，不构成已交付能力的承诺。当前未原生实现的方法，均以内置 vendor 为准，并在 README「测试设计方法」表中如实标注来源，绝不虚标。
