# literature-translator Specification (v2 Delta)

## ADDED Requirements

### Requirement: Inline placeholder protection

The system SHALL protect inline elements within sentences by replacing them with deterministic placeholders before translation, and restore them after translation completes.

#### Scenario: Inline math protection
- **WHEN** a sentence contains `$...$` inline math (e.g., `$\alpha$`, `$\mathbf{x}_i$`)
- **THEN** the system SHALL replace the inline math with `<MATH_NNN>` placeholder before translation
- **THEN** the system SHALL restore the original math after translation completes

#### Scenario: Citation reference protection
- **WHEN** a sentence contains citation references (e.g., `[1]`, `[1, 2]`)
- **THEN** the system SHALL replace the reference with `<REF_NNN>` placeholder before translation

#### Scenario: Figure/Table/Equation reference protection
- **WHEN** a sentence contains `Fig. N`, `Table N`, or `Eq. (N)` references
- **THEN** the system SHALL replace with `<FIG_NNN>`, `<TBL_NNN>`, or `<EQ_REF_NNN>` placeholder respectively

#### Scenario: Numeric value protection
- **WHEN** a sentence contains percentages (e.g., `95%`), p-values (e.g., `p < 0.05`), or ranges (e.g., `5-10`)
- **THEN** the system SHALL replace the value with `<NUM_NNN>` placeholder

#### Scenario: Known entity protection
- **WHEN** a sentence contains terms from glossary `keep_english` list
- **THEN** the system SHALL replace the entity with `<ENT_NNN>` placeholder

#### Scenario: Placeholder restoration
- **WHEN** all translations are complete
- **THEN** the system SHALL restore all placeholders to their original values using the placeholder map
- **THEN** the restored text SHALL be identical to the original pre-protection value

### Requirement: Enhanced quality gate checks

The quality gate SHALL perform 8 checks on each translated batch (up from 4), including 4 new checks for placeholder preservation, numeric/reference preservation, non-translation language detection, and per-block-type length validation.

#### Scenario: Placeholder preservation check
- **WHEN** `scripts/quality_gate.py` runs with a `--placeholder-map` argument
- **THEN** it SHALL verify that all input placeholders appear in the translated sentences
- **THEN** it SHALL verify that no unexpected placeholders are introduced in the output
- **THEN** it SHALL report `passed: false` if any input placeholder is missing or any unexpected placeholder appears

#### Scenario: Numeric/reference preservation check
- **WHEN** `scripts/quality_gate.py` runs on a translation
- **THEN** it SHALL verify that NUM, REF, FIG, TBL, EQ_REF type placeholders are preserved
- **THEN** it SHALL report `passed: false` if any numeric or reference placeholder is missing

#### Scenario: Non-translation language detection
- **WHEN** `scripts/quality_gate.py` scans translated text
- **THEN** it SHALL check for explanation/summary phrases ("大意是", "可以理解为", "简而言之", etc.)
- **THEN** it SHALL report `passed: false` and list violations if such phrases are found

#### Scenario: Per-block-type length check
- **WHEN** `scripts/quality_gate.py` measures translation length ratios
- **THEN** it SHALL apply type-specific thresholds (e.g., paragraph: 0.25-2.50, caption: 0.35-2.80)
- **THEN** violations SHALL be reported as warnings only (is_weak: true) and SHALL NOT affect pass/fail

#### Scenario: Language check with allowlist
- **WHEN** `scripts/quality_gate.py` checks language correctness
- **THEN** it SHALL remove `keep_english` terms, placeholders, URLs, and model names from the text before computing CJK ratio
- **THEN** the resolved text SHALL be used for term consistency checking

### Requirement: Structured translation review

The system SHALL perform a structured semantic review of all translated content before assembly, using a dedicated reviewer that outputs categorized error reports.

#### Scenario: Reviewer input construction
- **WHEN** all batches pass quality gate
- **THEN** the system SHALL construct a review input with source-translation pairs, context_profile, and glossary
- **THEN** each sentence pair SHALL include block_id, sentence_index, source text, and translated text

