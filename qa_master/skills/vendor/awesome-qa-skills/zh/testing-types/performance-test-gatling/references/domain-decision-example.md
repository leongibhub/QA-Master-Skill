# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

fixture版本由构建记录确认 Java DSL/Gatling3.13/JDK17，离线test-compile日志成功。G-1 单请求/用户，无循环重试，constantUsersPerSec(10).during(2)，实际20请求/2秒。G-2 constantConcurrentUsers(10)却未给完成请求数，宣称10RPS。G-3 queue feeder仅5行，20个用户各feed一次，第6次耗尽但忽略错误。G-4 未给SLO仍写p95<500ms并宣称通过。用 VALID/UNSUPPORTED/FAIL/UNKNOWN 判断；解释compile不等于运行通过及feeder需求。

## 逐项预期

| ID | DECISION |
| --- | --- |
| G-1 | VALID |
| G-2 | UNSUPPORTED |
| G-3 | FAIL |
| G-4 | UNKNOWN |

## 核对方法

1. 先读取项目 Gatling/插件/JDK 与 Java/Scala/Kotlin DSL 版本，沿用已有布局；选定同一 DSL 的 injection 与 assertion API，不能混用。生成资产先用项目构建的离线 test-compile 验证，依赖未缓存则标 BLOCKED 而非编译通过。
2. 开放模型控制用户到达率，只有每用户单请求且无额外循环/重试时才与目标 RPS 一一对应；封闭模型控制并发，RPS 要从实际请求数/时窗核对。
3. feeder 的总消费数按每用户/每循环 feed 次数复算；queue 耗尽须可见失败，circular 只在项目允许重复数据时使用，身份/业务键不冲突。
4. 门槛来自项目并使用版本支持的 assertion API，缺门槛输出未配置骨架而不放入自定500ms/1%数值；编译、负载达成和SLO通过分别记证据。
