# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

同样本 S/model M1/prompt P2/temperature0/seed7，协议要求 JSON 必含 decision、amount，decision=APPROVE、amount=20；reason 可用同义句。L-1 三次分别合法 JSON、金额20、理由同义。L-2 三次中第三次缺 amount。L-3 只有一次输出，团队声称稳定。L-4 三次 JSON 结构合法，但未给语义预期。判定 PASS/FAIL/INSUFFICIENT_EVIDENCE/UNKNOWN，并给 L-2 结构失败数及分母，不因理由措辞变化误报。

## 逐项预期

| ID | DECISION |
| --- | --- |
| L-1 | PASS |
| L-2 | FAIL |
| L-3 | INSUFFICIENT_EVIDENCE |
| L-4 | UNKNOWN |

## 核对方法

1. 固定样本 ID、模型/Prompt/工具/数据版本、temperature、seed（仅供应商支持时）和其他采样参数，记录项目指定重复次数；seed 相同不代表跨版本可复现。
2. 先比 schema、必需字段、允许枚举和政策等结构不变量，再依据项目 rubric 比语义结论；同义表达或获准顺序变化不应报错。
3. 逐样本报告重复分母、结构失败数、语义失败数与偶发失败；方差需明确数值变量、统计单位和算法，不将文本不同率冒充质量方差。
4. 缺重复数据只报告单次观察，缺 rubric 则语义一致性 UNKNOWN；不同参数或版本分组比较，不混成稳定性证据。
