## Context

首次迭代后验证发现：块级拆分由 LLM 执行时 agent 总想写临时脚本；句拆分时缩写误拆分导致碎片句；拼接时 BLOCK_END 重复输出。需要将 Phase 4 从 agent 执行转为脚本拆分 + agent 复核，并修复下游 bug。

## Goals / Non-Goals

**Goals:**
- blockify.py 在所有 70 篇示例论文上无崩溃运行
- block 标记在 blockify → sentencify → concatenate 全流程保持均衡
- 缩写不再被误拆为碎片句
- 多行段落中的换行符正确归一化
- 拼接后每条译文独立成行

**Non-Goals:**
- 不做语义级的 block 合并（由 agent 复核完成）
- 不做翻译质量验证（由 quality_gate.py 覆盖）

## Decisions

### Decision 1: 两遍扫描 + 状态机算法

blockify.py 使用两遍扫描：Pass 1 检测标题策略（proper_nesting vs flat_single_hash），Pass 2 进行状态机解析。

核心状态：`IDLE → EQUATION/TABLE/CODE/FIGURE_CAPTION/LIST/PARAGRAPH/ABSTRACT`

标题策略检测解决了学术论文中部分论文对所有级别使用 `#`（如 DAB-DETR）的问题，flat 模式下通过编号推断级别。

### Decision 2: 保守合并策略

blockify.py 按空白行作为段落边界，不做激进合并。相邻同类型块（paragraph+paragraph）在共享同一 heading 时合并。过度细分留待 agent 复核时做最终决策。

### Decision 3: 两阶段缩写保护

sentencify.py 使用两层保护：
1. 正则前瞻排除已知缩写（`Fig.`, `Dept.`, `e.g.` 等 + IGNORECASE）
2. 后处理合并以小写/数字开头的碎片（捕获正则未覆盖的边界情况）

### Decision 4: standalone test harness

pipeline_test.py 独立于 skill 执行流程，通过 mock translation 做结构验证。不引入测试框架依赖，纯 Python 标准库。

## Risks / Trade-offs

- 缩写白名单可能遗漏生僻学术缩写 → agent 在质量门禁前有机会修正
- `\n`→空格归一化可能破坏表格内故意换行 → table block 由 concatentate.py 保持原始行结构，sentencify 不做换行归一化
- flat_single_hash 标题策略对非标准编号的文档可能推断错误 → agent 复核修正
