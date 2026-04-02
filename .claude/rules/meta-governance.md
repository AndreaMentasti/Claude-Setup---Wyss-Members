# Meta-Governance: Research Project Conventions

**This repository is a template for collaborative research projects at [YOUR_INSTITUTION].**

These conventions ensure consistency across collaborators and machines.

---

## Decision Framework

When creating or modifying content, ask:

### "Should this be committed or kept local?"

**Commit to repo (shared across collaborators):**
- Code (Python scripts, Stata do-files, prompts)
- Output (figures, tables, logs)
- Workflow infrastructure (.claude/ rules, skills, agents, hooks)
- MEMORY.md (project learnings that help all collaborators)
- Quality reports (plans, session logs, merge reports)

**Keep local (gitignored, machine-specific):**
- `config_local.py` / `config_local.do` (data paths)
- `.claude/settings.local.json` (personal permissions)
- `.claude/state/` (session state)
- API keys, `.env` files
- Personal preferences

---

## Memory Management: Two-Tier System

### MEMORY.md (root directory, committed)

**Purpose:** Project learnings that help all collaborators.

**What goes here:**
- Pipeline decisions: `[LEARN:project] Stage 3 classification uses GPT-4o-mini for cost`
- Workflow patterns: `[LEARN:workflow] Always verify merge outcomes after pd.merge()`
- Analysis decisions: `[LEARN:analysis] Cluster standard errors at state level, not robust`

**Review cadence:** After every significant session.

**Size limit:** Keep under 200 lines (loaded into Claude's context every session).

---

### .claude/state/personal-memory.md (gitignored, local only)

**Purpose:** Machine-specific learnings for a single collaborator.

**What goes here:**
- Machine setup: `[LEARN:setup] Stata 17 on this PC lives at C:/Program Files/Stata17/`
- Tool quirks: `[LEARN:python] Need encoding='utf-8' on this Windows machine`
- Local paths: `[LEARN:paths] Dropbox at C:\Users\YourName\Dropbox\`

**Review cadence:** As needed.

---

## Cross-Machine / Cross-Collaborator Access

**Each collaborator:**
- Clones the repo → gets MEMORY.md, all infrastructure, code, outputs
- Creates own `config_local.py` / `config_local.do` pointing to their local data folder
- Builds `.claude/state/personal-memory.md` for their machine

**Key insight:** Project knowledge syncs via git; machine-specific config stays local.

---

## Workflow Standards

### Plan-First
- Enter plan mode for non-trivial tasks (>3 files, >1 hour, multi-step)
- Save plans to `quality_reports/plans/YYYY-MM-DD_description.md`
- Don't skip planning for "quick fixes" that turn into multi-hour tasks

### Quality Gates
- Run quality scoring before commits
- Nothing ships below 80/100
- Don't commit "WIP" code without quality verification

### Context Survival
- Update MEMORY.md with [LEARN] entries after sessions
- Save active plans to disk before compression
- Keep session logs current
- Don't rely solely on conversation history (it compresses)

---

## Quick Reference Table

| Content Type | Commit to Repo? | Where It Goes | Syncs Across Collaborators? |
|--------------|----------------|---------------|---------------------------|
| Python/Stata code | Yes | `code/` | Yes (via git) |
| Output (figures, tables) | Yes | `output/` | Yes |
| Workflow infrastructure | Yes | `.claude/` | Yes |
| Project learnings | Yes | `MEMORY.md` | Yes |
| Session logs, plans | Yes | `quality_reports/` | Yes |
| Machine-specific config | No | `config_local.*` | No (gitignored) |
| Local settings | No | `.claude/settings.local.json` | No (gitignored) |
| Session state | No | `.claude/state/` | No (gitignored) |
| API keys | No | `.env` | No (gitignored) |
| Raw data | No | `data/rawdata/` | Shared via Dropbox/cloud |
| Processed data | No | `data/processed/` | Shared via Dropbox/cloud |

---

## Amendment Process

**When to amend this file:**
- Collaboration workflow changes (new collaborator, new tool)
- Memory system needs adjustment
- Git/shared-storage boundaries shift

**Protocol:**
1. Propose change in chat
2. Update this file
3. Document with `[LEARN:meta]` entry in MEMORY.md
