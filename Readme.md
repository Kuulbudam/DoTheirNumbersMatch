# Do Their Numbers Match?

A pilot audit of quantitative claims about the Nigerian economy each traced to its primary comparator.

Live page: https://kuulbudam.github.io/DoTheirNumbersMatch/

## What this is

Public claims about inflation GDP exchange rates and reserves often quote official statistics. Two apparently different numbers do not always mean one is wrong. They may refer to different periods different definitions or different statistical vintages. This project builds the reconciliation layer. For each claim it records the official comparator the exact passage from the primary file and a classification of the relationship between the two.

## Dataset

Thirteen verified records in claims_final_revised_v2.csv. Fields:

- id sample natural-or-stress case_name
- claim_text speaker speaker_type date
- metric claimed_value claimed_period
- claim_url comparator primary_url
- primary_excerpt verbatim from the primary file
- primary_value label definition_note
- evidence_type primary-or-secondary
- independence_group CPI GDP Labour Exchange-rate Reserves
- status verified

## Reported outcome

Of thirteen verified records:

| Classification | Count |
|---|---|
| Match primary evidence grade A | 5 |
| Match provisional grade B | 3 |
| Unverifiable grade C | 2 |
| Rounding difference | 1 |
| Source does not support claim | 1 |
| Numerical discrepancy grade B | 1 |
| Total | 13 |

The thirteen records form six underlying evidence groups (CPI GDP Labour Exchange-rate Reserves). They are not independent observations. These are descriptive counts and not a population accuracy rate.

## Model evaluation

A small open weight language model (GLM 5.3 Flash temperature 0) was run against the twelve records available at the time of the evaluation. N31 was added afterwards and is not included in the model results.

The model reproduced seven of twelve classifications (58.3 per cent). Its five errors cluster on rows where evidence provenance or framing context matters:

- N07 and N21 (gold Unverifiable) classified as numerical discrepancy. The model cannot see the evidence grade.
- N17 (gold Match) classified as Unverifiable. The model cannot distinguish genuine ambiguity from a nearby alternative the auditor has already reconciled.
- N33 (gold Source does not support claim) classified as Match. Framing context is not recoverable from a single excerpt.
- N03 (gold Rounding difference) classified as Match. The 0.45 percentage point gap was not applied as rounding.

The finding: an automated checker without provenance information systematically over classifies as numerical error what a human auditor classifies as unverifiable.

## Verdict rules

First rule that applies in order:

1. Unverifiable the relevant figure cannot be located in the available evidence.
2. Source does not support claim the cited source does not establish the statement being checked.
3. Definition mismatch different metric definitions or calculation conventions.
4. Period mismatch different periods base dates or statistical vintages.
5. Match agrees at the stated precision.
6. Rounding difference consistent after reasonable rounding or approximate wording.
7. Numerical discrepancy a material difference remains after period definition and rounding checks.

## Evidence grades

- A primary file opened
- B official statement via a secondary copy a Match at this grade is provisional
- C not locatable in a primary source

## Rebuild

    python build_all.py claims_final_revised_v2.csv

Regenerates index.html from the CSV.

## Limitations

- Small selected pilot of thirteen records. The stress sample was chosen for difficulty and is reported separately.
- Records in one source group share a release so row counts overstate independent evidence.
- Single annotator review. No agreement score is reported.
- The model evaluation is exploratory. It runs on twelve records with a single model and seven of twelve accuracy is too small to support a general claim about model performance. Its value is qualitative. The five errors cluster on the specific failure modes the taxonomy is designed to catch.
- N31 (PDP claim of near 40 per cent inflation against an NBS May 2025 headline of 22.97 per cent) rests on secondary reporting of the NBS release. The primary NBS PDF was not opened and the row is graded B accordingly.
- Labels describe the relationship between a claim and its comparator. They say nothing about the honesty or intent of the speaker.

## LLM use

Claude (Anthropic) assisted with drafting taxonomy brainstorming preliminary source discovery and the evaluation script. All numerical claims classifications and verbatim excerpts were independently verified against primary statistical files.

## Citation

Kuulbudam T. (2026) Do Their Numbers Match? An Independent Audit of Quantitative Claims in Nigerian Government Communications. London: Apart Research AI x Epistemics Sprint. Available at: https://github.com/Kuulbudam/DoTheirNumbersMatch (Accessed: 15 November 2026).