# WorkBuddy

HOST-2

Use the [official WorkBuddy Chrome extension](https://chromewebstore.google.com/detail/workbuddy/ajnnogdfpilbhkeggdjlcokgglijmdde). Start local WorkBuddy, then install/enable the extension in the intended Chrome profile. It requires a Native Messaging connection to the local client and cannot run alone. Share only the intended tab with this task, then perform a read-only check. For a disconnected bridge follow the current client guidance; for an unshared tab enable sharing; for expired login let the recipient sign in. UI labels depend on the installed version. Keep these failure states separate.

In an isolated project copy the skill to .codebuddy/skills/portable-skill-creator, open the project and confirm discovery. Load one language. Use actual WorkBuddy tools, not Codex tool names or assumed CodeBuddy CLI commands. Verify extension, Native Messaging, tab sharing and login separately. Recipient fills feedback.json after independent tasks; status remains untested until then.

[Official project configuration](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project)
