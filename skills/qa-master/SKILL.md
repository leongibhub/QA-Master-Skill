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
先列举此工程内已实现的专业模块；按测试目标挑选并调用，不要仅凭文件名臆测存在。V0.1 仅提供上述流程规则及 `qa_master` 状态工具，尚没有完整专业测试生成器或运行时分派器。

## 本地验证 CLI
`python -m qa_master init "project-name"`
`python -m qa_master plan "只生成测试用例，不执行测试"`
`python -m qa_master answer requirements "没有"`
`python -m qa_master check execution`

CLI 不是外部系统连接器，不会自动执行测试。
