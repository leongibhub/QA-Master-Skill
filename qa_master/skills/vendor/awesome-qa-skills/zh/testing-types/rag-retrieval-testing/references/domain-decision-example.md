# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

queryQ租户A，已知相关文档集合{d1,d2,d3}，k=2，无重复。R-1返回d1/d2均A当前版本。R-2返回d1/B租户d9，即使d9相关也越权。R-3返回d1旧版，项目要求最新。R-4检索d1/d2正确但生成把原14天写30天。R-5无完整相关标注却宣称Recall100%。用RETRIEVAL_VALID/AUTHORIZATION_FAIL/STALE/GENERATION_FAIL/UNKNOWN，复算R-1precision和recall的分子分母，不把2个结果等于完整覆盖。

## 逐项预期

| ID | DECISION |
| --- | --- |
| R-1 | RETRIEVAL_VALID |
| R-2 | AUTHORIZATION_FAIL |
| R-3 | STALE |
| R-4 | GENERATION_FAIL |
| R-5 | UNKNOWN |

| METRIC | VALUE |
| --- | --- |
| precision_numerator | 2 |
| precision_denominator | 2 |
| recall_numerator | 2 |
| recall_denominator | 3 |

## 核对方法

1. 给query及相关集合固定标注规则、文档/chunk粒度、标注者与版本；Recall@k分母为已知相关集合，Precision@k按实际返回数和项目对重复chunk规则计算。
2. 逐结果核对top-k/rank、relevance、租户/权限过滤、新鲜度与文档版本；越权结果不能因相关而计成功，过时结果不由分数高抵消。
3. 控制相同query、索引、过滤和资源比较排序或配置变化；无完整相关集合只报代理指标和限制，不宣称真实召回完整。
4. 区分相关资料未取回的retrieval failure与取回正确但生成错误的generation failure；缺生成输出不能定位生成环节，缺标签保持UNKNOWN。
