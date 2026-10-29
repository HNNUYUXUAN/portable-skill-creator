# Task

DEMO-1

从技能根运行 PYTHON scripts/convert.py INPUT OUTPUT，其中 PYTHON 替换为 bootstrap 返回的解释器路径；输入是对象数组，每项必须仅有 name 和 count，name 为字符串，count 为非负整数且不是布尔值。输出 UTF-8 CSV。拒绝覆盖已有输出，先完整验证所有输入。

Run scripts/bootstrap.ps1 -Prepare to discover/create Python 3.12; use the returned executable. / 先运行 scripts/bootstrap.ps1 -Prepare，使用返回的解释器执行转换。
