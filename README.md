# Literature Translator

将学术文献自动翻译为目标语言，保留原文结构、公式、代码、引用和术语一致性。

## 项目结构

```
literature_translator/
├── AGENTS.md                          # 项目级 agent 约定
├── literature-translator/             # 核心 skill 包
│   ├── SKILL.md                       # 主执行指令（12 阶段流水线）
│   ├── assets/
│   │   ├── input.schema.json          # 输入 schema
│   │   ├── parameter.schema.json      # 参数 schema（target_language 默认值等）
│   │   ├── output.schema.json         # 输出 stdout JSON schema
│   │   └── runner.json                # 自动化框架运行时 manifest
│   ├── scripts/                       # 确定性 Python 脚本
│   │   ├── parse_input.py             # 输入类型检测与规范化
│   │   ├── blockify.py                # 块级拆分（状态机）
│   │   ├── sentencify.py              # 句级拆分（标点边界）
│   │   ├── protect_placeholders.py    # 行内元素占位符保护
│   │   ├── partition_batches.py       # 翻译批次均衡分区
│   │   ├── quality_gate.py            # 质量门禁（8 项检查）
│   │   ├── concatenate.py             # 译文拼接
│   │   ├── restore_placeholders.py    # 占位符还原
│   │   ├── export_alignment.py        # 双语对齐导出
│   │   └── export_qa_report.py        # 质量报告导出
│   └── references/                    # 按需读取的阶段指导文档
│       ├── stage-playbook.md          # 各阶段操作细则
│       ├── payload-contracts.md       # 所有脚本的 I/O schema
│       ├── subagent-protocol.md       # Subagent 委派协议
│       ├── translation-prompt.md      # 增强版翻译 worker prompt
│       ├── reviewer-prompt.md         # 结构化 reviewer prompt
│       └── repairer-prompt.md         # 局部修复模块 prompt
├── tests/pipeline_test.py             # 结构流水线回归测试
├── examples/                          # 60+ 篇示例论文 markdown
├── openspec/                          # OpenSpec 变更管理
└── workspace/                         # 历史运行记录
```

## 快速使用

```text
source_path: /path/to/paper.pdf
target_language: zh-CN
```

skill 自动执行 12 阶段流水线，产出：

| 产物 | 路径 |
|------|------|
| 最终译文 | `./output_zh-CN.md` |
| 术语表 | `./glossary.json` |
| 双语对齐 | `./alignment.json` |
| 质量报告 | `./qa_report.json` |

## 输入/输出约定

- **source_path**：来自 input.schema.json，支持 `.md` / `.pdf` / `.tex` 单文件或 LaTeX 工程目录
- **target_language**：来自 parameter.schema.json，默认 `zh-CN`
- **stdout**：单一 JSON 对象，符合 output.schema.json（success / cancelled / failed 三态）
- **中间文件**：写入 `.literature_translator_tmp/`

## 流水线概览

```
Phase 0:   环境分析
Phase 1:   输入解析 (parse_input.py)
Phase 2:   宏观分析与上下文档案 + 术语表（glossary.json, context_profile.json）
Phase 3:   源目标语言判断（source_language 与 target_language 是否同一种语言）
Phase 4a:  块级拆分 (blockify.py)
Phase 4b:  Agent 复核块标记
Phase 5:   句级拆分 (sentencify.py)
Phase 5a:  占位符保护 (protect_placeholders.py)
Phase 6:   翻译批次分割 (partition_batches.py)
Phase 7:   翻译执行 + 质量门禁 8 项检查 (quality_gate.py)
Phase 8a:  结构化 Reviewer 审查
Phase 8b:  局部修复（失败句逐句修复，最多 2 轮）
Phase 9a:  占位符还原 (restore_placeholders.py)
Phase 9b:  译文拼接 (concatenate.py)
Phase 10:  最终复核（确定性润色，禁止修改结构）
Phase 11:  导出对齐数据与质量报告 (export_alignment.py, export_qa_report.py)
```

## 架构要点

- **Tier 3（脚本辅助）**：LLM 负责语义任务（分析、翻译、审查），脚本负责确定性任务（拆分、校验、拼接、导出）
- **占位符保护**：行内公式 `$...$`、引用 `[1]`、数字 `0.01` 等翻译前替换为 `<MATH_NNN>`，翻译后还原
- **三级术语表**：`locked`（强制使用）/ `provisional`（建议使用）/ `keep_english`（保留原文）
- **局部句号**：句子以 `[index, text]` 对标识，reviewer/repairer 可精确定位到句
- **Subagent 委派**：可选并行翻译路径，不可用时主 agent 串行执行
