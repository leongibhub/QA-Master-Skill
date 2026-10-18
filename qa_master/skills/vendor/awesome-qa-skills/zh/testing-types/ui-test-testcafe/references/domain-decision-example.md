# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

fixture TestCafe3既有CLI/runner。T1所有t动作await，独立Role账户，paid20业务断言及清理。T2 test只断言Checkout标题，pending模式仍绿灯。T3 runner.run()返回failedCount=1，但入口忽略并process.exit0。T4 pending模式业务断言失败，CLI非0、截图可关联testID。T5两个Role实际共享同账户/业务键互相污染。用VALID/REPAIR/FAILURE_HIDDEN/EXPECTED_FAILURE/ISOLATION_FAIL逐项，产物存在不等于运行通过。

## 逐项预期

| ID | DECISION |
| --- | --- |
| T1 | VALID |
| T2 | REPAIR |
| T3 | FAILURE_HIDDEN |
| T4 | EXPECTED_FAILURE |
| T5 | ISOLATION_FAIL |

## 核对方法

1. 确认项目TestCafe/Node/browser、原生自动化模式与CI/reporter版本；生成fixture/test/config和现有runner兼容，缺配置保持待确认不推荐隐式升级。
2. 用Role或独立身份初始化隔离会话，账号/业务键同样隔离；异步t动作必须await，Selector/断言采用支持的智能等待而非固定sleep。
3. 核对付款后状态、金额和主体；stub外部边界不能绕过被测UI，正常标题不能代表成功，负对照应使业务断言失败。
4. CLI非0或programmatic runner返回failedCount>0必须使CI失败；reporter自定义不得吞失败，保留截图/控制台/测试ID与cleanup。配置静态可解析和真实执行分别记。
