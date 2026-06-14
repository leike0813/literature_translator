## Why

基于对文献翻译设计方案的深度分析，发现第一阶段实现存在翻译质量稳定性瓶颈：行内元素（公式、变量、引用）无保护易被模型误改、质量门禁覆盖不足无法检测占位符丢失、review 环节无结构化输出导致修复无法精确定位。需要在不改变整体架构的前提下，系统性增强流水线的稳定性机制。

## What Changes

- 新增 `scripts/protect_placeholders.py` 和 `scripts/restore_placeholders.py`，对句级拆分后的行内元素（行内公式、变量、引用编号、数字、URL、实体名）做占位符替换与还原
- 增强 `scripts/quality_gate.py` 从 4 项检查到 8 项（新增占位符保持、数字/引用保持、非翻译性语言检测、长度类型弱校验）
- 所有翻译相关脚本的句子格式升级为 `[index, text]` 对，支持 1-based 局部句号精确定位
- 引入结构化 reviewer subagent + 局部修复 repairer subagent 的分阶段审查流程
- 新增 `scripts/export_alignment.py` 和 `scripts/export_qa_report.py`，输出双语对齐数据和质量报告
- `SKILL.md` 流程从 10 阶段扩展到 11 阶段（Phase 5a 占位符保护、Phase 8a reviewer、Phase 8b repairer、Phase 11 导出）
- 术语表 `glossary.json` 从平坦结构升级为三级结构（locked / provisional / keep_english）
- 新增 3 份 prompt 模板：`references/translation-prompt.md`、`references/reviewer-prompt.md`、`references/repairer-prompt.md`

## Capabilities

### New Capabilities

- `placeholder-protection`: 对行内公式、变量、引用编号、数字、URL、实体名做自动化占位符替换，翻译完成后还原，防止模型误改
- `enhanced-quality-gate`: 8 项硬性检查 + 1 项弱校验，覆盖句数、长度、术语、语言、占位符、数字/引用、非翻译性语言
- `structured-review`: 结构化 reviewer subagent，输出 10 种错误类型的结构化 error report，支持 reviewer → repairer 循环
- `local-repair`: 基于 reviewer 输出的精确错误定位，只修复失败句，不重译整个 block
- `alignment-export`: 句级双语对齐数据导出，供下游精读 skill 使用
- `qa-report-export`: 结构化质量报告，包含所有检查结果、修复记录和高风险项
- `glossary-v2`: 三级术语表结构（locked / provisional / keep_english）

### Modified Capabilities

- `sentence-splitting`: 句子格式从 `string[]` 升级为 `[index, text][]`（1-based 局部句号），所有下游脚本兼容两种格式
- `translation-execution`: 翻译 worker prompt 增强，明确约束"不是总结器/解释器/润色器"，要求保留占位符和逻辑关系
- `final-polish`: 增加确定性渲染约束，禁止修改结构，仅允许语言通顺性修改

## Impact

- `literature-translator/SKILL.md`: 流程从 10 阶段扩展到 11 阶段，输出产物增加 alignment.json 和 qa_report.json
- `literature-translator/scripts/sentencify.py`: 句子格式改为 [index, text] 对，输出加 format: v2 标记
- `literature-translator/scripts/partition_batches.py`: 兼容两种句子格式
- `literature-translator/scripts/quality_gate.py`: 从 4 项检查增强到 8 项，支持 glossary v2 三级结构
- `literature-translator/scripts/concatenate.py`: 支持 [index, text] 格式解析
- `literature-translator/references/payload-contracts.md`: 新增 5 个 JSON schema 定义
- `literature-translator/references/stage-playbook.md`: 新增 Phase 5a/8a/8b/10/11 操作细则
- `literature-translator/references/translation-prompt.md`: **新增**增强版翻译 worker prompt
- `literature-translator/references/reviewer-prompt.md`: **新增**结构化 reviewer prompt
- `literature-translator/references/repairer-prompt.md`: **新增**局部修复模块 prompt
- `literature-translator/scripts/protect_placeholders.py`: **新增**行内占位符保护脚本
- `literature-translator/scripts/restore_placeholders.py`: **新增**占位符还原脚本
- `literature-translator/scripts/export_alignment.py`: **新增**对齐数据导出脚本
- `literature-translator/scripts/export_qa_report.py`: **新增**质量报告导出脚本
