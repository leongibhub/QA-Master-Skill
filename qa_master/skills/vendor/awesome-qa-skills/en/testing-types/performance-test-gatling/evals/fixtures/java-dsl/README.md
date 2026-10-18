# Java DSL Offline Compile and Input Boundaries

This independent synthetic fixture declares Gatling3.9.5/Java17 for DSL calibration, not the project current version or capacity. With cached dependencies use `mvn -o test-compile`; missing dependencies mean BLOCKED. Compilation requires no production calls.

The Simulation has no default base URL, arrival rate, duration or gates. Supply `fixture.baseUrl`, `fixture.usersPerSec`, `fixture.durationSeconds`, `fixture.p95Millis`, and `fixture.errorPercent` from explicit project input; omission must fail diagnostically.

Each user sends one request and consumes one queue record; the two-row CSV permits two consumptions. Twenty users exhaust it; circular reuse cannot hide uniqueness constraints. Status200 with pending or amount other than20 must fail. Do not run load without an authorized fixture service; throughput/SLO need separate evidence.

API: [Injection](https://docs.gatling.io/concepts/injection/), [Assertions](https://docs.gatling.io/concepts/assertions/).
