## Why

首次验证发现块级拆分由 LLM 执行时，agent 倾向于写临时脚本替代，说明该工作更适合确定性脚本。同时在句级拆分和拼接环节发现缩写误拆分、嵌入式换行、BLOCK_END 重复输出等影响翻译质量的 bug，需要系统性修复并建立测试回归。

## What Changes

- 新建 `scripts/blockify.py`：确定性块级拆分脚本，替代 agent 手工拆分
- 修改 `scripts/concatenate.py`：修复 `" ".join(sentences)` 导致多行塌缩、`i += 1` 位置错误导致 BLOCK_END 重复输出
- 修改 `scripts/sentencify.py`：扩展缩写白名单 + IGNORECASE、新增小写/数字开头合并规则、段落内 `\n`→空格归一化
- 修改 `SKILL.md`：Phase 4 改为"脚本拆分 + Agent 复核"；新增 blockify.py 入口；调整 LLM/Script 职责
- 修改 `references/stage-playbook.md`：拆分细则更新，区分脚本可靠识别和 Agent 需核验的类型
- 修改 `references/payload-contracts.md`：新增 blockify 输出格式说明
- 新建 `scripts/pipeline_test.py`：端到端结构测试 harness

## Capabilities

### New Capabilities

- `blockify-script`: 确定性块级拆分脚本，识别 heading/equation/table/figure/code/paragraph/list/abstract/bib_item/table_caption
- `pipeline-test-harness`: 结构测试 harness，验证 blockify→sentencify→partition→concatenate 全流程

### Modified Capabilities

- `literature-translator`: Phase 4 流程从"Agent 执行"改为"脚本拆分 + Agent 复核"

## Impact

- `literature-translator/scripts/blockify.py` — 新建
- `literature-translator/scripts/concatenate.py` — 2 处 bug 修复
- `literature-translator/scripts/sentencify.py` — 3 处改进
- `literature-translator/scripts/pipeline_test.py` — 新建
- `literature-translator/SKILL.md` — Phase 4 重写、Formal Entrypoints、LLM/Script 职责
- `literature-translator/references/stage-playbook.md` — 拆分细则
- `literature-translator/references/payload-contracts.md` — blockify 输出格式
