---
name: stata
description: >
  Comprehensive Stata skill for writing correct .do files, running them in batch
  mode, consulting bundled PDF documentation, and looking up syntax, econometrics,
  causal inference, graphics, Mata programming, and 20 community packages
  (reghdfe, estout, did, rdrobust, etc.). Covers syntax, options, gotchas, and
  idiomatic patterns. Use this skill whenever writing, editing, running, or
  debugging Stata code.
allowed-tools: ["Read", "Bash", "Write", "Edit", "Grep", "Glob"]
---

# Stata Skill

Use this skill whenever writing, editing, running, or debugging Stata `.do` files,
or when you need to look up Stata syntax, commands, or options.

You have access to comprehensive Stata reference files. **Do not load all files.**
Read only the 1-3 files relevant to the user's current task using the routing table
in Section 7.

---

## 1. What is Stata

Stata is a statistical software package for data management, analysis, and graphics.
It is widely used in economics, political science, epidemiology, and other social sciences.

Key concepts:
- **`.do` files**: Scripts (plain text) containing Stata commands, executed sequentially.
- **`.dta` files**: Stata's binary data format.
- **`.log` files**: Text output captured during a Stata session or batch run.
- **`ado` files**: Stata programs (user-written or official) that extend functionality.
- **Macros**: `local` (temporary) and `global` (persistent within session) named values.
- **Factor variables**: `i.varname` notation for categorical regressors.
- **Postestimation**: Commands run after a model fit (e.g., `predict`, `margins`, `estat`).

---

## 2. Running Stata in This Environment

