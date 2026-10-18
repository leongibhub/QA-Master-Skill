# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

同commit/义务/资源上限2workers：基线setup20s，tests A60s/B40s顺序，teardown10s。T1隔离后A/B并行，setup/teardown相同且金额故障仍被断言检出。T2也并行但共用账号使故障漏检。T3不同测试集只10s。T4只有候选估算没运行。用ACCEPT/REJECT/NOT_COMPARABLE/ESTIMATE，复算基线与T1关键路径时长，保留冷暖缓存口径。

## 逐项预期

| ID | DECISION |
| --- | --- |
| T1 | ACCEPT |
| T2 | REJECT |
| T3 | NOT_COMPARABLE |
| T4 | ESTIMATE |

| METRIC | VALUE |
| --- | --- |
| baseline_seconds | 130 |
| candidate_seconds | 90 |

## 核对方法

1. 用同commit/测试义务/数据/资源/窗口的事件profile分setup、execute、teardown、重试；沿依赖DAG求关键路径，重叠job不相加。
2. 单列cold/warm缓存、runner上限、并发、独立数据与资源争用；候选改变的因素有记录，不能用不同测试规模或环境推断提速。
3. 对照相同业务故障是否仍由有效断言检出，失败与日志/trace保留；加并行不能共享账号或吞异常，耗时改善不抵消失去保护。
4. 给基线/候选时长、资源成本、收益比例与回滚信号；只有实际可比运行才叫观察到收益，设计推算保持候选，不当生产保证。
