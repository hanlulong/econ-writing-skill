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
- **Dedicated formulas for every major section** -- Abstract (4-part formula), Introduction (Head's Hook-Question-Results-Antecedents-Roadmap formula), Literature Review (story-driven, embedded in the intro), and Conclusion (Bellemare's 4-part formula: Summary, Limitations, Policy, Future Research)
- **Identification strategy guidance** -- Specific writing advice for RCT, DiD, IV, RDD, Synthetic Control, and structural estimation papers
- **Theory paper support** -- Model presentation, proposition writing, and Glaeser's "start with an example" approach
- **Style rules from McCloskey and Cochrane** -- active voice, concrete language, triangular structure, reader-first writing
- **Modern empirical practices** -- pre-registration, multiple testing, specification robustness, transparency and reproducibility
- **Tables and figures best practices** -- self-contained captions, figure vs. table trade-offs, data visualization from Schwabish (JEP)
- **Before/after examples** -- see how vague, passive, throat-clearing prose transforms into clear, concrete economics writing
- **Expanded revision checklist** -- 22-item pre-submission checklist covering content, style, and modern standards

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

The skill works in three modes:

- **Drafting**: generates new text following the formulas and rules, marking areas that need your specific results with `[AUTHOR: ...]` placeholders.
- **Rewriting**: identifies violations of the rules (passive voice, vague language, buried leads, throat-clearing) and fixes them while preserving your meaning and contribution.
- **Reviewing**: checks existing text against all rules and provides a detailed report of issues with suggested fixes.

---

## Common Use Cases

- **Drafting a new paper section** -- Generate a first draft of any section (abstract, introduction, data, results, conclusion) that follows established formulas from the start.
- **Rewriting existing text for clarity** -- Tighten prose, eliminate passive voice, cut throat-clearing, and make results concrete.
- **Writing an introduction from scratch** -- Follow Head's formula exactly: Hook, Research Question, Main Results, Antecedents and Value Added, Literature Review, Roadmap.
- **Conducting and writing a literature review** -- Build a story-driven review of the 5-10 closest papers, embedded in the introduction, that establishes your paper's niche.
- **Writing up existing empirical results** -- Present results in the correct order (main result first, most parsimonious to least parsimonious) with proper emphasis on economic significance.
- **Writing a theory paper** -- Structure model presentation, write propositions with intuition before proofs, generate testable predictions.
- **Structuring a mixed theory-empirical paper** -- Map empirical tests back to specific model predictions.
- **Preparing a presentation** -- Get advice on slide structure, pacing, and delivery following Shapiro, Cochrane, and others ("Gene Fama usually starts with 'Look at table 1.' That's a good model.").

---

## What's Inside

The skill includes two files:

### `SKILL.md` (main skill file)

1. **Core Principles** -- Seven foundational rules (Reader First, Triangular Style, One Central Contribution, Concrete Not Abstract, Every Word Counts, Active Voice, Simple over Complex)
2. **Section Formulas** -- Step-by-step formulas for the Abstract, Introduction (with Head's formula), Literature Review, Conclusion (Bellemare's formula), Results, and Title
3. **Style Rules** -- Detailed guidance on sentence structure, word choice, voice, pronouns, footnotes, numbers, notation, and paragraphs
4. **Tables and Figures** -- Best practices for captions, formatting, figure vs. table trade-offs, and data visualization
5. **Empirical Work Rules** -- Identification, results presentation, heterogeneity analysis, mechanisms, and common mistakes
6. **Modern Empirical Practices** -- Pre-registration, multiple testing, specification robustness, transparency
7. **Paper Structure Templates** -- Templates for applied, theory, mixed theory-empirical, and structural papers
8. **Use Case Instructions** -- Specific instructions for drafting, rewriting, introductions, literature reviews, abstracts, conclusions, results, theory papers, and presentations
9. **Revision Checklist** -- A 22-item pre-submission checklist covering content, style, and modern standards

### `identification-strategies.md` (supporting file)

Detailed writing guidance tailored to each identification strategy: RCT, DiD, IV, RDD, Synthetic Control, Structural Estimation, and Descriptive/Measurement papers. Includes an introduction adaptation table showing how to adjust hooks, results paragraphs, and key threats for each paper type.

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
