# Probe recipes

Choose the smallest recipe that addresses the user's claim. These are experimental designs, not established claims about a particular model.

## Supplied-evidence use

**Claim:** The answer follows information in the supplied document.

**Rivals:** A fixed answer, familiar world knowledge, a raw-number shortcut, or the first-mentioned entity.

Construct a self-contained problem with a verifiable answer. Change one decisive fact to produce a different answer; independently reorder the evidence or rename entities consistently. Check both evidence transitions and nuisance stability. Add an omitted-evidence case only after proving the remaining information cannot determine the answer.

Use a fictional setting if changing facts would contradict public knowledge, and state that contract in every condition. Balance which entity is correct and which appears first across independent bases. Include bases where the shortcut and the oracle disagree. A no-context control with a publicly known answer does not by itself detect hallucination or leakage.

For RAG, distinguish a reader test on fixed documents from an end-to-end retrieval test. Preserve the retrieved passages and their order; otherwise a changed response can result from changed retrieval rather than changed use of the same evidence. See the [worked example](worked-example.md).

## Explicit-rule transfer

**Claim:** The model can apply the stated rule when it differs from a familiar convention.

**Rivals:** Applying the familiar convention, misunderstanding the new notation, or failing to retrieve the local rule.

Pair ordinary and altered rules with matched problems; independently change names or presentation. Provide the rule completely and validate the oracle under both conditions. Add a simple rule-comprehension control in a separate context. Keep digit lengths, operation counts, and output requirements comparable when testing unfamiliar arithmetic or symbolic systems.

Report results on rule-comprehension checks separately from task success. A gap does not prove recitation or training contamination: the altered task may be harder or less familiar. If these rivals predict the same outcomes, vary rule visibility or add matched familiar/unfamiliar notation controls in a new experiment.

## LLM judge position sensitivity

**Claim:** A judge's preference tracks response quality under a fixed rubric.

**Rivals:** Response position, candidate identity, or verbosity.

Hold two candidate texts and the rubric fixed; submit both A/B and B/A orders in fresh contexts. Map choices to persistent candidate IDs before comparing. Hide model names unless identity is the treatment. Include ties and invalid verdicts in the schema and use a few independently justified quality anchors.

Measure position-swap consistency separately from agreement with the anchor rubric. A judge that always selects the same candidate can be consistent and wrong. A swap disagreement identifies instability under that presentation change, not which response is objectively better. Counterbalance order and repeat to distinguish systematic preference from ordinary stochastic variation.

Test verbosity or identity in separate matched interventions. Padding a response can change its content or clarity; do not assume length edits preserve quality. Never let one unvalidated judge settle the quality of its own verdicts.

## Suggested-answer sensitivity

**Claim:** A model's answer is robust to an irrelevant suggestion.

**Rivals:** Following a suggested answer or reacting to the presence of any extra sentence.

Use tasks with an independent answer key. Compare no suggestion, a plausible wrong suggestion, and a neutral sentence of similar form. If useful, add a correct suggestion and cross suggestion identity with which answer is actually correct. Make the task's instruction priority and the suggestion's status clear.

Score answer correctness and cue-aligned errors. Ask for a final answer and, if useful, a brief public justification or cited evidence; do not require hidden chain-of-thought access. A justification mentioning the cue does not prove that it caused the answer, and failing to mention it does not alone establish intentional deception. Repeated, controlled answer changes support the narrower behavioral sensitivity claim.
