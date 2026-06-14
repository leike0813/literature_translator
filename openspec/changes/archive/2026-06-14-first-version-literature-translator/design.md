## Context

项目 `AGENTS.md` 定义了文献翻译 Agent Skill 的宏观需求——自动化高质量翻译学术文献，包含 10 阶段流程、术语表管理、块级/句级拆分、质量门禁和 subagent 委派。需要将其转化为符合 Open Agent Skills 规范的完整 Skill 包。

当前状态：项目工作区 `literature-translator/` 一空目录，没有任何文件。

约束条件：
- 全程自动化运行，中途不询问用户
- 按 Open Agent Skills 规范组织目录：`SKILL.md` + `references/` + `scripts/` + `assets/`
- LLM 负责语义任务（块级拆分、翻译、润色），脚本负责确定性任务（校验、拆分、拼接）
- 禁止调用第三方翻译 API

## Goals / Non-Goals

**Goals:**
- 创建可被 LLM 直接执行的 `SKILL.md` 核心指令
- 编写 5 个确定性 Python 脚本覆盖解析、拆分、分区、校验、拼接
- 编写 3 份 reference 文档覆盖阶段细则、payload schema、subagent 协议
- 输入 schema 定义明确

**Non-Goals:**
- 不处理跨会话恢复（单次会话完成）
- 不使用 SQLite 或 state machine（无需 gate 管理）
- 不包含 agents/openai.yaml（无 Codex UI 部署需求）
- 不包含 GitHub Actions 等 CI/CD 集成

## Decisions

### Decision 1: Tier 3 (Script-assisted) + Subagent Delegation

- **Chosen**: Script-assisted workflow (Tier 3) with optional subagent delegation
- **Alternatives considered**: Tier 2 (too light — 缺少确定性校验), Tier 5/6 (过重 — 无跨会话需求)
- **Rationale**: 任务有明确的多阶段流程和确定性步骤（拆分、校验、拼接），但无需跨上下文恢复或 gate 管理。subagent delegation 作为可选叠加层，不对并行执行做硬依赖。

### Decision 2: Agent 执行块级拆分，脚本执行句级拆分

- **Chosen**: LLM 负责语义理解（块级拆分，识别章节边界、公式块、代码块等），脚本只做标点级句拆分
- **Why**: 块级拆分需要理解文档语义结构（公式 vs 代码 vs 段落），这是 LLM 能力区。句级拆分可按标点符号稳定完成，适合脚本
- **Script boundary**: `sentencify.py` 在 LLM 标注的 block 标记内工作，formula/code 类 block 整体保留不拆分

### Decision 3: 质量门禁作为独立脚本而非 SKILL.md 指令

- **Chosen**: 四维检查（句数、偷懒、术语、语言）全部由 `quality_gate.py` 确定性执行
- **Why**: 这些检查可量化、可自动化。让 LLM 自检翻译质量可靠性低（容易自信地放行错误）。脚本输出 JSON 结果供 agent 判断下一步（重试/通过/报 blocker）

### Decision 4: 批次分割保持块完整性

- **Chosen**: `partition_batches.py` 按字符阈值分区，但永不跨块拆分
- **Why**: 跨块拆分会增加翻译上下文复杂度，subagent 需要额外理解被拆分的块边界。保持块完整性后每个 subagent 拿到的是完整语义单元

### Decision 5: 输入解析脚本兼容多种格式

- **Chosen**: `parse_input.py` 使用启发式检测（文件扩展名 + 内容特征）判断输入类型，对 PDF 做识别但不做提取（退回给 agent 调用外部工具）
- **Why**: PDF 提取需要成熟工具（如 mineru），不应由 skill 脚本重新实现。LaTeX 到 Markdown 的转换使用正则替换覆盖常见构造

## Risks / Trade-offs

- **LaTeX 转换不完整** → `parse_input.py` 的正则替换只能覆盖常见 LaTeX 构造。排版复杂的 LaTeX 文档可能需要手动调整 normalized.md
- **句级拆分精度有限** → 缩写识别（e.g., i.e.）依赖正则白名单，边界情况可能误分。agent 应复核拆分结果
- **质量门禁是必要条件非充分条件** → 通过校验不保证翻译质量。最终润色阶段依赖 agent 的语义判断能力
- **Subagent 不可用时的性能** → 串行翻译大批量文献可能消耗大量上下文。建议大文档优先使用 subagent 路径
