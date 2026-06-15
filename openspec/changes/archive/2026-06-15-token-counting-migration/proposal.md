## Why

当前 `partition_batches.py` 和 `quality_gate.py` 使用 Python `len()` 统计字符数作为批次划分和偷懒检测的基准。中英文在 token 密度上差异悬殊（同一文本量下中文 token 数约为英文的 8.8 倍），导致混合语言场景下 batch 划分不均匀、质量门禁的翻译长度比阈值实际效果随语言方向漂移。

引入 `tiktoken.cl100k_base` 做精确 token 计数替代 `len()` 字符计数，使两种语言在同一套度量下得到公平衡量。

## What Changes

- `scripts/partition_batches.py`：所有字符计数替换为 token 计数（`len()` → `_count_tokens()`）；输出字段名 `total_chars` → `total_tokens`，`target_size_chars` → `target_size_tokens`
- `scripts/quality_gate.py`：所有字符计数替换为 token 计数；常量重命名 `MIN_CHAR_RATIO` → `MIN_TOKEN_RATIO`、`MAX_CHAR_RATIO` → `MAX_TOKEN_RATIO`（阈值 0.3–3.0 不变）；输出字段名 `original_chars`/`translated_chars` → `original_tokens`/`translated_tokens`
- 同步更新所有引用"字符"概念的相关文档（`SKILL.md`、`references/stage-playbook.md`、`references/payload-contracts.md`、`AGENTS.md`）

## Capabilities

### New Capabilities
<!-- None - this is a refinement of existing capabilities -->

### Modified Capabilities
- `literature-translator`:
  - Requirement "Translation batch partitioning": 批次划分基准从字符数改为 token 数，默认目标大小从 1500 字符改为 1500 token
  - Requirement "Translation execution with quality gate": lazy_translation 检查的原文/译文长度比计算从字符级改为 token 级；输出字段名变更为 `original_tokens`/`translated_tokens`
  - Requirement "Stdout JSON contract / Payload contracts": Batch schema 和 Quality Gate schema 中相关字段重命名

## Impact

- `scripts/partition_batches.py`：新增 `tiktoken` 依赖；引入 `_count_tokens()` 惰性单例编码器；5 处 `len()` 替换；10+ 字段重命名
- `scripts/quality_gate.py`：同上模式；`check_lazy_translation()` 和 `check_length_by_type()` 中的计数替换；常量重命名
- `SKILL.md`：4 处"字符→token"文本更新
- `references/stage-playbook.md`：1 处更新（默认 batch size 描述）
- `references/payload-contracts.md`：Batch schema 和 Quality Gate schema 中的字段名更新
- `AGENTS.md`：2 处"字符→token"文本更新
