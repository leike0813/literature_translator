## ADDED Requirements

### Requirement: Fast translation mode

The system SHALL support a `mode` parameter (`fast` | `high_quality`, default `fast`) that controls translation depth. Fast mode SHALL translate at block level without sentence splitting, placeholder protection, or structured review.

#### Scenario: Fast mode input construction
- **WHEN** mode is `fast` and Phase 5 starts
- **THEN** the system SHALL call `scripts/build_block_sentences.py` to produce a v2 sentences.json
- **THEN** each block SHALL be represented as a single `[1, content]` sentence entry
- **THEN** the system SHALL skip sentencify.py, protect_placeholders.py, and restore_placeholders.py

#### Scenario: Fast mode quality gate
- **WHEN** `quality_gate.py` runs with `--mode fast`
- **THEN** placeholder_preservation and numeric_preservation checks SHALL return `{"passed": true, "skipped": true}`
- **THEN** all other checks SHALL run as normal

#### Scenario: Fast mode review
- **WHEN** mode is `fast` and all batches pass quality gate
- **THEN** the main agent SHALL perform block-level quick scan (checking for untranslated text, severe mistranslation, summary-style translation)
- **THEN** the system SHALL NOT invoke structured reviewer or local repair

#### Scenario: Fast mode alignment export
- **WHEN** `export_alignment.py` runs with `--mode fast`
- **THEN** alignment SHALL output `"pairs": []` for each block
- **THEN** `source_markdown` and `translated_markdown` SHALL be populated normally

## MODIFIED Requirements

### Requirement: Input parsing and normalization

The system SHALL accept a source file path and target language, detect input type (Markdown/PDF/LaTeX/directory), and normalize to a standard Markdown intermediate format. The system SHALL also accept an optional `mode` parameter to control translation depth. The temporary working directory SHALL be `.literature_translator_tmp/`.

#### Scenario: Mode parameter
- **WHEN** the system starts processing
- **THEN** it SHALL read `mode` from parameter (default: `fast`, options: `fast` | `high_quality`)
- **THEN** the mode SHALL determine whether sentence-level splitting, placeholder protection, and structured review are executed

#### Scenario: Temporary directory creation
- **WHEN** the system starts processing
- **THEN** intermediate artifacts SHALL be written under `.literature_translator_tmp/`

#### Scenario: Final artifact output
- **WHEN** translation completes
- **THEN** final output files SHALL be written to the CWD (not under `.literature_translator_tmp/`)

### Requirement: Sentence-level splitting (script-driven)

**Only in high_quality mode.** The system SHALL call `scripts/sentencify.py` to split block content into individual sentences by punctuation boundaries. In fast mode, the system SHALL call `scripts/build_block_sentences.py` instead, which wraps each block's entire content as a single sentence.

#### Scenario: Normal paragraph splitting (v2)
- **WHEN** mode is `high_quality` and a paragraph block contains multiple sentences ending with `.`, `!`, `?`, `。`, `！`, `？`
- **THEN** the system SHALL split into `[index, text]` pairs, preserving sentence order with 1-based indices

#### Scenario: No-split block types (v2)
- **WHEN** the block type is `equation` or `code`
- **THEN** the entire block content SHALL be kept as a single `[1, text]` pair without splitting

#### Scenario: Fast mode block-level input
- **WHEN** mode is `fast`
- **THEN** `build_block_sentences.py` SHALL produce sentences.json where each block has exactly one sentence `[1, "full_content"]` and `sentence_count: 1`

### Requirement: Inline placeholder protection

**Only in high_quality mode.** The system SHALL protect inline elements within sentences by replacing them with deterministic placeholders before translation, and restore them after translation completes. In fast mode, this phase SHALL be skipped entirely.

#### Scenario: Fast mode skip
- **WHEN** mode is `fast`
- **THEN** protect_placeholders.py and restore_placeholders.py SHALL NOT be called
- **THEN** translation input SHALL use raw sentences.json without placeholder substitution

#### Scenario: Inline math protection
- **WHEN** a sentence contains `$...$` inline math
- **THEN** the system SHALL replace the inline math with `<MATH_NNN>` placeholder before translation
- **THEN** the system SHALL restore the original math after translation completes

#### Scenario: [truncated — all other placeholder scenarios unchanged]

### Requirement: Enhanced quality gate checks

The quality gate SHALL perform up to 8 checks on each translated batch. In fast mode, placeholder_preservation and numeric_preservation checks SHALL be skipped (no placeholder data available). The `--mode` parameter controls which checks run.

#### Scenario: Fast mode skipped checks
- **WHEN** `quality_gate.py` runs with `--mode fast`
- **THEN** placeholder_preservation SHALL return `{"passed": true, "skipped": true, "reason": "fast mode — no placeholders"}`
- **THEN** numeric_preservation SHALL return `{"passed": true, "skipped": true, "reason": "fast mode — no placeholders"}`

#### Scenario: [all other quality gate scenarios unchanged]

### Requirement: Structured translation review

**Only in high_quality mode.** The system SHALL perform a structured semantic review of all translated content before assembly. In fast mode, a block-level quick scan by the main agent SHALL replace the structured reviewer.

#### Scenario: Fast mode block-level scan
- **WHEN** mode is `fast` and all batches pass quality gate
- **THEN** the main agent SHALL read all translated blocks and check for untranslated text, severe mistranslation, and summary-style translation
- **THEN** problematic blocks SHALL be re-translated and replaced directly
- **THEN** no structured reviewer subagent SHALL be invoked

#### Scenario: [all high_quality reviewer scenarios unchanged]

### Requirement: Local sentence repair

**Only in high_quality mode.** The system SHALL repair individual failed sentences based on reviewer output. In fast mode, failed blocks SHALL be re-translated in full rather than repaired at sentence level.

#### Scenario: Fast mode block re-translation
- **WHEN** mode is `fast` and a block fails quality gate or block-level review
- **THEN** the entire block SHALL be re-translated (no sentence-level repair)
- **THEN** repairer subagent SHALL NOT be invoked

### Requirement: Bilingual alignment export

The system SHALL export sentence-level bilingual alignment data after translation completes. In fast mode, alignment SHALL contain empty pairs arrays with populated block-level source/translated markdown.

#### Scenario: Fast mode alignment
- **WHEN** `export_alignment.py` runs with `--mode fast`
- **THEN** each block SHALL have `"pairs": []`
- **THEN** `source_markdown` and `translated_markdown` SHALL contain the full block-level text
