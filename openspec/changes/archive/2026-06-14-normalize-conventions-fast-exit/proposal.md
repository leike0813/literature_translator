## Why

本项目 assets/ 目录仅有一个 input.schema.json，缺少 output.schema.json、parameter.schema.json、runner.json 等自动化框架接入所需的标准文件。文献翻译需要接入统一的自动化框架，但当前缺少框架识别 skill 输入/输出/参数所需的 manifest 和 schema 文件。

此外，当前"源语言==目标语言"的退出路径依赖 LLM 通读全文后检测，如果用户已提供 source_language 参数，应在解析输入后立即退出，避免浪费 token。

## What Changes

- 新增 `assets/parameter.schema.json`、`assets/output.schema.json`、`assets/runner.json`
- 重写 `assets/input.schema.json`，增加 `extensions` 数组约定，`target_language` 移入 parameter.schema.json
- 中间文件目录从 `workspace/` 改为 `.literature_translator_tmp/`（匹配 literature-analysis 的 `.literature_analysis_tmp/` 约定）
- 最终产物直接输出到工作目录（output_<lang>.md、glossary.json、alignment.json、qa_report.json）
- SKILL.md 增加 Phase 1.5 快速退出路径，stdout 改为单一 JSON 对象
- 所有脚本和参考文档中的路径示例同步更新

## Capabilities

### New Capabilities
- `schema-and-runner`: 标准化的 input/parameter/output schema 和 runner.json，供自动化框架识别 skill 契约
- `fast-exit`: 当用户提供 source_language 且等于 target_language 时，在输入解析后立即退出

### Modified Capabilities
- `literature-translator`: 中间文件路径从 workspace/ 改为 .literature_translator_tmp/；最终产物输出到工作目录；stdout 改为单一 JSON 对象

## Impact

- `literature-translator/assets/input.schema.json`: 重写，新增 extensions 数组，移出 target_language
- `literature-translator/assets/parameter.schema.json`: 新增
- `literature-translator/assets/output.schema.json`: 新增
- `literature-translator/assets/runner.json`: 新增
- `literature-translator/SKILL.md`: 前件、路径、Phase 1.5、stdout 契约、产物路径全部更新
- `literature-translator/scripts/parse_input.py`: --workspace 默认值改为 .literature_translator_tmp/
- `literature-translator/references/payload-contracts.md`: 路径示例更新
- `literature-translator/references/stage-playbook.md`: 路径示例更新
