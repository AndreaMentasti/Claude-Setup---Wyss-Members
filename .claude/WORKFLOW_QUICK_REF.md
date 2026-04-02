# Workflow Quick Reference

**Model:** Contractor (you direct, Claude orchestrates)

---

## The Loop

```
Your instruction
    ↓
[PLAN] (if multi-file or unclear) → Show plan → Your approval
    ↓
[EXECUTE] Implement, verify, done
    ↓
[REPORT] Summary + what's ready
    ↓
Repeat
```

---

## I Ask You When

- **Design forks:** "Option A (fast) vs. Option B (robust). Which?"
- **Code ambiguity:** "Spec unclear on X. Assume Y?"
- **Replication edge case:** "Just missed tolerance. Investigate?"
- **Scope question:** "Also refactor Y while here, or focus on X?"

---

## I Just Execute When

- Code fix is obvious (bug, pattern application)
- Verification (tolerance checks, tests, script runs)
- Documentation (logs, commits)
- Plotting (per established standards below)
- Committing (after you approve, I ship automatically)

---

## Quality Gates (No Exceptions)

| Score | Action |
|-------|--------|
| >= 80 | Ready to commit |
| < 80  | Fix blocking issues |

---

## Non-Negotiables

- **Path convention:** All paths relative to project root.
  Python: `import config as cfg` → use `cfg.DATA_PROCESSED`, `cfg.FIGURES`, etc.
  Stata: `global root "..."` set at top of every .do file → all paths via `$root`.
- **Seed convention:** Python: `random.seed(42)` at top if stochastic.
  Stata: `set seed 42` before any random draws.
- **Figure standards:** PNG format, 300 DPI (`dpi=300, bbox_inches='tight'` in Python;
  `width(2400)` in Stata), white background, no gridlines in base style.
- **Color palette:** Neutral grays for bars/lines; a single accent color for highlights.
  Avoid red/green combinations (colorblind accessibility).
- **Tolerance thresholds:** OLS point estimates ≤ 0.01 diff; SEs ≤ 0.05 diff.

---

## Preferences

**Visual:** Always publication-ready — clean axes, labeled, no chart junk.
**Reporting:** Concise bullets by default; full details on request.
**Session logs:** Always (post-plan, incremental, end-of-session).
**Replication:** Strict — flag near-misses (within 2× tolerance). Report exact diff.

---

## Exploration Mode

For experimental work, use the **Fast-Track** workflow:
- Work in `explorations/` folder
- 60/100 quality threshold (vs. 80/100 for production)
- No plan needed — just a research value check (2 min)
- See `.claude/rules/exploration-fast-track.md`

---

## Next Step

You provide task → I plan (if needed) → Your approval → Execute → Done.
