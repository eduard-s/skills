# Science Research

Research practical science questions for people without a scientific background. The skill uses approved sources, checks evidence quality, and separates scientific findings from personal experiences.

## What it produces

- A concise scientific answer, normally 250–450 words, with direct source links.
- A separate Reddit/forum anecdote report, clearly labeled as personal experiences.
- Detailed research notes covering searches, evidence, exclusions, uncertainty, and limitations.

If the assistant can create files, it produces three linked Markdown reports. Otherwise, it uses three separate sections in chat. You can request science only or another output language.

## Add the skill

The complete skill is this folder: `skills/science-research/`. Its entry point is [SKILL.md](SKILL.md); keep the `references/` folder with it. All files are Markdown. No runtime scripts or additional software are needed.

- **Claude:** Add the skill through the available Skills upload interface. If a ZIP is required, compress the `science-research` folder, preserving that folder at the archive's top level. [Official instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- **Claude Code:** Copy this folder into `~/.claude/skills/` or a project's `.claude/skills/`, then invoke `/science-research`. [Official instructions](https://code.claude.com/docs/en/skills).
- **ChatGPT:** Add it through the skill-creation/upload surface available in your account. [Official skill documentation](https://learn.chatgpt.com/docs/build-skills).
- **Conversation fallback:** Attach `SKILL.md` and the Markdown reference files, then ask the assistant to follow them for that conversation.

Native installation options and browsing access depend on the host and account. The skill provides research instructions; the assistant supplies search and page-reading capabilities.

## Example request

> Does magnesium actually help adults sleep? Explain the research simply. Give me a short answer, links to detailed evidence, and a separate report of Reddit and other forum experiences.

## Approved sources

Edit [source-policy.md](references/source-policy.md) to choose eligible scientific sources and forums. The supplied list is a default preset. The assistant checks each source's exact host and path, document type, publication status, and support for the claim. It must exclude unknown sources rather than silently expand the list.

A source's location alone does not establish quality. Forum accounts cannot support scientific conclusions, and papers with unestablished peer review stay out of the scientific synthesis.

## Evaluation

See the [evaluation cases and results](../../evaluations/science-research/RESULTS.md) for development checks, examples, and limitations. Native Claude and ChatGPT imports have not been tested.

The organization was inspired by [asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill). These are original science-research instructions, not an ASD-STE100 implementation.
