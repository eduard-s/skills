# LLM Counterfactual Lab

Test what actually changes an LLM's answer. This skill turns claims about reasoning, evidence use, and evaluation into small controlled experiments with answer keys and interpretable results.

The central test has two parts: change a decisive fact and check that the answer changes correctly; change an irrelevant cue and check that the semantic answer stays the same. Cross the changes to expose cases where a model follows answer position or a familiar label. Repeated prompts help separate those effects from ordinary response variation.

## Example requests

> My document assistant gets the right answer. Design a small experiment to test whether it actually follows the supplied evidence. Include changed-evidence and missing-evidence cases. I don't have API access here.

> Our LLM judge prefers one response. Build an experiment that swaps presentation order, hides model identities, and keeps the scoring rubric fixed.

> Here are the prompts and raw outputs from 12 matched problem families. Measure correct evidence transitions and stability. Explain which conclusions the data support.

## What you get

- A testable claim, competing explanations, and predicted outcomes.
- Exact test prompts, a separate answer key, controls, a call budget, and a stopping rule.
- Analysis of supplied or collected responses, including failures and incomplete pairs.
- A conclusion limited to the observed behavior, plus a useful follow-up experiment.

The [worked example](references/worked-example.md) is a six-call lab-measurement test. It shows how a constant-answer model can score perfectly on stability while failing every evidence transition. Its response patterns are explicitly synthetic.

## Use the skill

Add this complete folder, `skills/llm-counterfactual-lab/`, to your assistant's supported skills location. Keep [SKILL.md](SKILL.md) and `references/` together. You can also attach those Markdown files to a conversation and ask the assistant to follow them.

Example invocation where named skills are supported:

> Use $llm-counterfactual-lab to test whether changing the decisive evidence changes the answer correctly.

The package contains static Markdown and requires no installed scripts or libraries. Designing experiments and analyzing pasted logs need no model API. Running an experiment requires a target interface supplied by the host or user; literature research uses available browsing tools. A plan never counts as a completed run.

## Scientific basis and scope

The workflow draws on behavioral NLP testing, counterfactual task evaluation, and research on LLM judge bias and explanation faithfulness. See [research-basis.md](references/research-basis.md) for primary sources and the specific ideas used. This is an original instructional synthesis, not a new scientific method or a reproduction of those papers' benchmarks.

Black-box tests can reveal sensitivity to a chosen intervention. They do not establish a model's internal reasoning algorithm or prove training-data contamination. A small pilot does not establish a deployment-wide failure rate.

Development checks and their limits are recorded in [evaluation results](../../evaluations/llm-counterfactual-lab/RESULTS.md). Native skill import and live target-model execution have not been tested.
