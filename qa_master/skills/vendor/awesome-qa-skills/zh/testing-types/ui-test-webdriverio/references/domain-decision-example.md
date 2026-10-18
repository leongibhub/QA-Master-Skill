# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

fixture WebdriverIO8/async/matched浏览器。W1配置service名字不存在安装包，启动失败日志明确module缺失。W2click未await且未断言状态。W3paid断言遇pending失败，日志含test/worker/session/browser version及原堆栈，CI非0。W4各worker独立账号/订单、await动作、paid20/主体断言与cleanup。W5捕获命令timeout后输出PASS并exit0。用CONFIG_ERROR/REPAIR/EXPECTED_FAILURE/VALID/FAILURE_HIDDEN逐项，保留原错误，不换框架来绕过配置。

## 逐项预期

| ID | DECISION |
| --- | --- |
| W1 | CONFIG_ERROR |
| W2 | REPAIR |
| W3 | EXPECTED_FAILURE |
| W4 | VALID |
| W5 | FAILURE_HIDDEN |

## 核对方法

1. 固定WebdriverIO/Node、runner/framework、browser/driver/service版本组合；核对capabilities、services与实际安装包、配置及远端支持，不从名称假定兼容。
2. 生成该版本的async spec/BDD步骤，所有异步命令await；等待以可观察业务状态和元素条件，原命令错误不得catch吞成通过。
3. 每worker独立session/身份/业务键，生命周期hooks负责初始化和清理；平台/浏览器差异仅覆盖项目支持矩阵，缺矩阵标未知。
4. 失败证据含testID、worker/session/capability、版本、URL、截图/日志和原堆栈；不兼容配置CONFIG_ERROR、业务断言失败与环境错误分列，均需可诊断并传播至CI。
