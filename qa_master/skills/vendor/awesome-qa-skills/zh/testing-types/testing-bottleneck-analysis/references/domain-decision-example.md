# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

工单T1在0min进入、等环境0-40、执行40-50、返工50-60、完成60；runner等待期间空闲。B1分析主要耗时阶段。同日同复杂度：并发2时完成10项/小时，WIP4；并发4时完成6项/小时，WIP8且DB锁等待日志增加。B2声称加并发一定提效；B3把40min等环境当人力不足事实；B4有DB争用假设需受控复验。用DEPENDENCY_WAIT/UNSUPPORTED/HYPOTHESIS，拆分执行10min/返工10min，不把60min全记工时。

## 逐项预期

| ID | DECISION |
| --- | --- |
| B1 | DEPENDENCY_WAIT |
| B2 | UNSUPPORTED |
| B3 | UNSUPPORTED |
| B4 | HYPOTHESIS |

| METRIC | VALUE |
| --- | --- |
| dependency_wait_minutes | 40 |
| execution_minutes | 10 |
| rework_minutes | 10 |

## 核对方法

1. 固定窗口、工作项ID/复杂度、到达/完成和状态事件；时间线区分queue/等待依赖、实际执行、返工、交接与阻塞，不能把总周期当工时。
2. WIP用同窗口内未完成项，吞吐用完成项/窗口，交付周期与各状态停留分别统计；样本/缺事件与窗口不一致时给限制，不凭平均推因果。
3. 找限制关键流的阶段及上游依赖，核对资源利用、到达和完成变化；资源闲置可能是资料/环境阻塞，增并发也可能增加争用和降低吞吐。
4. 给可测的小改进、before/after可比口径与回滚信号；人力不足只是需验证候选，不能从长等待直接定责或排名个人。
