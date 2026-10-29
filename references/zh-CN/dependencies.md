# dependencies

DEP-1

已有源码或任务记录时读取。运行 inspect，将报告保存到任务目录。检查脚本导入、外部进程、引用文件、模板、工作区规则、字体、桌面应用、浏览器、账号和用户输入。扫描器是启发式检查，不能证明发现所有依赖。逐条确认 findings，并检查动态导入与运行时生成路径。

为每个必要依赖填 id、kind、handling；kind 仅用 bundle/rebuild/host/configure/input/unsupported。分别标明 observed/static/declared/unknown 和是否实测。bundle 必须有合法来源、相对路径及发布文件清单；rebuild 需提供目标平台锁与可执行重建入口；configure 写明代码真实读取位置和优先级。

剪映案例须核对固定 D 盘、dotenv_values 专用配置、win-64 锁、videoeditor.dll、doctor 未调用 API；不从 Python 推断 Mac 草稿编辑可用。许可不明的资源列待解决，不直接复制。完成标准：每个发现项有处理方式或明确缺口。