#### Scenario: Error type classification
- **WHEN** the reviewer identifies a translation issue
- **THEN** it SHALL classify the error into one of 10 types: omission, addition, mistranslation, terminology, polarity, modality, relation, structure, placeholder, style
- **THEN** it SHALL assign severity (low/medium/high) and include source_span, translation_span, issue description, and repair instruction

#### Scenario: Verdict pass
- **WHEN** the reviewer finds no errors in the translation
- **THEN** it SHALL output `verdict: pass` with empty errors list

#### Scenario: Verdict fail
- **WHEN** the reviewer finds one or more errors
- **THEN** it SHALL output `verdict: fail` with a non-empty errors list

### Requirement: Local sentence repair

The system SHALL repair individual failed sentences based on reviewer output, without retranslating entire blocks.

#### Scenario: Targeted repair
- **WHEN** reviewer identifies medium or high severity errors
- **THEN** the system SHALL construct repair items for each failed sentence, including source text, current translation, issue description, and repair instruction
- **THEN** the repairer SHALL only modify the specified sentences and leave others unchanged

#### Scenario: Repair loop
- **WHEN** a repair is applied
- **THEN** the system SHALL re-run quality gate on the repaired batch
- **THEN** the system SHALL re-run reviewer on the repaired content
- **THEN** the repair SHALL be repeated up to 2 rounds maximum

#### Scenario: Risky sentence marking
- **WHEN** a sentence fails repair after 2 rounds
- **THEN** the system SHALL mark it as "risky"
- **THEN** the system SHALL keep the best available translation and the original source text in the final output

#### Scenario: Fallback to full retranslation
- **WHEN** more than 50% of sentences in a block have errors
- **THEN** the system SHALL fall back to full block retranslation instead of local repair

### Requirement: Bilingual alignment export

The system SHALL export sentence-level bilingual alignment data after translation completes.

#### Scenario: Alignment file structure
- **WHEN** translation and review are complete
- **THEN** the system SHALL generate `workspace/alignment.json`
- **THEN** each block SHALL contain its type, heading, and sentence-level pairs
- **THEN** each pair SHALL include original text, translated text, QA status (passed/repaired/risky), and repair count

#### Scenario: Alignment from restored translations
- **WHEN** alignment is exported
- **THEN** the system SHALL use restored translations (placeholders resolved) as the target text

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

## MODIFIED Requirements

### Requirement: Sentence-level splitting (script-driven)

The system SHALL call `scripts/sentencify.py` to split block content into individual sentences by punctuation boundaries. The script SHALL protect abbreviation periods from false splitting and normalize embedded newlines within paragraphs.

#### Scenario: Normal paragraph splitting (v2)
- **WHEN** a paragraph block contains multiple sentences ending with `.`, `!`, `?`, `。`, `！`, `？`
- **THEN** the system SHALL split into `[index, text]` pairs, preserving sentence order with 1-based indices

#### Scenario: No-split block types (v2)
- **WHEN** the block type is `equation` or `code`
- **THEN** the entire block content SHALL be kept as a single `[1, text]` pair without splitting

### Requirement: Translation execution with quality gate

Each batch SHALL be translated, then validated by `scripts/quality_gate.py` before acceptance. The quality gate SHALL support enhanced checks including placeholder preservation, numeric/reference preservation, non-translation language detection, and per-block-type length validation.

#### Scenario: Quality gate with placeholder map (v2)
- **WHEN** `scripts/quality_gate.py` runs on a translated batch with `--placeholder-map` provided
- **THEN** it SHALL resolve placeholders using the map before performing term consistency and language checks

#### Scenario: Enhanced quality gate output (v2)
- **WHEN** `scripts/quality_gate.py` produces output
- **THEN** the output SHALL include all 8 check fields: sentence_count, lazy_translation, term_consistency, language, placeholder_preservation, numeric_preservation, non_translation_phrases, length_check

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
