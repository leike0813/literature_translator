## 1. Batch partitioning 脚本改造

- [x] 1.1 在 `scripts/partition_batches.py` 中引入 `tiktoken`，实现 `_count_tokens()` 惰性单例编码器
- [x] 1.2 `calculate_block_sizes()` 中把所有 `len()` 替换为 `_count_tokens()`；`total_chars` → `total_tokens`
- [x] 1.3 `partition()` 中 `current_chars` → `current_tokens`，`char_count` → `token_count`；manifest 和统计输出中所有 `_chars` → `_tokens`
- [x] 1.4 更新 CLI help：`"Target batch size in characters"` → `"Target batch size in tokens"`

## 2. Quality gate 脚本改造

- [x] 2.1 在 `scripts/quality_gate.py` 中引入 `tiktoken`，实现 `_count_tokens()`；常量 `MIN_CHAR_RATIO`/`MAX_CHAR_RATIO` → `MIN_TOKEN_RATIO`/`MAX_TOKEN_RATIO`（值不变）
- [x] 2.2 `check_lazy_translation()` 中 `len()` → `_count_tokens()`；输出字段 `original_chars`/`translated_chars` → `original_tokens`/`translated_tokens`
- [x] 2.3 `check_length_by_type()` 中 `len(text_trans) / max(len(text_orig), 1)` → `_count_tokens()` 版本
- [x] 2.4 修复 pre-existing bug：补上 `all_translated_text` 变量的未定义缺失

## 3. 文档同步

- [x] 3.1 更新 `SKILL.md`：4 处"字符→token"（batch size、长度比、阈值、entrypoint 说明）
- [x] 3.2 更新 `references/stage-playbook.md`：默认 batch size 描述字符→token
- [x] 3.3 更新 `references/payload-contracts.md`：Batch 和 Quality Gate schema 中的字段重命名
- [x] 3.4 更新 `AGENTS.md`：字符阈值→token 阈值、字符级长度→token 级长度

## 4. 验证

- [x] 4.1 `_count_tokens()` 单元行为验证（中英文 token 密度差异确认）
- [x] 4.2 `pipeline_test.py` 回归测试通过：1/1 passed（261 blocks, 1237 sentences）
- [x] 4.3 `partition_batches.py` 真实数据验证：49321 tokens → 30 batches，字段名均为 `_tokens`
- [x] 4.4 `quality_gate.py` mock 验证：正常翻译（ratio=1.58）通过，偷懒翻译（ratio=0.29）拦截
