## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: Input parsing and normalization

The system SHALL accept a source file path and target language, detect input type (Markdown/PDF/LaTeX/directory), and normalize to a standard Markdown intermediate format. The temporary working directory SHALL be `.literature_translator_tmp/`.

#### Scenario: Temporary directory creation
- **WHEN** the system starts processing
- **THEN** intermediate artifacts SHALL be written under `.literature_translator_tmp/`

#### Scenario: Final artifact output
- **WHEN** translation completes
- **THEN** final output files SHALL be written to the CWD (not under `.literature_translator_tmp/`)
