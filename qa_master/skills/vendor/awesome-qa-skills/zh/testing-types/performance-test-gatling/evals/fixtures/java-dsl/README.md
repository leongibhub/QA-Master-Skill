# Java DSL离线编译与输入边界

本独立合成fixture声明Gatling3.9.5/Java17基线，仅作DSL资产校准，不是项目当前版本或容量保证。已有依赖缓存时执行 `mvn -o test-compile`；缺依赖为BLOCKED，不能调用生产接口来验证编译。

Simulation不默认baseUrl、用户率、时长或门槛，所需system properties均须来自明确项目输入：`fixture.baseUrl`、`fixture.usersPerSec`、`fixture.durationSeconds`、`fixture.p95Millis`、`fixture.errorPercent`。缺任一项必须可诊断失败。

每用户一个请求、一个queue feed；CSV两行只支持两次消费。20用户会耗尽，不能改circular掩盖需要唯一业务键的约束。错误返回pending或amount非20应成为失败请求，不因status200通过。未提供fixture服务时不运行负载；真实吞吐/SLO必须另取运行证据。

API: [Injection](https://docs.gatling.io/concepts/injection/), [Assertions](https://docs.gatling.io/concepts/assertions/).
