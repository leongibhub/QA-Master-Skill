# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

当前O1/O2/O3均v2。O1关联T1/T2，T1 v2有效断言runR1通过，T2未执行；O2仅有v1旧映射；O3有v2 T3映射但未执行。另两个来源重复ID=O9却分别“免运费”和“退款时限”。用O1 SATISFIED/O2 STALE/O3 MAPPED/O9 IDENTITY_CONFLICT，给当前三义务mapped和satisfied分子/分母，两个O1测试不能扩大分母。

## 逐项预期

| ID | DECISION |
| --- | --- |
| O1 | SATISFIED |
| O2 | STALE |
| O3 | MAPPED |
| O9 | IDENTITY_CONFLICT |

| METRIC | VALUE |
| --- | --- |
| mapped_obligations | 2 |
| satisfied_obligations | 1 |
| current_obligation_denominator | 3 |

## 核对方法

原RT/TC关系类型保持direct/derived/indirect/contradictory/missing，coverage status保持complete/partial/unverified/stale/unexecuted/unassessed。MAPPED/EXECUTED/SATISFIED与IDENTITY_CONFLICT只作附加判定列，不替换原枚举；有映射未执行保持unexecuted，身份冲突待解决前不计入已满足。

1. 固定requirement/obligation及实现/test/run的ID与版本，关系类型保持direct/derived/indirect/contradictory/missing；implements/validates/executed-by/satisfies只作为独立的边用途列，并记录证据来源；文件存在、名字相似不构成边。
2. 同义务多测试按义务唯一ID去重分母，保留测试层和具体断言；重复ID但不同内容先标IDENTITY_CONFLICT，不能合并计覆盖。
3. 分列MAPPED、EXECUTED、SATISFIED：映射有效不等于已运行，运行成功不等于该义务有有效断言。旧版本映射不能支持新版本满足。
4. 双向检查未映射义务、无来源测试与失效边；覆盖率注明当前唯一义务分母及排除/UNKNOWN，缺追踪不得填PASS。
