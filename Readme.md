# Do Their Numbers Match?

A pilot audit of quantitative claims about Nigeria's economy. Each claim is traced to its primary comparator and given a verdict under a fixed seven rule order.

Author: Trisma Kuulbudam  
Event: Apart Research AI x Epistemics Research Sprint, 13 to 15 November 2026

## Live page

https://kuulbudam.github.io/DoTheirNumbersMatch/

Open the link and click through it. No install is needed.

Index of records. Records are grouped by the source they share. Records in one group are not independent confirmations.

Workpaper. Select a record to see the claim, the comparator excerpt, the tie out and the decision ladder that shows which rule decided the verdict.

Reviewer sign-off. Tick the four checks and add a note. Your ticks are saved in your own browser only.

Exhibits. Three cross record exhibits recompute their arithmetic live from the inputs shown.

## Files

| File | What it is |
|---|---|
| `index.html` | The live page. It is self contained and includes all the data. |
| `claims_final.csv` | The claim comparator records, with verdicts, evidence status and notes. |
| `build_all.py` | Builds index.html from claims_final.csv. |
| `add_names.py` | Adds descriptive case names to the records in claims_final.csv. |

Python 3 is needed. Nothing else needs to be installed.

```bash
python build_all.py            # builds index.html and opens it in your browser
python build_all.py --serve    # builds, then serves it at http://127.0.0.1:8000/index.html
python build_all.py --no-open  # builds only
python build_all.py --only-verified   # hides provisional and unverifiable records
```

## How verdicts are decided

Each record gets the first rule that applies:

Unverifiable: the relevant figure cannot be located in the available evidence.

Source does not support claim: the cited source does not establish the statement.

Definition mismatch: different metric definitions or calculation conventions.

Period mismatch: different periods, base dates or statistical vintages.

Match: agrees at the stated precision.

Rounding difference: consistent after reasonable rounding or approximate wording.

Numerical discrepancy: a material difference remains after the checks above.

Evidence grades: A the primary file was opened. B an official statement reproduced by a secondary source; a Match at this grade is provisional. C not locatable in a primary source.

## Status and limits

This is a small pilot. The counts describe this dataset only. They are not estimates of how accurate Nigerian public communications are.

Natural and stress samples are reported separately and never pooled.

Records that share a release, statement or series are counted as one source group.

Single-annotator review. No agreement score is reported.

No model evaluation was run.

Labels describe how a statement relates to a comparator. They say nothing about a speaker's honesty or intent. Do not use this data to rank people or outlets.

## Preexisting code

No code in this repository was written before the sprint.

## Ethics

The data contains public statements, publication dates and public statistical releases only. There are no private communications or personal data. Names appear only to attribute a public statement in the speaker's public or professional capacity.

## LLM use

Claude (Anthropic) helped with drafting and taxonomy brainstorming.