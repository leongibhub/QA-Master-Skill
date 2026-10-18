# Non-GUI JMX Business Failure and CSV Controls

This JMeter5.6.3 fixture samples local synthetic JSR223 results without network calls. Closed-loop threads are not targetRPS; absent arrival control/measurement no rate can be claimed.

```sh
jmeter -n -t business-oracle.jmx -Jfixture.mode=good -Jfixture.loops=2 -l /tmp/fixture-good.jtl -j /tmp/fixture-good.log
jmeter -n -t business-oracle.jmx -Jfixture.mode=bug -Jfixture.loops=2 -l /tmp/fixture-bug.jtl -j /tmp/fixture-bug.log
python3 check_jtl.py /tmp/fixture-good.jtl --expected-samples 2 --p95-ms "$PROJECT_P95_MS" --error-percent "$PROJECT_ERROR_PERCENT"
python3 check_jtl.py /tmp/fixture-bug.jtl --expected-samples 2 --p95-ms "$PROJECT_P95_MS" --error-percent "$PROJECT_ERROR_PERCENT"
```

Gate variables come from the project; no default SLO is supplied. good yields paid/amount20; bug yields200 with pending and failedJTL assertions. A JMeter exit0 does not pass the CI gate. Use freshJTL paths to avoid appending old runs.

With loops3 and only two CSV rows, recycle=false/stopThread=true stops onEOF. A samples3 gate must fail; early termination is no achieved-load proof. Distributed runs need per-injector data paths/plugins/consumption; this fixture defines no topology. XML parsing,non-GUI execution,and gate acceptance remain separate.

API: [Test plan](https://jmeter.apache.org/usermanual/test_plan.html), [CSV lifecycle](https://jmeter.apache.org/usermanual/component_reference.html#CSV_Data_Set_Config).
