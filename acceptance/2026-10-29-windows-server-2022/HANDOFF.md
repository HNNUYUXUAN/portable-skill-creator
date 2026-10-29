# 需要你操作的步骤（复制即用）

本文件保存当前进度与需要人工接管的步骤。当前所有已执行项目已落盘，工作区可安全关闭或重开。

验收工作区：`C:\Users\admin\WorkBuddy\psc-acceptance-20261029`

---

## 一、在 WorkBuddy 中让技能被发现（待你操作）

已安装的技能目录（结构检查已通过，可供任何宿主读取）：

```
C:\Users\admin\WorkBuddy\psc-acceptance-20261029\.codebuddy\skills\portable-skill-creator
```

WorkBuddy 的项目级技能目录是 `<工作目录>/.codebuddy/skills/`，**发现范围跟随当前打开的工作目录**。本次会话的工作目录是另一个空目录，所以注册表层面尚未加载它（这不是文件复制失败）。

请按以下顺序操作：

1. 在 WorkBuddy 新建任务时把工作目录设为 `C:\Users\admin\WorkBuddy\psc-acceptance-20261029`（或直接用 WorkBuddy 打开该文件夹）。
2. 在新会话里查看技能列表，应出现 `portable-skill-creator`。
3. 若列表未刷新：关闭该任务会话再新建一次；仍无则重启客户端后再试。

完成后请把「技能列表里是否出现 portable-skill-creator」的结果告诉我。

---

## 二、真正的新会话独立验收（待你操作）

同一个技能，把下面整段复制到一个**新会话**（工作目录仍设为上面的验收工作区，或直接打开 `recipient` 目录）。这段提示词只给接收者必要信息，不含生成过程与预期答案。

```
你是这次任务的接收者。你只获得三样东西：

1. 一个技能目录：
C:\Users\admin\WorkBuddy\psc-acceptance-20261029\recipient\acceptance-note-triage
2. 一份输入文件：
C:\Users\admin\WorkBuddy\psc-acceptance-20261029\recipient-input.txt
3. 任务要求：使用这个技能处理输入并保存结果。

要求：
- 先读技能目录里的 SKILL.md，按它的指引选择一种语言，只读该语言的模块，然后严格按技能规则处理输入。
- 只读技能目录内的文件和上面的输入文件，不要读其它文件，不要联网。
- 结果保存为：C:\Users\admin\WorkBuddy\psc-acceptance-20261029\runs\new-session\result.md
- 不要反问，直接完成。

完成后用 4-8 行说明：(a) 你读了技能里的哪些文件（相对路径）；(b) 结果文件路径；(c) 是否用到脚本或依赖；(d) 你按哪条规则归类最后一行。
```

英文版（同一输入，验证中英文规则一致）：

```
You are the recipient of this task. You only get three things:

1. A skill directory:
C:\Users\admin\WorkBuddy\psc-acceptance-20261029\recipient\acceptance-note-triage
2. An input file:
C:\Users\admin\WorkBuddy\psc-acceptance-20261029\recipient-input.txt
3. Task: use this skill to process the input and save the result.

Constraints:
- Read SKILL.md first, follow its routing to pick a language, read only that module, apply the rules exactly.
- Read only files inside the skill directory plus the input file. No web access.
- Save the result to: C:\Users\admin\WorkBuddy\psc-acceptance-20261029\runs\new-session-en\result.md
- Do not ask questions; just finish.

Then answer in 4-8 lines: (a) files you read inside the skill; (b) result path; (c) any script or dependency used; (d) the rule you used for the last line.
```

---

## 三、浏览器样例（待你操作）

当前状态：Chrome 里 WorkBuddy 扩展 0.2.7 已安装，但原生消息宿主 `com.workbuddy.extension` 未注册，客户端桥接未连接；目标标签页也未共享。因此 `https://agentskills.io/home` 的浏览器读取**未完成**。

请依次：

1. WorkBuddy → 设置 → Agent → 浏览器控制 → 打开（这一步会写入原生消息宿主注册）。
2. 重启 WorkBuddy 客户端，然后完全退出并重启 Chrome（原生宿主只在浏览器启动时读取）。
3. `chrome://extensions` 确认 WorkBuddy 0.2.7 已启用、服务工作线程无报错；若仍连不上，从官方 Chrome 应用商店卸载后重装，再重复第 2 步。
4. 打开 `https://agentskills.io/home`，只把该标签页共享给当前任务。
5. 再执行页面读取，记录最终 URL、标题、一条可直接核对的事实、读取时间。

详细的检查证据见 `evidence/browser-status.txt`。未安装其它浏览器，未修改全局浏览器配置。

---

## 四、已知缺陷（需要上游修复，不由我提交）

`scripts/bootstrap.ps1` 第 3 行硬性要求 `OSVersion.Version.Build >= 22000`。本机是 Windows Server 2022（build 20348），脚本在任何参数下都直接抛错退出，`-Prepare`、`-Python` 都不能绕过，尽管本机已有可用的 Python 3.12.10。

影响：Windows 10（19041–19045）、Windows Server 2019/2022 全部无法使用该环境检测入口，即使解释器完全可用。

建议：把硬性 throw 改为「构建号低于基线时输出 warning 并继续，同时在返回 JSON 里加 `os_support: "untested"` 字段」，让调用方自行决定是否继续；或增加 `-AllowUnsupportedOS` 开关。原始复现证据见 `evidence/bootstrap-original.txt`，本地对照补丁见 `evidence/bootstrap-patch.diff`（未推送到任何远端）。
