# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

同 commit/test-set/runner：基线 queue=20s, install=30s，两个并行测试job分别60s/40s，report=5s，无重试。候选 CI-1：有效缓存 install=10s，其余相同且检出同一故障。CI-2：移除金额回归job，变快但故障未检出。CI-3：失败job用 || true，汇总绿灯。CI-4：lockfile变化但复用旧缓存未验证。判定 ACCEPT/REJECT/UNKNOWN，给基线与CI-1端到端时间和关键路径。

## 逐项预期

| ID | DECISION |
| --- | --- |
| CI-1 | ACCEPT |
| CI-2 | REJECT |
| CI-3 | REJECT |
| CI-4 | UNKNOWN |

| METRIC | VALUE |
| --- | --- |
| baseline_seconds | 115 |
| candidate_seconds | 95 |

## 核对方法

1. 以 commit/run/runner/config/test-set ID 固定比较对象；从事件时间线分解 queue、checkout/install、setup、execute、retry、report，区分端到端等待与 runner 忙时。
2. 沿 DAG 计算实际关键路径，重叠 job 不相加；报告重试次数与失败原始结果，不能用重跑绿灯隐藏首失败。
3. 缓存键包含项目相关 lockfile/工具链/配置身份；比较 cold/warm，记录命中和失效验证，不能复用不匹配缓存跳过依赖校验。
4. before/after 保持保护义务、测试集、故障检出、资源和窗口可比；删测试或吞失败的提速候选拒绝，提出可测收益和回滚信号。
