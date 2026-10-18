## Normalized endpoint contract

Generators produce smoke assertions for known fields only: require nonempty endpoints and explicit expected_statuses; optional expected_json and sourced max_response_ms. Missing data, unresolved parameters/variables, or schema assertions produce incomplete scaffolds and a nonzero exit. Read `references/generator-contract.md`; configure target and credentials explicitly.

```json
{
  "endpoints": [
    {
      "method": "POST",
      "path": "/orders",
      "headers": {
        "Content-Type": "application/json"
      },
      "body_encoding": "json",
      "body": {
        "qty": 1
      },
      "expected_statuses": [
        201
      ],
      "expected_json": {
        "qty": 1
      }
    }
  ]
}
```

Use `headers_env: {"Authorization": "TEST_AUTHORIZATION"}` for credentials; environment values include the complete header value, e.g. the Bearer prefix. Python/Java require `BASE_URL`; Supertest requires `API_BASE_URL` or an explicit absolute `SUPERTEST_APP` path; Bruno uses its `baseUrl` environment variable. There is no universal token, invented sample body, or fixed three-second gate.

For a protected OpenAPI operation, the parser retains `security_requirements` and `security_schemes`. Generation remains incomplete until `headers_env` maps every required header for at least one complete supported security alternative. Query/cookie API keys, mutualTLS, HTTP schemes other than Basic/Bearer (such as Digest), duplicate credential headers within one AND alternative, and unknown schemes need additional implementation; an anonymous alternative or operation-level `security: []` needs no credentials.

RestAssured represents sourced millisecond response limits in nanoseconds so fractional millisecond thresholds are preserved.

OpenAPI derives default success statuses from declared 2xx only; negative scenarios need explicit expected statuses. A request example does not prove business success, and status-only smoke does not establish acceptance. An agent must implement complex schema assertions before execution. WSDL preserves SOAP service addresses but needs an envelope and response assertions. YAML requires PyYAML and fails explicitly when absent. Report generation separately from executed test results.


The normalized JSON above can enter `scripts/run.sh`, or parser and generator can be called separately. If a curl/endpoint lacks explicit expectations, fill the sourced contract before running; scripts never invent expectations.
