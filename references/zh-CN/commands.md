# CLI

CLI-1

以下命令从技能根执行，PYTHON 替换为 bootstrap 返回的可执行路径。任务目录必须位于发布目录外。

```text
PYTHON scripts/creator.py session start TASK --goal GOAL --host HOST --model MODEL
PYTHON scripts/creator.py session record TASK --event EVENT.json
PYTHON scripts/creator.py session resume TASK
PYTHON scripts/creator.py session finish TASK
PYTHON scripts/creator.py inspect SKILL --out REPORT.json
PYTHON scripts/creator.py doctor SKILL --out CHECKS.json
PYTHON scripts/creator.py verify SKILL
PYTHON scripts/creator.py export SKILL NEW_DIR
PYTHON scripts/creator.py upgrade SKILL INSTALLED_DIR
PYTHON scripts/creator.py rollback INSTALLED_DIR
```

事件示例；输入文件也必须先脱敏。unknown 结果不可自动重发。

```json
{"step":"CAP-1","status":"executed","summary":"Read declared dependencies","evidence":"report.json; sha256 recorded separately","next":"Review dynamic references"}
```

doctor 的 probe 只支持 env_present/name 与 command/name；二者都不能证明服务有效。返回码：0 操作完成，1 结构失败或更新冲突，2 输入或操作错误。bootstrap 缺环境返回3。
