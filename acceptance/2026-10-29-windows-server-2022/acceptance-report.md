# portable-skill-creator 独立验收报告

验收时间：2026-10-29 23:30 – 23:45（UTC+8）
验收工作区：`C:\Users\admin\WorkBuddy\psc-acceptance-20261029`
验收执行者：WorkBuddy 5.9.3 会话内的 Agent（同机、同模型）

---

## 0. 结论摘要

| 问题 | 结果 |
|---|---|
| 是否成功安装 | 是。导出到 `.codebuddy/skills/portable-skill-creator`，49 个文件，结构检查通过 |
| 是否由 WorkBuddy 使用 | 部分。技能文件已由 WorkBuddy 的读取工具打开并按其指令执行了完整任务；但技能注册表层面的「自动发现」未确认（工作目录不同），需你打开验收项目后复核 |
| 是否生成可分发技能 | 是。`acceptance-note-triage`，双语、纯指令、无运行时依赖，导出到新的 recipient 目录，8 个文件 |
| 是否完成真正的新会话独立验收 | **否**。本次用的是不继承作者上下文的独立代理（新上下文、同机、同模型、同进程宿主）。真正的「新会话」提示词已备好，待你执行 |
| 浏览器路线 | **受阻**。扩展已装，原生消息宿主 `com.workbuddy.extension` 未注册，客户端桥接未连接 |
| 结算 | 12/12 单元测试通过；4 次结构检查全通过；运行时样例转换与拒绝覆盖均通过；发现 1 个 OS 门槛缺陷（已隔离复现） |

---

## 1. 环境（实际取值）

| 项 | 值 | 来源 |
|---|---|---|
| OS | **Microsoft Windows Server 2022 Datacenter**（不是 Windows 11） | `Win32_OperatingSystem.Caption` |
| 版本 / 构建号 | 10.0.**20348** | `Win32_OperatingSystem.Version` / `BuildNumber` |
| 架构 | AMD64（x64），64 位 OS | `PROCESSOR_ARCHITECTURE`, `OSArchitecture` |
| 虚拟化 | Alibaba Cloud ECS 虚拟机，AMD EPYC 9T24（8 核 / 16 线程 / 32 GB） | `Win32_ComputerSystem`, `Win32_Processor` |
| WorkBuddy | 5.9.3（exe 版本 5.9.3.0） | `WORKBUDDY_APP_VERSION`, 文件版本信息 |
| 内置 CLI | `@genie/agent-cli` 2.165.0 | `cli/package.json` |
| 模型标识 | **deepseek-v4.1-flash** | 会话运行时标识（DeepSeek-V4.1-Flash）；CLI `--model` 支持列表含 `deepseek-v4.1-flash`；本机 `~/.workbuddy/models.json` 为空，配置层未持久化 → 配置层 id 记为 unknown |
| 解释器 | `C:\Program Files\Python312\python.exe`，Python 3.12.10（MSC v.1943, 64-bit） | bootstrap 实际返回值 + `sys.version` |
| PowerShell | 7.x；执行策略 `LocalMachine = RemoteSigned`（未修改、未绕过） | `Get-ExecutionPolicy -List` |

> 与你描述的目标环境有一处实质差异：这台机器是 **Windows Server 2022（build 20348）**，不是 Windows 11。该差异直接触发了第 3 节的缺陷。

---

## 2. 仓库与安装

| 项 | 值 |
|---|---|
| 仓库 URL | `https://github.com/HNNUYUXUAN/portable-skill-creator.git` |
| 克隆位置 | `<ws>\source` |
| 分支 | `main` |
| 完整 commit SHA | `4174224ba419dffab66d4e7e3d49cc28175734a2` |
| commit 时间 | 2026-10-29T21:03:39+08:00 |
| 安装目标 | `<ws>\.codebuddy\skills\portable-skill-creator` |
| 导出前目标状态 | 不存在（`TARGET_FREE` 已核验） |
| 导出结果 | `status=exported`，`validation=structure_only`，exit 0 |
| 文件数 | 49（47 个许可文件 + `delivery.json` + `installed.json`） |
| 导出后再次 verify | `pass`，0 errors，47 files，exit 0 |

