# 领域判定示例

此脱敏合成 fixture 用于校准本 Skill 的分析，不是项目真实执行或业务验收记录；数值和协议仅适用于本示例。

## 输入

fixture Puppeteer23/browser来自该安装bundle。U1新窗口关联原page，核对目标receipt且paid20，finally关闭两page/browser。U2加载失败异常被catch忽略并return0，browser仍active。U3标题Checkout但state=pending。U4超时有截图/当前URL，原错误向runner传播，finally资源active0。U5给定不兼容browser启动日志。用VALID/FAIL/REPAIR/EXPECTED_FAILURE/CONFIG_ERROR，并给新窗口/加载失败/超时的资源核对证据。

## 逐项预期

| ID | DECISION |
| --- | --- |
| U1 | VALID |
| U2 | FAIL |
| U3 | REPAIR |
| U4 | EXPECTED_FAILURE |
| U5 | CONFIG_ERROR |

## 核对方法

1. 读取实际Puppeteer/Node/browser与launch配置/支持范围；版本或browser不兼容单列CONFIG_ERROR，不能把launch成功当所有功能兼容。
2. 新窗口从目标创建事件/关联opener定位并等待可用page，检查目标URI与权限；导航等待与业务就绪分开，以页面真实状态作oracle，固定sleep无此证据。
3. try/finally关闭新旧page及自建browser，保留超时/加载失败原异常；主错误与cleanup错误分别记录，不能吞异常后返回成功。
4. 最小fixture包含正常支付、wrong state、新窗口、加载失败与超时；核对业务状态/主体及截图/URL/日志/版本，不把文件生成或HTTP加载成功升级为业务通过。
