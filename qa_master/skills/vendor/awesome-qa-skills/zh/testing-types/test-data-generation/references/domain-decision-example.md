# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

schema：Order.id唯一、Refund.order_id必须存在、Refund.amount>0且累计<=Order.total；Order status=paid才能退款。D1 Order O1 total20 paid，Refund F1 O1 amount5，标valid。D2两个Order都id=O1，标valid。D3 Refund F2指O9不存在，标invalid，预期外键拒绝。D4 O2 pending却退款5，标valid。用VALID/INVALID/MATCHED_NEGATIVE逐组核对，交付一个固定seed7可重复的有效样本与清理Refund→Order。

## 逐项预期

| ID | DECISION |
| --- | --- |
| D1 | VALID |
| D2 | INVALID |
| D3 | MATCHED_NEGATIVE |
| D4 | INVALID |

## 核对方法

1. 从已提供schema、实体外键、唯一约束、状态关系与场景预期派生数据组；固定种子/生成器版本，缺规则保留UNKNOWN，不自动发明字段或真实用户。
2. 分开有效happy/boundary数据与定向无效数据，每组注明改变的约束、预期拒绝/允许和不受影响的关系；无效数据不能悄悄进入正常流程组。
3. 实际交付脱敏样本及验证：唯一性、外键存在、字段类型/范围、状态关联、可重复输出；重跑相同seed应得到相同数据身份而非只写可复现建议。
4. 使用隔离ID/命名空间，保留来源许可、个人数据限制和清理逆依赖顺序；缺授权不抓真实个人资料，不把生成样本当真实业务代表性证明。
