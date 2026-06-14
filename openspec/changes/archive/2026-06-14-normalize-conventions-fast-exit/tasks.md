## 1. Schema 与 runner 文件

- [x] 1.1 重写 `assets/input.schema.json`：增加 `extensions` 数组，`source_path` 保留，`target_language` 移出
- [x] 1.2 新增 `assets/parameter.schema.json`：定义 `target_language`（default: zh-CN）和 `source_language`
- [x] 1.3 新增 `assets/output.schema.json`：定义成功/取消/失败三种状态的 stdout JSON 格式
- [x] 1.4 新增 `assets/runner.json`：含 Jinja2 prompt 模板

## 2. SKILL.md 更新

- [x] 2.1 前件增加 `compatibility` 字段
- [x] 2.2 所有 `workspace/` 路径改为 `.literature_translator_tmp/`
- [x] 2.3 增加 Phase 1.5 快速退出路径描述
- [x] 2.4 Output Contract 修改：stdout 单一 JSON 对象，最终产物输出到 CWD
- [x] 2.5 更新 Inputs 说明：source_path 从 input 读取，target_language 从 parameter 读取

## 3. 脚本与参考文档更新

- [x] 3.1 `scripts/parse_input.py`：`--workspace` 默认值改为 `.literature_translator_tmp/`
- [x] 3.2 `references/payload-contracts.md`：所有路径示例更新
- [x] 3.3 `references/stage-playbook.md`：所有路径示例更新

## 4. 验证

- [x] 4.1 确认 4 个 schema/runner 文件为合法 JSON
- [x] 4.2 `python3 -c "import py_compile; py_compile.compile('scripts/parse_input.py')"`
- [x] 4.3 `pipeline_test.py` 回归测试
