# JMX非GUI业务失败与CSV对照

本fixture只执行本地合成JSR223结果，不发网络请求；基线JMeter5.6.3。线程闭环不是RPS目标，无timer/到达率插件就不能声称指定RPS。

```sh
jmeter -n -t business-oracle.jmx -Jfixture.mode=good -Jfixture.loops=2 -l /tmp/fixture-good.jtl -j /tmp/fixture-good.log
jmeter -n -t business-oracle.jmx -Jfixture.mode=bug -Jfixture.loops=2 -l /tmp/fixture-bug.jtl -j /tmp/fixture-bug.log
python3 check_jtl.py /tmp/fixture-good.jtl --expected-samples 2 --p95-ms "$PROJECT_P95_MS" --error-percent "$PROJECT_ERROR_PERCENT"
python3 check_jtl.py /tmp/fixture-bug.jtl --expected-samples 2 --p95-ms "$PROJECT_P95_MS" --error-percent "$PROJECT_ERROR_PERCENT"
```

门槛变量须来自项目；示例不提供默认SLO。good的state=paid/amount20；bug虽200仍pending，业务断言使JTL失败，即使JMeter进程退出0也不能通过CI gate。使用新JTL路径，避免追加混入旧运行。

将loops改3时只有两行CSV，recycle=false/stopThread=true应在EOF停止；预期samples3的gate必须失败，不能把提前停止当完整吞吐。分布式时CSV路径、插件和每injector消费量须独立准备；该fixture没有分布式拓扑。XML解析、nonGUI运行、门槛接受分别记录。

API: [Test plan](https://jmeter.apache.org/usermanual/test_plan.html), [CSV lifecycle](https://jmeter.apache.org/usermanual/component_reference.html#CSV_Data_Set_Config).
