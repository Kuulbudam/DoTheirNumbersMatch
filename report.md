# Do Their Numbers Match? An Independent Audit of Quantitative Claims in Nigerian Government Communications

## Abstract

Official statements routinely quote macroeconomic figures that are checked, if at all, by hand. We build an auditable pilot dataset of [FILL: N] claim–source pairs from Nigerian fiscal communications, each with a verbatim excerpt from the primary statistical file, a seven-way reconciliation classification, and a source register. Of the verified rows, [FILL: X]% are exact matches at the stated precision. The remaining discrepancies fall into three types that binary fact-checking cannot distinguish: rounding and framing differences, period-base differences (the same CBN exchange-rate series yields 6.51%, 6.96%, and 7.4% depending on which closing quote and which denominator are used), and definitional differences (an NBS Consumer Price Index rebasing revised the published November 2025 figure, flipping the direction of a December "eased from November" claim). We make no claim about intent. The contribution is the reconciliation layer — an audit trail a journalist, regulator, or citizen can walk from a claim to a primary statistic — and a demonstration that most apparent mismatches in the pilot are definitional or period-based rather than numerical. The sample is a pilot; it does not generalise to all Nigerian government communications.

## 1. Introduction

When a minister says inflation is 14.45%, or a reporting outlet says the naira gained 7.4% in 2025, the claim can be checked against the official statistical release. But checking it properly requires three steps that are tedious to do by hand: locate the primary file, extract the comparable figure, and decide whether any difference is a lie, a rounding convention, or a definitional gap. The third step is where most errors happen. A claim can be numerically wrong, or it can be right under a different metric definition, a different period, or a different rounding convention. The difference matters for how the claim should be reported.

This paper builds the reconciliation layer for a pilot sample of Nigerian fiscal claims. Each row of the accompanying dataset records the claim, the speaker, the claimed value and period, a link to where the claim was made, the official comparator, a verbatim passage from the primary statistical file, and one of seven classifications: Exact Match, Rounding Difference, Period Mismatch, Definition Mismatch, Numerical Discrepancy, Unverifiable, or Source Does Not Support Claim.

Contributions: (1) an auditable dataset structure with excerpt-level verification for every row; (2) a seven-way reconciliation taxonomy with a fixed priority order that prevents overlapping classifications; (3) two case studies showing how the same official number can appear under different percentages in reporting; (4) a methodology that a second researcher can replicate row by row.

No intent attribution is made. Classifications describe the relationship between a claim and its cited source, not the speaker's motive.

## 2. Related Work

**Claim verification.** AVeriTeC provides a benchmark of real-world claims paired with web evidence. Our task differs in that the comparator is a specific official statistical release, and the classifications distinguish definitional and period differences from numerical discrepancies.

**Model honesty benchmarks.** MASK, DarkBench, SycEval, and ELEPHANT probe model honesty, manipulation, and sycophancy. They test models, not public claims, and do not provide an excerpt-level audit trail back to a primary statistical file.

**Journalism fact-checking.** Africa Check, Dubawa, and Premium Times publish manual fact-checks that establish claims and verdicts. They do not publish structured reconciliation data in a form a second researcher can reproduce. Our dataset fills that layer.

## 3. Methodology

### 3.1 Scope

Numerical claims about Nigerian macroeconomic indicators — headline and food inflation, GDP growth, unemployment, oil production, FAAC allocation, exchange rate, external reserves — published between January 2025 and December 2025 by federal institutions, state governments, opposition parties, or reporting outlets.

### 3.2 Collection rule

The natural sample was collected under a fixed rule: for each speaker-type × metric cell, the first three qualifying documents in reverse-chronological order, with no claim excluded on the basis of its expected classification. The stress sample was chosen for claims involving rounding, period mixing, definitional ambiguity, or missing primaries. The two are reported separately and never pooled.

### 3.3 Verification

For each row, the primary statistical publication was opened and the comparable figure located. A row was marked `verified` only if the exact sentence containing the figure was pasted from the primary file. Rows without a pasted excerpt are excluded from every metric. Seven checks were applied to every row: indicator identity, reporting period, unit consistency, definitional consistency, comparison period, revision status, and rounding.

### 3.4 Classification order

Each row was assigned the first applicable classification: (1) Unverifiable — primary figure not locatable; (2) Source Does Not Support Claim — cited publication does not establish the claim; (3) Definition Mismatch — different metric definition; (4) Period Mismatch — different reporting period or base date; (5) Exact Match — equal at stated precision; (6) Rounding Difference — gap explained by rounding or framing; (7) Numerical Discrepancy — genuine disagreement after all methodological differences.

### 3.5 Reproducibility

Every row can be independently checked: open `claim_url`, open `primary_url`, find the sentence in the verbatim excerpt, compare claimed and primary values, read the classification and explanation. The workbook contains a Data Dictionary sheet defining every field and a Source Register listing every URL.

## 4. Results

### 4.1 Dataset composition

[FILL: paste from build_all.py output — "N verified claims, label distribution, by institution, by indicator"]

