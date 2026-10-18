# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

JMeter5.6.3/JDK17，脱敏JMX只请求本地fixture；规则p95<=200ms、error<=1%，CSV不允许重用。J-1 10线程无timer/实测吞吐却声称10RPS。J-2 CSV5行，10次读取，recycle=true违反不复用。J-3 JTL100条、2失败、p95=250ms，进程退出0。J-4 JTL100条无失败、p95=150ms，CSV足量/不复用，结构日志和业务断言正常。逐项 UNSUPPORTED/FAIL/PASS；给非GUI入口及缺插件/分布式前提。

## 逐项预期

| ID | DECISION |
| --- | --- |
| J-1 | UNSUPPORTED |
| J-2 | FAIL |
| J-3 | FAIL |
| J-4 | PASS |

## 核对方法

1. 确认项目 JMeter/JDK/插件与 JMX版本，逐个核对 TestPlan/ThreadGroup/Sampler 与相邻 hashTree、变量和属性；XML可解析只证明结构，不等于JMeter可执行或SLO通过。
2. 标准ThreadGroup控制闭环线程数；目标RPS需明确think time/timer、吞吐控制器或已安装到达率插件，记录实际吞吐和请求数，不能从线程数直接推出RPS。
3. CSV Data Set记录文件路径、编码、列、共享模式、recycle/stopThread；按循环与线程复算数据消费，分布式每injector的数据、插件、网络和负载分担独立核对。
4. 在授权环境用non-GUI入口保存JTL与日志，分别检查业务断言、时延/错误门槛及exit/CI传播；门槛未给保持UNKNOWN，失败样本不能被HTML报告或进程0掩盖。
