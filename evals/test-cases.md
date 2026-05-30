# Econ Writing Skill -- Test Cases

Test prompts and expected behaviors for evaluating the econ-write skill. Each test defines a prompt, the expected output characteristics, and common failure modes.

---

## Test 1: Abstract Concreteness

**Prompt**: "Write an abstract for a paper that uses DiD to study the effect of paid family leave on maternal labor supply"

**Expected**:
- [ ] 100-150 words (does not exceed 150)
- [ ] Contains a concrete effect size (coefficient or percentage)
- [ ] Names the identification strategy (difference-in-differences)
- [ ] Follows 4-part formula: what/how/findings/implications
- [ ] Active voice throughout
- [ ] No citations in the abstract
- [ ] No "we find interesting results" or equivalent vague language

**Failure modes**: Vague findings ("significant effects"), passive voice ("it was found"), exceeds 150 words, missing identification strategy

---

## Test 2: Introduction Formula

**Prompt**: "Write an introduction for a paper using an RDD on class size and student achievement"

**Expected**:
- [ ] Hook with a fact or policy relevance (not literature or philosophy)
- [ ] Research question stated by paragraph 3
- [ ] Main result with magnitude stated in the introduction
- [ ] Results occupy ~25-30% of the introduction
- [ ] Literature review tells a story (not a list)
- [ ] Literature review appears within the introduction, after the main-results paragraphs and before the roadmap (not as a separate section)
- [ ] Ends with a roadmap paragraph
- [ ] 3-5 pages total
- [ ] Active voice, no throat-clearing

**Failure modes**: Opening with "The literature has long..." or "Education is important...", no results in intro, literature as annotated bibliography, exceeds 5 pages

---

## Test 3: Conclusion Without Caveats

**Prompt**: "Write a conclusion for an RCT paper on microfinance and small business growth"

**Expected**:
- [ ] Follows 3-part formula: Summary, Implications, Future Research
- [ ] No generic caveats dump that undermines confidence (a brief, specific limitations note is acceptable, especially for experimental/policy work)
- [ ] Findings phrased differently from how they would appear in the abstract
- [ ] Policy implications with cost-benefit reasoning
- [ ] Concrete future research directions (not "more research is needed")
- [ ] Under one page
- [ ] No self-congratulation ("this paper contributes to...")
- [ ] Projects confidence in findings

**Failure modes**: Generic caveats dump that undermines confidence, copy-pastes abstract language, says "I leave X for future research", exceeds one page, ends with "our results contribute to the growing body of literature"

---

## Test 4: Passive Voice Detection

**Prompt**: "Rewrite this paragraph: 'It was found that wages are increased by education. The effect is shown to be significant by our analysis. It should be noted that the sample was restricted to urban workers.'"

**Expected**:
- [ ] All passive constructions converted to active voice
- [ ] "I find" or "We find" instead of "It was found"
- [ ] "Table X shows" instead of "The effect is shown"
- [ ] "It should be noted" deleted entirely
- [ ] Original meaning preserved
- [ ] Concrete magnitude added or placeholder noted

**Failure modes**: Leaves any passive voice, adds new throat-clearing, changes the meaning

---

## Test 5: Literature Review as Story

**Prompt**: "Write a literature review section about the effect of immigration on native wages, positioning a new paper that uses administrative data"

**Expected**:
- [ ] Narrative structure with a "however" or "although" pivot
- [ ] 5-10 papers discussed (closer to 5)
- [ ] Each paper's contribution AND remaining limitation stated
- [ ] Builds toward the current paper's niche
- [ ] Full author names (no abbreviations like "BLP")
- [ ] Generous credit to prior work (no insults)
- [ ] Ends by establishing what this paper adds

**Failure modes**: Laundry list ("X found A. Y found B."), too many papers, no narrative arc, abbreviated author names, no clear gap identified

---

## Test 6: Anti-AI Writing Patterns

**Prompt**: "Write a paragraph about how minimum wage affects employment"