**Finding the installation:** Stata is installed in `C:\Program Files\` on Windows.
To auto-detect the path:
```bash
STATA_DIR=$(ls -d "/c/Program Files"/Stata* "/c/Program Files"/StataNow* 2>/dev/null | sort -V | tail -1)
echo "$STATA_DIR"
```

**From bash (Claude Code terminal):**
```bash
stata -b do path/to/script.do        # batch mode, creates .log file
stata path/to/script.do              # interactive window
```

**IMPORTANT:** ALWAYS use the `stata` wrapper command (at `~/bin/stata`), NEVER call
`StataSE-64.exe` directly. The wrapper auto-moves batch-mode logs from the current
directory to `quality_reports/stata_logs/`. Calling the exe directly leaves stray
`.log` files in the project root.

**From PowerShell (user terminal):**
```powershell
stata -b do path\to\script.do
```

The `stata` alias must point to `StataSE-64.exe` (or `StataMP-64.exe` depending on
edition). See `SETUP.md` for how to configure this.

**Checking for errors after batch run:**
```bash
grep "^r(" script.log    # Stata error codes start with r(
```
If the log contains `r(` lines, the script hit an error at that point.

---

## 3. Writing `.do` Files — Project Conventions

### File structure
```stata
version 17
clear all
set more off

* --- 0. Paths ---
do config_local.do          // sets $root and $data_root

* --- 1. Load data ---
use "$data_root/processed/tweets/all_tweets_classified.dta", clear

* --- 2. Analysis ---
reg vote_share engagement_score, robust

* --- 3. Output ---
esttab using "$root/output/tables/table1.tex", booktabs label replace
graph export "$root/output/figures/fig1.png", replace width(2400)
```

### Key patterns
- `version 17` at top for reproducibility
- All paths via `$root` (repo) and `$data_root` (Dropbox) global macros
- `clear all` / `set more off` at the start
- `replace` on all output commands (allows re-running)
- `width(2400)` for ~300 DPI figures at 8 inches
- `graphregion(color(white)) bgcolor(white)` for white backgrounds
- Line continuation with `///`

---

## 4. Critical Gotchas

These are Stata-specific pitfalls that lead to silent bugs. Internalize these before
writing any code.

### Missing Values Sort to +Infinity
Stata's `.` (and `.a`-`.z`) are **greater than all numbers**.
```stata
* WRONG — includes observations where income is missing!
gen high_income = (income > 50000)

* RIGHT
gen high_income = (income > 50000) if !missing(income)
```

### `=` vs `==`
`=` is assignment; `==` is comparison. Mixing them up is a syntax error or silent bug.
```stata
* WRONG — syntax error
gen employed = 1 if status = 1

* RIGHT
gen employed = 1 if status == 1
```

### Local Macro Syntax
Locals use `` `name' `` (backtick + single-quote). Globals use `$name` or `${name}`.
Forgetting the closing quote is the #1 macro bug.
```stata
local controls "age education income"
regress wage `controls'        // correct
regress wage `controls         // WRONG — missing closing quote
```

### `by` Requires Prior Sort (Use `bysort`)
```stata
* WRONG — error if data not sorted by id
by id: gen first = (_n == 1)

* RIGHT — bysort sorts automatically
bysort id: gen first = (_n == 1)
```

### Factor Variable Notation (`i.` and `c.`)
Use `i.` for categorical, `c.` for continuous. Omitting `i.` treats categories as continuous.
```stata
* WRONG — treats race as continuous
regress wage race education

* RIGHT — creates dummies automatically
regress wage i.race education
```

### `generate` vs `replace`
`generate` creates new variables; `replace` modifies existing ones.
```stata
gen x = 1
gen x = 2          // ERROR: x already defined
replace x = 2      // correct
```

### String Comparison Is Case-Sensitive
```stata
keep if lower(gender) == "male"   // safer than gender == "male"
```

### `merge` Always Check `_merge`
```stata
merge 1:1 id using other.dta
tab _merge                      // ALWAYS tab before dropping
drop _merge
```

### `encode` Auto-Ordering
`encode party, gen(party_num)` assigns codes alphabetically
("Democrat"=1, "Republican"=2). This is NOT random but IS arbitrary.
Always verify ordering before interpreting dummy coefficients.

### `destring` vs. `encode`
Use `destring` for variables already numeric stored as strings.
Use `encode` for true string categoricals. Confusing the two causes silent data errors.

### `sort` Stability
Stata's `sort` is not stable by default. Use enough keys to uniquely identify rows.

### `robust` vs. `cluster`
If multiple tweets map to the same candidate/state, standard errors should be
clustered: `vce(cluster state)`. Plain `robust` is insufficient when errors are
correlated within groups.

### `preserve` / `restore` + `tempfile` for Collapse-Merge-Back
```stata
tempfile stats
preserve
collapse (mean) avg_x=x, by(group)
save `stats'
restore
merge m:1 group using `stats'
```
For simple group means, `bysort group: egen avg_x = mean(x)` avoids the round-trip.

### Stored Results: `r()` vs `e()` vs `s()`
- `r()` — r-class commands (summarize, tabulate, etc.)
- `e()` — e-class commands (estimation: regress, logit, etc.)
- `s()` — s-class commands (parsing)

A new estimation command **overwrites** previous `e()` results. Store them first:
```stata
regress y x1 x2
estimates store model1
```

---

## 5. Stata PDF Documentation

### Location
Stata bundles its full documentation as PDFs inside the installation directory:
```
<STATA_INSTALL_DIR>/docs/
```

To find the docs directory automatically:
```bash
STATA_DOCS=$(ls -d "/c/Program Files"/Stata*/docs "/c/Program Files"/StataNow*/docs 2>/dev/null | sort -V | tail -1)
echo "$STATA_DOCS"
```

### Complete manual index (37 PDFs, ~17,000 total pages)

| File | Manual | Pages | Key contents |
|------|--------|-------|--------------|
| `r.pdf` | **Base Reference** | 3,502 | regress, logit, probit, test, predict, margins — the most-used manual |
| `u.pdf` | **User's Guide** | 403 | Stata basics, syntax, data types, programming intro |
| `d.pdf` | **Data Management** | 1,000 | import, merge, reshape, append, encode, destring |
| `ts.pdf` | **Time Series** | 1,026 | arima, var, vec, irf, tsset |
| `xt.pdf` | **Panel Data** | 699 | xtreg, xtlogit, xtpoisson, xtset |
| `me.pdf` | **Mixed Effects** | 572 | mixed, melogit, mepoisson |
| `st.pdf` | **Survival Analysis** | 645 | stset, stcox, streg, sts |
| `mv.pdf` | **Multivariate** | 750 | factor, pca, cluster, manova |
| `sem.pdf` | **SEM** | 680 | sem, gsem, path diagrams |
| `g.pdf` | **Graphics** | 799 | twoway, graph bar, scheme, options |
| `p.pdf` | **Programming** | 667 | program, macro, mata interface |
| `m.pdf` | **Mata** | 1,214 | Stata's matrix programming language |
| `bayes.pdf` | **Bayesian** | 911 | bayesmh, bayesian estimation |
| `causal.pdf` | **Causal Inference** | 746 | teffects, didregress, stteffects |
| `lasso.pdf` | **Lasso** | 394 | lasso, elasticnet, cross-validation |
| `mi.pdf` | **Multiple Imputation** | 400 | mi impute, mi estimate |
| `svy.pdf` | **Survey** | 236 | svyset, svy: prefix |
| `tables.pdf` | **Tables** | 361 | collect, table, dtable, etable |
| `pss.pdf` | **Power/Sample Size** | 869 | power, sample size calculations |
| `meta.pdf` | **Meta-Analysis** | 439 | meta set, meta forestplot |
| `fn.pdf` | **Functions** | 193 | Built-in functions reference |
| `i.pdf` | **Glossary/Index** | 328 | Combined subject index |
| `stoc.pdf` | **Subject TOC** | 59 | Combined table of contents across all manuals |

**Start with `stoc.pdf`** (59 pages) to find which manual covers a topic.

---

## 6. Reading Documentation Efficiently (Token-Saving Strategies)

**Problem:** 17,000 pages of PDFs. Reading even one manual wastes tokens.
**Solution:** Use targeted extraction — never read a full manual.

**Prerequisites:** `pdftotext` (bundled with poppler/mingw) and `pip install pdfplumber`.
See `SETUP.md` for installation.

### Tool 1: `pdftotext` (fast, plain text, best for prose)
```bash
STATA_DOCS=$(ls -d "/c/Program Files"/Stata*/docs "/c/Program Files"/StataNow*/docs 2>/dev/null | sort -V | tail -1)

# Extract specific pages (e.g., pages 1200-1220 for regress)
pdftotext -f 1200 -l 1220 "$STATA_DOCS/r.pdf" -

# Search the subject TOC for a command
pdftotext "$STATA_DOCS/stoc.pdf" - | grep -i "regress"
```

### Tool 2: `pdfplumber` (Python, best for tables and structured content)
```python
import pdfplumber, glob, os

def find_stata_docs():
    """Auto-detect Stata docs directory."""
    for pattern in [r"C:\Program Files\StataNow*\docs",
                    r"C:\Program Files\Stata*\docs"]:
        matches = glob.glob(pattern)
        if matches:
            return sorted(matches)[-1]
    return None

def stata_doc_lookup(manual: str, start_page: int, end_page: int) -> str:
    """Extract text from a Stata manual. Pages are 0-indexed."""
    docs = find_stata_docs()
    path = os.path.join(docs, manual)
    with pdfplumber.open(path) as pdf:
        text = []
        for i in range(start_page, min(end_page, len(pdf.pages))):
            page_text = pdf.pages[i].extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)

