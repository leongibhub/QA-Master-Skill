# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

PR base=b1/head=h2，共享Money类型cents改decimal。E1 Money→refund→O-refund→T-refund，E2 Money→invoice→O-invoice→T-invoice。E3 同PR删除唯一T-tax，O-tax无其他覆盖。E4 plugin动态消费者未映射。E5 avatar服务独立契约且无金额依赖。判E1/E2 INCLUDE，E3 COVERAGE_GAP，E4 UNKNOWN，E5 EXCLUDE或据来源选择；输出base/head、testID与传递理由，不因文件小只跑单元。

## 逐项预期

| ID | DECISION |
| --- | --- |
| E1 | INCLUDE |
| E2 | INCLUDE |
| E3 | COVERAGE_GAP |
| E4 | UNKNOWN |
| E5 | EXCLUDE |

## 核对方法

1. 固定repo/base/head SHA与diff范围；为文件、符号、schema/config变化列来源，不按文件名猜影响或将不同HEAD的测试结果合并。
2. 输出变化符号→直接/传递消费者→保护义务→test ID/层级/执行版本的映射表，边标confirmed/candidate/unknown；只在有证据的隔离边界停止。
3. 删除或改弱测试要核对所保护义务是否仍有独立覆盖，不能仅从当前测试集选取导致消失的风险被漏掉。
4. 未知动态依赖或缺映射时保守纳入相关契约/集成候选并标缺口；区分候选范围、已执行和已满足，列追加验证/升级触发。
