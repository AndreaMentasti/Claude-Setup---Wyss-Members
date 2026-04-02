# Stata Code Conventions

Standards for all Stata scripts in `code/stata/`. Apply these during code generation
and when running `/data-analysis`.

---

## 1. Reproducibility (Non-Negotiable)

- **Version statement:** Every `.do` file starts with:
  ```stata
  version 17
  ```
  This ensures backward compatibility and documents the Stata version used.

- **Root path macro + config bridge:** Each `.do` file sets a fallback `$root` then loads `config_local.do`:
  ```stata
  global root "C:/Users/yourname/OneDrive/populism_and_narratives"
  do "$root/code/stata/config_local.do"
  ```
  `config_local.do` sets both `$root` and `$data_root`. All repo paths use `$root`; all data paths use `$data_root`.
  *(Note: each collaborator creates their own `config_local.do` from the template.)*

- **Seed:** Set before any stochastic operation (bootstrap, permutation, simulation):
  ```stata
  set seed 42
  ```
  Place immediately after the root macro, before `use` or `import`.

- **Entry point:** Every `.do` file must run cleanly with:
  ```
  stata -b do code/stata/<script>.do
  ```
  No interactive input, no error exit. Check the `.log` file for errors.

---

## 2. Style

- **File header:** Every `.do` file opens with a comment banner:
  ```stata
  /*
   * 0-data_prep.do — Summary statistics and engagement → vote share analysis
   * Inputs:  data/processed/tweets_processed.dta, election_data_processed.dta
   * Outputs: output/tables/table_summary.tex, output/figures/fig_engagement.png
   * Last updated: YYYY-MM-DD
   */
  ```

- **Section banners:** Separate major sections with:
  ```stata
  *---- 1. Load and merge data ----*
  ```

- **Variable labels:** Label every variable immediately after creation:
  ```stata
  gen vote_share = votes / total_votes
  label var vote_share "Party vote share (0-1)"
  ```

- **Value labels:** Apply value labels for categorical variables:
  ```stata
  label define partylab 0 "Democrat" 1 "Republican"
  label values party_num partylab
  ```

- **`tab` before regressions:** Always inspect N and distribution before running a model:
  ```stata
  tab party
  sum retweet_count favorite_count vote_share
  ```

- **Comment style:** Explain WHY, not WHAT.
  Bad: `* generate engagement`. Good: `* proxy for visibility: total interactions per tweet`

---

## 3. Tables (LaTeX Output)

Use `esttab` (part of `estout`) for publication-ready LaTeX tables:

```stata
eststo clear
eststo: reg vote_share engagement_score i.year, robust
eststo: reg vote_share engagement_score i.year i.state_num, robust

esttab using "$root/output/tables/table_main.tex", ///
    booktabs label replace ///
    title("Engagement and Vote Share") ///
    mtitles("OLS" "OLS + State FE") ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    b(3) se(3)
```

- Always use `booktabs` and `label` options.
- Always use `replace` to allow re-running.
- Include `se` (standard errors in parentheses) and significance stars.
- Use `b(3) se(3)` for 3 decimal places.
- Use `indicate` for Yes/No fixed-effects rows and `estadd local` for custom labels:
  ```stata
  estadd local fe_year "Yes"
  estadd local fe_state "Yes"
  esttab ..., scalars("fe_year Year FE" "fe_state State FE") ///
      drop(*.year *.state_num)
  ```
- For full `esttab`/`estout` reference, see the Stata skill: `packages/estout.md`.

---

## 4. Figures (PNG Output)

```stata
twoway (scatter vote_share engagement_score), ///
    xtitle("Engagement Score") ytitle("Vote Share") ///
    title("Engagement vs. Vote Share") ///
    graphregion(color(white)) bgcolor(white)

graph export "$root/output/figures/fig_engagement.png", replace width(2400)
```

- Always set `graphregion(color(white)) bgcolor(white)` for white background.
- `width(2400)` at standard screen resolution ≈ 300 DPI for an 8-inch figure.
- Use `replace` always.
- Save ALL figures to `$root/output/figures/`.

