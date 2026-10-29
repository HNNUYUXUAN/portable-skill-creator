# Task

DEMO-1

Run PYTHON scripts/convert.py INPUT OUTPUT from this skill root; replace PYTHON with the executable returned by bootstrap. Input is an object array; each object has only name and count, with string name and nonnegative integer count, excluding booleans. Write UTF-8 CSV. Refuse existing outputs and validate all input first.

Run scripts/bootstrap.ps1 -Prepare to discover/create Python 3.12; use the returned executable. / 先运行 scripts/bootstrap.ps1 -Prepare，使用返回的解释器执行转换。
