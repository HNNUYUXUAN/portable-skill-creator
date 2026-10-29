---
name: portable-skill-creator
description: Create distributable bilingual skills, capture task evidence, audit dependencies and guide recipient setup. 创建可分发双语技能、记录任务、审计依赖并引导接收端配置。
---
# Portable Skill Creator / 可分发技能创建器

Windows 11 x64 first. Model-independent core; Codex first, WorkBuddy recipient validation pending.
优先 Windows 11 x64；核心不绑定模型；先验收 Codex，再由接收者验证 WorkBuddy。

Select one language from explicit user preference, otherwise conversation language. Read only the current phase and required host guide. / 选一种语言，仅按需读取当前阶段与宿主说明。
Resolve this directory before running scripts. Use `scripts/bootstrap.ps1` to discover/prepare Python 3.12, then that interpreter with `scripts/creator.py --help`.
先定位技能根；用 bootstrap 查找或准备解释器，再运行辅助入口。

| Phase / 阶段 | 中文 | English |
|---|---|---|
| scope | [scope](references/zh-CN/scope.md) | [scope](references/en/scope.md) |
| capture | [capture](references/zh-CN/capture.md) | [capture](references/en/capture.md) |
| dependencies | [dependencies](references/zh-CN/dependencies.md) | [dependencies](references/en/dependencies.md) |
| author | [author](references/zh-CN/author.md) | [author](references/en/author.md) |
| onboard | [onboard](references/zh-CN/onboard.md) | [onboard](references/en/onboard.md) |
| acceptance | [acceptance](references/zh-CN/acceptance.md) | [acceptance](references/en/acceptance.md) |
| update | [update](references/zh-CN/update.md) | [update](references/en/update.md) |
| Codex | [宿主](references/zh-CN/codex.md) | [Host](references/en/codex.md) |
| WorkBuddy | [宿主](references/zh-CN/workbuddy.md) | [Host](references/en/workbuddy.md) |
| CLI | [命令](references/zh-CN/commands.md) | [Commands](references/en/commands.md) |

Start with scope; capture during work; audit dependencies before authoring; onboard and validate before claiming usability. Improve an existing skill in a copy.
先定范围，执行时记录，审计后编写，接收端检查与验收后再声明可用；改造已有技能使用副本。

Record observable evidence only. Never infer success from installation, key presence or prose. Unknown stays unknown. Keep secrets out of events and exports.
只记录可观察证据；安装、Key 存在和文字说明不代表成功；未知保持未知；秘密不进入记录及交付。

Deliver ordinary directories. No background recorder or model API is required.
默认普通目录交付；不依赖后台记录器或模型 API。
