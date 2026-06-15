## Context

`partition_batches.py` 和 `quality_gate.py` 使用 Python 内置 `len()` 做字符计数，在混合中英文场景下偏差严重：cl100k_base 编码下中文字符密度约为英文字符的 8.8 倍。这导致两个具体问题：

1. **Batch 划分不均匀**：同样 1500 字符的阈值，纯英文 block 可能只有 ~375 token（batch 太小浪费上下文），纯中文 block 可能达到 1500+ token（容易超限）。
2. **质量门禁阈值不对称**：EN→ZH 正常翻译的字符长度比典型值为 0.3–0.8，ZH→EN 为 1.5–3.0，同一套阈值（0.3–3.0）下两种语言方向实际分布在窗口的两端。改用 token 比后两种方向一致收敛到 0.5–1.5。

项目当前已有 tiktoken 依赖（在 `$HOME/.ar` 共享运行环境中），因此无需新增依赖安装步骤。

## Goals / Non-Goals

**Goals:**
- 将两处核心计数逻辑从 `len()` 字符替换为 tiktoken cl100k_base 精确 token 计数
- 确保 batch 划分在混合语言场景下均衡
- 确保质量门禁的 lazy_translation 检查在两种语言方向下表现一致
- 更新所有文档、schema、输出字段中的"字符"命名
- 保持所有阈值数值不变（0.3–3.0），只改变度量单位

**Non-Goals:**
- 不改变 quality_gate 中语言检查的 CJK 字符统计逻辑（那是 Unicode 分类，非长度计数）
- 不改变 `blockify.py`、`sentencify.py` 等与长度计数无关的脚本
- 不改变 `pipeline_test.py`（不消费长度字段名）
- 不调整默认 batch size 数值（1500 的语义从字符变为 token 后实际效果更合理）
- 不处理 tiktoken 编码回退或错误处理（cl100k_base 是标准编码，无退化路径）

## Decisions

### Decision 1: 惰性单例编码器模式

- **Chosen**: 模块级全局变量 + 线程安全的惰性初始化
  ```python
  _ENCODER = None
  def _count_tokens(text: str) -> int:
      global _ENCODER
      if _ENCODER is None:
          _ENCODER = tiktoken.get_encoding("cl100k_base")
      return len(_ENCODER.encode(text))
  ```
- **Alternatives**: 每次调用 `tiktoken.get_encoding()` 创建新编码器；在主入口处提前初始化
- **Rationale**: `tiktoken.get_encoding()` 内有缓存，调用多次也无显著开销。但每次调用仍有字典查找和 Python 函数调用开销。模块级单例将开销压缩到一次。`_count_tokens()` 函数封装比直接 inline 更易维护和测试。
- **Trade-off**: 简单直接，无多线程安全需求（项目为串行脚本），无退化路径。

### Decision 2: 使用 cl100k_base 编码

- **Chosen**: `tiktoken.get_encoding("cl100k_base")`
- **Rationale**: cl100k_base 是 GPT-4/GPT-4-turbo/GPT-3.5-turbo 使用的基础编码。项目的翻译模型上下文也是基于类似 GPT 系架构。o200k_base（GPT-4o 系列）的 token 分布不同，但本项目不直接消费 GPT-4o 输出，使用一致的编码更合理。`len(encoder.encode(text))` 是 tiktoken 的标准用法。
- **Trade-off**: 如果将来切换翻译模型编码方式，需要同步更新此编码器。但 batch 划分和门禁检查对精确 token 数不敏感（±10% 不影响决策），cl100k_base 的兼容性窗口较宽。

### Decision 3: 阈值不变

- **Chosen**: 保留 0.3–3.0 的阈值，不做任何调整
- **Rationale**: 字符计数下，EN→ZH 正常翻译比 0.3–0.8（贴下限），ZH→EN 正常翻译比 1.5–3.0（贴上限制）。0.3–3.0 窗口看似宽松，实际被语言方向差异消耗了大部分空间。改用 token 计数后，两种语言方向的 ratio 收敛到 0.5–1.5，0.3–3.0 的窗口实际上收窄了有效范围（排除了极端异常值如偷懒翻译 ratio < 0.1），更安全而非更宽松。
- **Trade-off**: 无。

### Decision 4: 输出字段重命名

- **Chosen**: 所有 JSON 输出字段中的 `_chars` 后缀统一改为 `_tokens`
- **Rationale**: 这是 breaking change，但项目的中间产物 JSON 均由脚本自动生成和消费，无人工依赖。下游消费方（`concatenate.py`、`export_qa_report.py`）不直接引用这些字段名。提前改比积累到后期改更合适。
- **Trade-off**: 已有运行目录中的中间产物字段名不一致，需重新生成。

## Risks / Trade-offs

- **Token 计数性能开销**：`tiktoken.encode()` 比 `len()` 慢约 2–3 个数量级（µs vs ns）。但项目运行在翻译 pipeline 中，翻译本身的 LLM 调用延迟是秒级，token 计数的额外开销（每 batch 几百次 encode，总计数毫秒级）可忽略。
- **编码器不可用**：cl100k_base 是 tiktoken 内置预置编码，无需下载文件，不存在网络依赖或文件丢失问题。风险极低。
- **字段名兼容性**：已有中间产物中的 `_chars` 字段不会被新代码消费。旧脚本版本与新产物不兼容的问题只会在切换过程中出现；全量改动后所有生成和消费端统一为 `_tokens`，无兼容期。
