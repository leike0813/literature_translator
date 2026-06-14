## 1. 句子格式升级（局部句号）

- [x] 1.1 修改 `scripts/sentencify.py`：句子格式从 `string[]` 改为 `[index, text][]`（1-based），输出加 `"format": "v2"` 标记
- [x] 1.2 修改 `scripts/partition_batches.py`：兼容 v1（string[]）和 v2（[index, text][]）两种格式
- [x] 1.3 修改 `scripts/concatenate.py`：`load_translations()` 支持 v2 格式解析，提取 `extract_sentence_text()` 工具函数

## 2. 占位符保护

- [x] 2.1 新增 `scripts/protect_placeholders.py`：行内占位符替换（正则按 7 级优先级），输出 `placeholder_map.json`
- [x] 2.2 新增 `scripts/restore_placeholders.py`：翻译完成后将占位符还原为原始值，支持 v1/v2 句子格式
- [x] 2.3 端到端验证：保护 → mock 翻译 → 还原，检查 100% 匹配

## 3. 质量门禁增强

- [x] 3.1 实现占位符保持检查：输入占位符全部出现，译文无非法占位符
- [x] 3.2 实现数字/引用保持检查：NUM/REF/FIG/TBL/EQ_REF 类占位符保留
- [x] 3.3 实现非翻译性语言检测：检查"大意是""可以理解为"等解释性短语
- [x] 3.4 实现按 block 类型的长度阈值检查（弱校验，仅 warning）
- [x] 3.5 增强语言检查：支持 keep_english 豁免列表，通过 placeholder_map 解析后再做术语/语言检查

## 4. Prompt 模板

- [x] 4.1 新增 `references/translation-prompt.md`：增强版翻译 worker prompt（"不是总结器/解释器/润色器"等硬约束）
- [x] 4.2 新增 `references/reviewer-prompt.md`：结构化 reviewer prompt（10 种错误类型分类）
- [x] 4.3 新增 `references/repairer-prompt.md`：局部修复模块 prompt（只修失败句）

## 5. 结构化审查与修复流程

- [x] 5.1 `SKILL.md` 中新增 Phase 8a（结构化 reviewer）和 Phase 8b（局部修复）的描述与控制逻辑
- [x] 5.2 `SKILL.md` 中新增 Phase 5a（占位符保护）的完整描述
- [x] 5.3 `SKILL.md` 中新增 Phase 9a（占位符还原）和 Phase 11（导出）的描述
- [x] 5.4 `SKILL.md` 中 Phase 10 增加确定性渲染约束

## 6. 导出脚本

- [x] 6.1 新增 `scripts/export_alignment.py`：双语对齐数据导出，包含原文/译文/QA 状态
- [x] 6.2 新增 `scripts/export_qa_report.py`：结构化质量报告，汇总检查/修复/风险

## 7. 参考文档更新

- [x] 7.1 更新 `references/payload-contracts.md`：新增 v2 Sentence JSON、Protected Sentences、Placeholder Map、Translation Result v2、Quality Gate v2、Alignment JSON、QA Report JSON 共 7 个 schema 定义
- [x] 7.2 更新 `references/stage-playbook.md`：新增 Phase 5a 占位符保护细则、Phase 8a reviewer 细则、Phase 8b repairer 细则、Phase 10 润色约束、Phase 11 导出细则

## 8. 回归验证

- [x] 8.1 所有脚本语法检查通过（10 个 Python 脚本）
- [x] 8.2 `pipeline_test.py` 回归测试：2/2 通过（49-block 和 136-block fixture）
- [x] 8.3 占位符保护端到端测试：344 个占位符正确提取，100% 还原匹配
- [x] 8.4 导出脚本功能验证：alignment.json 和 qa_report.json 结构与字段正确
