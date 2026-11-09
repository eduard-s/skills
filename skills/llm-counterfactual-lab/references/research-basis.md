# Research basis

These primary papers motivate parts of the workflow. The skill combines them into an instructional protocol; its six-call example and scoring contract are local design choices. It does not reproduce the papers' datasets, effect sizes, or evaluations, and their results do not establish how a current target model will behave.

## Behavioral tests beyond aggregate accuracy

Ribeiro et al., **Beyond Accuracy: Behavioral Testing of NLP Models with CheckList**, ACL 2020. [Publisher page and abstract](https://aclanthology.org/2020.acl-main.442/).

The paper introduces task-agnostic behavioral testing across capabilities and test types. It motivates testing specified behaviors with controlled transformations alongside aggregate correctness. This skill's paired success metrics are explicitly defined in [design-and-analysis.md](design-and-analysis.md); they should not be presented as quoted CheckList metrics.

## Counterfactual task variants

Wu et al., **Reasoning or Reciting? Exploring the Capabilities and Limitations of Language Models Through Counterfactual Tasks**, NAACL 2024. [Publisher page and abstract](https://aclanthology.org/2024.naacl-long.102/).

The paper evaluates variants that alter default task assumptions. It motivates checking whether performance survives a relevant rule or assumption change. A resulting performance gap needs interpretation: this skill does not treat it as proof of memorization or absence of reasoning.

## Judge position bias

Wang et al., **Large Language Models are not Fair Evaluators**, ACL 2024. [Publisher page and abstract](https://aclanthology.org/2024.acl-long.511/).

The paper studies response-order effects in LLM evaluation. It motivates swapping candidate positions and preserving candidate identity during scoring. Swapping positions is a diagnostic control; consistency alone does not establish agreement with a justified quality rubric.

## Explanations and behavioral evidence

Turpin et al., **Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting**, NeurIPS 2023. [Proceedings paper](https://proceedings.neurips.cc/paper_files/paper/2023/file/ed3fea9033a80fea1376299fa7863f4a-Paper-Conference.pdf).

The paper investigates answer changes under biasing prompt features and explanations that fail to disclose those features. It motivates testing outputs under interventions rather than treating a written justification as a direct account of internal computation. The skill does not request private reasoning traces or infer intentional deception from omitted explanations.

## Verification scope

During skill development on 9 November 2026, the three ACL Anthology publication pages and abstracts and the NeurIPS paper's abstract were inspected through web tools. The NeurIPS abstract-page fetch timed out; the proceedings PDF was available through search extraction. This is a targeted methods bibliography, not a systematic or current literature review, a replication, or a claim that every paper's full text was reviewed.
