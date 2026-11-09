# Fixture and structure checks

Date: **9 November 2026** (Asia/Dubai). These are deterministic development checks, not live-model observations or independent behavioral evaluations.

## Executed calculation checks

An ephemeral Python standard-library check read the actual prompt blocks and synthetic scoring table from [worked-example.md](../../skills/llm-counterfactual-lab/references/worked-example.md). It parsed specimen rows, computed corrected signals directly, and recomputed the table metrics against those answers. No checker or runtime dependency is shipped in the skill.

| Check | Result |
| --- | --- |
| Five complete target prompt blocks are present | Pass: four crossed conditions and Missing |
| Task instruction is identical across prompt blocks | Pass |
| N0 → N1 only reverses specimen rows | Pass in both evidence conditions |
| E0 → E1 only changes Neral's blank from 9 to 1 | Pass in both row orders |
| Independently calculated four-cell key | Pass: Sovel, Sovel, Neral, Neral |
| Missing-evidence ambiguity | Pass: compatible blanks 1 and 9 yield different winners |
| Follow-up separates constant-name and largest-raw shortcuts | Pass: corrected signals 13 and 11 favor Neral; raw maximum favors Sovel |

The following scores were recomputed from the synthetic outputs printed in the worked example. All four rows matched their documented values.

| Constructed pattern | Accuracy | Raw evidence changes | Correct transitions | Order stability |
| --- | --- | --- | --- | --- |
| Oracle | 4/4 | 2/2 | 2/2 | 2/2 |
| Always Neral | 2/4 | 0/2 | 0/2 | 2/2 |
| First row | 2/4 | 0/2 | 0/2 | 0/2 |
| Always wrong but changes | 0/4 | 2/2 | 0/2 | 2/2 |

## Incomplete and relabeled fixtures

The separate synthetic incomplete fixture was `Sovel`, `Sovel or Neral`, `Neral`, and no response, in E0 N0, E0 N1, E1 N0, E1 N1 order. The check confirmed:

- Four scheduled cases; three returned outputs, including one invalid; one unavailable response.
- Accuracy 2/3 among returned outputs.
- Correct evidence transitions 1/1, with only 1/2 planned evidence pairs complete.
- Order stability 0/1, with only 1/2 planned order pairs complete.

An all-unavailable fixture produced unavailable accuracy and pair measures, not zero or perfect scores. A candidate-order fixture mapped verdict A in the maple/birch order and verdict B in the birch/maple order to the same identity, maple.

These checks exercise arithmetic and denominator edge cases. They do not show that a fresh assistant will choose the correct analysis, preserve logs, or avoid unsupported conclusions; those behaviors remain subjects of the [unexecuted cases](behavioral-cases.md).

## Package validation

The skill-creator `quick_validate.py` validator passed the new skill's frontmatter and naming checks. Its PyYAML dependency was installed only in a temporary validation environment outside the repository; it is not a skill dependency.

Repository checks confirmed that local Markdown links resolve, the new package contains only Markdown files, no unfinished scaffold markers remain, and changed files have no trailing whitespace. These are structural checks, not a native installation test.
