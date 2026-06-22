## Why

一次 `high_quality` 模式真 run 暴露了质量门禁循环的脆弱性：41 batch 的 SAM 2 论文中，多个 batch 在 term_consistency 和 placeholder_preservation 之间反复"打地鼠"——修术语时丢失占位符，修占位符时术语又出错。agent 把大量时间消耗在个别 batch 的逐次重试上，最终在 3600s 硬超时下只修完 35/41 batch，6 个仍未通过。

三个核心问题：
1. 每次重译都是"盲修"——agent 只看到 quality gate 的错误报告（"术语 X 未出现""占位符 Y 丢失"），但没有结构性上下文辅助精确定位和修复
2. 没有全局时间/次数预算——agent 可以无限次在某个 batch 上重试，耗尽整个 pipeline 的时间
3. term_consistency 检查是精确字符串匹配，对同义词、同意译法的变体翻译一律报错，产生大量假阳性

## What Changes

- **quality_gate.py**: term_consistency 检查从精确字符串匹配改为子串级宽松匹配（仅检查语义等价译法，不允许近似）。新增全局失败上限：同一 batch 重试 2 次不通过即标记为 `risky` 并继续下一个 batch；总计超 10 次重试时剩余 batch 全部标记 warning 继续。
- **SKILL.md Phase 7**: 新增重试预算机制描述；重译时要求 agent 输出"失败项 → 修正方案"对照表后再落笔；强化 placeholder 保护在重译时的优先级
- **references/stage-playbook.md**: 新增"质量门禁重试细则"
- **references/translation-prompt.md**: 重译提示增加"失败项针对性修正"模板

## Capabilities

### Modified Capabilities
- `literature-translator`:
  - Requirement "Enhanced quality gate checks": term_consistency 检查策略调整；新增全局重试上限
  - Requirement "Translation execution with quality gate": 新增重试预算和退路机制
  - Requirement "Structured translation review": 重译时增加结构化修正逻辑

## Impact

- `scripts/quality_gate.py`: term_consistency 匹配策略 + main() 中重试上限逻辑
- `SKILL.md`: Phase 7 重试预算、修正对照表
- `references/stage-playbook.md`: 质量门禁重试细则
- `references/translation-prompt.md`: 重译修正模板
