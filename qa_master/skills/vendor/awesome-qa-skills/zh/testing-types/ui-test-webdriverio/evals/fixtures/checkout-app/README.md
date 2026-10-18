# 最小应用与业务失败对照

本fixture仅使用本地合成订单；不连接支付服务。先使用项目锁定的框架/Node/browser依赖，不自动安装或升级。此包的spec用于审查和显式运行，Skill安装不得执行它。

在本目录的独立终端启动 `node server.mjs`，执行结束后Ctrl-C关闭。端口4173仅为本fixture约定，可改server及spec一致的本地地址。

```sh
MODE=good npx wdio run wdio.conf.cjs
MODE=bug npx wdio run wdio.conf.cjs
```

good预期通过；bug保持标题Checkout却使订单pending，预期非0。timeout不更新状态，也应失败。A/B使用不同业务键；spec核对持久化金额/主体/状态并清理。3s等数值是fixture等待上限，不是产品SLO。

运行证据需另存实际框架/browser版本、命令/exit、失败产物与资源清理；静态语法检查不等同真实框架执行。

API依据：[Official documentation](https://webdriver.io/docs/async-migration).
