## 1. 新增脚本

- [x] 1.1 创建 `scripts/build_block_sentences.py`：解析 blocked.md 块标记，每个 block 输出 1 sentence 的 v2 sentences.json
- [x] 1.2 验证：对 137-block fixture 生成 sentences.json，确认格式为 v2，每 block 1 sentence

## 2. Quality gate 模式适配

- [x] 2.1 `scripts/quality_gate.py` 新增 `--mode` 参数（fast | high_quality，default: high_quality）
- [x] 2.2 fast 模式下 placeholder_preservation 和 numeric_preservation 输出 `{"passed": true, "skipped": true}`
- [x] 2.3 回归验证：high_quality 模式行为不变

## 3. Alignment export 模式适配

- [x] 3.1 `scripts/export_alignment.py` 新增 `--mode` 参数
- [x] 3.2 fast 模式输出 `"pairs": []`，`source_markdown` / `translated_markdown` 正常填充
- [x] 3.3 验证：fast 模式 alignment 产物格式正确

## 4. Schema 更新

- [x] 4.1 `assets/parameter.schema.json`：新增 `mode` 字段（enum: fast/high_quality，default: fast）；移除 `source_language`
- [x] 4.2 `assets/input.schema.json`：移除 `source_language`

## 5. SKILL.md 流程重写

- [x] 5.1 Inputs 部分新增 mode 参数说明
- [x] 5.2 Phase 5–11 完整重写为模式分支流程
- [x] 5.3 新增 `build_block_sentences.py` entrypoint 说明
- [x] 5.4 更新 sentencify/protect/restore entrypoint 标注为 [high_quality]
- [x] 5.5 更新 quality_gate / export_alignment entrypoint 添加 --mode 参数
- [x] 5.6 更新 Script Responsibilities 章节
- [x] 5.7 更新 Never 章节（区分 fast/high_quality 约束）
- [x] 5.8 更新 Happy Path example

## 6. 参考文档更新

- [x] 6.1 `references/stage-playbook.md`：新增 "Fast 模式细则" 章节
- [x] 6.2 `references/payload-contracts.md`：Quality Gate 输入增加 --mode/--placeholder-map 说明；check 表标注 fast 模式跳过行为

## 7. 验证

- [x] 7.1 所有修改脚本语法检查通过
- [x] 7.2 quality_gate.py --mode fast 验证：placeholder/numeric 返回 skipped
- [x] 7.3 quality_gate.py --mode high_quality 回归：行为不变
- [x] 7.4 export_alignment.py --mode fast 验证：pairs 为空，source/translated_markdown 正常
