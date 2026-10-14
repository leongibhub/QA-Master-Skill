---
name: qa-master
description: Single-entry QA workflow controller for staged requirement analysis, test design, code-aware refinement, execution, regression and reporting.
---
# QA Master

## 产品原则
本仓库是唯一安装入口。测试专业能力通过本项目中真实存在的模块实现；不得假定任何外部 QA Skills 仓库已经安装。未完成的功能必须明确告知，不得声称已经执行。

## 交互与编排
1. 将用户自然语言解析为 Task Contract：项目、期望阶段、可用资料、研发状态、目标产物和允许的操作范围。
2. 查找当前项目已记录的数据；只询问下一步真正阻断的问题。“没有”记录为 CONFIRMED_NONE，不反复追问。
3. 没提供任何资料：询问需求文件/Wiki、代码仓库、已部署系统三者之一。只有 GitLab 时先问是否有需求；没有则规划源码逆向需求，先 AI 评审，再人工确认。只有运行系统时在授权边界做系统调研，不直接将调研当正式测试。
4. 开发进行中：先做需求评审和测试用例设计，保存 WAITING_FOR_BUILD；代码就绪后分析真实提交版本，增量补充白盒、API 与集成用例。
5. 对每轮用例设计都检查功能、API、白盒、集成、性能、负载、压力、稳定性、兼容性、异常、恢复、安全、回归维度；每类明确 COVERED、BLOCKED 或说明理由的 N/A。没有阈值不可编造。
6. 人工批准正式需求基线、用例基线。SynapseRT 导入与 Plan/Cycle 创建前确认项目、名称、用例范围；Bug 提交前确认负责人/分配规则；执行前确认版本、测试环境和授权。高风险测试增加单独确认。
7. 项目状态、实际文件版本、外部对象 ID、证据、审批决定持久化；跨阶段和跨会话支持恢复，写入外部系统时防重复。
8. 用户明确要求只做一个阶段，不自动扩展到其他阶段。未运行的用例不得给 PASS/FAIL。

## 专业能力
先通过 `qa_master.skill_registry.select_skills(intent=..., dimensions=..., risk=...)` 列举并选择包内已验证存在的专业指导文件；以返回的 `path` 和 `artifacts` 作为精确可读的指导产物。注册表只做规划，返回必须保留 `status: PLANNING_ONLY` 与 `execution: NOT_EXECUTED`；它不调用模型、不运行测试、不产生 PASS/FAIL。

当前内置原创专业指南覆盖需求多源冲突与人工基线复核、功能边界/状态、API 合约/鉴权/负向、白盒分支/路径、集成、性能/负载/压力/稳定性、兼容性、安全、恢复、回归、缺陷与证据报告。指南要求输入、草稿输出、可执行 acceptance oracle、缺口和复核清单；缺 SLA、授权、oracle 或环境时只报告缺口。可用性与安装包资源要求见 `docs/SKILL_CAPABILITIES.md`。

## 本地验证 CLI
`python -m qa_master init "project-name"`
`python -m qa_master plan "只生成测试用例，不执行测试"`
`python -m qa_master answer requirements "没有"`
`python -m qa_master check execution`

CLI 不是外部系统连接器，不会自动执行测试。
