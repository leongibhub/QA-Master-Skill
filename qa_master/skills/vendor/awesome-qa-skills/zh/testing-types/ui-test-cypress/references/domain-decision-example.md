# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

现有项目Cypress13/E2E（fixture锁定基线，非推荐最新）；页面标题一直Checkout。C1真实付款后order.state=paid/amount20，主体A，spec断言这些值。C2 bug模式仍title正常但state=pending，spec只断言title。C3 cy.intercept只stub外部支付响应，真实UI状态pending，业务断言应失败。C4失败spec的CI命令追加||true。C5隔离账号A/B与cleanup均有证据。判C1/C5 VALID、C2 REPAIR、C3 EXPECTED_FAILURE、C4 INVALID；说明retry/边界与失败传播。

## 逐项预期

| ID | DECISION |
| --- | --- |
| C1 | VALID |
| C2 | REPAIR |
| C3 | EXPECTED_FAILURE |
| C4 | INVALID |
| C5 | VALID |

## 核对方法

1. 从项目lockfile/config确认Cypress、Node和浏览器版本及component/E2E边界；按该版本生成配置、custom command、spec与CI命令，不默认升级或混用旧配置。
2. 保留真实页面/组件与业务逻辑，cy.intercept只替换已确认外部边界；仅验证stub回包不足以证明真实后置条件。明确fixture数据与session隔离/注销。
3. 区分可重试query/assertion与执行一次的动作及整个test重试；等待以别名请求/可观察状态而不是sleep，重试不能掩盖首失败或重复副作用。
4. 最小应用正/负对照核对付款后订单状态/金额/主体；标题正常但业务错误必须断言失败且CI非0。记录截图/视频/原失败、teardown与真实运行证据，文件存在不等于通过。
