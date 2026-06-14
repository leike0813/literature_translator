## Context

第一版 literature-translator 实现了 10 阶段流水线，但在实际运行中发现三个核心问题：

1. **行内元素无保护**：block 级别已保护公式 `$$` 和代码块，但行内公式 `$...$`、变量名 `\alpha`、引用编号 `[1]`、数字 `0.01`、URL 等直接暴露给翻译 worker，模型常误改或丢失。
2. **质量门禁覆盖不足**：`quality_gate.py` 的 4 项检查（句数、长度、术语、语言）无法检测占位符丢失、数字改动、解释性翻译等常见问题。
3. **Review 无结构化输出**：Phase 8 主 agent review 是自由格式通读，无法精确定位错误位置，修复时只能整 batch 重翻，已通过的句子也可能被改坏。

当前约束：保持 Tier 3 架构（脚本辅助 + LLM 语义任务）、不引入外部翻译 API、不增加跨会话状态管理。

## Goals / Non-Goals

**Goals:**
- 行内元素占位符保护与还原，消除翻译 worker 误改风险
- 质量门禁从 4 项增强到 8 项，覆盖占位符、数字、引用、非翻译性语言
- 引入结构化 reviewer + 局部 repairer 的分阶段审查流程
- 句子格式升级为 `[index, text]` 对，支持精确定位到句
- 输出双语对齐数据和质量报告，为下游精读 skill 提供基础设施
- 更新 pipeline_test.py 回归测试验证结构完整性

**Non-Goals:**
- 不改变 block 级划分逻辑（`blockify.py` 不做修改）
- 不引入翻译缓存（留待下一版本）
- 不实现双译本仲裁
- 不做表格深度 cell 级翻译
- 不处理跨会话恢复

## Decisions

### Decision 1: 占位符保护插入句级拆分之后而非之前

- **Chosen**: Phase 5（句级拆分）→ Phase 5a（占位符保护）
- **Alternatives**: 句级拆分前做占位符保护
- **Rationale**: 句级拆分后的每个句子是独立语义单元，保护逻辑更清晰。如果先做保护再做拆分，需要额外处理占位符与标点边界的交互。拆分后的句子数量更多但每句保护成本更低。
- **Trade-off**: `placeholder_map.json` 需要在翻译完成后传递给 `restore_placeholders.py` 和 `quality_gate.py`（术语/语言检查需要解析占位符），增加了数据流复杂度。

### Decision 2: 正则替换优先于 ML 识别

- **Chosen**: 手工编写的正则表达式链（按优先级有序替换）
- **Alternatives**: 用 ML 模型识别行内元素
- **Rationale**: 行内公式、引用、数字、URL 有明确的语法边界，正则比 ML 更可靠（无漏判/误判）、更可预测（确定性输出）、更快（毫秒级）。ML 可能漏掉边缘格式或引入误替换。
- **Trade-off**: 正则维护成本高，遇到非标准 LaTeX 格式可能需要扩展。

### Decision 3: Reviewer 为独立受限 subagent，非主 agent 子步骤

- **Chosen**: Reviewer 作为独立受限 subagent（禁用工具/代码执行）
- **Alternatives**: 主 agent 自行 review（当前做法）
- **Rationale**: 主 agent 在 Phase 7 翻译后上下文已较满，独立 reviewer 可保持客观性。需要结构化输出（10 种错误类型分类），独立 subagent 更易约束。reviewer 不应拥有改代码的能力（只读审查）。
- **Trade-off**: 多一次 subagent 调用增加 token 消耗和延迟。

### Decision 4: 局部修复优先于整 batch 重翻

- **Chosen**: 优先逐句修复，仅系统性失败（>50% 句子有错误）时回退到整 batch 重翻
- **Alternatives**: 总是整 batch 重翻（当前做法）
- **Rationale**: 局部修复避免了已通过句子被改坏的风险。质量门禁中约 80% 失败是单个句子问题（丢失占位符、术语不一致），局部修复足够。整 batch 重翻代价高且可能引入新问题。
- **Trade-off**: 实现复杂度更高，需要修复合并逻辑和循环终止条件。

### Decision 5: glossary 三级结构保持向后兼容

- **Chosen**: 新格式使用 `locked`/`provisional`/`keep_english` 三级，`quality_gate.py` 同时支持 v1 平坦格式和 v2 三级格式检测
- **Rationale**: v1 平坦格式中的条目自动归入 `locked` 保证兼容。`keep_english` 中的词在语言检查中被豁免。下游使用 `glossary.json` 路径不变。
- **Trade-off**: 脚本需要做格式检测分支，增加少量复杂度。

## Risks / Trade-offs

- **占位符正则漏匹配** → 遇到非标准 LaTeX 格式（如 `\(...\)` 行内公式）时可能漏保护。逐步扩展正则覆盖，优先覆盖 arXiv 论文常见格式。
- **Reviewer subagent 不可用时退路** → 如果环境不支持 subagent，退回到主 agent 手工结构化 review（按 reviewer-prompt.md 的检查清单逐项检查）。
- **修复循环不收敛** → reviewer 和 repairer 可能陷入循环（repairer 修复后 reviewer 仍报不同错误）。设置最多 2 轮限制，超限后标记为 risky。
- **长度弱校验假阳性** → 中文译文可能比原文短（中文信息密度更高），但仍在正常范围。弱校验仅 warning 不打回。
- **v2 格式下游兼容性** → 已有 workspace/run_3 等中间产物使用 v1 格式。所有修改的脚本均兼容两种格式（检测 `format` 字段或检测句子元素类型）。
