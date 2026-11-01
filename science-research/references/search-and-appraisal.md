# Search and appraisal

## Applying the source policy

`source-policy.json` is the single list of eligible exact hosts and paths. Subdomains are not implicitly included. A scientific source passes only when all four gates pass:

1. **Location:** The final URL matches a `science-candidate` rule or an explicit addition authorized by the user for this run. Resolve DOI links and validate the destination too. A redirect to a new publisher or CDN does not inherit approval. Record any blocked destination.
2. **Document:** It is an eligible scientific document as defined below, rather than news, a press release, opinion, advertising, a forum post, or a search page. This applies even on an eligible host.
3. **Verification:** You opened enough of it to verify the claim, publication status, and important limitations. Check publisher notices and linked corrections/retractions; use PubMed publication types where relevant. If status cannot be checked, record “not verified,” reduce confidence as warranted, and do not describe it as cleared.
4. **Support:** Its design, population/system, comparator, outcome, and time scale support the particular statement. A sound paper can still be irrelevant to the question.

Eligible document types:

- Peer-reviewed systematic reviews, meta-analyses, and research papers with assessable methods. Establish peer review from readable official article metadata or a verified journal/proceedings review policy applicable to this document type. A journal name, a DOI, and PubMed's “Journal Article” label alone do not establish peer review. If that status cannot be established, exclude the paper from the scientific synthesis and record it as an unverified candidate in the notes. A review is useful only if its methods and included studies fit the question.
- Evidence-based guidelines, official scientific/technical assessments, technical standards, official datasets with methods, and agency health information that identifies its evidence. Label these accurately; do not call them trials or peer-reviewed papers without verification.
- Peer-reviewed conference papers for fields such as computing where they are normal research outputs. Verify the specific proceedings and review process; exclude slides, product announcements, magazines, and unreviewed workshop abstracts.
- Scientific case reports for possible rare events, labeled as weak evidence for causality or generalization. These belong to the scientific lane, distinct from unverifiable forum accounts.

Exclude retracted findings from support. A retraction notice may explain an exclusion. Flag an expression of concern; do not let the disputed result drive the conclusion. Use corrected results when verified. Preprints, trial registrations, theses, and unpublished claims are discovery/context only under the default policy, even inside an eligible repository. If the user explicitly requests preprints, add a separate **unreviewed evidence** appendix and keep it out of the established-evidence confidence judgment.

