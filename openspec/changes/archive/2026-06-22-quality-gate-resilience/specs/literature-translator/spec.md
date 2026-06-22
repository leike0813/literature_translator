## MODIFIED Requirements

### Requirement: Enhanced quality gate checks

The quality gate SHALL perform up to 8 checks on each translated batch. The term_consistency check SHALL use substring matching for glossary entries where the translation differs from the original (i.e., terms that should be translated), and exact matching for "do-not-translate" terms where original equals translation. The quality gate SHALL also enforce a global retry budget to prevent individual batches from consuming all available time.

#### Scenario: Term consistency substring matching (translated terms)
- **WHEN** `check_term_consistency()` checks a glossary entry where `original != translation` (a term that should be translated)
- **THEN** it SHALL verify that the glossary-defined translation appears as a substring or as a token within the translated text
- **THEN** matching SHALL be case-insensitive
- **THEN** glossary translations shorter than 3 characters SHALL use exact matching to avoid false positives on common short words

#### Scenario: Term consistency exact matching (do-not-translate terms)
- **WHEN** `check_term_consistency()` checks a glossary entry where `original == translation` (a term that must remain in English)
- **THEN** it SHALL verify that the original term appears exactly in the translated text
- **THEN** matching SHALL be case-sensitive

#### Scenario: Fast mode skipped checks
- **WHEN** `quality_gate.py` runs in fast mode (detected from `mode.txt`)
- **THEN** placeholder_preservation SHALL return `{"passed": true, "skipped": true, "reason": "fast mode — no placeholders"}`
- **THEN** numeric_preservation SHALL return `{"passed": true, "skipped": true, "reason": "fast mode — no placeholders"}`

### Requirement: Translation execution with quality gate (retry budget)

Each batch SHALL be translated and validated by quality gate. The system SHALL enforce retry limits: individual batches SHALL be retried at most 2 times (3 total attempts), and the global retry count across all batches SHALL not exceed 10. Batches exceeding the per-batch limit SHALL be marked as `risky` with their best available translation retained. When the global limit is exceeded, remaining failed batches SHALL be accepted as-is with warnings.

#### Scenario: Per-batch retry limit
- **WHEN** a batch fails quality gate 2 times (3 total attempts)
- **THEN** the agent SHALL mark the batch as `risky` and retain the best available translation
- **THEN** the agent SHALL proceed to the next batch without further retries on the failed one

#### Scenario: Global retry budget
- **WHEN** the total number of quality gate retries across all batches reaches 10
- **THEN** all remaining failed batches SHALL be accepted as-is with a warning marker
- **THEN** the agent SHALL NOT retry any more batches and SHALL proceed to Phase 8

#### Scenario: Retry context enrichment
- **WHEN** the agent retries a failed batch translation
- **THEN** the agent SHALL first output a "failure-to-fix" mapping table listing each failed check, the specific violation, the root cause analysis, and the concrete fix plan
- **THEN** the agent SHALL include the list of required placeholders in the retry prompt
- **THEN** the agent SHALL explicitly re-verify that all placeholders from the original batch are present after retranslation
