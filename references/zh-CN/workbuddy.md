# WorkBuddy

HOST-2

浏览器配置使用 [WorkBuddy 官方 Chrome 扩展](https://chromewebstore.google.com/detail/workbuddy/ajnnogdfpilbhkeggdjlcokgglijmdde)。先打开本机 WorkBuddy，再在使用的 Chrome 配置中安装并启用扩展；它通过 Native Messaging 连接本机客户端，不能单独使用。仅将目标标签页共享给当前任务，再执行只读验证。已装但桥接失联时，按当前客户端官方指引修复连接；未共享标签页则先完成共享；登录过期由用户登录。具体 UI 名称以当前版本界面为准，不将这三类状态合并为“缺插件”。

在独立项目中将技能目录复制到 .codebuddy/skills/portable-skill-creator，打开项目并确认技能被发现。只加载当前语言模块。使用 WorkBuddy 实际工具，不能套用 Codex 工具名或 CodeBuddy CLI 命令。浏览器扩展、Native Messaging、标签页共享和站点登录逐项验收。用户独立运行验收任务后填写 feedback.json；之前保持 untested。

[Official project configuration](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project)
