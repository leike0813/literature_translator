## Context

一次 `high_quality` 模式真 run（SAM 2 论文，41 batch，bailian/qwen3.7-plus）暴露了质量门禁循环的系统脆弱性：

- **batch_0000**: 第1次 term_consistency 失败 → 第2次 placeholder_preservation 失败 → 第3次通过
- **batch_0002**: 第1次 placeholder 失败 → 第2次 term_consistency 失败 → 第3次通过
- **batch_0017**: term_consistency + language (cjk_ratio=0.04) + placeholder 同时失败，来不及重试即超时

最终 35/41 通过、6 个未通过，3600s 硬超时。

根因有三：
1. 重译缺乏结构性上下文——agent 看到"术语 X 未出现"，但不知道 X 在哪里、译文为什么没包含
2. 无全局预算——可以无限次在一个 batch 上消耗时间
3. term_consistency 精确字符串匹配敏感度过高——"Segment Anything 模型"与"分割一切模型"等价但被报错

## Goals / Non-Goals

**Goals:**
- 新增全局重试预算机制，防止个别 batch 消耗全部时间
- 强化重译时的失败定位信息，减少"打地鼠"
- term_consistency 改为子串匹配，减少假阳性
- 快速模式下此问题不涉及（快速模式没有占位符保护也不会遇到 term_consistency-placeholder 交叉失败）

**Non-Goals:**
- 不修改 sentencify / protect / restore 流程
- 不引入翻译缓存或断点续传
- 不改变 quality gate 的 pass/fail 判定逻辑结构

## Decisions

### Decision 1: 全局重试预算 + 软降级

- **Chosen**: 在 SKILL.md Phase 7 中声明两个上限：
  - 单个 batch 最多重试 2 次（第 3 次仍失败 → 标记为 `risky`，保留现有最佳译文，继续下一个 batch）
  - 整个管道累计重试次数不超过 10 次（超时 → 剩余未通过 batch 全部标记 warning，跳过质量门禁要求直接写入译文）
- **Alternatives**: 脚本中实现硬上限
- **Rationale**: 这是 agent 行为约束问题，不是脚本逻辑问题。在 SKILL.md 中声明比在脚本中加状态机更简单可维护。agent 在执行时自主追踪 `retry_count` 和 `total_retries`。
- **Trade-off**: 依赖 agent 正确追踪状态。如果 agent 不追踪，门禁仍会失败。但 agent 已经有 quality gate stdout 输出作为信号。

### Decision 2: term_consistency 子串匹配

- **Chosen**: `check_term_consistency()` 中，对于 glossary 中 `original != translation` 的术语（即需要翻译的术语），检查译文文本是否包含 glossary 中定义的译法**或其任何子串**。保持对 "do-not-translate" 术语（original == translation）的精确匹配不变。
- **Alternatives**: 完全跳过术语一致性检查；用 LLM 做术语一致性判断
- **Rationale**: 当前问题在于精确匹配对同意译法的变体过于敏感。"Segment Anything 模型" 和 "分割一切" 都可接受。子串匹配（即 `translation_text` 包含 `glossary_translation` 中的至少一个词或整体）可显著减少假阳性，同时仍能捕获真正的术语遗漏。do-not-translate 术语（如 "masklet"）保持精确匹配是正确的——这些词必须原样出现。
- **Trade-off**: 子串匹配偶尔会漏掉术语翻译的错误形式（例如 "注意力" 子串匹配可能错误接受 "注意力机制不完善" 这样的短语），但比当前精确匹配的假阳性率低得多。可接受。

### Decision 3: 重译时输出"失败项 → 修正方案"对照表

- **Chosen**: 在 SKILL.md 中要求 agent 在重译失败 batch 前，先将 quality gate stdout 中的每个失败项翻译为具体的修正方案，然后再重译
- **Alternatives**: 不做结构化修正，agent 自行判断
- **Rationale**: "打地鼠"的核心原因是 agent 在重新翻译时忘记了原始的占位符位置和术语表约束。强制输出对照表有两个作用：(1) 迫使 agent 精确定位问题 (2) 形成可追溯的修正记录，避免重复犯错
- **Trade-off**: 增加单次重译的 token 消耗，但减少了重译次数，总体节省。

## Risks / Trade-offs

- **子串匹配漏检** → 如果 glossary 译法是一个常见的短词（如"模型"），子串可能匹配到无关上下文。缓解：只对长度 ≥ 3 的 glossary 译法做子串匹配，更短的仍用精确匹配。
- **agent 不追踪重试预算** → SKILL.md 中的约束是软性的。如果 agent 忽略，现象不变。缓解：在 Phase 7 开头显式要求 agent 声明两个计数器变量（per-batch retry 和 global retry），形成执行惯性。
- **软降级导致翻译质量下降** → 标记 risky/warning 的 batch 不会被修复，最终产物不完整。缓解：这些 batch 在 QA report 中列出，下游用户可选择性手动修复。对 41 batch 的论文而言，5-6 个未修复 batch 影响可控。