已读文档：`README.md`、`SKILL.md`、`references/zh-CN/{scope,capture,dependencies,author,acceptance,commands,workbuddy,onboard}.md`、`assets/contracts.json`、`examples/note-triage` 与 `examples/json-to-csv` 的样例说明。**未**批量加载 `references/en/*` 全量文件，仅按任务需要读取；后续英文接收者验收才读 `en` 模块。

---

## 3. 关键偏差：OS 构建号硬性门槛（真实缺陷）

### 3.1 原始版本结果（未修改仓库文件）

`scripts/bootstrap.ps1` 第 3 行：

```powershell
if ([Environment]::OSVersion.Version.Build -lt 22000) { throw 'Windows 11 or newer build required; other systems untested' }
```

三种调用都失败，全部在参数解析之前抛错：

| 调用 | 结果 |
|---|---|
| `bootstrap.ps1 -Root <ws>\runtime` | 异常：`Windows 11 or newer build required; other systems untested`，无退出码（终止性错误） |
| `bootstrap.ps1 -Root <ws>\runtime -Prepare` | 同上，证明 **`-Prepare` 无法绕过** |
| `examples/json-to-csv/scripts/bootstrap.ps1 -Prepare` | 同上（该文件与主脚本 SHA256 同为 `4506893…1c165`） |

证据：`evidence/bootstrap-original.txt`、`evidence/bootstrap-original-prepare.txt`、`evidence/sample-bootstrap-original.txt`。

影响面：Windows 10（19041–19045）、Windows Server 2019（17763）、Windows Server 2022（20348）全部无法使用该入口，即便本机已有可用 Python 3.12。

### 3.2 本地修改后结果（仅放宽该门槛）

修改文件：`<ws>\patched\scripts\bootstrap.ps1`，**只改第 3 行**，把 `throw` 换成 `Write-Warning`。差异全文见 `evidence/bootstrap-patch.diff`（1 行 -，1 行 +，无其它改动）。

```
-if (... -lt 22000) { throw 'Windows 11 or newer build required; other systems untested' }
+if (... -lt 22000) { Write-Warning ('LOCAL ACCEPTANCE PATCH: build ... gate relaxed; ...') }
```

修改后结果：

```json
{ "status": "ready", "scope": "creator_runtime_only",
  "python": "C:\\Program Files\\Python312\\python.exe", "cloud_api_called": false }
```

即：门槛之外的全部逻辑正常，自动发现并复用真实 Python 3.12.10，未下载 uv、未建私有环境、未改 PATH。证据：`evidence/bootstrap-patched.txt`。

样例侧做了同样的一行补丁（`evidence/sample-bootstrap-patch.diff`），返回同一解释器（`evidence/sample-bootstrap-patched.txt`）。

> 原始版本与修改后版本的结果**分开记录**。导出与后续所有检查都使用**未修改的仓库源码**（`source/`），补丁只用于隔离缺陷、证明门槛是唯一阻塞点，未提交到任何远端。

---

## 4. 基础检查

### 4.1 单元测试（真实执行）

```
命令: "C:\Program Files\Python312\python.exe" -B -m unittest discover -s tests -v
CWD : <ws>\source
结果: Ran 12 tests in 1.366s — OK
退出码: 0
```

覆盖：allowlist 排除秘密、非法输入不产生产物、已删除安装判冲突、路径逃逸、已有输出保留、无 workspace 导出、剪映静态模式、语言缺失、包与配对、脱敏、恢复未知状态、升级冲突与配置。
证据：`evidence/unittest-source.txt`。

### 4.2 结构检查（4 次全部 pass）

| 对象 | 结果 | 文件数 | 证据 |
|---|---|---|---|
| `source/` | pass，0 errors | 47 | `evidence/verify-source.txt` |
| 导出后的 `portable-skill-creator` | pass，0 errors | 47 | `evidence/verify-exported.txt` |
| 自建 `acceptance-note-triage`（作者侧） | pass，0 errors（首次即通过，无需修复） | 6 | `evidence/verify-authored.txt` |
| `recipient/acceptance-note-triage`（导出后） | pass，0 errors | 6 | `evidence/verify-recipient.txt` |

