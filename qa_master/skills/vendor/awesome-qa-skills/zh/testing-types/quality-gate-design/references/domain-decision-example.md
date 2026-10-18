# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

门禁Gate-v3：关键义务均PASS且证据<=24h才可放行；UNKNOWN/BLOCKED fail-closed；例外必须负责人签字且未过期。G-1 测试记录缺失。G-2 环境故障不能运行。G-3 新鲜运行断言失败，有已过期签字例外。G-4 必要义务新鲜PASS且版本匹配。G-5 48h旧PASS。逐项UNKNOWN/BLOCKED/FAIL/PASS/UNKNOWN；同时给推进STOP/GO建议，旧或缺记录不能绿灯。

## 逐项预期

| ID | DECISION |
| --- | --- |
| G-1 | UNKNOWN |
| G-2 | BLOCKED |
| G-3 | FAIL |
| G-4 | PASS |
| G-5 | UNKNOWN |

## 核对方法

1. 为每个门槛记录义务、输入/版本/时效、比较符、PASS/FAIL、不可执行BLOCKED、缺证据或无法判断UNKNOWN的真值表；没有记录不得视为PASS。
2. 聚合规则由项目指定：必要门槛FAIL优先，无法验证按fail-closed停止；UNKNOWN/BLOCKED保持原因而不是折算失败率。所有必要门槛有新鲜有效PASS才可推荐通过。
3. 例外单列义务范围、授权人、理由、批准证据、有效期、补偿控制与撤销条件；过期/越界/无授权不生效，不改写原始FAIL。
4. 明确门禁触发、负责人、重新验证和回滚/停止条件；设计、静态证据判定与实际流水线实施分别报告，缺规则提交待Human决策。
