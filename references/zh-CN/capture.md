# capture

CAP-1

任务开始时读取；已有任务只能记录可获得的证据。先运行 session start；每个关键工具结果、外部请求提交和阶段结束后追加事件。只允许 step/status/summary/evidence/next/request_id 字段；status 为 planned、executed、failed、unknown。事件文件使用脱敏内容，不保存原始敏感输出。

完成动作后写 executed，不能提前写。evidence 指向必要的本地产物或核验记录；记录文件哈希、工具及实际版本，不记录密钥。命令中的凭据和签名 URL 在传给记录器前移除。记录器的过滤只是第二层保护。

中断后执行 session resume。逐项检查 unresolved 与已生成文件；外部请求结果未知时先查询状态，不能盲目重发。历史不确定事件保留；用后续事件写明调查结果。session finish 会保留 finished_with_gaps，人工审计后在验收报告说明已解决项。普通 Skill 无法截获其他聊天或所有进程。完成标准：依赖、产物、失败与证据缺口均有记录。
