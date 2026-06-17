# literature-translator Specification

## Purpose
TBD - created by archiving change first-version-literature-translator. Update Purpose after archive.
## Requirements
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

### Requirement: Macro analysis and glossary generation

The agent SHALL read the full normalized text, produce a macro analysis report (source language, document type, research field, summary), and build a case-sensitive glossary of technical terms.

#### Scenario: Glossary construction

- **WHEN** the agent reads the normalized text and identifies technical terms
- **THEN** the glossary SHALL contain `{"original": "translation"}` pairs for terms that should be translated, and identity pairs (`{"term": "term"}`) for terms that must remain untranslated (e.g. model names like `Transformer`, author names)

#### Scenario: Language equality detection

- **WHEN** source language equals target language
- **THEN** the system SHALL terminate execution with a cancelled status JSON, without entering translation

### Requirement: Block-level splitting (script-first + agent review)

The system SHALL call `scripts/blockify.py` for deterministic block-level splitting, then the agent SHALL review and correct the output. Block markers use `<!-- BLOCK: id | type: type -->` format.

#### Scenario: Script detects structural elements

- **WHEN** the script encounters a display equation (`$$...$$` or `\[...\]`)
- **THEN** the equation SHALL be a single block of type `equation` and SHALL NOT be split across blocks
- **WHEN** the script encounters a fenced code block
- **THEN** the entire code block SHALL be a single block of type `code` and SHALL NOT be split
- **WHEN** the script encounters HTML `<table>` tags
- **THEN** the entire table SHALL be captured as a single block of type `table`

#### Scenario: Agent review and fix

- **WHEN** the script outputs `workspace/blocked.md`
- **THEN** the agent SHALL review the block markers and fix misclassifications, missed headings, wrong types, and merge adjacent same-type blocks as needed before proceeding to Phase 5

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

### Requirement: Translation assembly

The system SHALL call `scripts/concatenate.py` to assemble all translated blocks back into a complete Markdown document, preserving original block order and untranslated content. The system SHALL first restore placeholders via `scripts/restore_placeholders.py` before assembly.

#### Scenario: Placeholder restoration before assembly (v2)
- **WHEN** translations pass review and repair
- **THEN** the system SHALL call `scripts/restore_placeholders.py` before concatenation
- **THEN** the restored translations SHALL be used as input to concatenate

### Requirement: Final review and polish

The agent SHALL review the assembled document for fluency, terminology consistency, formula/code integrity, and structural completeness before outputting the final result. The polish phase SHALL be restricted to language fluency improvements only and SHALL NOT modify document structure.

#### Scenario: Structural preservation constraint (v2)
- **WHEN** the agent polishes the assembled document
- **THEN** the agent SHALL NOT merge or split paragraphs
- **THEN** the agent SHALL NOT add or delete content
- **THEN** the agent SHALL NOT modify formula, code, citation numbers, or heading levels
- **THEN** the agent SHALL NOT change glossary-locked terminology

#### Scenario: Additional output artifacts (v2)
- **WHEN** final polish is complete
- **THEN** the system SHALL produce `workspace/alignment.json` (bilingual alignment data)
- **THEN** the system SHALL produce `workspace/qa_report.json` (quality report)

### Requirement: Fast-exit on language equality

The system SHALL exit immediately after input parsing when the user provides an explicit source_language that matches the target_language.

#### Scenario: User provides matching languages
- **WHEN** input.source_language is provided and equals parameter.target_language
- **THEN** the system SHALL output a cancelled-status JSON to stdout
- **THEN** the system SHALL NOT proceed to Phase 2 (macro analysis) or any translation phases

#### Scenario: Fallback to LLM detection
- **WHEN** source_language is NOT provided by the user
- **THEN** the system SHALL proceed to Phase 2 for LLM-based language detection
- **THEN** Phase 3 SHALL still compare detected source_language with target_language as a safety net

### Requirement: Stdout JSON contract

The system SHALL output exactly one JSON object to stdout, conforming to assets/output.schema.json.

#### Scenario: Success output
- **WHEN** translation completes successfully
- **THEN** stdout SHALL contain a JSON object with status="success" and artifact paths

#### Scenario: Cancelled output
- **WHEN** the pipeline is cancelled (language equality or other reason)
- **THEN** stdout SHALL contain a JSON object with status="cancelled" and a reason field

#### Scenario: Failure output
- **WHEN** an unrecoverable error occurs
- **THEN** stdout SHALL contain a JSON object with status="failed" and an error description in the reason field

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

### Requirement: Quality report export

The system SHALL export a structured quality report summarizing all checks, repairs, and risks.

#### Scenario: Report structure
- **WHEN** the pipeline completes
- **THEN** the system SHALL generate `workspace/qa_report.json`
- **THEN** the report SHALL contain summary (total blocks, units, passed/repaired/risky counts)
- **THEN** the report SHALL contain check results per check type (passed/warning/failed/skipped)
- **THEN** the report SHALL list all repaired items with error type and repair count
- **THEN** the report SHALL list all risky items with reason, source, and best translation

### Requirement: Glossary v2 three-level structure

The glossary SHALL support a three-level structure distinguishing locked terms, provisional terms, and keep-english terms.

#### Scenario: V2 glossary structure
- **WHEN** the system reads `workspace/glossary.json`
- **THEN** it SHALL support both v1 flat format and v2 three-level format
- **THEN** in v2 format, `locked` terms MUST be used exactly as specified
- **THEN** in v2 format, `keep_english` terms SHALL be preserved in English and excluded from language checks

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

