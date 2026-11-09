# LLM Counterfactual Lab development checks

Date: **9 November 2026** (Asia/Dubai).

The package is static Markdown. Its scope is controlled behavioral experiment design and analysis for LLMs, separate from the everyday-science research skill.

## Validation record

Development validation covers skill frontmatter, local Markdown links, static-only packaging, worked-example arithmetic, and the constructed response patterns in the example. These checks validate structure and scoring examples; they do not establish how an assistant follows the instructions or how a target model performs.

See [fixture-checks.md](fixture-checks.md) for the exact fixtures, expected calculations, and check results. The fixture responses are deliberately synthetic and are never represented as measured model outputs.

## Behavioral validation status

The [behavioral cases](behavioral-cases.md) are forward-test specifications. They have **not** been executed by an independent agent or against a live target model. Native skill import in Claude or ChatGPT has not been tested. No target endpoint was configured, no model calls were made for the experiment, and no API keys or runtime dependencies are required to install the skill.

The worked protocol therefore remains **not run**. Its answer key and synthetic scoring patterns are teaching material, not an empirical benchmark result.
