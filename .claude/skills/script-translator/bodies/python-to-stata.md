# Python → Stata Mapping

## Stata Boilerplate

```stata
version 17
clear all
set more off
macro drop _all
capture log close

global root "..."
log using "$root/quality_reports/stata_logs/[name].log", replace
do "$root/code/stata/config_local.do"
```

## Construct Mapping Table

| Python (pandas) | Stata |
|----------------|-------|
| `pd.read_stata("f.dta")` | `use "f.dta", clear` |
| `pd.read_csv("f.csv")` | `import delimited "f.csv", clear` |
| `df.to_stata("f.dta")` | `save "f.dta", replace` |
| `df.to_csv("f.csv")` | `export delimited "f.csv", replace` |
| `df[df["x"] > 0].copy()` | `keep if x > 0` |
| `df.dropna(subset=["x"])` | `drop if missing(x)` |
| `df[["var1", "var2"]]` | `keep var1 var2` |
| `df.drop(columns=["var1"])` | `drop var1` |
| `df["y"] = df["x"] + df["z"]` | `gen y = x + z` |
| `df.loc[df["x"] < 0, "y"] = 0` | `replace y = 0 if x < 0` |
| `df.rename(columns={"old": "new"})` | `rename old new` |
| `df.sort_values(["v1", "v2"])` | `sort v1 v2` |
| `df.drop_duplicates()` | `duplicates drop` |
| `df.groupby("x")["y"].mean()` | `collapse (mean) y, by(x)` |
| `df.groupby("x").agg({"y":"sum","z":"mean"})` | `collapse (sum) y (mean) z, by(x)` |
| `df.groupby("x")["y"].transform("mean")` | `egen y_mean = mean(y), by(x)` |
| `df.groupby("x")["y"].transform("std")` | `egen y_sd = sd(y), by(x)` |
| `df.groupby("x")["y"].transform("count")` | `egen y_count = count(y), by(x)` |
| `~df.duplicated(subset=["x"])` | `egen tag = tag(x)` |
| `df.merge(df2, on="key", how="left")` | `merge m:1 key using "f.dta"` |
| `pd.concat([df, df2])` | `append using "f.dta"` |
| `df.pivot(index="id", columns="t", values="y")` | `reshape wide y, i(id) j(t)` |
| `pd.melt(df, id_vars=["id"])` | `reshape long y, i(id) j(t)` |
| `df["x"].astype("category").cat.codes` | `encode x, gen(x_num)` |
| `pd.to_numeric(df["x"], errors="coerce")` | `destring x, replace force` |
| `df["x"].astype(str)` | `tostring x, replace` |
| `df["x"].describe()` | `summarize x` |
| `df["x"].value_counts()` | `tabulate x` |
| `pd.crosstab(df["x"], df["y"])` | `tab x y` |
| `(df["x"] > 0).sum()` | `count if x > 0` |
| `assert len(df) > 0` | `assert _N > 0` |
| `df["x"].isna()` | `missing(x)` |
| `df["x"].notna()` | `!missing(x)` |
| `df["x"].isin([1, 2, 3])` | `inlist(x, 1, 2, 3)` |
| `df["s"].str[:3]` | `gen s3 = substr(s, 1, 3)` |
| `df["s"].str.len()` | `gen slen = strlen(s)` |
| `df["s"].str.lower()` | `gen s_low = lower(s)` |
| `df["s"].str.contains("pat")` | `gen has_pat = regexm(s, "pat")` |
| `pd.to_datetime(df["s"])` | `gen d = date(s, "YMD")` |
| `df["d"].dt.year` | `gen yr = year(d)` |

## Regression Mapping

| Python | Stata |
|--------|-------|
| `smf.ols("y ~ x1 + x2", df).fit(cov_type="HC1")` | `reg y x1 x2, robust` |
| `smf.ols(...).fit(cov_type="cluster", cov_kwds={"groups": df["g"]})` | `reg y x1 x2, vce(cluster g)` |
| `smf.ols("y ~ x1 + C(cat)", df).fit()` | `reg y x1 i.cat` |
| `PanelOLS(y, x, entity_effects=True).fit()` | `xtreg y x1, fe` |
| `smf.logit("y ~ x1 + x2", df).fit()` | `logit y x1 x2` |
| `smf.probit("y ~ x1 + x2", df).fit()` | `probit y x1 x2` |
| `results.predict()` | `predict yhat` |
| `results.f_test("x1 = x2")` | `test x1 = x2` |

## Figure Mapping

