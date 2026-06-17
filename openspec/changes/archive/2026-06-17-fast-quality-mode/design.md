## Context

当前 skill 有且仅有一条完整精翻路径。在实际使用中，用户有时只需要快速概览文献内容，不需要句级精翻 + 占位符保护 + 结构化审查的全套流程。需要新增一个模式参数让用户在"快"和"精"之间选择。

约束：不改动现有句级精翻脚本（sentencify/protect/restore）；不改变 partition_batches.py / concatenate.py 的输入格式；fast 模式的产物必须与 high_quality 结构兼容以保持下游 skill 可用。

## Goals / Non-Goals

**Goals:**
- 新增 `mode` 参数，fast（默认）和 high_quality 两种模式
- fast 模式跳过句级拆分、占位符保护/还原、结构化 reviewer/局部修复
- fast 模式复用现有批处理、质量门禁、拼接、导出脚本
- fast 模式产出与 high_quality 结构兼容的产物（alignment 空 pairs）

**Non-Goals:**
- 不修改 sentencify.py / protect_placeholders.py / restore_placeholders.py
- 不修改 partition_batches.py / concatenate.py
- 不给 fast 模式单独定义不同的品质阈值
- 不在 fast 模式下给 translation/review/repair 增加 subagent 委派

## Decisions

### Decision 1: 每 block 1 sentence（而非改动 partition_batches.py）

- **Chosen**: 新增 `build_block_sentences.py`，将每个 block 整体作为 1 sentence 生成 v2 sentences.json
- **Alternatives**: 修改 partition_batches.py 直接消费 blocked.md
- **Rationale**: 复用现有 partition_batches.py / batch payload 格式 / quality_gate 全部不变。下游脚本无需感知 mode 差异。修改集中在"生成什么 sentences.json"这一个点上。
- **Trade-off**: 块级内容可被非常大（几千 token），单个 "sentence" 会形成大 batch。但 partition_batches.py 的 greedy 算法自动处理大块。

### Decision 2: quality_gate 跳过 placeholder/numeric 而非放松阈值

- **Chosen**: fast 模式下 placeholder_preservation 和 numeric_preservation 返回 `{"passed": true, "skipped": true}`，其余检查阈值不变
- **Alternatives**: 保留 8 项检查但放宽阈值
- **Rationale**: fast 模式没有 placeholder_map 输入，placeholder/numeric 检查无数据源，跳过是唯一正确选择。其余检查（sentence_count、lazy_translation、term_consistency、language、non_translation_phrases、length_check）的输入都存在，阈值不变是合理的。
- **Trade-off**: 无。

### Decision 3: 主 agent 块级速览替代 structured reviewer

- **Chosen**: fast 模式下主 agent 通读所有块，检查漏翻/严重误译/总结式翻译
- **Alternatives**: 仍然委派 structured reviewer（每 block 1 pair）
- **Rationale**: fast 模式的价值在于"快"，块级速览已经足够捕获严重问题。structured reviewer 的 10 种错误分类对块级原文/译文 pair 的效用有限（块内可能包含数十句混合内容）。
- **Trade-off**: 可能遗漏 subtle 语义错误（modality/polarity），这是速度换精度的 trade-off。

### Decision 4: alignment 空 pairs 保持格式兼容

- **Chosen**: fast 模式 alignment 输出 `"pairs": []`，同步填充 source_markdown / translated_markdown
- **Rationale**: 下游 literature-deep-reading skill 期望 alignment 有一定格式契约。空 pairs + 块级原文/译文文本保证下游可以降级工作，不会报 JSON parse error。
- **Trade-off**: 下游 skill 需要处理空 pairs 的情况（这在下游已经约定）。

## Risks / Trade-offs

- **fast 模式翻译质量降低** → 预期行为。fast 对块的翻译更可能出现细节丢失（相比句级精翻），但这对"快速概览"的使用场景是可接受的。
- **块级内容超长导致 batch 过大** → partition_batches.py 自动将超大块独立成 batch，不会撑破上下文。
- **mode 参数遗漏导致错误** → default 为 fast 是保守选择（不阻塞），用户若需要精翻明确指定 high_quality。
