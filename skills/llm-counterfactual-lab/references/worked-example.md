# Worked example: a lab-measurement reader

This is an **unexecuted protocol** with a verified answer key and synthetic response patterns. No responses below were collected from a target model. The measurements and specimen names are invented.

## Question and rival predictions

Does the reader select the specimen with the greater corrected signal when one decisive blank measurement changes, while preserving its selection when rows are reordered?

- **Rule-following prediction:** E0 selects Sovel in either row order; E1 selects Neral in either order.
- **First-row shortcut:** Selection follows whichever specimen appears first.
- **Always-Neral / largest-raw-value shortcut:** Neral in every complete-evidence condition. These two rivals make identical predictions here; this family cannot distinguish them.

The task oracle is subtraction and comparison, not a model judgment. Corrected signal is raw signal minus the specimen's own blank. All values use the same arbitrary signal unit. Only Neral's blank changes, from 9 to 1.

| Condition | Neral corrected | Sovel corrected | Gold answer |
| --- | --- | --- | --- |
| E0 N0 | 20 − 9 = 11 | 16 − 1 = 15 | Sovel |
| E0 N1 | 20 − 9 = 11 | 16 − 1 = 15 | Sovel |
| E1 N0 | 20 − 1 = 19 | 16 − 1 = 15 | Neral |
| E1 N1 | 20 − 1 = 19 | 16 − 1 = 15 | Neral |
| Missing | Cannot determine | 16 − 1 = 15 | INSUFFICIENT |
| Repeat of E0 N0 | 11 | 15 | Sovel |

For Missing, a blank of 1 would make Neral greater, while a blank of 9 would make Sovel greater. Both are compatible with the remaining data, so the required abstention is justified.

## Exact target inputs

Each prompt below is a separate target input. Send only the prompt block, without its heading, the answer key, or other conditions. Start a fresh target context each time.

### E0 N0

```text
Use only this fictional lab record. Corrected signal = raw signal minus that specimen's blank. Select the specimen with the greater corrected signal. If the record cannot determine a unique winner, return INSUFFICIENT. Return exactly Neral, Sovel, or INSUFFICIENT.
Specimen | Raw signal | Blank
Neral | 20 | 9
Sovel | 16 | 1
```

### E0 N1

```text
Use only this fictional lab record. Corrected signal = raw signal minus that specimen's blank. Select the specimen with the greater corrected signal. If the record cannot determine a unique winner, return INSUFFICIENT. Return exactly Neral, Sovel, or INSUFFICIENT.
Specimen | Raw signal | Blank
Sovel | 16 | 1
Neral | 20 | 9
```

### E1 N0

```text
Use only this fictional lab record. Corrected signal = raw signal minus that specimen's blank. Select the specimen with the greater corrected signal. If the record cannot determine a unique winner, return INSUFFICIENT. Return exactly Neral, Sovel, or INSUFFICIENT.
Specimen | Raw signal | Blank
Neral | 20 | 1
Sovel | 16 | 1
```

### E1 N1

```text
Use only this fictional lab record. Corrected signal = raw signal minus that specimen's blank. Select the specimen with the greater corrected signal. If the record cannot determine a unique winner, return INSUFFICIENT. Return exactly Neral, Sovel, or INSUFFICIENT.
Specimen | Raw signal | Blank
Sovel | 16 | 1
Neral | 20 | 1
```

### Missing

```text
Use only this fictional lab record. Corrected signal = raw signal minus that specimen's blank. Select the specimen with the greater corrected signal. If the record cannot determine a unique winner, return INSUFFICIENT. Return exactly Neral, Sovel, or INSUFFICIENT.
Specimen | Raw signal | Blank
Neral | 20 | not recorded
Sovel | 16 | 1
```

### Repeat

Resend the E0 N0 block exactly in a fresh context. This is an exact repeat, not another independent base problem.

## Execution and scoring contract

**Status:** Not run. Target, configuration, date, and observations are unset.

This discovery protocol schedules six calls: four crossed conditions, one omitted-evidence control, and one exact repeat. Stop after those six attempts; no automatic retries. Save the realized shuffled order and full returned outputs or errors. One repeat pair is a diagnostic, not a reliable estimate of stochastic variability. Additional bases and repetitions require a separately declared budget.

Trim leading/trailing whitespace only. Accept exactly `Neral`, `Sovel`, or `INSUFFICIENT`; other text is invalid. For a returned output, invalid formatting counts as task failure. A transport error is unavailable and leaves any affected pair incomplete.

- Complete-evidence accuracy: correct answers out of the four returned crossed-condition outputs; report any unavailable cells.
- Evidence transitions: compare E0 N0 ↔ E1 N0 and E0 N1 ↔ E1 N1. Success requires Sovel → Neral in each pair.
- Order stability: compare E0 N0 ↔ E0 N1 and E1 N0 ↔ E1 N1. Success requires valid, identical semantic answers in each pair, even if those answers are wrong; interpret with accuracy.
- Missing-evidence success: exactly `INSUFFICIENT` on Missing.
- Repeat agreement: compare E0 N0 with Repeat; report invalid/missing responses separately.

The missing and repeat controls are reported separately from the four-cell accuracy and crossed-pair statistics. Total independent base count is **one**.

## Synthetic scoring traps

The following are constructed patterns for the four crossed conditions only, in the order E0 N0, E0 N1, E1 N0, E1 N1. They are **not observed model outputs**.

| Synthetic pattern | Outputs in condition order | Accuracy | Raw evidence changes | Correct evidence transitions | Order stability |
| --- | --- | --- | --- | --- | --- |
| Oracle | Sovel, Sovel, Neral, Neral | 4/4 | 2/2 | 2/2 | 2/2 |
| Always Neral | Neral, Neral, Neral, Neral | 2/4 | 0/2 | 0/2 | 2/2 |
| First row | Neral, Sovel, Neral, Sovel | 2/4 | 0/2 | 0/2 | 0/2 |
| Always wrong but changes | Neral, Neral, Sovel, Sovel | 0/4 | 2/2 | 0/2 | 2/2 |

Perfect order stability is compatible with ignoring the evidence. Perfect raw answer-change rate is compatible with getting every answer wrong. This is why the experiment reports correctness, successful transitions, and stability together.

## Discriminating follow-up

To separate always-Neral from largest-raw-value behavior, introduce a new base with Neral raw 14, blank 1 and Sovel raw 20, blank 9. The corrected values are 13 and 11: the oracle and always-Neral select Neral, while largest-raw-value selects Sovel. Combine this with another base where Sovel is the correct identity to challenge constant-name behavior.

This follow-up addresses surviving rivals; it does not make one family representative. Freeze new families and the analysis before querying the target. Any claim about a deployed document assistant also needs representative documents, retrieval records where relevant, and independent bases beyond this toy calculation.
