# Science research skill

`science-research/` is one portable Agent Skills folder for practical science questions. It gives non-scientists a concise answer with citations, detailed research notes, and a separate report of Reddit/forum experiences.

The workflow was structurally inspired by [asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill): a focused entry point, supporting references, plain language, and a narrow validation helper. These are original scientific-research instructions, not an ASD-STE100 implementation or certification.

## Use it

Example request after selecting the skill:

> Does magnesium actually help adults sleep? Explain the research simply. Give me a short answer, links to detailed evidence, and a separate report of Reddit and other forum experiences.

You can also request science only, change the output language, or specify sources to include/exclude. The skill uses the search and reading tools available in its host; it does not provide a search engine, bypass paywalls, or enable browsing by itself.

## Install

- **Claude:** Upload `dist/science-research.zip` through **Customize → Skills → + / Create skill → Upload a skill**, then enable it. Code execution/file creation and workspace permissions may be required. [Official Claude instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude), [ZIP layout](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).
- **Claude Code:** Copy the whole `science-research` folder into `~/.claude/skills/` for personal use or `.claude/skills/` in a project. Invoke `/science-research`. [Official documentation](https://code.claude.com/docs/en/skills).
- **ChatGPT:** Use the available skill-creation/upload surface in your account. Workspace agents support **Add skill** and upload; the desktop app exposes **Skills**. Select the installed skill with `@` where supported. Features and permissions vary by account/workspace; a Claude ZIP upload flow is not guaranteed in every ChatGPT surface. [Build skills](https://learn.chatgpt.com/docs/build-skills), [workspace-agent skill upload](https://developers.openai.com/cookbook/articles/chatgpt-agents-sales-meeting-prep#3-enabling-skills-and-memories-for-consistent-customized-outputs).
- **Fallback chat use:** If native skill installation is unavailable, attach `SKILL.md` and all four files in `references/`, then ask the assistant to follow them for the conversation. This is conversation context, not a persistently installed skill. The Python helper is optional.

The ZIP contains a top-level `science-research/` folder. It has no credentials, paid API dependency, or product-specific search calls. `agents/openai.yaml` supplies optional OpenAI UI metadata; other hosts can ignore it.

## Choose approved sources

Edit `science-research/references/source-policy.json` **before packaging/installing** to set your approved locations. Rebuild and re-upload after changes. The supplied policy is a curated starting set, not a claim that you already approved it. It covers health, behavior, education, environment, physics, and computing, with separate scientific, discovery, and anecdotal lanes.

Each rule has an exact `hosts` list, `path_prefixes`, a unique `id`, and one `lane`: `science-candidate`, `anecdote-candidate`, `discovery-only`, or `blocked`. No wildcards or implicit subdomains. A prefix `/publications` matches that path and its children, not `/publications-store`. Unknown locations stay excluded. Avoid overlapping rules with different lanes; invalid policies fail closed.

```json
{"id":"example-agency","lane":"science-candidate","hosts":["research.example.org"],"path_prefixes":["/publications/"]}
```

This is a **location gate**, followed by required document and claim checks. It does not certify every item on an eligible host. For example, PubMed can contain preprints, and a publisher can host editorials. Retracted findings, preprints, advertisements, news, and forum comments cannot support the established scientific answer under the default policy.

```bash
python3 science-research/scripts/check_source.py https://pubmed.ncbi.nlm.nih.gov/33865376/
```

The helper uses Python's standard library and makes no network requests. Exit status: `0` = all URLs are science/anecdote candidates; `1` = at least one discovery-only or blocked URL; `2` = invalid policy or CLI input. Read each returned **lane**: status `0` does not mean scientific approval. It cannot verify redirects, article content, peer review, corrections, or factual support. Noncanonical URLs and encoded paths fail closed; resolve an authentic canonical link and check it again.

The skill's research rules are instructions to the model, not a network firewall. For a technical guarantee that only approved domains can be accessed, the host must enforce the same restrictions on its browsing tools. Discovery searches will naturally reveal excluded results, which the skill must not use as evidence.

## Outputs and verification

The default deliverables are `evidence-summary.md` (about 250–450 words), `anecdotal-report.md` (separate, normally 150–300 words), and `research-notes.md` (queries, source appraisal, claim map, exclusions, and limits). Chat-only hosts use three distinct sections instead.

Run the automated checks and rebuild the upload package from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/package_skill.py
```

Behavioral cases and observed results are in `tests/`. These tests distinguish URL-policy correctness from research behavior. Native Claude/ChatGPT import and execution should also be checked in your target account; an agent evaluation does not establish cross-product behavior.
