## ADDED Requirements

### Requirement: Input parsing and normalization

The system SHALL accept a source file path and target language, detect input type (Markdown/PDF/LaTeX/directory), and normalize to a standard Markdown intermediate format.

#### Scenario: Markdown input

- **WHEN** source_path points to a valid `.md` file
- **THEN** the system SHALL copy the file to `workspace/normalized.md` and output metadata JSON with type `markdown`

#### Scenario: PDF input

- **WHEN** source_path points to a `.pdf` file
- **THEN** the system SHALL detect PDF type and instruct the agent to use an external extraction tool (e.g. mineru) to convert to Markdown

#### Scenario: LaTeX directory input

- **WHEN** source_path points to a directory containing `.tex` files
- **THEN** the system SHALL locate the main `.tex` file (containing `\documentclass`), convert LaTeX constructs to Markdown, and write `workspace/normalized.md`

#### Scenario: Unsupported format

- **WHEN** source_path points to an unsupported file type (e.g. `.png`, `.docx`)
- **THEN** the system SHALL report a blocker and output a failure JSON with status `failed`

### Requirement: Macro analysis and glossary generation

The agent SHALL read the full normalized text, produce a macro analysis report (source language, document type, research field, summary), and build a case-sensitive glossary of technical terms.

#### Scenario: Glossary construction

- **WHEN** the agent reads the normalized text and identifies technical terms
- **THEN** the glossary SHALL contain `{"original": "translation"}` pairs for terms that should be translated, and identity pairs (`{"term": "term"}`) for terms that must remain untranslated (e.g. model names like `Transformer`, author names)

#### Scenario: Language equality detection

- **WHEN** source language equals target language
- **THEN** the system SHALL terminate execution with a cancelled status JSON, without entering translation

### Requirement: Block-level splitting (agent-driven)

The agent SHALL semantically split the normalized text into blocks, marking each with `<!-- BLOCK: id | type: type -->` markers. This step MUST be performed by the LLM, not by scripts.

#### Scenario: Block type identification

- **WHEN** the agent encounters a display equation (`$$...$$` or `\[...\]`)
- **THEN** the equation SHALL be a single block of type `equation` and SHALL NOT be split across blocks

#### Scenario: Code block integrity

- **WHEN** the agent encounters a fenced code block
- **THEN** the entire code block SHALL be a single block of type `code` and SHALL NOT be split

#### Scenario: Adjacent short block merging

- **WHEN** multiple adjacent blocks have the same type (e.g., consecutive paragraphs under the same section)
- **THEN** the agent SHOULD merge them into a single block to reduce batch fragmentation

### Requirement: Sentence-level splitting (script-driven)

The system SHALL call `scripts/sentencify.py` to split block content into individual sentences by punctuation boundaries.

#### Scenario: Normal paragraph splitting

- **WHEN** a paragraph block contains multiple sentences ending with `.`, `!`, `?`, `。`, `！`, `？`
- **THEN** the system SHALL split into separate sentence strings, preserving sentence order

#### Scenario: No-split block types

- **WHEN** the block type is `equation` or `code`
- **THEN** the entire block content SHALL be kept as a single sentence element without splitting

### Requirement: Translation batch partitioning

The system SHALL call `scripts/partition_batches.py` to divide sentences into balanced batches for translation, keeping each block's sentences intact within the same batch.

#### Scenario: Balanced partitioning

- **WHEN** the sentences JSON contains blocks with total characters exceeding the target batch size (default 1500 characters)
- **THEN** the system SHALL partition into multiple batches, each as close to the target size as possible while never splitting a block across batches

### Requirement: Translation execution with quality gate

Each batch SHALL be translated, then validated by `scripts/quality_gate.py` before acceptance.

#### Scenario: Subagent delegation (optional)

- **WHEN** the environment supports subagent delegation
- **THEN** the system MAY delegate each batch to a subagent following the protocol in `references/subagent-protocol.md`

#### Scenario: Quality gate sentence count check

- **WHEN** `scripts/quality_gate.py` runs on a translated batch
- **THEN** it SHALL verify the number of translated sentences matches the original, and report `passed: false` if mismatched

#### Scenario: Quality gate lazy translation check

- **WHEN** `scripts/quality_gate.py` runs on a translated batch
- **THEN** it SHALL verify the character length ratio (translation / original) is at least 0.3 and at most 3.0, and report `passed: false` if outside this range

#### Scenario: Quality gate retry limit

- **WHEN** a batch fails quality gate for the 3rd consecutive time
- **THEN** the agent SHALL report a blocker and stop

### Requirement: Translation assembly

The system SHALL call `scripts/concatenate.py` to assemble all translated blocks back into a complete Markdown document, preserving original block order and untranslated content (equations, code).

#### Scenario: Successful assembly

- **WHEN** all blocks have corresponding translations
- **THEN** the script SHALL output `workspace/assembled.md` with all translated content in original block sequence

#### Scenario: Missing translation

- **WHEN** one or more blocks lack a corresponding translation
- **THEN** the script SHALL report `status: incomplete`, list missing block IDs, and keep original content for missing blocks

### Requirement: Final review and polish

The agent SHALL review the assembled document for fluency, terminology consistency, formula/code integrity, and structural completeness before outputting the final result.

#### Scenario: Formula preservation check

- **WHEN** the agent reviews the assembled document
- **THEN** all formula blocks SHALL remain in their original form, unmodified

#### Scenario: Output delivery

- **WHEN** final polish is complete
- **THEN** the system SHALL copy the result to `workspace/output_<target_language>.md` and report the output path to the user
