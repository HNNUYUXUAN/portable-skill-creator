# author

WRITE-1

依赖已整理后读取。按用户任务写可执行规则，保留实际输入输出约束和失败恢复。使用短 SKILL.md 路由到所选语言模块。创建器与产物都提供 zh-CN/en；显式语言要求优先，否则跟随会话。两种语言保持相同步骤 ID、命令、状态和验收规则。

入口最多 4096 字节，语言模块最多 8192 字节；当前阶段只读相关模块。脚本承担确定性转换和检查，模型负责理解与提炼。命令从技能根运行或使用解析出的绝对脚本路径，禁止假定调用者当前目录。

生成 delivery.json，schema_version=1，name/version/files/requirements；files 为明确相对路径列表，不含 delivery.json 本身或 installed.json。requirements 每项含 id/kind/handling，可带 probe。参考 examples 的三种成品；不要把示例任务限制复制成所有技能的限制。完成后运行 verify，修复结构问题，再独立执行真实任务。verify 不证明语义等价或功能可用。
