## Why

当前 skill 只有一条完整精翻流程（句级拆分 → 占位符保护 → 分批翻译 → 8 项检查 → 结构化 reviewer → 局部修复 → 占位符还原）。流程成本高，适合追求翻译精度的场景，但对于快速查看文献内容的用户过于冗长。需要新增模式开关让用户在"快"和"精"之间按需选择。

## What Changes

- 新增 `mode` parameter（`fast` | `high_quality`，默认 `fast`），控制翻译深度
- 新增 `scripts/build_block_sentences.py`：将 `blocked.md` 转为每 block 1 sentence 的 v2 sentences.json
- 修改 `scripts/quality_gate.py`：新增 `--mode` 参数，fast 模式跳过 placeholder_preservation / numeric_preservation 检查
- 修改 `scripts/export_alignment.py`：新增 `--mode` 参数，fast 模式输出 `"pairs": []`
- `SKILL.md`：Phase 5–11 重写为模式分支流程
- `parameter.schema.json`：新增 `mode` 字段；移除残留的 `source_language`
- `input.schema.json`：移除残留的 `source_language`
- `references/stage-playbook.md`、`references/payload-contracts.md`：同步更新

## Capabilities

### New Capabilities
- `fast-mode`: 块级快速翻译路径，跳句级拆分、占位符保护、结构化 review，以块为单位翻译，产出与高质量模式结构兼容的产物

### Modified Capabilities
- `literature-translator`:
  - Requirement "Input parsing and normalization": 新增 mode 参数输入
  - Requirement "Sentence-level splitting": fast 模式下替换为 `build_block_sentences.py`（块级输入构建）
  - Requirement "Translation execution with quality gate": 支持 fast/high_quality 双模式门禁
  - Requirement "Bilingual alignment export": fast 模式输出空 pairs 数组
  - Requirement "Inline placeholder protection": fast 模式不调用
  - Requirement "Structured translation review": fast 模式替换为块级速览

## Impact

- `assets/parameter.schema.json`: 新增 mode，移除 source_language
- `assets/input.schema.json`: 移除 source_language
- `scripts/build_block_sentences.py`: **新增**
- `scripts/quality_gate.py`: 新增 --mode 参数，fast 模式跳过 2 项检查
- `scripts/export_alignment.py`: 新增 --mode 参数，fast 模式空 pairs
- `SKILL.md`: Inputs + 整个 Phase 5–11 重写 + entrypoints 更新 + Script Responsibilities 更新 + Examples
- `references/stage-playbook.md`: 新增 Fast 模式细则
- `references/payload-contracts.md`: Quality Gate 输入说明、check 表标注
