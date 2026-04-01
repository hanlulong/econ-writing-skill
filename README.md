# Econ Writing Skill

**An Agent Skill that transforms AI assistants into expert economics paper writers, synthesizing best practices from 50+ authoritative guides by Nobel laureates, Clark Medal winners, and leading economists.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-green.svg)](https://agentskills.io)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Ready-blueviolet.svg)](https://docs.anthropic.com/en/docs/claude-code)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI%20Codex-Ready-black.svg)](https://openai.com/index/codex/)

---

## What Is This?

Econ Writing Skill is an open-source [Agent Skill](https://agentskills.io) that gives AI coding assistants deep knowledge of how to write economics papers. It distills actionable advice from over 50 guides by John Cochrane, Deirdre McCloskey, Jesse Shapiro, Keith Head, Marc Bellemare, Claudia Goldin, Edward Glaeser, Michael Kremer, and many others into a single structured skill file. Compatible with the Agent Skills open standard, it works with Claude Code and OpenAI Codex out of the box.

---

## Key Features

- **Works for all paper types** -- Applied empirical, pure theory, mixed theory-empirical, structural, and descriptive papers each get tailored structure and guidance
- **Dedicated formulas for every major section** -- Abstract (4-part formula), Introduction (Head's Hook-Question-Results-Literature Review & Value Added-Roadmap formula), Model Section (Glaeser/Varian), Data Section, Conclusion (3-part formula: Summary, Implications, Future Research)
- **Identification strategy guidance** -- Specific writing advice for RCT, DiD (including staggered DiD), IV, RDD, Synthetic Control, Synthetic DiD, Bunching, Shift-Share/Bartik, Event Studies, ML for Causal Inference, Structural Estimation, Descriptive papers, and guidance for papers using multiple strategies
- **Theory paper support** -- Model presentation, proposition writing, and Glaeser's "start with an example" approach
- **Style rules from McCloskey and Cochrane** -- active voice, concrete language, triangular structure, reader-first writing
- **Anti-AI writing patterns** -- Eliminate telltale AI-generated writing (banned words, uniform sentence length, generic phrasing) and write like a real economist
- **Paper review and audit mode** -- Simulated 3-reviewer feedback (Methodologist, Field Expert, Writing Critic) with a 100-point scoring rubric
- **Title evaluation framework** -- Score titles on clarity, specificity, length, and memorability with good/bad examples
- **LaTeX formatting guide** -- Practical LaTeX tips for tables (booktabs, threeparttable), figures, bibliography (natbib), and journal submission requirements for AER/QJE/Econometrica/REStud/JPE
- **Modern empirical practices** -- pre-registration, multiple testing, specification robustness, transparency and reproducibility
- **Tables and figures best practices** -- self-contained captions, figure vs. table trade-offs, data visualization from Schwabish (JEP)
- **Before/after examples** -- see how vague, passive, throat-clearing prose transforms into clear, concrete economics writing
- **Referee response guidance** -- Point-by-point response structure for revise-and-resubmit
- **Citation integrity** -- Anti-hallucination guidance for verifying references, distinguishing working paper vs. published versions, and avoiding misattributed citations
- **Job market paper (JMP) guidance** -- Tailored advice for the most important paper of your career: title, abstract, introduction polish, length, signaling breadth
- **Coauthorship conventions** -- Voice consistency, designated "voice editor", signaling individual contributions
- **Grant proposal writing** -- NSF, NBER, ERC proposal guidance: feasibility demonstration, budget justification, timeline structure, and the key difference between selling a plan vs. presenting findings
- **Policy brief and op-ed writing** -- Translate findings for non-academic audiences: plain language, everyday magnitudes, concrete recommendations
- **Economic significance framework** -- How to translate coefficients into meaningful units, policy benchmarks, and back-of-envelope calculations
- **Evaluation test suite** -- 11 test cases with expected criteria for benchmarking skill output quality
- **Pre-submission checklist** -- 24-item checklist covering content, style, and modern standards
- **AEA replication package standards** -- Data Editor requirements: README template, data citation, directory structure, code reproducibility, license declaration
- **AI use disclosure guidance** -- Journal-specific policies (AEA, Econometric Society) for disclosing AI assistance in manuscript preparation
- **Field-specific conventions** -- Macro (calibration tables, IRFs, DSGE), trade (gravity, PPML), development (CONSORT, cost-effectiveness), finance (Fama-MacBeth, winsorization)
- **Dissertation structure** -- Three-essays format: introduction chapter, standalone papers, conclusion chapter, authorship rules
- **Survey and review paper writing** -- JEL, JEP, Handbook chapter conventions: organizing by theme, citation density, accessibility
- **Working paper to journal conversion** -- Cutting strategy, journal-specific length norms (AER, AER Insights, REStat), appendix organization

---

## Installation

### One-Line Install (Recommended)

Install globally for all projects with a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/install.sh | bash
```

This installs the skill to `~/.claude/skills/econ-write/` (Claude Code) and `~/.codex/skills/econ-write/` (Codex). The skill is immediately available in all your projects.

### Install from Claude Code

You can install without leaving your AI assistant. Tell Claude Code:

```
Run this command to install the econ-writing skill globally:
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/install.sh | bash
```

After installation, restart your session. Then use `/econ-write` followed by your task.

### Install from Codex

Tell Codex:

```
Run this command to install the econ-writing skill globally:
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/install.sh | bash
```

### Install via npx

```bash
npx skills add hanlulong/econ-writing-skill
```

### Git Clone

```bash
git clone https://github.com/hanlulong/econ-writing-skill.git
cd econ-writing-skill
./install.sh              # Global install (default)
./install.sh --local .    # Install to current project only
```

### Manual Installation

#### Global (all projects)

```bash
mkdir -p ~/.claude/skills/econ-write
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/.claude/skills/econ-write/SKILL.md -o ~/.claude/skills/econ-write/SKILL.md
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/.claude/skills/econ-write/identification-strategies.md -o ~/.claude/skills/econ-write/identification-strategies.md
```

#### Project-specific

```bash
git clone https://github.com/hanlulong/econ-writing-skill.git
cp -r econ-writing-skill/.claude/skills/econ-write/ /path/to/your/project/.claude/skills/econ-write/
```

### Install Options

| Flag | Behavior |
|------|----------|
| (default) | Install globally for all projects |
| `--local` | Install to current project only |
| `--claude` | Install for Claude Code only |
| `--codex` | Install for Codex only |

Example: `./install.sh --local --claude /path/to/project`

---

## Usage

Once installed, invoke the skill from your AI assistant:

```
/econ-write write introduction for my paper on the effect of minimum wage on employment
```

```
/econ-write rewrite this abstract to be more concrete and under 150 words
```

```
/econ-write draft a conclusion for my RDD paper on school funding
```

```
/econ-write review this paragraph for style violations
```

```
/econ-write help me structure the model section for my theory paper
```

```
/econ-write audit my full paper and score it
```

The skill works in four modes:

- **Drafting**: generates new text following the formulas and rules, marking areas that need your specific results with `[AUTHOR: ...]` placeholders.
- **Rewriting**: identifies violations of the rules (passive voice, vague language, buried leads, throat-clearing) and fixes them while preserving your meaning and contribution.
- **Reviewing**: checks existing text against all rules and provides a detailed report of issues with suggested fixes.
- **Auditing**: scores the full paper from three simulated reviewer perspectives and returns a 100-point rubric with prioritized feedback.

---

## Common Use Cases

- **Drafting a new paper section** -- Generate a first draft of any section (abstract, introduction, data, results, conclusion) that follows established formulas from the start.
- **Rewriting existing text for clarity** -- Tighten prose, eliminate passive voice, cut throat-clearing, and make results concrete.
- **Writing an introduction from scratch** -- Follow Head's formula exactly: Hook, Research Question, Main Results, Literature Review & Value Added, Roadmap.
- **Conducting and writing a literature review** -- Build a story-driven review of the 5-10 closest papers, embedded in the introduction, that establishes your paper's niche.
- **Writing up existing empirical results** -- Present results in the correct order (main result first, most parsimonious to least parsimonious) with proper emphasis on economic significance.
- **Writing a theory paper** -- Structure model presentation, write propositions with intuition before proofs, generate testable predictions.
- **Structuring a mixed theory-empirical paper** -- Map empirical tests back to specific model predictions.
- **Preparing a presentation** -- Get advice on slide structure, pacing, and delivery following Shapiro, Cochrane, and others ("Gene Fama usually starts with 'Look at table 1.' That's a good model.").
- **Reviewing a full paper** -- Get a structured audit with 3 simulated reviewer perspectives and a 100-point score.
- **Writing a grant proposal** -- Structure an NSF, ERC, or institutional proposal that sells a research plan, not a finished paper.
- **Writing for policy audiences** -- Translate academic findings into plain-language policy briefs and op-eds.
- **Converting a working paper to journal format** -- Cut strategically, meet journal length norms, organize the online appendix.
- **Preparing a replication package** -- Follow AEA Data Editor standards for data citation, code reproducibility, and README structure.

---

## What's Inside

The skill includes four files:

### `SKILL.md` (main skill file)

1. **Core Principles** -- Seven foundational rules (Reader First, Triangular Style, One Central Contribution, Concrete Not Abstract, Every Word Counts, Active Voice, Simple over Complex)
2. **Section Formulas** -- Step-by-step formulas for the Abstract, Introduction (Head's formula), Model Section (Glaeser/Varian), Data Section, Conclusion (3-part formula), and Title (with evaluation criteria)
3. **Style Rules** -- Detailed guidance on sentence structure, word choice, voice, pronouns, footnotes, numbers, notation, paragraphs, and anti-AI writing patterns
4. **Tables and Figures** -- Best practices for captions, formatting, figure vs. table trade-offs, and data visualization
5. **Empirical Work Rules** -- Identification, results presentation, null results, heterogeneity analysis, mechanisms, and common mistakes
6. **Modern Empirical Practices** -- Pre-registration, multiple testing, specification robustness, transparency
7. **Paper Structure Templates** -- Templates for applied, theory, mixed theory-empirical, and structural papers, plus appendix organization guidance
8. **Use Case Instructions** -- Specific instructions for drafting, rewriting, reviewing/auditing, introductions, literature reviews, abstracts, conclusions, results, theory papers, data sections, presentations, and referee responses
9. **Revision Checklist** -- A 24-item pre-submission checklist covering content, style, and modern standards
10. **Field-Specific Conventions** -- Adaptations for macro, trade, development, and finance
11. **AEA Replication Standards** -- Data Editor requirements for replication packages, data citation, and AI disclosure
12. **Dissertation Structure** -- Three-essays format and JMP positioning

### `identification-strategies.md`

Detailed writing guidance tailored to each identification strategy: RCT, DiD, IV, RDD, Synthetic Control, Structural Estimation, Descriptive/Measurement, Bunching Estimation, Shift-Share/Bartik Instruments, Event Studies, and Machine Learning for Causal Inference. Includes an introduction adaptation table showing how to adjust hooks, results paragraphs, and key threats for 12 paper types.

### `latex-tips.md`

Practical LaTeX guidance for economics papers: document structure, essential packages (booktabs, threeparttable, natbib, siunitx), regression table formatting, figure best practices (PDF vector graphics, subfigures), bibliography management, math formatting, cross-referencing with cleveref, journal submission requirements (AER, QJE, Econometrica, REStud, JPE), Beamer presentations, and common pitfalls.

### `review-checklist.md`

Structured paper review framework with quick-scan mode (5-minute check), deep-review mode (3 simulated reviewers: Methodologist, Field Expert, Writing Critic), anti-AI detection checklist, 100-point pre-submission scoring rubric, and journal fit assessment for top-5 vs. field journal targeting.

---

## Sources and Acknowledgements

This skill synthesizes advice from **50+ authoritative sources**. The top 10 sources by authority and impact:

| Rank | Source | Author(s) | Institution |
|------|--------|-----------|-------------|
| 1 | Writing Tips for Ph.D. Students | John H. Cochrane | U Chicago Booth / Hoover |
| 2 | Economical Writing | Deirdre N. McCloskey | UIC / U Chicago |
| 3 | Four Steps to an Applied Micro Paper | Jesse M. Shapiro | Harvard |
| 4 | The Introduction Formula | Keith Head | UBC Sauder |
| 5 | Ten Most Important Rules of Writing Your JMP | Claudia Goldin & Lawrence F. Katz | Harvard |
| 6 | Writing Tips for Economics Research Papers | Plamen Nikolov | Binghamton / Harvard |
| 7 | How to Write Applied Papers in Economics | Marc F. Bellemare | U Minnesota |
| 8 | How to Give an Applied Micro Talk | Jesse M. Shapiro | Harvard |
| 9 | Writing Papers: A Checklist | Michael Kremer | Harvard / UChicago |
| 10 | An Economist's Guide to Visualizing Data | Jonathan A. Schwabish | JEP (AEA) |

Notable authorities include **Nobel laureates** (Goldin 2023, Kremer 2019), a **Clark Medal winner** (Shapiro 2022), and editors of leading journals (Bellemare at AJAE, Beatty at AJAE, Shimshack at JEEM).

The full ranked list of all 50+ sources with links, tiers, and notes is available in [`sources/SOURCES_RANKED.md`](sources/SOURCES_RANKED.md).

---

## Examples

See [`examples/before-after.md`](examples/before-after.md) for full before-and-after transformations. Here is a brief preview:

**Before (vague, passive, throat-clearing):**

> "I analyze data on executive compensation and find many interesting results."

**After (concrete, active, direct):**

> "CEOs at S&P 500 firms whose compensation exceeded $10 million received 40% of their pay from stock options, yet a one-standard-deviation increase in option grants predicts no significant improvement in firm ROA over the following three years (coeff. = 0.002, SE = 0.003)."

The first version tells the reader nothing. The second gives a concrete finding with a magnitude, a context, and a standard error -- exactly what Cochrane, Shapiro, and Goldin and Katz demand.

---

## Related Projects

Other useful tools for economists working with AI assistants:

- [awesome-econ-ai-stuff](https://github.com/meleantonio/awesome-econ-ai-stuff) -- Curated AI skills for economists (data analysis, Beamer, R)
- [claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow) -- Ready-to-fork Claude Code template for academics using LaTeX/R
- [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) -- Full academic writing pipeline with multi-reviewer simulation
- [claude-skills (econ/finance)](https://github.com/zirui-song/claude-skills) -- Claude Code skills for empirical research in economics and finance
- [anthropics/skills](https://github.com/anthropics/skills) -- Official Agent Skills specification and skill creator

---

## Contributing

Contributions are welcome. If you know of an authoritative economics writing guide that should be included, or if you have suggestions for improving the skill's formulas or rules, please open an issue or submit a pull request.

Areas where contributions are especially useful:

- Additional before/after examples
- Field-specific adaptations (development, trade, labor, macro, finance)
- Translations of the skill for other AI assistant platforms
- Corrections or refinements to existing rules

---

## License

This project is licensed under the [MIT License](LICENSE).

---

*Built by [Lu Han](https://luhan.io). Synthesizes the collective wisdom of the economics profession on how to write well.*
