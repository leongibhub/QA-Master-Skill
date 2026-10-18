## Normalized endpoint contract

生成脚本只生成已知字段的 smoke 断言：必须提供非空 endpoints、明确 expected_statuses；可提供 expected_json 和来源化 max_response_ms。缺数据、未解析参数/变量或 response_schema 待实现时生成失败工件并非零退出，不能运行成绿色。先读 `references/generator-contract.md`，目标与凭据必须显式配置。

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

凭据使用 `headers_env: {"Authorization": "TEST_AUTHORIZATION"}`，环境变量值包含完整头值（如 Bearer 前缀）。Python/Java 用 `BASE_URL`；Supertest 用 `API_BASE_URL` 或 `SUPERTEST_APP` 的显式绝对路径；Bruno 配置 `baseUrl` 环境变量。无通用 token、sample body 或固定 3 秒阈值。

对受保护的 OpenAPI 操作，解析器会保留 `security_requirements` 与 `security_schemes`。只有 `headers_env` 为至少一个完整且受支持的安全方案映射了全部必需请求头，生成才可继续；query/cookie API key、mutualTLS、Basic/Bearer 之外的 HTTP 认证方案（如 Digest）、同一 AND 备选方案中重复使用凭据头的情况，以及未知方案都需要补充实现。若存在匿名备选方案，或操作级 `security: []` 覆盖全局认证，则不需要凭据。

OpenAPI 只从已声明 2xx 提取默认成功状态；负向场景需显式声明预期状态。请求示例不证明业务成功，生成的 status-only smoke 也不能代表业务验收。复杂 schema 校验需 Agent 实现后才能执行。WSDL 保留 SOAP 服务地址，但 envelope 与响应断言需另行实现。YAML 解析需要 PyYAML，缺依赖报错。生成完成与实际测试通过分开报告。


可将上述规范化 JSON 作为 `scripts/run.sh` 的输入，也可分别调用 parser 和 generator。输入只有 curl/端点而缺明确预期时，先填来源化契约再运行；脚本不会补造预期。