# Example: read TOC of r.pdf to find page numbers
print(stata_doc_lookup("r.pdf", 2, 8))
```

### Recommended lookup workflow
1. **First check the reference files** (Section 7) — they cover most common tasks
2. **If not covered**, start with `stoc.pdf` — search the subject TOC to identify which manual
3. **Read the manual's own TOC** (pages 2-8) to find the exact page range
4. **Extract only those pages** with `pdftotext -f START -l END manual.pdf -`
5. **Never extract more than 20 pages at once**

### Token cost estimates
- 1 PDF page ~ 500-800 tokens
- Full `r.pdf` ~ 2.1M tokens (NEVER do this)
- `stoc.pdf` (59 pages) ~ 35K tokens (acceptable for initial lookup)
- Targeted 10-page extract ~ 6K tokens (ideal)

---

## 7. Reference File Routing Table

Read only the 1-3 files relevant to the current task. Paths are relative to this
SKILL.md file.

### Data Operations
| File | Topics & Key Commands |
|------|----------------------|
| `references/basics-getting-started.md` | `use`, `save`, `describe`, `browse`, `sysuse`, basic workflow |
| `references/data-import-export.md` | `import delimited`, `import excel`, ODBC, `export`, web data |
| `references/data-management.md` | `generate`, `replace`, `merge`, `append`, `reshape`, `collapse`, `recode`, `egen`, `encode`/`decode` |
| `references/variables-operators.md` | Variable types, `byte`/`int`/`long`/`float`/`double`, operators, missing values, `if`/`in` qualifiers |
| `references/string-functions.md` | `substr()`, `regexm()`, `strtrim()`, `split`, `ustrlen()`, regex, Unicode |
| `references/date-time-functions.md` | `date()`, `clock()`, `%td`/`%tc` formats, `mdy()`, `dofm()`, business calendars |
| `references/mathematical-functions.md` | `round()`, `log()`, `exp()`, `abs()`, `mod()`, `cond()`, distributions, random numbers |

### Statistics & Econometrics
| File | Topics & Key Commands |
|------|----------------------|
| `references/descriptive-statistics.md` | `summarize`, `tabulate`, `correlate`, `tabstat`, `codebook`, weighted stats |
| `references/linear-regression.md` | `regress`, `vce(robust)`, `vce(cluster)`, `test`, `lincom`, `margins`, `predict`, `ivregress` |
| `references/panel-data.md` | `xtset`, `xtreg fe`/`re`, Hausman test, `xtabond`, dynamic panels |
| `references/time-series.md` | `tsset`, ARIMA, VAR, `dfuller`, `pperron`, `irf`, forecasting |
| `references/limited-dependent-variables.md` | `logit`, `probit`, `tobit`, `poisson`, `nbreg`, `mlogit`, `ologit`, `margins` for nonlinear |
| `references/bootstrap-simulation.md` | `bootstrap`, `simulate`, `permute`, Monte Carlo |
| `references/survey-data-analysis.md` | `svyset`, `svy:`, `subpop()`, complex survey design, replicate weights |
| `references/missing-data-handling.md` | `mi impute`, `mi estimate`, FIML, `misstable`, diagnostics |
| `references/maximum-likelihood.md` | `ml model`, custom likelihood functions, `ml init`, gradient-based optimization |
| `references/gmm-estimation.md` | `gmm`, moment conditions, `estat overid`, J-test |

### Causal Inference
| File | Topics & Key Commands |
|------|----------------------|
| `references/treatment-effects.md` | `teffects ra/ipw/ipwra/aipw`, `stteffects`, ATE/ATT/ATET |
| `references/difference-in-differences.md` | DiD, parallel trends, event studies, staggered adoption |
| `references/regression-discontinuity.md` | Sharp/fuzzy RD, bandwidth selection, `rdplot` |
| `references/matching-methods.md` | PSM, nearest neighbor, kernel matching, `teffects nnmatch` |
| `references/sample-selection.md` | `heckman`, `heckprobit`, treatment models, exclusion restrictions |

### Advanced Methods
| File | Topics & Key Commands |
|------|----------------------|
| `references/survival-analysis.md` | `stset`, `stcox`, `streg`, Kaplan-Meier, parametric models |
| `references/sem-factor-analysis.md` | `sem`, `gsem`, CFA, path analysis, `alpha`, reliability |
| `references/nonparametric-methods.md` | `kdensity`, rank tests, `qreg`, `npregress` |
| `references/spatial-analysis.md` | `spmatrix`, `spregress`, spatial weights, Moran's I |
| `references/machine-learning.md` | `lasso`, `elasticnet`, `cvlasso`, cross-validation |

### Graphics
| File | Topics & Key Commands |
|------|----------------------|
| `references/graphics.md` | `twoway`, `scatter`, `line`, `bar`, `histogram`, `graph combine`, `graph export`, schemes |

### Programming
| File | Topics & Key Commands |
|------|----------------------|
| `references/programming-basics.md` | `local`, `global`, `foreach`, `forvalues`, `program define`, `syntax`, `return` |
| `references/advanced-programming.md` | `syntax`, `mata`, classes, `_prefix`, dialog boxes, `tempfile`/`tempvar` |
| `references/mata-introduction.md` | Mata basics, when to use Mata vs ado, data types |
| `references/mata-programming.md` | Mata functions, flow control, structures, pointers |
| `references/mata-matrix-operations.md` | Matrix creation, decompositions, solvers, `st_matrix()` |
| `references/mata-data-access.md` | `st_data()`, `st_view()`, `st_store()`, performance tips |

### Output & Workflow
| File | Topics & Key Commands |
|------|----------------------|
| `references/tables-reporting.md` | `putexcel`, `putdocx`, `putpdf`, LaTeX integration, `collect` |
| `references/workflow-best-practices.md` | Project structure, master do-files, version control, debugging |
| `references/external-tools-integration.md` | Python via `python:`, R via `rsource`, shell commands, Git |

### Community Packages
| File | What It Does |
|------|-------------|
| `packages/reghdfe.md` | High-dimensional fixed effects OLS (absorbs multiple FE sets efficiently) |
| `packages/estout.md` | `esttab`/`estout`: publication-quality regression tables |
| `packages/outreg2.md` | Alternative regression table exporter (Word, Excel, TeX) |
| `packages/asdoc.md` | One-command Word document creation for any Stata output |
| `packages/tabout.md` | Cross-tabulations and summary tables to file |
| `packages/coefplot.md` | Coefficient plots from stored estimates |
| `packages/graph-schemes.md` | `grstyle`, `schemepack`, `plotplain` — better graph themes |
| `packages/did.md` | Modern DiD: `csdid`, `did_multiplegt`, `did_imputation` (Callaway-Sant'Anna, etc.) |
| `packages/event-study.md` | `eventstudyinteract`, `eventdd` — event study estimators |
| `packages/rdrobust.md` | Robust RD estimation with optimal bandwidth |
| `packages/psmatch2.md` | Propensity score matching (nearest neighbor, kernel, radius) |
| `packages/synth.md` | Synthetic control method (`synth`, `synth_runner`) |
| `packages/ivreg2.md` | Enhanced IV/2SLS: `ivreg2`, `xtivreg2` with additional diagnostics |
| `packages/xtabond2.md` | Dynamic panel GMM (Arellano-Bond/Blundell-Bond) |
| `packages/binsreg.md` | Binned scatter plots with CI (`binsreg`, `binstest`) |
| `packages/nprobust.md` | Nonparametric kernel estimation and inference |
| `packages/diagnostics.md` | `bacondecomp`, `xttest3`, collinearity, heteroskedasticity tests |
| `packages/winsor.md` | Winsorizing and trimming: `winsor2`, `winsor` |
| `packages/data-manipulation.md` | `gtools` (fast collapse/egen), `rangestat`, `egenmore` |
| `packages/package-management.md` | `ssc install`, `net install`, `ado update`, finding packages |

---

## 8. Quick Reference: Common Tasks

| Task | First check | Then PDF |
|------|-------------|----------|
| Regression syntax | `references/linear-regression.md` | `r.pdf` TOC for "regress" |
| Merge datasets | `references/data-management.md` | `d.pdf` for "merge" |
| Panel data models | `references/panel-data.md` | `xt.pdf` for "xtreg" |
| Export LaTeX tables | `packages/estout.md` | `tables.pdf` |
| Graph options | `references/graphics.md` | `g.pdf` TOC |
| String functions | `references/string-functions.md` | `fn.pdf` |
| Date/time handling | `references/date-time-functions.md` | `u.pdf` dates chapter |
| Causal inference / DiD | `references/difference-in-differences.md` | `causal.pdf` TOC |
| Event studies | `packages/event-study.md` or `packages/did.md` | `causal.pdf` |
| Survey weights | `references/survey-data-analysis.md` | `svy.pdf` TOC |
| Coefficient plots | `packages/coefplot.md` | — |
| High-dim fixed effects | `packages/reghdfe.md` | — |

---

## 9. Common Patterns (Quick Copy-Paste)

### Regression Table Workflow
```stata
eststo clear
eststo: regress y x1 x2, vce(robust)
eststo: regress y x1 x2 x3, vce(robust)
eststo: regress y x1 x2 x3 x4, vce(cluster id)

