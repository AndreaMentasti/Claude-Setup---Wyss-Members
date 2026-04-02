# Project Memory — Populism and Narratives

Two sections: **Project Knowledge** (non-obvious decisions and lessons) and **Progress Log** (what was done, session by session).

---

## Project Knowledge

### Research
- **Research question:** How do populist narratives in political tweets relate to engagement and electoral outcomes? Correlational framing — causal language requires identification strategy (IV, RD, DiD, experiment).
- **Data:** Dropbox `populism_and_narratives/data/rawdata/`: virality/ (4.2M tweets + GPT predictions), politicians_tweets/, usa_elections_MIT/, media_data/ (Google Trends, TV mentions), gadm_410-gpkg/. All rawdata is PROTECTED — never overwrite.
- **Tweet data limitation:** Current tweet dataset lacks a candidate/party link — needed for real engagement → vote share analysis. Merge key is missing.

### Pipeline
- **Stages:** 01_data_prep.py (geocoding) → 02-04_annotation_openai (3-stage GPT classification) → 05_visibrain → 06-07_prediction_prep → Stata analysis. OpenAI scripts need API key via .env or environment variable.
- **Two Python config modules coexist:** existing scripts use `config_path.change_paths()` (returns dict); new scripts use `import config as cfg` (module-level constants). Both read DATA_ROOT from gitignored `config_local.py`.

### Environment (Raffaella's machine)
- **Stata:** StataNow 19 (SE) at `C:\Program Files\StataNow19\`. On PATH via wrapper at `~/bin/stata`.
- **Stata PDF manuals:** 37 PDFs (~17K pages) at `C:\Program Files\StataNow19\docs\`. Use `pdftotext` for prose, `pdfplumber` for tables. pandoc cannot read PDFs.
- **Pandoc 3.9:** installed at `~/tools/pandoc-3.9/`. PowerShell profile is at the OneDrive Documents path (non-standard).
- **Stata logs:** go to `quality_reports/stata_logs/` — wrapper auto-moves batch logs there.

### Workflow lessons
- **Stata grouped bar charts:** `graph bar` can't do grouped bars with a color legend; use `twoway bar` with manual x-positions after `reshape wide`. Drop extra variables before `reshape wide` or it fails.
- **OneDrive + git:** OneDrive locks `.git/` files — recommend moving repo outside OneDrive eventually.

---

## Progress Log

### 2026-03-12 — Workflow configuration setup
- Adapted forked `claude-code-my-workflow` template to this project
- Rewrote CLAUDE.md (project name, folder structure, commands, pipeline state)
- Created `python-code-conventions.md` and `stata-code-conventions.md` rules
- Rewrote `domain-reviewer.md` for empirical social science (was for lecture slides)
- Extended `verify-reminder.py` hook to cover `.py` and `.do` files
- Extended `protect-files.sh` to protect raw data files
- Filled `WORKFLOW_QUICK_REF.md` with concrete project standards

### 2026-03-13 — Setup walkthrough & capability demo
- Verified `01_data_prep.py` runs clean (15 tweets, 12 U.S.)
- Found and fixed Stata `$root` path error (extra `\Attachments\`)
- Created `output/figures/` and `output/tables/` folder structure
- Wrote `02_scatter_engagement.py` and `03_vote_share_barplot.py` as demos
- Full Python (28 issues) and Stata (13 issues) review — all fixed
- Created branch, PR #1 merged to main
- Built first version of `/translate-code` skill (later replaced)

### 2026-03-16 — Stata environment & skills
- Stata wrapper on PATH (`~/bin/stata`) — alias doesn't work in non-interactive shells
- Pandoc 3.9 installed, pdfplumber already present
- Created `SETUP.md` collaborator guide
- Created `/stata` skill (project-level + user-level) with PDF manual index
- Created `/script-translator` skill (SKILL.md + 6 bodies/ files for all language pairs)
- Tested end-to-end Stata run (`1-test_analysis.do` — table + scatter, r=0.9986)
- Created `quality_reports/stata_logs/`, updated wrapper and all do-files
- PR #2 and #3 merged: fixed hardcoded paths in py scripts and stata-reviewer

### 2026-03-18 — Rules and memory cleanup
- Added Rule 6: `old/` folders are read-only archives
- Rewrote MEMORY.md: stripped generic template content, added progress log

---

## Open Items
- [ ] Fill in `[INSTITUTION]` in `CLAUDE.md`
- [ ] Clean up test translation artifacts (`test_translation.py` and outputs) from 2026-03-16
- [ ] Start Stata analysis — pipeline Stage 5 is next (`1-analysis_*.do`)
- [ ] Add bibliography entries for key social media + elections papers
