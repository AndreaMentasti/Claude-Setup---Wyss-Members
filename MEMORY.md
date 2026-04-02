# Project Memory — [YOUR_PROJECT_NAME]

Two sections: **Project Knowledge** (non-obvious decisions and lessons) and **Progress Log** (what was done, session by session).

> This file is loaded into Claude's context every session. Keep it under 200 lines.
> Add entries with `[LEARN:category] wrong → right` when Claude is corrected.

---

## Project Knowledge

### Research
- **Research question:** [Describe your research question here]
- **Data:** [Describe your data sources and key datasets]
- **Key constraint:** [Note any important data limitations or methodological constraints]

### Pipeline
- **Stages:** [Describe your pipeline stages in order]
- **Config pattern:** Python scripts use `import config as cfg`; Stata scripts use `$root` and `$data_root`

### Environment
- **[LEARN:setup]** Add machine-specific learnings to `.claude/state/personal-memory.md` (gitignored), not here

### Workflow lessons
- **[LEARN:workflow]** Always verify merge outcomes after `pd.merge()` — check row counts
- **[LEARN:workflow]** `bysort` in Stata auto-sorts; `by` requires prior sort — always use `bysort`

---

## Progress Log

### [YYYY-MM-DD] — [Session description]
- [What was done]
- [Key decisions made]
- [Issues encountered and resolved]

---

## Open Items
- [ ] Fill in `[YOUR_PROJECT_NAME]` and `[YOUR_INSTITUTION]` in CLAUDE.md
- [ ] Fill in collaborator names and repo URL in COLLABORATION.md
- [ ] Add project-specific pipeline stages to CLAUDE.md
- [ ] Update `requirements.txt` with your project's Python dependencies