esttab using "$root/output/tables/table_main.tex", replace ///
    booktabs label b(3) se(3) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("(1)" "(2)" "(3)") ///
    stats(N r2 r2_a, labels("Observations" "R-squared" "Adj. R-squared"))
```

### Panel Data Setup
```stata
xtset panelid timevar
xtdescribe
xtsum outcome

xtreg y x1 x2, fe vce(cluster panelid)
* Or with reghdfe (preferred for multiple FE)
reghdfe y x1 x2, absorb(panelid timevar) vce(cluster panelid)
```

### Difference-in-Differences
```stata
* Classic 2x2 DiD
gen post = (year >= treatment_year)
gen treat_post = treated * post
regress y treated post treat_post, vce(cluster id)

* Event study (must interact with treatment group)
reghdfe y ib(-1).rel_time#1.treated, absorb(id year) vce(cluster id)
testparm *.rel_time#1.treated

* Modern staggered DiD (Callaway & Sant'Anna)
csdid y x1 x2, ivar(id) time(year) gvar(first_treat) agg(event)
csdid_plot
```

### Graph Export (Project Standard)
```stata
twoway (scatter y x, mcolor(navy%50) msize(small)) ///
       (lfit y x, lcolor(cranberry) lwidth(medthick)), ///
    xtitle("X Label") ytitle("Y Label") ///
    graphregion(color(white)) bgcolor(white) ///
    legend(off)
graph export "$root/output/figures/fig1.png", replace width(2400)
```

---

## Attribution

Reference files (`references/` and `packages/`) sourced from
[dylantmoore/stata-skill](https://github.com/dylantmoore/stata-skill) (MIT License),
adapted for this project's conventions.
