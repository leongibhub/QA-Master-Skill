# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

词典v2：会员=member，金额分(cents)=元×100。C-1同v2会员限额100元与member限额10000分。C-2同v2同退款限额100元与120元。C-3同名“active”分别v1账户/v2订阅，没给实体和迁移映射。C-4同v2退款状态字典明确done=refunded，两文用不同词。用EQUIVALENT/CONTRADICTED/NOT_COMPARABLE逐项比较并列单位/版本/实体来源，别把词不同或同名跨版本直接判矛盾。

## 逐项预期

| ID | DECISION |
| --- | --- |
| C-1 | EQUIVALENT |
| C-2 | CONTRADICTED |
| C-3 | NOT_COMPARABLE |
| C-4 | EQUIVALENT |

## 核对方法

上述判定不改RC/BR契约：EQUIVALENT对应Relation=aligned、Status=assessed；CONTRADICTED在同适用域下对应conflict/assessed；NOT_COMPARABLE对应unassessed或stale的证据状态，不强填aligned/conflict。决策附表与原Relation/Status分列。

1. 固定比较来源及版本/生效时间，建立术语别名、实体ID、单位和状态映射；映射要有词典/契约证据，名字相同不自动同义。
2. 比较同范围、同版本、同条件下的业务规则；单位按证据换算，状态按明示映射归一，不静默合并跨版本或不同业务实体。
3. EQUIVALENT有可追溯同义/数值一致证据，CONTRADICTED有相同适用条件下无法同时成立的规则，NOT_COMPARABLE因身份、版本或单位映射缺失而不能比较。
4. 逐项给原文、归一值、来源/映射、影响和最小澄清；单来源不能证明跨文档一致，未指定权威源不得自动择一覆盖。
