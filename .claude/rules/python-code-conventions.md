# Python Code Conventions

Standards for all Python scripts in `code/py/`. Modelled on `r-code-conventions.md`.
Apply these during code generation and when running `/data-analysis`.

---

## 1. Reproducibility (Non-Negotiable)

- **Paths:** Always import `config as cfg` and use `cfg.DATA_RAW`, `cfg.DATA_PROCESSED`,
  `cfg.FIGURES`, etc. Never hardcode absolute paths. Never use `os.getcwd()` as a base.
- **Seed:** Add `random.seed(42)` and `np.random.seed(42)` at the top of the script
  if ANY stochastic operations are used. If no randomness: omit.
- **Dependencies:** Keep `requirements.txt` current. Pin major versions (e.g., `pandas>=2.0`).
- **Entry point:** Every script must be runnable as `python code/py/<script>.py`
  with no interactive input and no error exit code.

---

## 2. Style (PEP 8 + Project Conventions)

- **Line length:** 100 characters max (exception: long string literals, URLs).
- **Strings:** Use f-strings for interpolation. Avoid `%` formatting or `.format()`.
- **No bare `print()` for warnings:** Use `logging.warning(...)` for non-output messages.
  `print()` is acceptable only for progress indicators in long scripts.
- **Imports:** Standard library → third-party → local (`config`). One blank line between groups.
- **Naming:** `snake_case` for variables and functions. `UPPER_SNAKE` for module-level constants.

---

## 3. Pandas Idioms

- **No chained assignment:** Never `df['col1']['col2'] = val`. Use `.loc[row, col]`.
- **Use `.copy()`:** After any slice or filter that you will modify:
  `df_clean = df[df['votes'] > 0].copy()`
- **No `inplace=True`:** Always reassign: `df = df.drop(columns=['col'])` not `df.drop(..., inplace=True)`.
- **Explicit dtypes:** Set dtypes after loading. Don't rely on pandas inference for key columns.
- **Merge checks:** Always verify merge outcomes:
  ```python
  merged = df_a.merge(df_b, on='key', how='left', validate='many_to_one')
  assert merged.shape[0] == df_a.shape[0], "Merge changed row count unexpectedly"
  ```

---

## 4. Outputs

- **Figures:**
  ```python
  fig, ax = plt.subplots(figsize=(8, 6))
  # ... plotting ...
  fig.savefig(cfg.FIGURES / "figure_name.png", dpi=300, bbox_inches='tight')
  plt.close(fig)
  ```
  Always close figures after saving to avoid memory leaks.

- **LaTeX tables:** Use `df.to_latex(...)` or `tabulate` with `tablefmt='latex_booktabs'`.
  Save to `cfg.FIGURES / "table_name.tex"`.

- **Processed data:** Save as both `.csv` (human-readable) and `.dta` (Stata-readable)
  using `df.to_stata(cfg.DATA_PROCESSED / "file.dta", write_index=False)`.

---

## 5. Documentation

- **Module docstring:** Every script starts with a docstring:
  ```python
  """
  01_data_prep.py — Data cleaning and feature engineering.

  Inputs:  data/rawdata/sample_tweets.csv, data/rawdata/election_results.csv
  Outputs: data/processed/tweets_processed.{csv,dta},
           data/processed/election_data_processed.{csv,dta}
  """
  ```
- **Function docstrings:** Every function gets a one-line docstring minimum.
- **Inline comments:** Explain WHY, not WHAT. Bad: `# add column`. Good: `# engagement proxy: sum of shares and likes`.
- **Section banners:** Use `# --- Section Name ---` to break long scripts into logical sections.

---

## 6. Verification Checklist

After writing or modifying a Python script:

- [ ] Script runs cleanly: `python code/py/<script>.py` exits 0
- [ ] All output files created in expected locations
- [ ] No hardcoded paths (grep for `/Users`, `C:\\`, `../` outside config)
- [ ] No unhandled exceptions (wrap I/O in try/except where appropriate)
- [ ] Figures saved at 300 DPI to `cfg.FIGURES`

---

## Known Pitfalls

- **`pandas.read_csv` encoding:** Specify `encoding='utf-8'` explicitly; Windows may
  default to cp1252 and silently misread special characters.
- **`.dta` version:** Stata 17 requires `version=117` in `to_stata()`. Default is fine
  for Stata 14+.
- **Date parsing:** Always pass `parse_dates=['date']` explicitly; don't rely on auto-detection.
- **Integer overflow:** `retweet_count` can exceed int32 for popular accounts; ensure int64.
