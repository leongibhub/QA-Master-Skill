## TC-PROFILE-01 — member 身份获取个人资料时返回约定字段

来源：用户提供的需求 REQ-PROFILE-01。
已知环境与前提：ProfileDemo，构建 profile-2；member 测试身份已可用。

| 步骤 | 操作步骤 | 预期结果 |
| --- | --- | --- |
| 1 | 使用已可用的 member 测试身份发送 `GET /profile` 请求。 | 返回 HTTP 200；响应字段 `source_role` 精确等于 `member`，响应字段 `Trace` 精确等于 `trace-demo-01`。依据：REQ-PROFILE-01。 |

收尾：未提供。
待确认：目标环境地址及身份使用方式未提供，影响第 1 步的实际执行；其他响应字段未规定，不追加断言。
状态：草稿，未执行。

可导入 JSON：

```json
{
  "id": "TC-PROFILE-01",
  "source_role": "direct_input",
  "Trace": ["REQ-PROFILE-01"],
  "execution": "NOT_RUN",
  "steps": [
    {
      "action": "GET /profile",
      "expected": "HTTP 200; source_role=member; Trace=trace-demo-01"
    }
  ]
}
```