附加：`inspect` 对 `acceptance-note-triage` 返回 **0 findings**（无绝对路径、无脚本、无 cloud/env 引用）；导出目录 `grep` 未命中任何作者绝对路径或任务记录引用。证据：`tasks/acceptance-note-triage/inspect-skill.json`。

### 4.3 导出冲突保护（真实执行）

对同一 recipient 目录二次导出：

```
{"status": "error", "message": "Destination must be new and outside source"}
退出码: 2
```

原目录内容未被改动（再次 verify 仍 pass）。证据：`evidence/export-conflict.txt`。

### 4.4 逐项状态

| 检查项 | 状态 |
|---|---|
| 运行时是否可用 | **可用**（真实 Python 3.12.10，bootstrap 返回；但原版脚本在本 OS 上被门槛拦住，需补丁） |
| 技能目录是否安装完成 | **完成**（49 文件，结构 pass，installed.json 哈希指纹已写） |
| WorkBuddy 是否实际发现并使用 | **部分**：文件已由 WorkBuddy 工具读取并按指令执行；注册表自动发现未确认（见第 5 节） |
| 结构检查是否通过 | **通过**（4/4） |
| 行为测试通过/失败 | **通过 12 / 失败 0** |

测试通过只代表上述检查通过，**不**推断浏览器、账号或异机兼容性。

---

## 5. 技能发现状态（未完成，需你接管）

事实：

- 目标路径 `<ws>\.codebuddy\skills\portable-skill-creator` 已存在且完整，WorkBuddy 的 Read 工具可正常读取其中 `SKILL.md`、`references/zh-CN/*`。
- 本会话的工作目录是 `C:\Users\admin\WorkBuddy\2026-10-29-23-30-01`（另一个空目录），而 WorkBuddy 的项目级技能发现范围**跟随打开的工作目录**（官方文档：项目级 `.codebuddy/skills/`，「切换项目后加载结果自动跟随当前项目」）。
- 本会话可用技能列表中**没有** `portable-skill-creator`；`skill_management list` 返回空（该工具的统计口径是用户安装并启用的技能）。
- 内置 CLI 可执行 `--help`，但 `-p` 无头调用返回 `Authentication required`，无独立登录，**无法**用它起一个隔离会话。

结论：**「文件复制成功」不等于「技能已加载」**。安装完成 = 是；自动发现 = 待你打开项目后确认。操作步骤见 `HANDOFF.md` 第一节。证据：`evidence/discovery-status.txt`、`evidence/cli-probe.txt`。

---

## 6. 创建任务：acceptance-note-triage

### 6.1 任务记录（创建器 capture 阶段，真实执行）

```
creator.py session start tasks/acceptance-note-triage \
  --goal "Author bilingual acceptance-note-triage skill ... " \
  --host "WorkBuddy 5.9.3 Windows build 20348" \
  --model "deepseek-v4.1-flash"
```

会话 id `bbb0355b-7c1d-49ef-9a27-a7b3552b603d`，共 15 条事件（E1–E15），每条在动作完成后写入，未提前写 executed。检查点：`tasks/acceptance-note-triage/checkpoint.json`（15 events，unresolved = E2 failed、E7/E15 unknown）。

### 6.2 技能设计

纯指令技能，无脚本、无运行时依赖（`requirements` 只有 1 条 `host`）。

| 文件 | 字节 | 作用 |
|---|---|---|
| `SKILL.md` | 974 | 入口：一句话能力 + 中英双链接 |
| `references/zh-CN/task.md` | 1697 | 中文规则，TRIAGE-1…13 |
| `references/en/task.md` | 1845 | 英文规则，TRIAGE-1…13（步骤 ID 与中文一一对应） |
| `references/zh-CN/acceptance.md` | 877 | 中文验收说明，ACC-1…6 |
| `references/en/acceptance.md` | 1070 | 英文验收说明，ACC-1…6 |
| `examples/input.txt` | 117 | 原始输入样例 |
| `delivery.json` | 503 | 分发清单 |

