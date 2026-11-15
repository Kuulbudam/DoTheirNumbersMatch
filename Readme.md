# Do Their Numbers Match?

A pilot audit of quantitative claims about Nigeria's economy, each traced to its primary comparator.

**Live page:** https://kuulbudam.github.io/DoTheirNumbersMatch/

## Files

- `index.html`  interactive audit-workpaper viewer (the live page)
- `claims_final_revised_v2.csv`  dataset (source of truth)
- `DoTheirNumbersMatch_Workbook.xlsx`  six-sheet workbook
- `build_all.py`  regenerates `index.html` from the CSV
- `report.md`  written report

## Verdict rules

First rule that applies, in order:

1. Unverifiable
2. Source does not support claim
3. Definition mismatch
4. Period mismatch
5. Match
6. Rounding difference
7. Numerical discrepancy

## Evidence grades

- A  primary file opened
- B  official statement via a secondary copy (Match at this grade is provisional)
- C  not locatable in a primary source

## Limitations

- Small, selected pilot. Stress sample chosen for difficulty, reported separately.
- Records in one source group share a release; row counts overstate independent evidence.
- Single-annotator review. No agreement score.
- No model evaluation. Dataset and procedure, not a measure of AI accuracy.
- Labels describe claim-to-comparator relationship. Say nothing about honesty or intent.

## LLM use

Claude (Anthropic) assisted with drafting, taxonomy brainstorming, preliminary source discovery, and the evaluation script. All numerical claims, classifications, and verbatim excerpts were independently verified against primary statistical files.

## Citation

Kuulbudam, T. (2026). Do Their Numbers Match? An Independent Audit of Quantitative Claims in Nigerian Government Communications. Apart Research AI x Epistemics Sprint.
