---
name: data-analysis
description: End-to-end Python+Stata data analysis workflow from exploration through regression to publication-ready tables and figures
argument-hint: "[dataset path or description of analysis goal]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]
---

# Data Analysis Workflow

Run an end-to-end data analysis using Python (data prep) and Stata (regression/output).

**Input:** `$ARGUMENTS` — a dataset path (e.g., `data/processed/tweets/all_tweets_classified.dta`) or a description of the analysis goal (e.g., "correlate populist narrative share with tweet engagement by state").

---

## Constraints

- **Follow Python conventions** in `.claude/rules/python-code-conventions.md`
- **Follow Stata conventions** in `.claude/rules/stata-code-conventions.md`
- **Python scripts** go in `code/py/` — use `config_path.change_paths()` (existing) or `import config as cfg` (new)
- **Stata scripts** go in `code/stata/` — use `$root` and `$data_root` via `config_local.do`
- **Figures** to `output/figures/` (PNG, 300 DPI, white background)
- **Tables** to `output/tables/` (LaTeX, booktabs)
- **Processed data** to Dropbox `data/processed/` as `.dta` (Stata-readable) and `.csv` (human-readable)
- **Correlational framing only** — no causal language without identification strategy

---

## Workflow Phases

### Phase 1: Data Exploration (Python)

1. Read `.claude/rules/python-code-conventions.md` for standards
2. Create or edit a Python script with proper header (docstring with inputs/outputs)
3. Load and inspect the dataset:
   - `df.shape`, `df.dtypes`, `df.describe()`
   - Missingness rates per column
   - Key variable distributions
4. Save diagnostic figures to `output/figures/` (prefix with `diag_`)

```python
import config_path
import pandas as pd
import matplotlib.pyplot as plt

P = config_path.change_paths()
df = pd.read_stata(P["processed"] / "tweets" / "dataset.dta")

print(f"Shape: {df.shape}")
print(df.describe())
```

### Phase 2: Data Preparation (Python)

If new variables or transformations are needed:
1. Create/modify a prep script in `code/py/`
2. Use `.copy()` after any filter/slice
3. Verify merges: check `_merge` distribution, assert row counts
4. Save output as both `.csv` and `.dta`:

```python
df.to_stata(P["processed"] / "tweets" / "analysis_ready.dta", write_index=False)
df.to_csv(P["processed"] / "tweets" / "analysis_ready.csv", index=False, encoding="utf-8")
```

### Phase 3: Main Analysis (Stata)

1. Create a `.do` file in `code/stata/` with proper header
2. Load data via `$data_root`:
   ```stata
   version 17
   clear all
   set more off

   do "$root/code/stata/config_local.do"
   use "$data_root/processed/tweets/analysis_ready.dta", clear
   ```
3. Inspect before regressing: `tab`, `sum`, check N
4. Build specifications progressively: simple OLS → add controls → add FE → cluster SE
5. Use `eststo` to store models for comparison

### Phase 4: Publication-Ready Output (Stata)

**Tables:**
```stata
esttab using "$root/output/tables/table_main.tex", ///
    booktabs label replace ///
    title("Engagement and Populist Narratives") ///
    mtitles("OLS" "Controls" "State FE") ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    b(3) se(3)
```

**Figures:**
```stata
twoway (scatter engagement narrative_share), ///
    xtitle("Populist Narrative Share") ytitle("Engagement") ///
    graphregion(color(white)) bgcolor(white)
graph export "$root/output/figures/fig_name.png", replace width(2400)
```

### Phase 5: Review

1. Run the script: `stata -b do code/stata/<script>.do`
2. Check the log for errors: `grep "^r(" <script>.log`
3. Verify all output files exist in `output/figures/` and `output/tables/`
4. Run `/review-python` and `/review-stata` on the generated scripts

---

## Important

- **Reproduce, don't guess.** If the user specifies a regression, run exactly that.
- **Show your work.** Print summary statistics before jumping to regression.
- **Check for issues.** Multicollinearity, outliers, clustered errors at right level.
- **No hardcoded paths.** All paths via config modules.
- **Correlational framing.** "associated with", "predicts", "correlated" — never causal.
