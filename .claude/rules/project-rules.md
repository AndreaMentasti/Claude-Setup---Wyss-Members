# Project Rules — Populism and Narratives

**These rules are non-negotiable.** They apply to every task, every session.
To change a rule, edit this file explicitly — never override silently.

---

## Rule 1: Raw Data Is Sacred

**NEVER delete, overwrite, or modify any file in `data/rawdata/`.**

- `data/rawdata/virality/` — tweets and GPT predictions from the virality project
- `data/rawdata/politicians_tweets/` — politician tweet datasets
- `data/rawdata/usa_elections_MIT/` — MIT election data
- `data/rawdata/media_data/` — Google Trends and TV mention data
- `data/rawdata/gadm_410-gpkg/` — geographic boundary shapefiles

If you need a cleaned or transformed version, write it to `data/processed/`.
The protect-files.sh hook enforces this at the tool level, but the rule holds even
if the hook is bypassed.

**Rationale:** Raw data is irreproducible. Any transformation must be traceable to the raw source.

---

## Rule 2: Correlational Framing

**Never use causal language (causes, leads to, drives, effect of) without a valid
identification strategy (IV, RD, DiD, experiment).**

The correct framing for this project is:
- ✅ "populist narratives are associated with higher engagement"
- ✅ "narrative framing predicts tweet virality"
- ✅ "the correlation between populist rhetoric and engagement is..."
- ❌ "populist narratives drive engagement"
- ❌ "narrative framing causes higher vote share"

The domain-reviewer agent flags causal language as CRITICAL. Fix before committing.

---

## Rule 3: All Paths Via Config

**Python scripts must use either `import config as cfg` (new scripts) or
`import config_path; P = config_path.change_paths()` (existing scripts).**
**Stata scripts must set `global root "..."` and use `$root` for all paths.**
Both Python config modules read `DATA_ROOT` from the gitignored `config_local.py`.

No hardcoded absolute paths anywhere. This makes the project portable across machines.

---

## Rule 4: Publication-Ready Figures Only

**All figures saved to `output/figures/` must meet publication standards:**

- PNG format
- 300 DPI (Python: `dpi=300`; Stata: `width(2400)`)
- White background
- Labeled axes with units
- No chart junk (no unnecessary gridlines, 3D effects, etc.)

If a figure is exploratory/diagnostic, save it to `explorations/` instead.

---

## Rule 5: Scripts Must Run Clean

**Every `.py` and `.do` script must run to completion with exit code 0
before it can be committed.**

- Python: `python code/py/<script>.py` — no errors, no unhandled exceptions
- Stata: `stata -b do code/stata/<script>.do` — `.log` file shows no `r(` errors

The verify-reminder hook will remind you after every edit.

---

## Rule 6: "old" Folders Are Read-Only Archives

**Never modify, delete, rename, or create files inside any folder named `old/`.**

These folders are treated as frozen archives — they exist for reference only.
If you need a modified version of something inside `old/`, copy it out and
save the new version in the appropriate active directory.

**Rationale:** `old/` folders preserve prior working states. Overwriting them
destroys the ability to trace what changed and why.

---

## Rule 7: Ask Before Modifying Scripts

**Always ask the user for explicit permission before editing any `.py` or `.do` file.**

Before making any change to a Python or Stata script, state:
- Which file you intend to modify
- What change you plan to make and why

Then wait for the user to confirm before proceeding. This applies even when a fix seems obvious or minor.

**Rationale:** Python and Stata scripts are the core analytical pipeline. Unintended changes can silently alter results, break reproducibility, or introduce hard-to-trace bugs.

---

## Amendment Protocol

To change a rule: state "I want to amend Rule N" in the chat.
Claude will ask whether this is a permanent amendment (update this file)
or a one-time override (proceed without changing the rule).
