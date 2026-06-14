# pipeline-test Specification

## Purpose
TBD - created by archiving change block-sentencify-followup. Update Purpose after archive.
## Requirements
### Requirement: Pipeline structural test harness

The system SHALL provide `tests/pipeline_test.py` that runs blockify → sentencify → partition → mock translations → concatenate on given inputs and validates structural integrity.

#### Scenario: Structural checks

- **WHEN** the harness runs on any valid Markdown file
- **THEN** it SHALL verify BLOCK/BLOCK_END balance after blockify and concatenate
- **THEN** it SHALL verify no duplicate or missing block IDs
- **THEN** it SHALL verify no empty blocks exist in the assembled output
- **THEN** it SHALL verify every block's sentence count matches its line count in assembled output (one sentence per line)

### Requirement: Sentence splitting accuracy

The script SHALL NOT split on periods that are part of abbreviations, and SHALL normalize embedded newlines within paragraphs.

#### Scenario: Abbreviation protection

- **WHEN** the text contains common academic abbreviations (e.g., Fig., Dept., Comp., Sci., Dr., Prof., e.g., i.e., vs., al., cf.)
- **THEN** the script SHALL NOT split the sentence at that period
- **WHEN** a period is preceded by a single uppercase letter (J. in J. Smith)
- **THEN** the script SHALL NOT split the sentence at that period

#### Scenario: Embedded newline normalization

- **WHEN** a block's content contains single newlines within a paragraph (multi-line author affiliations, addresses, etc.)
- **THEN** the script SHALL normalize those newlines to spaces before sentence splitting, preserving the semantic flow

### Requirement: Concatenation integrity

The concatenation script SHALL preserve each translated sentence on its own line and produce balanced block markers.

#### Scenario: Sentence-per-line output

- **WHEN** concatenating translated sentences into the output document
- **THEN** each translated sentence SHALL appear on its own line (not joined with spaces into a single line)
- **WHEN** the script encounters non-translatable blocks (equation, code)
- **THEN** the original content SHALL be preserved line-by-line

#### Scenario: Block marker balance

- **WHEN** concatenation completes
- **THEN** every `<!-- BLOCK:` marker SHALL have exactly one corresponding `<!-- BLOCK_END:` marker in the output

