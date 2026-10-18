# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Synthetic baseline: JMeter 5.6.3/JDK 17, local fixture only; supplied gates p95<=200ms and error<=1%; CSV reuse forbidden. J-1 claims 10 RPS from 10 threads without timers or measured throughput. J-2 consumes 10 rows from a 5-row CSV with recycle=true. J-3 has 100 JTL samples, 2 failures, p95=250ms and process exit 0. J-4 has 100 samples, no failures, p95=150ms, enough non-reused CSV rows and valid business assertions. Decide UNSUPPORTED/FAIL/PASS, giving the non-GUI entry and plugin/distributed prerequisites.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| J-1 | UNSUPPORTED |
| J-2 | FAIL |
| J-3 | FAIL |
| J-4 | PASS |

## Verification Method

1. Confirm project JMeter/JDK/plugins and JMX version. Check TestPlan/ThreadGroup/Sampler and adjacent hashTree structure, variables, and properties. Parseable XML proves structure only, not execution or SLO success.
2. Standard ThreadGroup controls closed-loop threads. Target RPS needs declared think time/timers, throughput control, or an installed arrival-rate plugin; verify achieved throughput/counts rather than inferring RPS from threads.
3. Record CSV path, encoding, columns, sharing, recycle/stopThread settings and consumption per thread/loop. For distributed runs check each injector's data/plugins/network and load allocation.
4. Use non-GUI entry in authorized environments, preserving JTL/logs. Check business assertions, latency/error gates, and CI propagation separately. Missing thresholds are UNKNOWN; HTML reports or exit 0 cannot hide failed samples.
