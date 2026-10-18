# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

fixture Selenium4/Python，driver版本匹配已确认。S1页面rerender后持有旧element重试点击付款3次。S2重新通过data-testid定位、等待paid状态，动作仅一次且账务一条。S3异常退出未quit，Grid session活跃。S4异常截图/原错误保留且finally quit，session为0。S5并行两个session共用账号/订单。用REPAIR/VALID/RESOURCE_LEAK/EXPECTED_FAILURE/ISOLATION_FAIL；不把sleep增大当通用修复。

## 逐项预期

| ID | DECISION |
| --- | --- |
| S1 | REPAIR |
| S2 | VALID |
| S3 | RESOURCE_LEAK |
| S4 | EXPECTED_FAILURE |
| S5 | ISOLATION_FAIL |

## 核对方法

1. 固定项目Selenium/binding/browser/driver/Grid版本、capabilities和runner，生成兼容配置与POM；未提供Grid不自建拓扑，版本冲突先诊断。
2. 显式等待可观察条件（元素可交互、业务状态/窗口/URL达成），区分presence/visibility/业务ready；不混用implicit/explicit或以固定sleep修复所有时序。
3. rerender导致stale时依稳定locator重新查找并等待新状态，有限重试按项目策略；不能盲目重放付款动作引入重复效果。
4. 每并行session独立账号/业务键；try/finally driver.quit，失败留截图/日志/Grid session与原错误；重新渲染、业务失败、异常退出对照都需检查资源和失败传播。