**Expected**:
- [ ] No banned words: "delve", "landscape", "multifaceted", "notably", "crucial", "comprehensive", "leverage" (as verb), "pivotal", "groundbreaking", "shed light on", "pave the way"
- [ ] Sentence length varies (mix of short and long)
- [ ] Uses field-specific terms naturally (e.g., "disemployment effects", "extensive margin")
- [ ] Contains at least one parenthetical aside or em-dash
- [ ] No perfect parallel structure in lists
- [ ] Specific institutional details (names actual datasets, policies, or countries)

**Failure modes**: Uses "delve into the landscape of minimum wage research", every sentence 15-20 words, generic phrasing without institutional specifics

---

## Test 7: Theory Paper Introduction

**Prompt**: "Write an introduction for a theory paper on optimal taxation with heterogeneous agents"

**Expected**:
- [ ] Opens with a puzzle or empirical fact, NOT "the literature lacks a model"
- [ ] Main theoretical insight stated in first 2 paragraphs
- [ ] Concrete mechanism described
- [ ] At least one testable prediction mentioned
- [ ] Model described in plain English before any math
- [ ] No "this paper contributes to the literature by"

**Failure modes**: Opens with literature gap, no concrete insight, mechanism described only in math, no testable prediction

---

## Test 8: Title Evaluation

**Prompt**: "Evaluate these three titles: (A) 'A Study of Various Factors', (B) 'Cash Transfers and Child Health: Evidence from Rural Mexico', (C) 'A Regression Discontinuity Analysis of Education Policy Using Administrative Data'"

**Expected**:
- [ ] Title B rated highest
- [ ] Title A criticized for vagueness (says nothing about treatment or outcome)
- [ ] Title C criticized for leading with methodology
- [ ] Scoring on clarity, specificity, length, memorability dimensions
- [ ] Specific suggestions for improving A and C

**Failure modes**: Rates A or C highest, doesn't identify the methodology-leading problem in C

---

## Test 9: Results Section Ordering

**Prompt**: "Write a results section for a paper with main DiD results, heterogeneity by gender and income, mechanisms (two channels tested), and robustness checks"

**Expected**:
- [ ] Main result stated first with magnitude
- [ ] Specifications ordered most parsimonious to least
- [ ] Economic significance translated (not just statistical)
- [ ] Heterogeneity presented after main result with magnitudes for each subgroup
- [ ] Multiple testing acknowledged for heterogeneity
- [ ] Mechanisms tested with evidence (not listed and speculated)
- [ ] Robustness checks summarized concisely (detailed versions in appendix)

**Failure modes**: Starts with robustness checks, no magnitudes, "the effect is heterogeneous" without numbers, mechanisms listed but not tested

---

## Test 10: Referee Response

**Prompt**: "Write a response to this referee comment: 'The authors do not adequately address the possibility of reverse causality. The instrument seems weak.'"

**Expected**:
- [ ] Opens with respectful acknowledgment
- [ ] Quotes the referee's comment
- [ ] Addresses reverse causality with specific new analysis or argument
- [ ] Reports first-stage F-statistic for instrument strength
- [ ] States what was changed in the paper and where (page/section)
- [ ] Never defensive or dismissive
- [ ] Provides evidence, not just assertions

**Failure modes**: Defensive tone ("we disagree with the referee"), no specific changes described, doesn't address both concerns separately

---

## Test 11: Grant Proposal

**Prompt**: "Write a project description for an NSF grant proposal studying the effect of remote work on urban housing markets"

**Expected**:
- [ ] Opens with why this question matters now (post-pandemic relevance)
- [ ] States expected contribution in one concrete sentence
- [ ] Names specific datasets and identification strategy
- [ ] Includes a realistic timeline
- [ ] Demonstrates feasibility (preliminary evidence or pilot data mentioned)
- [ ] Connects to broader impacts / policy relevance
- [ ] Reads as a research PLAN, not a finished paper
- [ ] Under 15 pages worth of content (concise)

**Failure modes**: Reads like a literature review, vague methods ("I will collect data"), no timeline, no broader impacts, presents completed findings instead of a research plan

---

## Test 12: Replication Package README

**Prompt**: "Write a README for a replication package for a DiD paper using Census data and Stata"

**Expected**:
- [ ] Follows Social Science Data Editors template structure
- [ ] Includes Data Availability & Provenance section
- [ ] Lists computational requirements (Stata version, packages, expected runtime)
- [ ] Maps tables/figures to specific code files
- [ ] Addresses restricted-access data procedures if applicable
- [ ] Includes license declaration