规则要点（与你的要求逐条对应）：

- 只按**行首**标记分类：`TODO:`/`DONE:`/`BLOCKED:`，位置必须是第 1 个字符，全大写 + 半角冒号；`todo:`、`TODO :`、前导空格等一律 `UNMARKED`（TRIAGE-6）。
- 不按语义推断，不改写原文（TRIAGE-7、TRIAGE-8），组内保持输入顺序（TRIAGE-9）。
- 空行不是条目，跳过且不计数（TRIAGE-10）。
- 输出 Markdown，四个二级标题 `## TODO (n)` / `## DONE (n)` / `## BLOCKED (n)` / `## UNMARKED (n)`，`- ` 列表，空组写 `(0)` 与 `- （无条目）`（TRIAGE-11…13）。
- 双语等价：同步骤 ID、同命令、同验收规则，入口按需选语言。

### 6.3 导出与哈希

导出到 `recipient/acceptance-note-triage`（目标原本不存在），8 个文件：

```
758092a6f1822cab627997face4c4e101f9c53e425693369a01f044245fabb11   974  SKILL.md
31adf944ff3774a915217d95108cbb204c0a0f14152fcc6bf8b9fb7df3639371   503  delivery.json
258d9e8af60b260d165251fa34c9e792f1bc158c1749f963091398e54d74b6eb   117  examples/input.txt
ae4268398d86fd326b91993244b3a2ec3c28144b80e058f5639bdcd9bdebcc01   662  installed.json
8c0323100334c3887cc710d01f7ced32e1ced725dc1505884e14095802c69f5b  1070  references/en/acceptance.md
95599f6e1e7b4a2b6e1e880979f1e05bd7ab9489d89cb5bc7d3fcf6ce6a91618  1845  references/en/task.md
2d73af0e8786f3af866cf0e050a8c2e04dde538c23c2c615afa64e210950c4f3   877  references/zh-CN/acceptance.md
26bfece9f37d191b3b5de15d4763829b3fe5478eff95943b88fc3a8155a059d0  1697  references/zh-CN/task.md
```

证据：`evidence/recipient-manifest.txt`、`evidence/export-recipient.txt`。
未装入生成技能的内容：本次任务记录（`tasks/`）、作者绝对路径、`acceptance-report.md`、任何私人配置。已用 grep 核验（0 命中）。

---

## 7. 独立接收者验收

### 7.1 执行方式（重要限定）

**不是**「新会话独立验收」。本次由两个**不继承作者上下文**的独立代理执行：新上下文、不含本对话历史、只拿到「技能目录 + 输入 + 任务要求」三项。同机、同模型、同宿主进程。

真正的 WorkBuddy 新会话验收**待你执行**，提示词已备好（`HANDOFF.md` 第二节，含技能路径与输入路径）。我没有把同一会话的自检称作独立验收。

### 7.2 结果（中文 / 英文各一次，同一输入）

| 组 | 期望条数 | 中文结果 | 英文结果 |
|---|---|---|---|
| TODO | 2 | 2 ✅ | 2 ✅ |
| DONE | 2 | 2 ✅ | 2 ✅ |
| BLOCKED | 1 | 1 ✅ | 1 ✅ |
| UNMARKED | 1 | 1 ✅ | 1 ✅ |
| 合计 | 6 | 6 = 非空行数 6 ✅ | 6 = 非空行数 6 ✅ |

检查维度（由验收方脚本 `tasks/acceptance-note-triage/checker.py` 机械核对，非模型自评）：标题顺序、每组条目**逐字符**与输入行一致、组内顺序、括号内计数、总数与非空行数一致。两份结果 `ok=true`，退出码 0。
证据：`evidence/check-zh.json`、`evidence/check-en.json`、`runs/zh/result-zh.md`、`runs/en/result-en.md`。

注意：两组都正确地没有把「稍后确认付款」按语义猜成 TODO/BLOCKED，而是放进 `UNMARKED` —— 这正是「不推断」要求的判定点。

