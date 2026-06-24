# score_schema

A **SCORE-2017-aligned** schema for EEG reports (Beniczky et al., *Standardized Computer-based
Organized Reporting of EEG – Second version*, Clin Neurophysiol 2017), implemented as
[Pydantic v2](https://docs.pydantic.dev/) models.

This package is the **single source of truth** for the report data model. It is used to:

1. **validate and (de)serialise** OpenSCORE's `.score` files, and
2. export a **language-neutral JSON Schema** (`score_schema.json` at the repo root) that any
   other tool can consume — a future C++/Qt EDFBrowser fork, or schema-constrained ("guided")
   decoding for local-LLM extraction of structured data from free-text EEG reports.

> Pydantic is just the authoring binding. The **JSON Schema is the durable artefact** — it
> outlives any particular GUI language.

## Scope (clinical-core subset)

This implements the clinically central SCORE modules. Deferred: neonatal template (§16), RPPs
(§9), trend analysis (§14), polygraphic channels (§13), and full source-imaging localization.

| Model | SCORE-2017 section / table | New vs legacy OpenSCORE |
|---|---|---|
| `PatientInformation`, `Referral` | §2 Patient information & referral (Table 1) | ported |
| `RecordingConditions` | §3 Recording conditions | ported (+ multi-value alertness) |
| `ModulatorsAndProcedures` | §4 Modulators & procedures (Table 2) | **new** |
| `BackgroundActivity`, `PosteriorDominantRhythm`, `OrganisedRhythm` | §6 Background activity (Table 4) | ported |
| `SleepAndDrowsiness` | §7 Sleep & drowsiness | **new** |
| `InterictalFindings`, `InterictalGraphoelement`, `TimeRelatedFeatures` | §8 Interictal findings (Tables 5/6) | **new** |
| `Episodes`, `Episode`, `SemiologyPhase` | §10 Episodes / ictal (Tables 9–13) | **new** |
| `DiagnosticSignificance` | §15 Diagnostic significance (Table 17) | formalised |
| `ClinicalComments` | Clinical comments | ported |

## Design notes

- **Legacy-compatible keys.** Every field carries an `alias` equal to OpenSCORE's existing
  human-readable `.score` key (e.g. `"Posterior dominant rhythm"`). Dump with
  `model_dump(mode="json", by_alias=True)` to reproduce the `.score` shape; `populate_by_name`
  also lets you construct models with the Python field names.
- **Tristate (`Ternary`).** Fixes the legacy null/`false` ambiguity (issues #23/#24): an
  unconsidered feature is `not_assessed`, distinct from a deliberate `absent`.
- **Deliberate diagnosis (issue #24).** `DiagnosticSignificance.diagnosis` defaults to `None`,
  never silently `"Normal"`.
- **Multi-value alertness (issue #17).** `RecordingConditions.alertness` is a list.
- **Enums for bounded SCORE choice lists.** These export into the JSON Schema as `enum`
  constraints — the vocabulary a guided-decoding LLM is restricted to.
- **Provenance hook.** `EegReport.provenance` (`"Extraction"`) is an optional, forward-compatible
  place for the deferred extractor to record model + confidence for inter-model agreement testing.

## Relationship to HED-SCORE

[HED-SCORE](https://hed-schemas.readthedocs.io/en/latest/hed_score_schema.html) is a HED
*library schema* — a controlled **tag vocabulary** for annotating events in EEG **time-series
recordings** (BIDS `events.tsv`). It encodes the SCORE *findings* terminology but, by design,
**does not** model a report document: it excludes patient/administrative data, diagnostic
significance, and clinical comments.

The two are complementary, so we use both:

- `score_schema` remains the **report-document model** (the thing report-extraction outputs).
- The **findings vocabulary** here (interictal morphology, time-related features, episode types,
  sleep graphoelements, special patterns) uses **HED-SCORE node names as enum values**, pinned to
  `score_schema.hed.HED_SCORE_VERSION` (`score_2.1.0`). So a finding's value *is* its HED short
  tag, and `score_schema.hed.hed_tag(value)` yields a namespaced tag (e.g. `sc:Sharp-wave`).
- Findings/episodes carry an optional `hed_tags` list (`"HED tags"`) for explicit HED export to
  BIDS/HED tooling (`hedtools`).

PDR/recording/diagnostic fields keep human-readable SCORE wording (HED-SCORE has no equivalent, or
its node names are unwieldy). Verify node spellings against the schema file with `hedtools` before
extending the aligned enums.

## Usage

```python
from score_schema import EegReport, validate

report = EegReport.load("example.score")     # read + validate
report.diagnostic_significance.diagnosis      # -> Diagnosis.ABNORMAL | None
report.save("example.score")                  # validated write (4-space indent)

validate(some_dict)                           # raises pydantic.ValidationError on bad data
```

Regenerate the JSON Schema artefact after changing any model:

```
python -m score_schema.export_schema      # writes ../score_schema.json
```

Run the tests:

```
python -m pytest tests/test_score_schema.py -q
```
