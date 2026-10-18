# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

变更配置 v8：金额单位 cents→decimal。证据 E1：配置→checkout 读取→退款金额义务 O1→T-refund；E2：checkout→invoice 共享金额→O2→T-invoice；E3：plugin registry 动态消费者未知；E4：图片服务明确独立契约、不读金额配置。判定 O1/O2 INCLUDE，E3 UNKNOWN，E4 EXCLUDE 或按证据自行判断 INCLUDE/EXCLUDE/UNKNOWN，列边来源及未知依赖的保守验证。

## 逐项预期

| ID | DECISION |
| --- | --- |
| O1 | INCLUDE |
| O2 | INCLUDE |
| E3 | UNKNOWN |
| E4 | EXCLUDE |

## 核对方法

1. 固定变更版本及范围，输出 changed 文件/符号/配置→dependent→业务义务→test ID 的带类型证据图；每条边记录来源、版本与 confirmed/candidate/unknown。
2. 遍历直接和传递消费者，去重循环；只有契约隔离或已证明无消费者边才可停止，记录停止依据，不能以目录边界截断。
3. 动态注册、运行时配置或未追踪依赖保持 unknown；按风险增加消费者契约/集成验证候选，不把没有映射当无影响。
4. 输出纳入/排除理由、最小验证、残余风险及追加范围触发；本 Skill 可分析代码、数据、配置等变更，PR 专项另保留 base/head 与 diff 身份。
