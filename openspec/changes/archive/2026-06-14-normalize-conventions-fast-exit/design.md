## Context

本 change 不改变翻译核心逻辑，只做三个方面的工作：
1. 按 literature-analysis 的约定补充 schema 和 runner 文件
2. 统一路径规范（workspace/ → .literature_translator_tmp/，最终产物输出到工作目录）
3. 增加快速退出路径

## Decisions

### Decision 1: 借鉴 literature-analysis 的路径约定

- `.literature_analysis_tmp/` → `.literature_translator_tmp/`
- Stdout 输出必须是单一 JSON 对象（成功/取消/失败三种状态）
- `runner.json` 中的 prompt 模板使用 Jinja2 变量引用 `{{ input.source_path }}` 和 `{{ parameter.target_language }}`

### Decision 2: 快速退出在 Phase 1 与 Phase 2 之间

- 放在 Phase 1（parse_input.py）之后、Phase 2（LLM 宏观分析）之前
- 条件：`source_language` 显式提供且等于 `target_language`
- Phase 3 保留为安全网（LLM 检测后二次比较）

### Decision 3: Schema 版本管理

- input.schema.json 版本号不动（内容更新，路径不变，向后兼容）
- runner.json 使用 version 2.0.0 标记本次不兼容变更（产出物目录变化）
