# Econ Writing Skill

**An Agent Skill that transforms AI assistants into expert economics paper writers, synthesizing best practices from 50+ authoritative guides by Nobel laureates, Clark Medal winners, and leading economists.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-green.svg)](https://agentskills.io)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Ready-blueviolet.svg)](https://docs.anthropic.com/en/docs/claude-code)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI%20Codex-Ready-black.svg)](https://openai.com/index/codex/)

---

## What Is This?

Econ Writing Skill is an open-source [Agent Skill](https://agentskills.io) that gives AI coding assistants deep knowledge of how to write economics papers. It distills actionable advice from over 50 guides by John Cochrane, Deirdre McCloskey, Jesse Shapiro, Keith Head, Marc Bellemare, Claudia Goldin, Michael Kremer, and many others into a single structured skill file. Compatible with the Agent Skills open standard, it works with Claude Code and OpenAI Codex out of the box.

---

## Key Features

- **Dedicated formulas for every major section** -- Abstract (4-part formula), Introduction (Head's Hook-Question-Results-Antecedents-Roadmap formula), Literature Review (story-driven, embedded in the intro), and Conclusion (Bellemare's 4-part formula: Summary, Limitations, Policy, Future Research)
- **Style rules from McCloskey and Cochrane** -- active voice, concrete language, triangular structure, reader-first writing
- **Empirical work and identification guidance** -- Cochrane's "three most important things: Identification, Identification, Identification"
- **Tables and figures best practices** -- self-contained captions, sensible units, data visualization principles from Schwabish (JEP)
- **Before/after examples** -- see how vague, passive, throat-clearing prose transforms into clear, concrete economics writing
- **Revision checklist** -- a pre-submission checklist covering every common mistake

---

## Installation

### For Claude Code

```bash
git clone https://github.com/hanlulong/econ-writing-skill.git
cp -r econ-writing-skill/.claude/skills/econ-write/ /path/to/your/project/.claude/skills/econ-write/
```

### For OpenAI Codex

```bash
git clone https://github.com/hanlulong/econ-writing-skill.git
cp -r econ-writing-skill/.agents/skills/econ-write/ /path/to/your/project/.agents/skills/econ-write/
```

### Manual Installation

You can also copy the single `SKILL.md` file directly into the appropriate directory:

- Claude Code: `.claude/skills/econ-write/SKILL.md`
- OpenAI Codex: `.agents/skills/econ-write/SKILL.md`

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

The skill works in two modes:

- **Drafting**: generates new text following the formulas and rules, marking areas that need your specific results with `[AUTHOR: ...]` placeholders.
- **Rewriting**: identifies violations of the rules (passive voice, vague language, buried leads, throat-clearing) and fixes them while preserving your meaning and contribution.

---

## Common Use Cases

- **Drafting a new paper section** -- Generate a first draft of any section (abstract, introduction, data, results, conclusion) that follows established formulas from the start.
- **Rewriting existing text for clarity** -- Tighten prose, eliminate passive voice, cut throat-clearing, and make results concrete.
- **Writing an introduction from scratch** -- Follow Head's formula exactly: Hook, Research Question, Main Results, Antecedents and Value Added, Literature Review, Roadmap.
- **Conducting and writing a literature review** -- Build a story-driven review of the 5-10 closest papers, embedded in the introduction, that establishes your paper's niche.
- **Writing up existing empirical results** -- Present results in the correct order (main result first, most parsimonious to least parsimonious) with proper emphasis on economic significance.
- **Preparing a presentation** -- Get advice on slide structure, pacing, and delivery following Shapiro, Cochrane, and others ("Gene Fama usually starts with 'Look at table 1.' That's a good model.").

---

## What's Inside

The skill file (`SKILL.md`) contains:

1. **Core Principles** -- Seven foundational rules (Reader First, Triangular Style, One Central Contribution, Concrete Not Abstract, Every Word Counts, Active Voice, Simple over Complex)
2. **Section Formulas** -- Step-by-step formulas for the Abstract, Introduction (with Head's formula), Literature Review, Conclusion (Bellemare's formula), Results, and Title
3. **Style Rules** -- Detailed guidance on sentence structure, word choice, voice, pronouns, footnotes, numbers, notation, and paragraphs
4. **Tables and Figures** -- Best practices for captions, formatting, and data visualization
5. **Empirical Work Rules** -- Identification strategy, results presentation, and common mistakes to avoid
6. **Paper Structure Overview** -- The standard 10-section applied economics paper template
7. **Use Case Instructions** -- Specific instructions for drafting, rewriting, introductions, literature reviews, abstracts, conclusions, results, and presentations
8. **Revision Checklist** -- A pre-submission checklist covering 15 critical items

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