---

## 5. Merging Data

```stata
use "$data_root/processed/tweets/all_tweets_classified.dta", clear
merge m:1 party year using "$data_root/processed/election_data/election_data_processed.dta"
tab _merge
keep if _merge == 3          // keep matched only; log how many dropped
drop _merge
```

Always inspect `_merge` before dropping. Document how many observations are unmatched
and why it's expected (or unexpected).

---

## 6. Known Pitfalls

### Silent-Bug Gotchas (Critical)

- **Missing values sort to +infinity:** Stata's `.` is greater than all numbers.
  `gen high = (x > 100)` includes missings! Always add `if !missing(x)`.

- **`=` vs `==`:** `=` is assignment; `==` is comparison. `gen y = 1 if x = 1` is
  a syntax error or silent bug. Always use `==` in conditions.

- **Local macro syntax:** Locals use `` `name' `` (backtick + single-quote).
  Forgetting the closing `'` is the #1 macro bug:
  ```stata
  local controls "age education"
  regress wage `controls'    // correct
  regress wage `controls     // WRONG — missing closing quote
  ```

- **`by` requires prior sort:** Use `bysort id:` (which sorts automatically)
  instead of `by id:` (which errors if data is unsorted).

- **Factor variables:** Omitting `i.` treats categoricals as continuous.
  `regress y race` treats race=3 as 3x the effect of race=1. Use `regress y i.race`.

- **`generate` vs `replace`:** `gen x = 2` errors if `x` already exists.
  Use `replace x = 2` for existing variables.

- **String comparison is case-sensitive:** Use `lower(gender) == "male"` not
  `gender == "male"` to avoid missing "Male", "MALE", etc.

- **`test` vs `testparm` for factor variables:** `test` cannot handle negative
  factor levels or wildcards. Use `testparm` instead:
  ```stata
  * WRONG — test cannot handle negative levels
  test 1.treated#-5.time

  * RIGHT — testparm handles wildcards and level lists
  testparm 1.treated#(-5 -4 -3 -2).time
  ```

### Project-Specific Pitfalls

- **`encode` auto-ordering:** `encode party, gen(party_num)` assigns numeric codes
  alphabetically ("Democrat"=1, "Republican"=2). This is NOT random but IS arbitrary.
  Always verify ordering before interpreting dummy coefficients.

- **`destring` vs. `encode`:** Use `destring` for variables that are already numeric
  stored as strings. Use `encode` for true string categoricals. Confusing the two
  causes silent data errors.

- **`sort` stability:** Stata's `sort` is not stable by default. Use `sort var1 var2`
  with enough keys to uniquely identify rows, or use `gsort`.

- **`robust` vs. `cluster`:** If multiple tweets map to the same candidate/state,
  standard errors should be clustered: `vce(cluster state)`. Plain `robust` is
  insufficient when errors are correlated within groups. Need ~50+ clusters for
  reliable inference.

- **Log file:** Always check `<script>.log` after batch runs. A non-zero exit code
  means Stata hit an error; the log shows where.

- **Stored results overwrite:** A new estimation command overwrites previous `e()`
  results. Always `estimates store model1` before running the next model.

- **`preserve`/`restore` pattern:** When collapsing data for group stats and merging
  back, use the tempfile pattern:
  ```stata
  tempfile stats
  preserve
  collapse (mean) avg_x=x, by(group)
  save `stats'
  restore
  merge m:1 group using `stats'
  ```
  For simple group means, `bysort group: egen avg_x = mean(x)` avoids the round-trip.

---

## 7. Verification Checklist

After writing or modifying a `.do` file:

- [ ] Script runs cleanly: `stata -b do code/stata/<script>.do` exits 0
- [ ] `.log` file shows no errors (search for `r(`)
- [ ] All output files created: `output/tables/*.tex`, `output/figures/*.png`
- [ ] Variable labels applied to all new variables
- [ ] `$root` macro set and all paths use it
- [ ] `set seed 42` present if any stochastic operations
