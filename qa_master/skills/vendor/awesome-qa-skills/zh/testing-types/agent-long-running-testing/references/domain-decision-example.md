# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

协议 L-v1：checkpoint v2 存已提交步骤；过期 lease 禁止提交；同 task_id 只执行一次；取消提交点后返回已完成。L-1：崩溃前步骤 A 提交；从 v2 恢复只执行 B，资源 active=0。L-2：恢复再次执行 A 并产生第二条 A 写入。L-3：旧 lease=4 已失效，worker 仍提交。L-4：取消发生于任务提交后，返回 completed，资源 active=0。分别 PASS/FAIL，核对版本、提交和释放证据。

## 逐项预期

| ID | DECISION |
| --- | --- |
| L-1 | PASS |
| L-2 | FAIL |
| L-3 | FAIL |
| L-4 | PASS |

## 核对方法

1. 从实际协议写出 queued→running→checkpointed→interrupted→resuming→completed 和 running→cancelling→cancelled；未定义状态或转换标为待确认。
2. 每个 checkpoint 记录 task_id、schema/状态版本、已提交 step ID、来源和完整性；恢复先校验版本与已提交效果，版本不兼容不得盲目重放。
3. 记录 owner、lease/fencing token 和过期规则。租约丢失的 worker 不得继续提交；重复 task_id 按项目幂等协议合并或拒绝，不能假定 exactly-once。
4. 按时间线检查取消与提交竞争：用项目定义的提交点判定赢家，保留已提交结果；核对终态、资源释放和取消确认，规则缺失交 Human 决策。
