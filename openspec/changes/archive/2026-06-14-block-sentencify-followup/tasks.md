## 1. 块级拆分脚本

- [x] 1.1 编写 `scripts/blockify.py`：两遍扫描状态机，支持两种标题策略，覆盖全部 10 种块类型
- [x] 1.2 语法验证通过

## 2. 句拆分修复

- [x] 2.1 扩展缩写白名单（学术缩写 + IGNORECASE）
- [x] 2.2 新增小写/数字开头碎片合并规则
- [x] 2.3 段落内 `\n`→空格归一化

## 3. 拼接修复

- [x] 3.1 修复 `" ".join(sentences)` 导致多行塌缩（改用 `extend`）
- [x] 3.2 修复 `i += 1` 在 `else` 分支内导致 BLOCK_END 重复输出

## 4. SKILL.md 与参考文档更新

- [x] 4.1 Phase 4 改为"脚本拆分 + Agent 复核"
- [x] 4.2 description、Formal Entrypoints、LLM/Script 职责更新
- [x] 4.3 stage-playbook.md 更新：区分脚本可靠类型与 Agent 需核验类型
- [x] 4.4 payload-contracts.md 新增 blockify 输出格式

## 5. 测试 Harness 与验证

- [x] 5.1 编写 `scripts/pipeline_test.py`：全流程结构测试 harness
- [x] 5.2 70/70 篇示例论文全部通过结构检查
