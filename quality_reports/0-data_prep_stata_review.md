# Stata Code Review: 0-data_prep.do
**Date:** 2026-03-12
**Reviewer:** stata-reviewer (via review-stata skill)

---

## Summary

- **Overall assessment:** MAJOR ISSUES
- **Total issues:** 13
- **Critical:** 2 — blocks reproducibility on any machine
- **High:** 6 — blocks professional quality / correctness
- **Medium:** 3 — improvement recommended
- **Low:** 2 — style / polish

---

## Issues

### Issue 1: Missing `version` declaration
- **Location:** `0-data_prep.do`, line 1 (should be first line after header)
- **Category:** Header & Structure / Reproducibility
- **Severity:** Critical
- **Current:** *(no version statement anywhere)*
- **Proposed fix:**
  ```stata
  version 17
  ```
  Add as the very first executable line, before `clear all`.
- **Rationale:** Without `version`, Stata's behavior may change silently across updates. Required for replication packages.

---

### Issue 2: Hardcoded absolute path with wrong user and wrong project name
- **Location:** `0-data_prep.do`, line 25
- **Category:** Reproducibility
- **Severity:** Critical
- **Current:**
  ```stata
  global DIR = "C:\Users\RaffaellaIntinghero\Dropbox\mini-toy-project"
  ```
- **Proposed fix:**
  ```stata
  global root "C:\Users\AndreaMentasti\Dropbox\example-project"
  ```
  - Rename macro from `DIR` to `root` (project convention)
  - Update path to correct user and project name
  - Drop the `=` sign (Stata convention for globals is `global name "value"`, not `global name = "value"`)
- **Rationale:** This path will fail on any other machine, and currently refers to a different user (`RaffaellaIntinghero`) and a different project folder (`mini-toy-project`). Nothing downstream can run correctly.

---

### Issue 3: No log file opened
- **Location:** `0-data_prep.do`, line 17
- **Category:** Log & Error Checking
- **Severity:** High
- **Current:**
  ```stata
  capture log close   ← closes a previous log, but never opens one
  ```
- **Proposed fix:**
  ```stata
  capture log close
  log using "$root/quality_reports/0-data_prep.log", replace text
  ```
  Add `log close` at the very end of the script.
- **Rationale:** Without a log, there is no record of what ran, what the results were, or where errors occurred. The `capture log close` at the top is correct practice but is only useful if a log is actually opened.

---

### Issue 4: `esttab` missing required options — not publication-ready
- **Location:** `0-data_prep.do`, lines 40–43
- **Category:** Table Output
- **Severity:** High
- **Current:**
  ```stata
  esttab using "output/tables/summary_stats.tex", ///
      cells("mean(fmt(2)) sd(fmt(2)) min max count") ///
      title("Summary Statistics - Tweet Data") ///
      replace
  ```
- **Proposed fix:**
  ```stata
  esttab using "$root/Figures/summary_stats.tex", ///
      cells("mean(fmt(2)) sd(fmt(2)) min(fmt(2)) max(fmt(2)) count") ///
      title("Summary Statistics -- Tweet Data") ///
      label booktabs replace
  ```
- **Rationale:** Missing `booktabs` (required for publication formatting) and `label` (uses variable labels instead of raw names). Also see Issue 5 for the path problem.

---

### Issue 5: Output paths use `output/` directory which doesn't match project convention and may not exist
- **Location:** `0-data_prep.do`, lines 41 and 59
- **Category:** Reproducibility / Table Output / Figure Output
- **Severity:** High
- **Current:**
  ```stata
  esttab using "output/tables/summary_stats.tex", ...
  graph export "output/figures/vote_share_by_state.png", replace
  ```
- **Proposed fix:**
  ```stata
  * Tables → Figures/ (project convention)
  esttab using "$root/Figures/summary_stats.tex", ...

  * Figures → Figures/ (project convention)
  graph export "$root/Figures/vote_share_by_state.png", replace width(2400)
  ```
  Also add a guard before the first export:
  ```stata
  cap mkdir "$root/Figures"
  ```
