## 1. quality_gate.py — term_consistency 子串匹配

- [x] 1.1 修改 `check_term_consistency()`：对 `original != translation` 的术语（需翻译的术语），改为检查 glossary 译法是否作为子串出现在译文中（大小写不敏感）。长度 < 3 的译法保持精确匹配。
- [x] 1.2 对 `original == translation` 的术语（不翻译的术语），保持现有的大小写敏感精确匹配行为。
- [x] 1.3 验证：构造 mock 数据——同意译法的变体翻译应通过、完全不相关的翻译应拒绝、do-not-translate 术语缺失应拒绝。

## 2. SKILL.md Phase 7 — 重试预算与修正对照表

- [x] 2.1 在 Phase 7 的门禁结果处理部分新增重试预算规则：
  - 单 batch 最多 2 次重试（3 次总尝试），超出标记 risky 继续
  - 全局累计重试不超过 10 次，超出后剩余失败 batch 接受 as-is
- [x] 2.2 新增"重译修正流程"小节：要求 agent 在重译失败 batch 前，先输出"失败项 → 根因 → 修正方案"对照表
- [x] 2.3 新增 placeholder 重译保护提示：重译时显式列出该 batch 原文中的所有占位符，要求 agent 逐一确认保留

## 3. references/translation-prompt.md — 重译模板

- [x] 3.1 新增"重译指引"小节：当翻译是针对失败 batch 的重译时，原文占位符列表必须显式提供，agent 必须逐一检查每个占位符在译文中出现
- [x] 3.2 新增术语保护提醒：重译时术语表 locked 中的术语必须使用指定译法并验证出现

## 4. references/stage-playbook.md — 重试细则

- [x] 4.1 新增"质量门禁重试细则"小节：重试预算的详细规则、risky 标记格式、warning 标记格式

## 5. payload-contracts.md — Quality Gate 输出更新

- [x] 5.1 更新 term_consistency check 输出说明，标注子串匹配策略
- [x] 5.2 更新 Quality Gate 输出 schema 示例

## 6. 验证

- [x] 6.1 term_consistency 子串匹配 mock 测试：正常术语变体通过、短词精确匹配、do-not-translate 精确匹配
- [x] 6.2 term_consistency 精确匹配回归：do-not-translate 缺失应拒绝
- [x] 6.3 SKILL.md 重试预算规则可读性检查
- [x] 6.4 语法检查通过
