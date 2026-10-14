# 源码候选需求评审包

V1.0 开发模块 `qa_master/review_packet.py`。

处理链路：`GitLabReader` 读取源码 → `reverse_requirements.inspect_repository` 输出静态观察 → `create_review_packet` 生成证据与待确认问题 → 用户对每项观察确认或驳回 → `build_requirement_drafts` 输出需求草稿。

## 使用示例

```python
from qa_master.review_packet import create_review_packet, build_requirement_drafts

inspection = {
    "candidates": [{
        "source": {"path":"backend/auth.py","line":42,"symbol":"login","ref":"pinned-sha"},
        "observed": "函数存在，包含分支",
        "risk_hints": ["BRANCHES"]
    }],
    "gaps": []
}
packet=create_review_packet(inspection)
print(packet["findings"])
observation_id=packet["observations"][0]["id"]

# 以下决策应当来自真实的人类确认；仅用于演示 API 形状
decisions={
    observation_id:{
        "decision":"accept",
        "requirement":"合法用户登录后获得有效会话",
        "acceptance":"返回经授权的会话标识，且用户可访问授权资源"
    }
}
draft=build_requirement_drafts(packet,decisions)
assert draft["baseline_approved"] is False
```

### 关键限制

- 此模块不解析完整业务语义。它为静态观察生成待确认问题，不自动编造业务规则。
- **确认一条候选观察 ≠ 批准整个需求基线**。最终需求仍应经过 AI 需求评审及人工批准。
- 源码可能有 Bug；不得直接将现有代码行为作为测试的预期正确结果。
- 代码证据包含原始文件路径和行号，建议使用固定 Commit SHA。
- 此模块不连接 Jira/SynapseRT，也不启动测试执行。

### 验证

在本地独立实现上运行了 15 项针对性单元测试，全部通过；提交的文件亦包含对应 15 项自动化测试。尚需核验完整仓库 CI、真实 GitLab 和真正的需求专家评审流程。