### Plot Types
| Python (matplotlib) | Stata |
|---------------------|-------|
| `ax.scatter(x, y)` | `twoway scatter y x` |
| `ax.plot(x, y)` | `twoway line y x` |
| `np.polyfit` + `ax.plot` (linear fit) | `twoway lfit y x` |
| `ax.bar(x, height)` | `twoway bar y x` or `graph bar y, over(x)` |
| `ax.hist(x)` | `histogram x` |

### Labels and Titles
| Python | Stata |
|--------|-------|
| `ax.set_title("T")` | `title("T")` |
| `ax.set_xlabel("X")` | `xtitle("X")` |
| `ax.set_ylabel("Y")` | `ytitle("Y")` |
| `ax.set_xlim(a, b)` | `xscale(range(a b))` |
| `ax.set_ylim(a, b)` | `yscale(range(a b))` |
| `ax.set_xticks([...])` + `set_xticklabels([...])` | `xlabel(val1 "lab1" val2 "lab2", ...)` |

### Colors, Transparency, Markers
| Python | Stata |
|--------|-------|
| `color="blue"` | `mcolor(blue)` or `color(blue)` |
| `alpha=0.7` | `%70` suffix: `mcolor(blue%70)` |
| `edgecolors="white"` | `mlcolor(white)` |
| `linewidth=0.5` (marker edge) | `mlwidth(vthin)` |
| `marker="o"` | `msymbol(circle)` |
| `s=80` (marker size) | `msize(large)` |
| `linewidth=2` (line) | `lwidth(medium)` or `lwidth(medthick)` |
| `color="red"` (line) | `lcolor(red)` |
| `linestyle="--"` | `lpattern(dash)` |

### Grid
| Python | Stata |
|--------|-------|
| `ax.grid(True, alpha=0.3)` | `ylabel(, grid glcolor(gs14))` or `xscale(grid) yscale(grid)` |
| `ax.grid(False)` / no grid call | Do NOT add any grid options |

### Legend
| Python | Stata |
|--------|-------|
| `ax.legend()` (default: upper right) | `legend(order(1 "A" 2 "B"))` |
| `ax.legend(loc="lower right")` | `legend(... position(5) ring(0))` |
| `ax.legend(loc="upper left")` | `legend(... position(11) ring(0))` |
| `ax.legend(loc="upper right")` | `legend(... position(1) ring(0))` |
| No legend / `legend=False` | `legend(off)` |

### Point Labels / Annotations
| Python | Stata |
|--------|-------|
| `ax.annotate(text, (x,y), fontsize=7, ha="left", xytext=(4,2), textcoords="offset points")` | `mlabel(var) mlabsize(tiny) mlabposition(3) mlabgap(1)` |
| No annotations | Do NOT add `mlabel` |

### Background and Output
| Python | Stata |
|--------|-------|
| `fig.patch.set_facecolor("white")` | `graphregion(color(white))` |
| `ax.set_facecolor("white")` | `bgcolor(white)` |
| `figsize=(8, 6)` | `xsize(8) ysize(6)` |
| `fig.savefig("f.png", dpi=300, bbox_inches="tight")` | `graph export "f.png", replace width(2400)` |
| `plt.close(fig)` | `graph drop _all` |

### Stata legend position reference
```
11=upper-left   12=upper-center   1=upper-right
 9=center-left  10=center         2=center-right
 7=lower-left    8=lower-center   5=lower-right
ring(0) = inside plot area
```

## Known Traps

1. **Data in memory:** Stata holds one dataset at a time. If the Python script works with multiple DataFrames simultaneously, you must `preserve`/`restore` or `tempfile` in Stata.
2. **Chained operations:** Python `df.groupby().agg().merge()` chains must be broken into separate Stata commands (collapse, then merge).
3. **`collapse` destroys:** Python `groupby` returns a new object. Stata `collapse` replaces the data in memory. Use `preserve`/`restore` or `tempfile` if the original data is needed later.
4. **0-based indexing:** Python `df.iloc[0]` = first row. Stata `_n == 1` = first row. Adjust index-based operations.
5. **NaN propagation:** Python NaN propagates in arithmetic (NaN + 5 = NaN). Stata missing also propagates (. + 5 = .). Behavior matches.
6. **Missing in comparisons:** Python `NaN > 0` = False. Stata `. > 0` = True. If the Python code relies on NaN being excluded from boolean filters, the Stata equivalent already excludes missing from `keep if` but NOT from `gen y = (x > 0)`.
7. **matplotlib → Stata graphics:** Stata graphics options are positional within `twoway`. Place `title`, `xtitle`, `legend` after the comma. Multiple plot overlays use parentheses: `twoway (scatter ...) (lfit ...)`.
8. **`esttab` not built-in:** Install `estout` package first: `ssc install estout`. Add a comment noting this dependency.