- **Rationale:** Project convention (CLAUDE.md, stata-code-conventions.md) designates `Figures/` for all outputs. The `output/` directory does not exist in this repository. These paths will produce `file not found` errors. All paths must use `$root`.

---

### Issue 6: Figure missing white background
- **Location:** `0-data_prep.do`, lines 55–58
- **Category:** Figure Output
- **Severity:** High
- **Current:**
  ```stata
  graph bar vote_share, over(party) over(state) ///
      title("Vote Share by State and Party (2020)") ///
      ytitle("Vote Share") ///
      bar(1, color(blue)) bar(2, color(red))
  ```
- **Proposed fix:**
  ```stata
  graph bar vote_share, over(party) over(state) ///
      title("Vote Share by State and Party (2020)") ///
      ytitle("Vote Share") ///
      bar(1, color(blue)) bar(2, color(red)) ///
      graphregion(color(white)) bgcolor(white)
  ```
- **Rationale:** Without explicit white background, `s2color` scheme produces a grey plot background. Project Rule 4 requires white background for all figures in `Figures/`.

---

### Issue 7: Figure export missing `width(2400)` — low resolution output
- **Location:** `0-data_prep.do`, line 59
- **Category:** Figure Output
- **Severity:** High
- **Current:**
  ```stata
  graph export "output/figures/vote_share_by_state.png", replace
  ```
- **Proposed fix:**
  ```stata
  graph export "$root/Figures/vote_share_by_state.png", replace width(2400)
  ```
- **Rationale:** Without `width(2400)`, Stata exports at the default screen size (~800px), which is far below 300 DPI for an 8-inch figure. Project Rule 4 requires 300 DPI.

---

### Issue 8: Global macro named `DIR` instead of `root`
- **Location:** `0-data_prep.do`, line 25
- **Category:** Reproducibility / Polish
- **Severity:** High
- **Current:**
  ```stata
  global DIR = "..."
  cap cd "$DIR"
  ```
- **Proposed fix:**
  ```stata
  global root "C:\Users\AndreaMentasti\Dropbox\example-project"
  ```
  Then replace all `$DIR` references with `$root` throughout the file. Also remove `cap cd` — it's unnecessary once all paths use `$root`, and `cap` silently masks the error if the directory is wrong.
- **Rationale:** Convention in `stata-code-conventions.md` uses `$root`. Consistency matters for maintenance and for future scripts in this project. `cap cd` with a wrong path silently fails, causing confusing downstream errors.

---

### Issue 9: Comments describe WHAT, not WHY
- **Location:** Multiple lines (33, 35, 49, 51, 54)
- **Category:** Comment Quality
- **Severity:** Medium
- **Current:**
  ```stata
  * Summary statistics
  * Export summary stats table
  * Summary by party
  * Simple bar graph of vote share by state and party
  ```
- **Proposed fix:**
  ```stata
  * inspect distribution before any analysis — flag outliers or data quality issues
  * export descriptive table for Section 2 of write-up
  * check N by party before visualization — asymmetric groups affect bar chart interpretation
  * primary output figure: compares how vote share varies by party within each state
  ```
- **Rationale:** Comments should explain the analytical purpose, not restate the code. "WHY this, not WHAT is done."

---

### Issue 10: Tweets and election data are loaded separately but never linked
- **Location:** Structural — overall script design
- **Category:** Domain Correctness
- **Severity:** Medium
- **Current:** The script runs summary stats on tweets (Section 1) then loads a completely separate election dataset (Section 2). The two are never merged or related to each other.
- **Proposed fix (for a future task):** The core research question is *engagement → vote share*. This requires merging the two datasets and running at least a simple regression. As-is, this script is only exploratory — that's fine, but should be documented:
  ```stata
  * NOTE: This script is exploratory only. Regression analysis in 1-analysis.do
  ```
- **Rationale:** A reader expecting "analysis of tweet engagement vs. vote share" would find no such analysis here. The script should either include it or explicitly document that it's out of scope.

---

### Issue 11: `cap cd "$DIR"` silently masks directory errors
- **Location:** `0-data_prep.do`, line 26
- **Category:** Reproducibility
- **Severity:** Medium
- **Current:**
  ```stata
  cap cd "$DIR"
  ```