**Failure modes**: Missing data availability statement, no code-to-output mapping, doesn't mention software versions, no directory structure

---

## Test 13: Field-Specific Adaptation (Macro)

**Prompt**: "Write a results section for a DSGE paper on the effects of monetary policy shocks"

**Expected**:
- [ ] Presents impulse response functions as primary results (not regression tables)
- [ ] Includes model fit / moment comparison table
- [ ] Framed as "the model generates" rather than "I find"
- [ ] Reports calibration choices with sources
- [ ] Discusses sensitivity to key parameter values

**Failure modes**: Presents results as regression coefficients, uses applied-micro conventions, no model fit discussion, no calibration table

---

## Test 14: Presentation / Job Talk Slides

**Prompt**: "Outline job-talk slides for my DiD paper on the minimum wage and employment"

**Expected**:
- [ ] Main result appears within the first ~3 slides (first 10 minutes)
- [ ] No opening literature-review or motivation slide
- [ ] Slides built around a key table, figure, or equation -- not full-sentence bullet points
- [ ] Result-first structure ("Look at Table 1")
- [ ] Backup-slide strategy mentioned for anticipated questions

**Failure modes**: Opens with motivation/literature, bullet-point-heavy slides, main result buried past the first few slides

---

## Test 15: Working Paper to Journal Conversion

**Prompt**: "I have a 70-page working paper. Help me cut it to a journal submission for REStat"

**Expected**:
- [ ] Identifies the ~15-page core contribution
- [ ] Proposes cuts in the skill's priority order (redundant motivation, literature tangents, non-essential robustness, restated theory, verbose captions)
- [ ] Respects REStat's length norm (45-page limit, overlong papers returned unreviewed; Short Papers track noted if relevant)
- [ ] Moves robustness/proofs to an online supplement while keeping a main-text reference to each
- [ ] Does not add new content

**Failure modes**: Uses the wrong REStat page limit, fails to identify a core, cuts nothing concrete, leaves orphaned appendix references

---

## Test 16: Survey / Review Paper

**Prompt**: "Draft the introduction and section outline for a JEP survey on the economics of remote work"

**Expected**:
- [ ] States an organizing framework in the introduction
- [ ] Sections organized by research question or theme, NOT by chronology or method
- [ ] Builds a narrative about where the field stands and where it should go
- [ ] Minimal math; accessible to all economists (JEP convention)
- [ ] Not an annotated bibliography

**Failure modes**: Lists papers without a framework, organizes by method/chronology, heavy math, no argument about the state of the field

---

## Test 17: Policy Brief / Op-Ed

**Prompt**: "Turn my finding -- a 0.3 SD test-score gain from smaller classes -- into a 600-word op-ed"

**Expected**:
- [ ] Opens with the policy takeaway, not the research question
- [ ] No standard errors, p-values, confidence intervals, or Greek letters
- [ ] Magnitude translated into everyday terms
- [ ] One concrete example or anecdote
- [ ] Ends with a concrete recommendation, not "more research is needed"
- [ ] Within the length limit

**Failure modes**: Leads with methods, includes regression jargon, vague magnitude, ends with "more research is needed", exceeds length

---

## Test 18: Paper Audit (Three-Reviewer)

**Prompt**: "Review this introduction: 'This paper studies education and wages. The literature has long debated this. We use data and find effects. Section 2 describes the data...'"

**Expected**:
- [ ] Applies the three reviewer perspectives (Methodologist, Field Expert, Writing Critic)
- [ ] Component scores toward a /100 total (per review-checklist.md)
- [ ] Lists the top 3 fixes first
- [ ] Flags the buried lead, the literature-first opening, and the absence of a concrete result/magnitude
- [ ] Gives concrete fix examples, not just diagnoses

**Failure modes**: Single undifferentiated review, no scoring, misses the missing-magnitude problem, vague feedback

---

## How to Use These Tests

1. Run each prompt through the skill
2. Check output against the expected criteria
3. A passing test meets ALL checked criteria
4. Track pass rates across skill versions to measure improvement
5. When a test fails, identify which rule in SKILL.md is underspecified and strengthen it
