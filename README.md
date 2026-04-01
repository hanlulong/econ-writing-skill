# Econ Writing Skill

**Turn your AI assistant into an expert economics paper writer.** Synthesizes 50+ guides by Cochrane, McCloskey, Shapiro, Head, Bellemare, Goldin, Glaeser, Kremer, and other leading economists into a single skill file.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-green.svg)](https://agentskills.io)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Ready-blueviolet.svg)](https://docs.anthropic.com/en/docs/claude-code)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI%20Codex-Ready-black.svg)](https://openai.com/index/codex/)

## Quick Start

```bash
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/install.sh | bash
```

Then restart your session and use:

```
/econ-write write introduction for my DiD paper on minimum wage
/econ-write rewrite this abstract to be concrete and under 150 words
/econ-write audit my full paper and score it
```

---

## Before / After

**Before** (Cochrane's illustration of what NOT to write):

> "I analyze data on executive compensation and find many interesting results."

**After** (same topic, rewritten by the skill):

> "CEOs at S&P 500 firms whose compensation exceeded $10 million received 40% of their pay from stock options, yet a one-standard-deviation increase in option grants predicts no significant improvement in firm ROA over the following three years (coeff. = 0.002, SE = 0.003)."

12 full before/after examples (abstract, introduction, literature review, results, conclusion, data section, theory paper, heterogeneity, title evaluation, referee response, macro DSGE) in [`examples/before-after.md`](examples/before-after.md).

---

## What It Does

### Write Every Section

Dedicated formulas for each part of a paper:

| Section | Formula / Approach |
|---------|-------------------|
| Abstract | 4-part: What / How / Findings / Implications (under 150 words) |
| Introduction | Head's formula: Hook, Question, Results, Literature & Value Added, Roadmap |
| Model | Glaeser/Varian: example first, simplest model, intuition before proofs |
| Data | Source/time/unit first, sample construction, descriptive stats |
| Results | Main result first, parsimonious → complex, economic significance |
| Conclusion | 3-part: Summary, Implications, Future Research (no caveats) |
| Title | Under 12 words, treatment + outcome, scored on clarity and memorability |

### Handle Any Paper Type

Applied empirical, pure theory, mixed theory-empirical, structural, and descriptive -- each with tailored structure templates and conventions.

### Adapt to Your Identification Strategy

Writing advice for 13 strategies: RCT, DiD (including staggered), IV, RDD, Synthetic Control, Synthetic DiD, Bunching, Shift-Share/Bartik, Event Studies, ML for Causal Inference, Structural Estimation, Descriptive, plus guidance for papers combining multiple strategies.

### Enforce Style Rules

- 7 core principles from Cochrane, McCloskey, and Goldin & Katz
- Active voice, concrete language, triangular structure
- Anti-AI writing patterns: banned words, sentence variety, field-specific vocabulary
- Phrases to delete on sight ("It should be noted that...", "This paper contributes to...")

### Review and Audit Papers

- **3 simulated reviewers**: Methodologist, Field Expert, Writing Critic
- **100-point scoring rubric** across 8 dimensions
- **Anti-AI detection checklist**
- **Journal fit assessment** for top-5 vs. field journal targeting

### Cover the Full Academic Workflow

| Task | What it does |
|------|-------------|
| Job market paper | Title, abstract, introduction polish, length, signaling breadth |
| Grant proposal | NSF / ERC structure, feasibility, budget justification, timeline |
| Referee response | Point-by-point with evidence, respectful tone, page references |
| Policy brief | Plain language, everyday magnitudes, concrete recommendations |
| WP → journal | Cutting strategy, journal length norms, appendix organization |
| Dissertation | Three-essays format, chapter structure, authorship rules |
| Survey paper | JEL / JEP / Handbook chapter conventions |
| Replication package | AEA Data Editor standards, data citation, README template |
| AI disclosure | AEA and Econometric Society journal policies |
| Presentations | Shapiro/Cochrane: result first, tables not bullets |
| Coauthorship | Voice consistency, designated voice editor |
| LaTeX | Tables, figures, natbib, journal formatting, Beamer |

### Adapt to Your Field

Field-specific conventions for macro (calibration tables, IRFs, DSGE), trade (gravity, PPML), development (CONSORT, cost-effectiveness), and finance (Fama-MacBeth, winsorization).

---

## Installation

### One-Line Install (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/install.sh | bash
```

Installs to `~/.claude/skills/econ-write/` and `~/.codex/skills/econ-write/`. Available in all projects immediately.

### Other Methods

<details>
<summary>Git clone, npx, manual install, install options</summary>

**Git clone:**
```bash
git clone https://github.com/hanlulong/econ-writing-skill.git
cd econ-writing-skill
./install.sh              # Global install (default)
./install.sh --local .    # Install to current project only
```

**npx:**
```bash
npx skills add hanlulong/econ-writing-skill
```

**Manual (global):**
```bash
mkdir -p ~/.claude/skills/econ-write
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/.claude/skills/econ-write/SKILL.md -o ~/.claude/skills/econ-write/SKILL.md
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/.claude/skills/econ-write/identification-strategies.md -o ~/.claude/skills/econ-write/identification-strategies.md
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/.claude/skills/econ-write/latex-tips.md -o ~/.claude/skills/econ-write/latex-tips.md
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/.claude/skills/econ-write/review-checklist.md -o ~/.claude/skills/econ-write/review-checklist.md
```

**Install flags:**

| Flag | Behavior |
|------|----------|
| (default) | Install globally for all projects |
| `--local` | Install to current project only |
| `--claude` | Install for Claude Code only |
| `--codex` | Install for Codex only |

</details>

---

## What's Inside

| File | Lines | Contents |
|------|-------|----------|
| `SKILL.md` | 773 | Core principles, section formulas, style rules, use case instructions, revision checklist, field conventions, AEA standards |
| `identification-strategies.md` | 153 | Writing guidance for 13 identification strategies + adaptation table |
| `latex-tips.md` | 149 | Document structure, tables, figures, bibliography, journal requirements, Beamer |
| `review-checklist.md` | 122 | 3 simulated reviewers, 100-point rubric, anti-AI checklist, journal fit |

Plus [`evals/test-cases.md`](evals/test-cases.md) (13 test cases for benchmarking skill output quality) and [`examples/before-after.md`](examples/before-after.md) (12 before/after transformations).

---

## Sources

Synthesizes **50+ authoritative guides**. The top 10:

| # | Source | Author | Institution |
|---|--------|--------|-------------|
| 1 | Writing Tips for Ph.D. Students | John H. Cochrane | Chicago Booth / Hoover |
| 2 | Economical Writing | Deirdre N. McCloskey | UIC / Chicago |
| 3 | Four Steps to an Applied Micro Paper | Jesse M. Shapiro | Harvard |
| 4 | The Introduction Formula | Keith Head | UBC Sauder |
| 5 | Ten Most Important Rules of Writing Your JMP | Claudia Goldin & Lawrence F. Katz | Harvard |
| 6 | Writing Tips for Economics Research Papers | Plamen Nikolov | Binghamton / Harvard |
| 7 | How to Write Applied Papers in Economics | Marc F. Bellemare | U Minnesota |
| 8 | How to Give an Applied Micro Talk | Jesse M. Shapiro | Harvard |
| 9 | Writing Papers: A Checklist | Michael Kremer | Harvard / Chicago |
| 10 | An Economist's Guide to Visualizing Data | Jonathan A. Schwabish | JEP (AEA) |

Includes **Nobel laureates** (Goldin 2023, Kremer 2019), a **Clark Medal winner** (Shapiro 2022), and editors of leading journals. Full ranked list: [`sources/SOURCES_RANKED.md`](sources/SOURCES_RANKED.md).

---

## Contributing

Contributions welcome -- open an issue or submit a PR. Especially useful:

- Additional before/after examples
- Field-specific adaptations (development, trade, labor, macro, finance)
- Translations for other AI assistant platforms
- Corrections or refinements to existing rules

---

## License

[MIT License](LICENSE)

---

*Built by [Lu Han](https://luhan.io). Synthesizes the collective wisdom of the economics profession on how to write well.*