### 7.3 语言模块读取记录

| 接收者 | 自报读取的文件 |
|---|---|
| 中文 | `SKILL.md`、`references/zh-CN/task.md`、`references/zh-CN/acceptance.md` |
| 英文 | `SKILL.md`、`references/en/task.md`、`references/en/acceptance.md` |

这是接收者的自报，**无法**从宿主侧交叉验证（未获取文件访问审计日志）。因此「实际读取了哪些模块」只能记为「接收者自报」，不能记为「已审计」。

---

## 8. 运行环境样例 A：examples/json-to-csv

目录（含中文与空格）：`<ws>\samples\样例 目录 空格测试\json-to-csv`

| 步骤 | 命令 / 动作 | 结果 |
|---|---|---|
| 环境准备 | `bootstrap.ps1 -Prepare`（原版） | 被 OS 门槛拦住（见 3.1） |
| 环境准备 | 同一行补丁后 `-Prepare` | `status=ready`，`python=C:\Program Files\Python312\python.exe` |
| 转换 | `"C:\Program Files\Python312\python.exe" scripts/convert.py examples/input.json "out/结果 输出.csv"`（CWD = 技能根） | exit 0，生成 UTF-8 CSV（CRLF） |
| CSV 解析核对 | `csv.DictReader` | 数据行 2；字段 `['name','count']`；`中文, item` → 2；`second` → 0；含逗号字段往返一致（原始字节为 `"中文, item",2`） |
| 拒绝覆盖 | 同参数再跑一次 | exit 2，`Output already exists; choose a new output path. Existing file preserved.`；前后 SHA256 同为 `e1ddb65…12aa`，文件未变 |

实际解释器：`C:\Program Files\Python312\python.exe`（3.12.10）。
证据：`evidence/sample-bootstrap-patched.txt`、`evidence/sample-convert.txt`、`evidence/sample-parse.txt`、`evidence/sample-overwrite-refusal.txt`。

---

## 9. 浏览器样例 B：examples/page-evidence（受阻）

逐层判定，不合并成「缺插件」：

| 层 | 状态 | 依据 |
|---|---|---|
| 扩展是否安装 | **是** | Chrome `Default\Extensions\ajnnogdfpilbhkeggdjlcokgglijmdde\0.2.7_0`，manifest `name=WorkBuddy version=0.2.7`，含 `nativeMessaging` 权限 |
| 客户端桥接是否连接 | **否** | 扩展 `connectNative("com.workbuddy.extension")`；该宿主在 HKCU/HKLM Chrome 与 HKCU Edge 的 `NativeMessagingHosts` 下**都未注册**，磁盘上也找不到 `com.workbuddy.extension.json`。已注册的宿主只有金山、BrowserCore、OpenAI codex、夸克、FDM |
| 目标标签页是否共享 | **未知** | 本会话无浏览器控制工具/技能，无法发起共享或读取共享状态 |
| 页面是否可读 | **未测** | 阻断在前一层 |

因此：`https://agentskills.io/home` 的**最终 URL、页面标题、页面事实、读取时间一律记为 unknown**，没有用搜索结果或文本抓取替代浏览器读取。

补充（明确**不计入**浏览器验收）：一次普通 HTTP 文本抓取返回标题 `Agent Skills Overview - Agent Skills`，仅用于证明该页从本机网络可达。它不是通过 WorkBuddy 连接的浏览器读取。

配置步骤（详见 `HANDOFF.md` 第三节 / `evidence/browser-status.txt`）：设置 → Agent → 浏览器控制 → 打开；重启客户端与 Chrome；`chrome://extensions` 确认无报错；只共享目标标签页；再执行只读验证。

未安装其它浏览器，未修改全局浏览器配置。公共页面即便读取成功，也不代表账号登录或机构访问权限已验证。

---

## 10. 证据等级标记

