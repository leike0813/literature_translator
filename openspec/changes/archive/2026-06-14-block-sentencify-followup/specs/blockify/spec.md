## ADDED Requirements

### Requirement: Deterministic block-level splitting

The system SHALL call `scripts/blockify.py` to perform deterministic block-level splitting on normalized Markdown output, producing block markers compatible with `sentencify.py`.

#### Scenario: Heading strategy detection

- **WHEN** the input Markdown contains `##` or `###` headings
- **THEN** the script SHALL use `proper_nesting` strategy (level determined by `#` count)
- **WHEN** ALL headings use exactly one `#`
- **THEN** the script SHALL use `flat_single_hash` strategy (level inferred from section numbering)

#### Scenario: Structural element detection

- **WHEN** encountering `$$...$$` delimiters
- **THEN** the script SHALL treat the enclosed content as an `equation` block, preserving delimiters and `\tag{}`
- **WHEN** encountering `<table...>`...`</table>`
- **THEN** the script SHALL treat the enclosed content as a `table` block
- **WHEN** encountering `![](...)` image references
- **THEN** the script SHALL create a `figure_caption` block including the image line and following caption text

#### Scenario: Agent review step

- **WHEN** the script produces `workspace/blocked.md`
- **THEN** the agent SHALL review block markers and fix misclassifications (missed headings, wrong types, unmerged adjacent paragraphs) before proceeding to Phase 5

### Requirement: Headless 70/70 pass on example corpus

The system SHALL pass all structural integrity checks on the 70-example corpus without crashes or data loss.

#### Scenario: Full corpus integrity

- **WHEN** the script runs on all 70 example papers
- **THEN** every output SHALL have balanced BLOCK/BLOCK_END markers
- **THEN** every output SHALL have unique, sequential block IDs without gaps or duplicates
- **THEN** no block SHALL be empty