PubMed and PMC indexing do not establish quality or peer review: see the [NLM disclaimer](https://pubmed.ncbi.nlm.nih.gov/disclaimer/). Publisher-hosted news and commentary are ineligible even when their URL looks like an article. A host match never overrides the document gate. Distinguish **unestablished peer review** (a paper fails admission) from **incomplete integrity checking** (document the checks attempted and remaining uncertainty; absence of a notice is not proof that none exists). Official guidance and technical assessments use their own eligible document category and must not be mislabeled as peer-reviewed papers.

Search engines may expose excluded results. Use them only to discover an eligible original document, identify a research lead, or check integrity status. Do not use an excluded page's scientific claims as evidence. Search snippets are insufficient for scientific claims or anecdotes.

## Where to search

Use general web search with site restrictions if a database interface is unavailable. Do not assume a named integration is installed. Cite the exact source document, not these entry points.

| Topic | Start with | Follow up with |
| --- | --- | --- |
| Health, sleep, nutrition | [PubMed](https://pubmed.ncbi.nlm.nih.gov/), [Cochrane](https://www.cochranelibrary.com/), [NICE](https://www.nice.org.uk/guidance), [WHO](https://www.who.int/publications) | Recent eligible trials, harms, contraindications; [NIH supplement facts](https://ods.od.nih.gov/factsheets/list-all/), NCCIH, CDC/FDA notices |
| Psychology, behavior, education | PubMed, [APA PsycNet](https://psycnet.apa.org/), [Campbell](https://www.campbellcollaboration.org/), [What Works Clearinghouse](https://ies.ed.gov/ncee/wwc/) | Replications, longitudinal research, measurement quality, systematic reviews; population/cultural limits |
| Environment, climate, exposure | [IPCC](https://www.ipcc.ch/assessment-report/), [EPA IRIS](https://www.epa.gov/iris), [USGS](https://pubs.usgs.gov/), NOAA | Exposure-specific field evidence, local conditions, official measurements and methods |
| Physics, space, materials | [NASA ADS](https://ui.adsabs.harvard.edu/) / [SciX](https://scixplorer.org/) for discovery, [NIST](https://www.nist.gov/publications), NASA technical reports | Eligible original papers, reproducibility, measurement uncertainty; established models versus speculation |
| Computing, engineering | [ACM](https://dl.acm.org/), [IEEE](https://ieeexplore.ieee.org/), NIST technical reports | Independent benchmarks, peer-reviewed proceedings/journals, setup and realistic workloads |

These are navigation suggestions, not extra allowlist entries. A linked index can be used for discovery; the document it finds still needs the JSON and document checks. For fields or local authorities poorly covered by the preset, disclose that scope limit and propose named additions rather than treating the preset as the whole literature.

## Search plan and stopping

- Express the question with everyday terms and scientific synonyms: population/system + intervention/exposure + outcome, adding a comparison when useful.
- Find a suitable synthesis/assessment; check its **search end date**, not only publication date. Then search for newer eligible work and important omitted harms or opposing results.
- Example search shapes: `site:pubmed.ncbi.nlm.nih.gov [topic] systematic review`, `[topic] randomized trial adverse effects`, `site:pubs.usgs.gov [exposure] [outcome]`. Choose study terms appropriate to the field. For intervention benefits, good reviews and randomized trials are often useful; harms, prognosis, prevalence, and exposures may require observational evidence. For physics and engineering, assess measurement, calibration, model assumptions, and operating conditions.
- Record actual queries, tools/indexes, search date, date/language filters, and access failures. Do not invent screening totals or imply an exhaustive multilingual search.
- Seek independent evidence where available. Multiple pages about one trial, assessments relying on it, and reviews containing it are not independent replications.
- Search null findings, harms, and disagreement before stopping. Do not impose a paper quota or mistake many citations for high confidence. If coverage remains thin, say so.

## Evidence notes

For each source used, keep a compact record in `research-notes.md`:

`ID | title + direct URL/DOI | publication/update date | type + peer-review status | access (full/abstract/summary) | population/system + sample size when relevant | intervention/exposure + comparator + duration | outcome/effect + units + uncertainty | main limits + funding/conflicts if reported | correction/retraction check + result | claim supported`

Use “not reported” or “not checked” rather than guessing. Record what is missing from an abstract. An abstract can support a narrow claim if explicit enough; it cannot establish unreported methods or harms. Do not upgrade an agency summary into a full-text study appraisal. Preserve denominators, confidence intervals where available, and time frames. Case reports and observational associations do not by themselves prove cause.

Add a **claim map** linking each central conclusion to source IDs and whether it is direct evidence, indirect evidence, or your inference. List material exclusions and reasons, including relevant unavailable or out-of-policy sources. Do not list every irrelevant search hit.

## Confidence and disagreement

Use these informal labels per central finding, with a short reason. They are **not a formal GRADE assessment**:

- **High:** Direct, consistent, strong evidence or a robust scientific assessment; remaining limits are unlikely to reverse the practical conclusion.
- **Moderate:** Useful evidence, with material limits in precision, bias, consistency, or applicability.
- **Low:** Sparse, small, indirect, inconsistent, or substantially biased evidence; the conclusion could change.
- **Insufficient:** No eligible accessible evidence answers the question well enough to conclude.

If a review reports formal GRADE certainty, attribute its rating and scope exactly, separately from your judgment. Do not invent numeric confidence percentages. The [Cochrane Handbook on certainty](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-14) explains relevant considerations; this workflow does not substitute for a formal assessment.

Explain disagreements through design, baseline risk, dose/exposure, population, duration, outcomes, bias, review overlap, and date. Do not resolve them by counting papers or votes. An old strong study can be more useful than a new weak one. Animal, laboratory, simulation, and mechanism findings can explain a hypothesis; label their indirectness and do not translate them into established real-world benefit.
