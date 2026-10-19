# TASK-117 README 与导航检查

- Change: CR-028
- Document State: DRAFT
- Evidence Status: OBSERVED
- 检查角色：文档作者；不是独立评审或跨宿主验收。
- 文档冻结版本：`0ff9ad47ab0d442dff2157f6bf7d10e322a83f75`

## 改动

重写 README 的用户入口，说明交付物、单阶段/组合/完整流程、执行授权和实际交付边界；移除未经证实的 released 标签及多 Agent 兼容性断言。Windows 与 Linux 的快速安装使用虚拟环境解释器完整路径，避免激活脚本差异。

新增 `docs/GETTING_STARTED.md`，覆盖安装目标、安装后助手自检、状态位置、更新和暂停恢复。新增 `docs/SKILL_CATALOG.md`，按实际资料目录生成 165 个逻辑技能的中英文链接，区分 10 项工作流、150 项测试类型、5 项技能工程。README 分别解释 5 种确定性方法与 165 项双语技能，未把目录数量视为质量或执行证明。第三方资料和许可证未改动。

## 已执行检查

使用 `D:\codex-rd-platform\.venv\Scripts\python.exe`，在仓库根目录执行以下等效命令；状态与输出写入由 `tempfile.TemporaryDirectory` 创建的独立临时目录，结束后由上下文清理。

```text
python -m qa_master --state <temp>/campaign.json init demo-login
python -m qa_master --state <temp>/campaign.json plan "需求评审 + 测试计划 + 编写用例，不执行测试"
python -m qa_master --state <temp>/campaign.json status
python -m qa_master design --input examples/design-methods.json --output <temp>/methods.json
```

四条命令均退出 0，标准输出均可解析为 JSON；`design` 返回 `DRAFT_UNAPPROVED`。这次命令冒烟检查发生在文档冻结前，不冒充冻结后的全量回归。这里只验证命令可运行与上述输出事实，未独立断言所有路由字段，也没有执行教学模型对应的业务测试。

冻结后再次从三份文档提取 Markdown 链接，排除 HTTP(S) 与仅锚点链接；对本地链接去掉片段并相对文档目录检查目标存在：

| 文档 | 本地链接数 | 缺失目标 |
| --- | ---: | ---: |
| README.md | 26 | 0 |
| docs/GETTING_STARTED.md | 7 | 0 |
| docs/SKILL_CATALOG.md | 333 | 0 |

目录生成时逐项确认中文入口对应的英文 `SKILL.md` 存在，共 165 行。README 的不区分大小写 `awesome` 文本检查无匹配。

## 限制

未检查网页渲染或标题锚点解析，未把外链可用性作为本记录结果。没有重复执行完整测试套件或构建共享工作树。独立安装后 330 个目录发现、路由修复与算法覆盖验证由各自测试记录负责，本记录不代替其结果。