| 类型 | 本次是否完成 | 说明与依据 |
|---|---|---|
| 真实执行 | **是** | 克隆、bootstrap（原版失败 + 补丁成功）、4 次 verify、12 项 unittest、两次 export、冲突保护、CSV 转换与覆盖拒绝，均在本机实际运行并留证 |
| 静态检查 | **是** | `verify` 属结构检查；`inspect` 属启发式依赖扫描（0 findings）；两者都不证明语义等价或功能可用 |
| 模拟场景 | **是** | `acceptance-note-triage` 用固定 6 行样例验收，属模拟场景；真实业务文本未测 |
| 同机重定位 | **是** | 技能从 `skills-src/` 导出到 `recipient/`（不同路径、新目录）后仍可直接使用，结构检查与行为结果一致 |
| 新会话独立验收 | **否（待你操作）** | 本次为独立代理（新上下文）而非 WorkBuddy 新会话；提示词已备好 |
| 干净系统或异机验收 | **否** | 全部在同一台 Windows Server 2022 虚拟机、同一 WorkBuddy、同一模型上完成。**不得**称为异机或干净系统验收 |

---

## 11. 失败项、未完成项与复现步骤

| 项 | 状态 | 复现 / 说明 |
|---|---|---|
| 原版 `bootstrap.ps1` 在本机不可用 | **失败（上游缺陷）** | `& <ws>\source\scripts\bootstrap.ps1 -Root <ws>\runtime` → throw；加 `-Prepare`、加 `-Python` 同样失败。根因：build 20348 < 22000 |
| 技能注册表自动发现 | **未确认（待你操作）** | 工作目录不同；`skill_management list` 为空；本会话技能列表无此技能 |
| 新会话独立验收 | **未执行** | 内置 CLI `-p` 需独立登录（`Authentication required`），我无法自行开隔离会话 |
| 浏览器页面读取 | **受阻** | 原生消息宿主未注册；无浏览器控制工具 |
| 英文模块实际读取审计 | **无法确认** | 仅接收者自报 |
| 账号登录 / 机构权限 | **未验证** | 不在本次范围，且公共页面成功也不代表它 |
| 模型标识（配置层） | **unknown** | `~/.workbuddy/models.json` 为空；以运行时标识与 CLI 支持列表为据 |

---

## 12. 缺陷与修复建议（未提交到 GitHub）

**缺陷**：`scripts/bootstrap.ps1` 把 Windows 构建号当作硬性闸门（`throw`），与「运行时检测」职责不匹配；对 Windows 10 / Server 2019 / Server 2022 造成完全不可用，即使 Python 3.12 已就绪。

**复现**：在 build < 22000 的 Windows 上执行 `bootstrap.ps1`（任意参数组合）。

**建议**（任选其一）：

1. 降级为警告并在返回 JSON 增加 `os_support: "untested"`，由调用方决定是否继续；
2. 增加显式开关如 `-AllowUnsupportedOS`，保持默认行为不变；
3. 若坚持硬门槛，至少在 README「验证与适用范围」中列出受影响的 Windows 版本与可用的绕行方式（当前 README 只写「Windows 11 / Codex 有本机证据」，未提示这是硬失败）。

原始证据保留在 `evidence/bootstrap-original*.txt`；本地补丁（1 行）在 `evidence/bootstrap-patch.diff`。未向 GitHub 提交或发布任何内容。

---

## 13. 文件索引

| 路径 | 内容 |
|---|---|
| `<ws>\.codebuddy\skills\portable-skill-creator` | 安装的技能（49 文件） |
| `<ws>\recipient\acceptance-note-triage` | 可分发的新技能（8 文件） |
| `<ws>\runs\zh\result-zh.md`、`runs\en\result-en.md` | 两次接收者输出 |
| `<ws>\tasks\acceptance-note-triage` | 创建器任务记录（session.json / events.jsonl / checkpoint.json / checker.py / inspect-skill.json） |
| `<ws>\evidence\*` | 全部命令输出、diff、哈希清单、浏览器状态 |
| `<ws>\HANDOFF.md` | 需要你操作的步骤（发现技能、新会话验收、浏览器） |
| `<ws>\acceptance-results.json` | 机器可读结果 |
