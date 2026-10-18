# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

同一时钟：根 span R [0,100]ms；同步子 A [10,70]、B [40,90]；A/B 同 parent=R。X-1：有人将100+60+50当端到端210ms。X-2：求R可见独占时间。X-3：异步 C link到R，无起止数据，声称C是根因。X-4：队列enqueue=20/dequeue=35ms。逐项 WRONG/CALCULABLE/UNKNOWN，给区间并集与队列计算，不把最慢span当根因。

## 逐项预期

| ID | DECISION |
| --- | --- |
| X-1 | WRONG |
| X-2 | CALCULABLE |
| X-3 | UNKNOWN |
| X-4 | CALCULABLE |

| METRIC | VALUE |
| --- | --- |
| observed_exclusive_ms | 20 |
| queue_ms | 15 |

## 核对方法

1. 固定 trace/span ID、parent ID、异步 links、服务/部署版本、起止时刻和采样范围；核对父子包含关系与时钟偏差，link 不自动当同步父子。
2. 同一时钟域内按区间并集扣除同步子 span 得 observed exclusive time；重叠子 span 不能相加。缺 span 时只报可见区间，不能宣称真实独占时间。
3. 关键路径根据真实依赖顺序和阻塞等待识别；queue time 需 enqueue/dequeue 证据，不把未解释空白都归为排队。
4. 最慢 span 仅是调查候选，根因需日志/指标/故障实验佐证；缺 span、采样和时钟不确定性分别限制结论。
