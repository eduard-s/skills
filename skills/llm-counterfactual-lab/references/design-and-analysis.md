# Design and analysis

## Fix the task contract

Before querying the target, record:

| Field | What must be recoverable |
| --- | --- |
| Claim | Observable behavior, task distribution, and conditions under which it should hold |
| Rival | Another process that could produce the same baseline answer |
| Oracle | Calculation, verified facts, program, or human rubric that determines correctness |
| Treatments | Exact edits and expected same/changed answer relations |
| Unit | One independently constructed base problem and all its related variants |
| Settings | Target identifier, full prompt/context, tools, decoding/reasoning controls; unknowns labeled |
| Scoring | Output parser, valid answers, abstention rule, pair definitions, exclusions |
| Execution | Number of bases, variants, repetitions, model/settings combinations, retry cap |
| Decision | Descriptive pilot or a predeclared decision threshold, and when to stop |

If the user supplies a completed run, recover this contract from their records and expose gaps. Do not pretend a retrospective choice was preregistered.

## Cross content and cue

Let **E0/E1** denote original and changed evidence, and **N0/N1** the two versions of an irrelevant cue. For a binary task with a validated answer-changing intervention:

| Condition | Expected semantic answer |
| --- | --- |
| E0 N0 | A |
| E0 N1 | A |
| E1 N0 | B |
| E1 N1 | B |

This creates two evidence pairs, holding the cue fixed, and two nuisance pairs, holding the evidence fixed. They share one base problem; they are not four independent replications.

Check each nuisance comparison in each evidence condition. An overall average can hide a cue that matters only when it conflicts with the evidence. An interaction is interesting but needs enough independent bases and replication to estimate reliably.

Use a simpler matched pair when only one intervention is relevant. Add omitted-evidence, sham-edit, or repeated-prompt controls when they address a real rival; a full factorial design is not mandatory for every question.

### Validity checks

- **Answer labels:** If choices are reordered, the correct letter may change while the answer's identity stays fixed. Define the canonical identity map before scoring.
- **Names:** Renaming an entity can change gender cues, common knowledge, tokenization, or task difficulty. Rename consistently, inspect the result, and bound the claim to that edit.
- **World knowledge:** State a fictional or supplied-evidence-only contract when altered facts contradict reality. Without that contract, following real-world knowledge may be task-correct.
- **Missing evidence:** Prove the answer is underdetermined. Redundant facts, a known public answer, or a remaining logical implication can make abstention the wrong target.
- **Distractors:** Check that an allegedly irrelevant sentence is irrelevant to the actual question. Adding an instruction is a different treatment from adding a fact.
- **Scope:** A synthetic document-reading test holds retrieval fixed. It cannot establish whether a live retriever found the right document. For a pipeline claim, capture and test that stage separately.

## Execution discipline

Estimate total calls as bases × variants × repetitions × model/settings combinations, adding any separately scheduled controls. State token/output limits if available. Do not advertise a fixed monetary cost without current pricing and actual usage assumptions.

Freeze a discovery protocol before the first call. Shuffle cases across conditions and bases; save the realized order. Run one target-visible case per fresh context unless history is the intended treatment. Use the same output format and settings across matched conditions. Do not show answer keys or another condition's answer in the target context.

For each attempt, retain case/base/condition IDs, repetition index, exact visible messages, raw response, model/configuration, timestamp, and any transport error. Separate optional parser-normalized answers from the original text. Use the declared retry cap and retain failed attempts; do not regenerate a valid wrong answer until it becomes right.

Low temperature is a setting, not proof of determinism. Repeat identical prompts across conditions when estimating response variability. A single observed answer difference can be a useful counterexample, but does not by itself estimate an intervention's effect on response probabilities.

## Scoring and denominators

Define normalization before inspecting responses. For an exact-label task, a small explicit rule such as trimming whitespace may suffice. Do not use a second LLM to guess what malformed text “really meant” unless subjective interpretation is part of a declared, checked rubric.

| Measure | Numerator / denominator |
| --- | --- |
| Task accuracy | Correct responses / returned responses in that condition; count malformed output and task-invalid refusals as failures |
| Correct evidence transitions | Pairs with both answers correct and the required semantic change / evidence pairs with two returned responses |
| Nuisance stability | Pairs with valid, equivalent canonical answers / nuisance pairs with two returned responses |
| Missing-evidence success | Required valid abstentions / returned responses on genuinely underdetermined cases |
| Repeat disagreement | Different valid canonical answers / identical-prompt repeat pairs with two valid answers; show invalid-repeat counts separately |

Also report raw answer changes when useful, but never equate them with successful transitions. Report stability alongside accuracy: identical wrong answers can be stable. A valid abstention counts as correct only where the task contract calls for it.

For each measure show raw counts. Include scheduled, attempted, returned, invalid/refusal, and unavailable counts, plus complete-pair coverage. Transport failures are unavailable observations, not evidence of wrong model reasoning. A pair missing one response is incomplete; report it separately and disclose any condition-dependent missingness. Invalid *returned* responses stay in task-success and applicable pair-success denominators. If all pairs are incomplete, the pair measure is unavailable, not zero or perfect.

When comparing models or prompt variants, use matched base families and describe incomplete overlap. More retries or more output tokens can change the comparison; report the budget difference rather than assigning it to the model alone.

## Uncertainty, discovery, and stopping

For a handful of bases, describe the tested cases with counts and failure examples. A confidence interval from a convenience sample does not make it representative of real traffic.

If interval estimates are warranted, preserve dependence: for a cluster bootstrap, resample whole base families with all their variants and repetitions, then recompute the paired statistic. State what population the sampling supports. Repeating one base many times estimates variability for that base, not generalization across problems.

Distinguish independent base count, target call count, and number of contrasts. Avoid an ordinary binomial interval that treats every correlated contrast as an independent trial. For many exploratory interventions, disclose selection and multiplicity; reserve confirmatory claims for a frozen analysis on untouched families. A tuned prompt and its discovery examples cannot serve as its own held-out confirmation.

Stop at the declared cap or a protocol-invalidating issue. If debugging the task, version it and preserve earlier observations. Do not stop when a preferred ranking becomes significant or quietly pool edited cases with the original experiment.

## Wording the finding

Prefer: “On these eight families, 11/16 evidence pairs changed to the correct answer in both conditions; 14/16 order pairs preserved answer identity. Two outputs were invalid. This suggests order robustness exceeded evidence-following success in this pilot.”

That sentence is an illustrative reporting pattern, not a measured result. Follow it with the actual rival explanations and the task/sample limits. A failure after an unfamiliar rule change is compatible with several causes, including instruction difficulty and distribution shift. It does not identify memorization on its own.
