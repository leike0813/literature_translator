## MODIFIED Requirements

### Requirement: Translation batch partitioning

The system SHALL call `scripts/partition_batches.py` to divide sentences into balanced batches for translation, keeping each block's sentences intact within the same batch. Batch size SHALL be measured in tokens (using tiktoken cl100k_base encoding) rather than characters.

#### Scenario: Balanced partitioning (token-based)
- **WHEN** the sentences JSON contains blocks with total tokens exceeding the target batch size (default 1500 tokens)
- **THEN** the system SHALL partition into multiple batches, each as close to the target token size as possible while never splitting a block across batches

### Requirement: Translation execution with quality gate

Each batch SHALL be translated, then validated by `scripts/quality_gate.py` before acceptance. The lazy_translation check SHALL use token-level ratio (tiktoken cl100k_base) instead of character-level ratio to compare original and translated text length. The quality gate SHALL support enhanced checks including placeholder preservation, numeric/reference preservation, non-translation language detection, and per-block-type length validation.

#### Scenario: Lazy translation check (token-based)
- **WHEN** `scripts/quality_gate.py` runs the lazy_translation check
- **THEN** it SHALL compute the length ratio as `sum(tokens(translated)) / max(sum(tokens(original)), 1)` using tiktoken cl100k_base encoding
- **THEN** the output SHALL contain `original_tokens` and `translated_tokens` fields instead of `original_chars` and `translated_chars`
- **THEN** the ratio threshold SHALL be `MIN_TOKEN_RATIO=0.3` and `MAX_TOKEN_RATIO=3.0`