### 4.2 Discrepancy rates

[FILL: "Of the N verified claims, X were exact matches, Y rounding differences, Z period mismatches, W definition mismatches, V numerical discrepancies, U unverifiable."]

### 4.3 Case study: the naira close of 2025

Three outlets reported the same CBN close as three different appreciation figures. The official year-on-year series closes at N1,435.75 against N1,535.82 at end-2024, a 6.51% gain. A separate 7.4% gain is measured from the 2 January 2025 opening of N1,541.36. A third outlet reported N1,429 and 7.4%, using a different closing quote and the new-rate denominator. The three percentages are all internally consistent with their own inputs. The differences come from two choices — which intraday quote is treated as the close, and whether the denominator is the old or new rate — that are not disclosed in the reporting. This is not a lie; it is an unaudited convention. A binary checker would flag at least one of the three as wrong. A reconciliation taxonomy separates the truth from the convention.

### 4.4 Case study: CPI rebasing

The November 2025 headline CPI was originally published as 14.45%. The December 2025 CPI release revised November to 17.33% and reported December at 15.15%. A claim that December "eased from November" is true against the revised November but false against the originally published November: 15.15% is lower than 17.33% but higher than 14.45%. This is a period-vintage mismatch — the same agency revised the same month — and it cannot be caught by comparing a claim to a single PDF. The classification depends on which vintage of the November comparator the claim is checked against. This is a structural feature of statistical revision, not a defect in the claim.

### 4.5 Answer to the research question

In the pilot, most apparent mismatches are definitional, period-based, or rounding, not numerical. The verified set contains no confirmed numerical discrepancy; the two candidates identified during collection were excluded because their primary excerpts could not be pasted within the sprint window. The pilot therefore does not establish that numerical discrepancies are rare in Nigerian government communications — it establishes that when a fixed reconciliation procedure is applied to a sample, most apparent discrepancies resolve into rounding, definitional, or period issues rather than fabrication. That is itself an important finding: it means a binary "true/false" checker over-flags, and a reconciliation taxonomy is a more honest instrument.

## 5. Discussion

**For journalists.** The audit trail — claim, comparator, verbatim excerpt, classification, innocent explanation — is the minimum for a defensible fact-check. The naira case shows why: three outlets, three numbers, one official series. A fact-check that says "The Sun got it wrong" would be less useful than one that says "Three different conventions are in use, and only one is transparent about its inputs."

**For regulators.** A manipulation ban (e.g. EU AI Act Article 5) needs a measurement procedure, and a measurement procedure needs a taxonomy. Binary true/false does not distinguish a lie from a methodology switch. The classification scheme here is a candidate starting point.

**For future dataset builders.** The reconciliation layer is buildable but labour-intensive. Agent-assisted discovery can locate claims, but verification of the excerpt is human work. A second pilot should target numerical discrepancies specifically, by selecting claims where the reporting outlet is known to disagree with the primary release.

## 6. Limitations and Dual-Use / Ethical Considerations

**Scope.** This is a pilot of [FILL: N] verified claims, not a national audit. The natural sample is not representative of all Nigerian government communications. Claims identified but not excerpted within the sprint window are excluded from every reported metric.

**Label coverage.** The verified set contains no confirmed numerical discrepancy and no unverifiable row. The distribution is dominated by exact matches. Per-label statistics on rare labels are not statistically meaningful at this N.

**Coverage gap.** No sitting state-government speaker is included in the verified set. State-level figures in the dataset are reported by outlets citing NBS, not claimed by state governments. We report the imbalance rather than fabricate balance.

**No intent attribution.** Classifications describe the relationship between a claim and its cited source. A Numerical Discrepancy may be an error, a paraphrase, or a deliberate overstatement; the dataset does not distinguish.

**Dual-use.** The dataset could be used to smear individuals or outlets. Mitigations: (1) neutral classifications; (2) an explanation column recording innocent readings; (3) no ranking of speakers or outlets by accuracy; (4) the report's central argument is that reconciliation, not flagging, is the appropriate response. Anyone using the dataset to rank politicians would be misusing it.

**AI tools.** AI tools were used for drafting and code. Every verbatim excerpt in a verified row was pasted from the primary file by hand. The team is responsible for all content.

**Personal data.** No personal data is processed. All speakers are public officials or outlets making public statements.

## References

[Fill from your URLs. Suggested:]

- National Bureau of Statistics. Consumer Price Index, November 2025.
- National Bureau of Statistics. Consumer Price Index, December 2025.
- National Bureau of Statistics. Gross Domestic Product Report Q4 2025.
- National Bureau of Statistics. Nigeria Labour Force Report Q2 2024.
- Central Bank of Nigeria. Exchange Rate by Currency.
- Office of the Accountant-General of the Federation. FAAC Disbursement Reports.
- BusinessDay. "Naira ends year with over N100 gain as external reserves rise." 31 Dec 2025.
- TheCable. "Cardoso: Nigeria's net reserves hit $34.8bn." Mar 2026.
- AVeriTeC benchmark.