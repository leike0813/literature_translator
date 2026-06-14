## Why

项目 AGENTS.md 中定义了文献翻译 Agent Skill 的宏观需求，但缺乏可被 LLM 直接执行的可操作指令。需要将宏观需求转化为符合 Open Agent Skills 规范的完整 Skill 包，包含可执行的核心指令、确定性脚本、明细参考文档和输入 schema。

## What Changes

- 新建 `literature-translator/` 目录，创建符合 Open Agent Skills 规范的完整 Skill 包
- 编写 `SKILL.md`：10 阶段执行流程（环境分析→输入解析→宏观分析→块级拆分→句级拆分→批次分割→翻译执行+质量门禁→主 Agent 复核→译文拼接→最终润色）
- 编写 3 份 reference 文档：`stage-playbook.md`、`payload-contracts.md`、`subagent-protocol.md`
- 编写 5 个 Python 脚本：`parse_input.py`、`sentencify.py`、`partition_batches.py`、`quality_gate.py`、`concatenate.py`
- 编写 JSON schema：`assets/input.schema.json`

## Capabilities

### New Capabilities

- `literature-translator`: 将学术文献（Markdown/PDF/LaTeX）从源语言高质量翻译为目标语言的 Agent Skill，支持术语表管理、块级+句级拆分、subagent 委派翻译、质量门禁和自动拼接

### Modified Capabilities

- （无）

## Impact

- `literature-translator/SKILL.md`: 核心指令文件，定义完整执行流程和约束
- `literature-translator/references/stage-playbook.md`: 各阶段操作细则
- `literature-translator/references/payload-contracts.md`: 所有脚本的 I/O schema
- `literature-translator/references/subagent-protocol.md`: Subagent 委派协议
- `literature-translator/scripts/parse_input.py`: 输入类型检测与规范化
- `literature-translator/scripts/sentencify.py`: 句级拆分
- `literature-translator/scripts/partition_batches.py`: 翻译批次均衡分区
- `literature-translator/scripts/quality_gate.py`: 翻译质量门禁（句数/偷懒/术语/语言校验）
- `literature-translator/scripts/concatenate.py`: 译文拼接
- `literature-translator/assets/input.schema.json`: 输入 payload JSON schema
- `AGENTS.md`: 项目级 AGENTS 文件（被 skill 实现覆盖）