- **Proposed fix:** Remove the `cd` entirely once all paths use `$root`. If `cd` is kept for another reason:
  ```stata
  cd "$root"   /* remove cap — let it fail loudly if directory is wrong */
  ```
- **Rationale:** `cap` (capture) suppresses the error if the directory doesn't exist, so the script continues silently with the wrong working directory. Errors should fail loudly.

---

### Issue 12: File header missing inputs/outputs list and date
- **Location:** `0-data_prep.do`, lines 1–8
- **Category:** Header & Structure
- **Severity:** Low
- **Current:**
  ```stata
  /*******************************************************************************
  *                        MINI TOY PROJECT                                      *
  *              Simple analysis of sample tweet data                            *
  ********************************************************************************
  Author:   Example
  Preamble: this dofile loads processed data and produces summary statistics
            and a simple figure.
  *******************************************************************************/
  ```
- **Proposed fix:**
  ```stata
  /*******************************************************************************
  * 0-data_prep.do — Exploratory summary statistics and visualization
  * Author:   [Your Name]
  * Inputs:   data/processed/tweets_processed.dta
  *           data/processed/election_data_processed.dta
  * Outputs:  Figures/summary_stats.tex
  *           Figures/vote_share_by_state.png
  *           quality_reports/0-data_prep.log
  * Updated:  2026-03-12
  *******************************************************************************/
  ```
- **Rationale:** Inputs/outputs list makes the script's contract clear at a glance. Required by `stata-code-conventions.md`.

---

### Issue 13: `global DIR = "..."` uses `=` sign (non-standard Stata style)
- **Location:** `0-data_prep.do`, line 25
- **Category:** Polish
- **Severity:** Low
- **Current:**
  ```stata
  global DIR = "C:\Users\..."
  ```
- **Proposed fix:**
  ```stata
  global root "C:\Users\..."
  ```
- **Rationale:** `global macroname = "value"` evaluates the right-hand side as an expression. For string literals, the idiomatic form is `global macroname "value"` (no `=`). While both work for simple strings, the `=` form can cause unexpected behavior with special characters.

---

## Checklist Summary

| Category | Pass | Issues |
|----------|------|--------|
| Header & Structure | ❌ | 2 (missing version, incomplete header) |
| Reproducibility | ❌ | 3 (hardcoded path, no log, `cap cd`) |
| Variable Management | ✅ | 0 (no new variables created) |
| Data & Merges | ✅ | 0 (no merges; flagged structurally in Issue 10) |
| Regression & Econometrics | N/A | 0 (no regressions yet) |
| Table Output | ❌ | 2 (missing options, wrong path) |
| Figure Output | ❌ | 3 (no white bg, no width, wrong path) |
| Comment Quality | ❌ | 1 (WHAT not WHY) |
| Log & Error Checking | ❌ | 1 (no log file) |
| Professional Polish | ❌ | 1 (global macro style) |

---

## Critical Recommendations (Priority Order)

1. **[CRITICAL]** Fix the hardcoded path on line 25 — change user, project name, rename to `$root`, drop `=`
2. **[CRITICAL]** Add `version 17` as first executable line
3. **[HIGH]** Open a log file immediately after `capture log close`
4. **[HIGH]** Fix all output paths to use `$root/Figures/` (both table and figure)
5. **[HIGH]** Add `booktabs label` to `esttab`
6. **[HIGH]** Add `graphregion(color(white)) bgcolor(white) width(2400)` to figure export

Fixing issues 1–6 makes the script runnable and publication-ready.
Issues 7–13 can be addressed in the same pass for completeness.

---

## Positive Findings

1. **Good setup block** — `clear all`, `clear mata`, `set more off`, `macro drop _all`, `capture log close` is a solid, professional setup sequence.
2. **`replace` on all exports** — both `esttab` and `graph export` have `replace`, allowing clean re-runs.
3. **`tabulate party, summarize(vote_share)`** — checking distribution before visualization is good analytical hygiene.
