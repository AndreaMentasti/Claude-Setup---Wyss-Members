# Claude Code Setup — Wyss Academy for Nature

A ready-to-use Claude Code setup template for empirical research projects. Clone this, fill in the placeholders, and your team has a fully configured AI-assisted research workflow in minutes.

---

## What's Included

| Component | Description |
|-----------|-------------|
| `.claude/rules/` | Non-negotiable project rules Claude follows automatically |
| `.claude/agents/` | Specialist review agents (Python, Stata, domain, proofreader, etc.) |
| `.claude/skills/` | Slash commands (`/commit`, `/data-analysis`, `/review-stata`, `/lit-review`, etc.) |
| `.claude/hooks/` | Automation hooks (verify after edits, protect raw data, session logging) |
| `CLAUDE.md` | Claude's operating manual for the project |
| `ONBOARDING.md` | 20-minute onboarding guide for new collaborators |
| `SETUP.md` | Machine setup instructions (Python, Stata, PATH, plugin) |
| `COLLABORATION.md` | Git workflow guide for teams |
| `MEMORY.md` | Shared project memory — persists learnings across sessions |
| `code/py/config.py` | Two-folder path configuration (repo + shared data) |
| `code/stata/config_local.do.template` | Stata path configuration template |
| `templates/` | Templates for session logs, plans, quality reports |
| `quality_reports/` | Plans, session logs, merge reports |

---

## Quick Start

### 1. Use This Template

Click **"Use this template"** on GitHub (or clone directly):

```bash
git clone https://github.com/AndreaMentasti/Claude-Setup---Wyss-Members.git your_project
cd your_project
```

### 2. Fill in the Placeholders

Search for `[YOUR_PROJECT_NAME]`, `[YOUR_INSTITUTION]`, `[YOUR_GITHUB_REPO_URL]`, and `[YOUR_REPO_NAME]` across the following files and replace with your project's details:

- `CLAUDE.md`
- `ONBOARDING.md`
- `COLLABORATION.md`
- `MEMORY.md`

### 3. Connect Your Data Folder

The template uses a **two-folder design**:
- **Code** lives in GitHub (this repo)
- **Data** lives in a shared folder (Dropbox, SharePoint, etc.) — never committed to git

Each collaborator creates a local `config_local.py` / `config_local.do` that bridges the two. See `SETUP.md` for instructions.

### 4. Onboard Collaborators

Send new collaborators to `ONBOARDING.md`. They paste one prompt into Claude Code and their environment is fully configured.

---

## Design Principles

**Plan first.** Claude enters plan mode before non-trivial tasks and saves plans to `quality_reports/plans/`.

**Quality gates.** Nothing is committed below a score of 80/100. `/review-python` and `/review-stata` run automated quality checks.

**Two-tier memory.** `MEMORY.md` (committed) holds shared project knowledge. `.claude/state/personal-memory.md` (gitignored) holds machine-specific notes.

**Correlational framing.** The domain-reviewer agent flags causal language automatically. All observational findings use association language unless a valid identification strategy is in place.

**Raw data is sacred.** The `protect-files.sh` hook blocks writes to `data/rawdata/` at the tool level.

---

## Adapting to Your Project

1. **Edit `CLAUDE.md`** — update folder structure, commands, and pipeline stages for your project
2. **Edit `.claude/rules/project-rules.md`** — update the raw data paths for your datasets
3. **Edit `.claude/agents/domain-reviewer.md`** — customize the domain review criteria for your field
4. **Update `requirements.txt`** — add your Python dependencies
5. **Delete skills you don't need** — e.g. remove `compile-latex`, `translate-to-quarto` if you don't use LaTeX/Quarto

---

## Stack

Designed for research projects using **Python + Stata**, but adaptable to any combination of Python, R, and Stata. The `.claude/skills/` folder includes translators between all three.

---

## Questions?

Open an issue or contact the Wyss Academy for Nature research team.
