# Skills

A collection of reusable Markdown skills for Claude and ChatGPT. Each skill lives in its own folder under `skills/`, with a `SKILL.md` entry point and supporting Markdown references.

## Catalog

| Skill | Purpose |
| --- | --- |
| [Science Research](skills/science-research/README.md) | Research everyday science questions using approved sources. Give a concise explanation, detailed evidence notes, and a separate Reddit/forum anecdote report. |

## Use a skill

Open the skill's README for its instructions, then add that individual skill folder to your assistant. These skills contain static Markdown; they require no Python, scripts, or package installation. Research skills use the browsing tools already available in the assistant.

## Add a skill

Create `skills/<skill-name>/SKILL.md`, keep any supporting Markdown files inside that folder, and add an entry to the catalog above.
