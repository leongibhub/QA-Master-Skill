# 多维测试用例生成（开发里程碑）

新增 `qa_master.coverage_design.design_matrix(requirements, applicable=...)`，把已结构化需求按功能、API、白盒、集成、性能、负载、压力、稳定性、兼容性、异常、安全、恢复及回归维度分别登记。

输入可使用如下结构：

```python
from qa_master.coverage_design import design_matrix
requirements=[{
 "id":"REQ-01","text":"文件上传",
 "dimension":"functional","dimensions":["functional","api","performance"],
 "acceptance":"文件列表展示新文件",
 "oracles":{"api":"HTTP 201 且响应包含文件 ID",
            "performance":"P95 不超过经批准的阈值"},
 "thresholds":{"performance":{"p95_ms":500}},
 "approved":True,"source":"PRD v1","priority":"P1"
}]
result=design_matrix(requirements)
print(result["cases"], result["coverage"],result["gaps"])
```

所有案例仍是 `DRAFT_UNAPPROVED`。未明确的业务预期、非功能阈值和未批准需求将保留缺口，不得擅自输出合格结论。测试步骤是设计骨架，**不是完整可执行脚本**。维度未覆盖时标 `UNASSESSED`；只有说明理由的显式 N/A 才能标为 `N/A`。

验证：本地工程运行 `python -m unittest discover -s tests -q`：104 项通过，其中 15 项为新增矩阵测试。远端 GitHub Actions 和真实业务项目用例质量尚未验证。
