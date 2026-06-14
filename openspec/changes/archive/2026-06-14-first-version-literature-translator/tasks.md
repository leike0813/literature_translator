## 1. Skill 骨架与核心指令

- [x] 1.1 创建 `literature-translator/` 目录结构（scripts/, references/, assets/）
- [x] 1.2 编写 `SKILL.md`：10 阶段执行流程、输入输出、约束、示例、失败处理

## 2. 确定性脚本

- [x] 2.1 编写 `scripts/parse_input.py`：输入类型检测（Markdown/PDF/LaTeX/目录），规范化输出 normalized.md 和元信息
- [x] 2.2 编写 `scripts/sentencify.py`：句级拆分（公式/代码块整体保留），输出 sentences.json
- [x] 2.3 编写 `scripts/partition_batches.py`：按字符阈值均衡分区，永不跨块拆分，输出 batch payload
- [x] 2.4 编写 `scripts/quality_gate.py`：四维校验（句数一致、偷懒检测、术语一致、语言正确性）
- [x] 2.5 编写 `scripts/concatenate.py`：按块顺序拼接译文，支持部分缺失报告

## 3. 参考文档

- [x] 3.1 编写 `references/stage-playbook.md`：术语表规范、块拆分细则、翻译执行细则、润色清单
- [x] 3.2 编写 `references/payload-contracts.md`：所有脚本的 I/O schema 和字段语义
- [x] 3.3 编写 `references/subagent-protocol.md`：委派 prompt 模板、payload 协议、结果返回和失败处理

## 4. Schema 与质量验证

- [x] 4.1 编写 `assets/input.schema.json`：prompt payload JSON schema
- [x] 4.2 Python 语法验证：所有 5 个脚本通过 `py_compile` 检查
- [x] 4.3 质量门禁审查：13 项 quality gates 全部通过（触发、复杂度、来源、可执行性、I/O 等）
