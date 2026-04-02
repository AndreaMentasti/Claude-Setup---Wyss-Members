# Stata → Python Mapping

## Required Imports

```python
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from linearmodels.panel import PanelOLS  # if panel data
import matplotlib.pyplot as plt
import config as cfg
```

## Construct Mapping Table

| Stata | Python (pandas/statsmodels) |
|-------|---------------------------|
| `use "file.dta", clear` | `df = pd.read_stata("file.dta")` |
| `import delimited "f.csv"` | `df = pd.read_csv("f.csv", encoding="utf-8")` |
| `save "file.dta", replace` | `df.to_stata("file.dta", write_index=False)` |
| `export delimited "f.csv"` | `df.to_csv("f.csv", index=False)` |
| `keep if x > 0` | `df = df[df["x"] > 0].copy()` |
| `drop if missing(x)` | `df = df.dropna(subset=["x"]).copy()` |
| `keep var1 var2` | `df = df[["var1", "var2"]].copy()` |
| `drop var1` | `df = df.drop(columns=["var1"])` |
| `gen y = x + z` | `df["y"] = df["x"] + df["z"]` |
| `replace y = 0 if x < 0` | `df.loc[df["x"] < 0, "y"] = 0` |
| `rename old new` | `df = df.rename(columns={"old": "new"})` |
| `sort var1 var2` | `df = df.sort_values(["var1", "var2"])` |
| `duplicates drop` | `df = df.drop_duplicates()` |
| `collapse (mean) y, by(x)` | `df = df.groupby("x", as_index=False)["y"].mean()` |
| `collapse (sum) y (mean) z, by(x)` | `df = df.groupby("x", as_index=False).agg({"y": "sum", "z": "mean"})` |
| `egen y_mean = mean(y), by(x)` | `df["y_mean"] = df.groupby("x")["y"].transform("mean")` |
| `egen y_sd = sd(y), by(x)` | `df["y_sd"] = df.groupby("x")["y"].transform("std")` |
| `egen y_count = count(y), by(x)` | `df["y_count"] = df.groupby("x")["y"].transform("count")` |
| `egen tag = tag(x)` | `df["tag"] = ~df.duplicated(subset=["x"])` |
| `merge m:1 key using "f.dta"` | `df = df.merge(df2, on="key", how="left", validate="m:1")` |
| `tab _merge` | `print(df["_merge"].value_counts())` |
| `append using "f.dta"` | `df = pd.concat([df, df2], ignore_index=True)` |
| `reshape wide y, i(id) j(t)` | `df = df.pivot(index="id", columns="t", values="y").reset_index()` |
| `reshape long y, i(id) j(t)` | `df = pd.melt(df, id_vars=["id"], var_name="t", value_name="y")` |
| `encode strvar, gen(numvar)` | `df["numvar"] = df["strvar"].astype("category").cat.codes` |
| `destring strvar, replace` | `df["strvar"] = pd.to_numeric(df["strvar"], errors="coerce")` |
| `tostring numvar, replace` | `df["numvar"] = df["numvar"].astype(str)` |
| `summarize x` | `print(df["x"].describe())` |
| `tabulate x` | `print(df["x"].value_counts())` |
| `tab x y` | `print(pd.crosstab(df["x"], df["y"]))` |
| `count if x > 0` | `print((df["x"] > 0).sum())` |
| `assert _N > 0` | `assert len(df) > 0` |
| `assert x >= 0` | `assert (df["x"] >= 0).all()` |
| `missing(x)` | `df["x"].isna()` |
| `!missing(x)` | `df["x"].notna()` |
| `inlist(x, 1, 2, 3)` | `df["x"].isin([1, 2, 3])` |
| `substr(s, 1, 3)` | `df["s"].str[:3]` |
| `strlen(s)` | `df["s"].str.len()` |
| `lower(s)` | `df["s"].str.lower()` |
| `regexm(s, "pat")` | `df["s"].str.contains("pat", regex=True)` |
| `date(s, "YMD")` | `pd.to_datetime(df["s"])` |
| `year(d)` | `df["d"].dt.year` |

## Regression Mapping

| Stata | Python |
|-------|--------|
| `reg y x1 x2, robust` | `smf.ols("y ~ x1 + x2", data=df).fit(cov_type="HC1")` |
| `reg y x1 x2, cluster(g)` | `smf.ols("y ~ x1 + x2", data=df).fit(cov_type="cluster", cov_kwds={"groups": df["g"]})` |
| `reg y x1 i.cat` | `smf.ols("y ~ x1 + C(cat)", data=df).fit()` |
| `areg y x1, absorb(fe)` | `smf.ols("y ~ x1 + C(fe)", data=df).fit()` or use `linearmodels.PanelOLS` |
| `xtreg y x1, fe` | `PanelOLS(df["y"], df[["x1"]], entity_effects=True).fit()` |
| `logit y x1 x2` | `smf.logit("y ~ x1 + x2", data=df).fit()` |
| `probit y x1 x2` | `smf.probit("y ~ x1 + x2", data=df).fit()` |
| `predict yhat` | `df["yhat"] = results.predict()` |
| `eststo` / `esttab` | Use `stargazer` or manual LaTeX with `results.summary().as_latex()` |
| `test x1 = x2` | `results.f_test("x1 = x2")` |
| `margins, dydx(x1)` | `results.get_margeff().summary()` |

## Figure Mapping

### Plot Types
| Stata | Python (matplotlib) |
|-------|---------------------|
| `twoway scatter y x` | `ax.scatter(df["x"], df["y"])` |
| `twoway line y x` | `ax.plot(df["x"], df["y"])` |
| `twoway lfit y x` | `np.polyfit(x, y, 1)` then `ax.plot(x_fit, slope*x_fit + intercept)` |
| `twoway bar y x` / `graph bar y, over(x)` | `ax.bar(df["x"], df["y"])` |
| `histogram x` | `ax.hist(df["x"])` |

### Labels and Titles
| Stata | Python |
|-------|--------|
| `title("T")` | `ax.set_title("T")` |
| `xtitle("X")` | `ax.set_xlabel("X")` |
| `ytitle("Y")` | `ax.set_ylabel("Y")` |
| `xscale(range(a b))` | `ax.set_xlim(a, b)` |
| `yscale(range(a b))` | `ax.set_ylim(a, b)` |
| `xlabel(val1 "lab1" val2 "lab2")` | `ax.set_xticks([val1, val2])` + `ax.set_xticklabels(["lab1", "lab2"])` |

### Colors, Transparency, Markers
| Stata | Python |
|-------|--------|
| `mcolor(blue)` | `color="blue"` |
| `mcolor(blue%70)` | `color="blue", alpha=0.7` |
| `mlcolor(white)` | `edgecolors="white"` |
| `mlwidth(vthin)` | `linewidth=0.5` (in scatter) |
| `msymbol(circle)` | `marker="o"` |
| `msize(large)` | `s=80` |
| `lcolor(red)` | `color="red"` (in plot) |
| `lwidth(medium)` | `linewidth=2` |
| `lpattern(dash)` | `linestyle="--"` |

### Grid
| Stata | Python |
|-------|--------|
| `ylabel(, grid glcolor(gs14))` / `xscale(grid)` | `ax.grid(True, alpha=0.3)` |
| No grid options present | Do NOT add `ax.grid()` |

### Legend
| Stata | Python |
|-------|--------|
| `legend(order(1 "A" 2 "B"))` | `ax.legend(["A", "B"])` |
| `legend(... position(5) ring(0))` | `ax.legend(loc="lower right")` |
| `legend(... position(11) ring(0))` | `ax.legend(loc="upper left")` |
| `legend(... position(1) ring(0))` | `ax.legend(loc="upper right")` |
| `legend(off)` | Do NOT call `ax.legend()` |

### Point Labels / Annotations
| Stata | Python |
|-------|--------|
| `mlabel(var) mlabsize(tiny) mlabposition(3)` | `ax.annotate(text, (x,y), fontsize=7, ha="left", va="bottom", xytext=(4,2), textcoords="offset points")` |
| No `mlabel` option | Do NOT add annotations |

### Background and Output
| Stata | Python |
|-------|--------|
| `graphregion(color(white))` | `fig.patch.set_facecolor("white")` |
| `bgcolor(white)` | `ax.set_facecolor("white")` |
| `xsize(8) ysize(6)` | `fig, ax = plt.subplots(figsize=(8, 6))` |
| `graph export "f.png", replace width(2400)` | `fig.savefig("f.png", dpi=300, bbox_inches="tight")` |
| `graph drop _all` | `plt.close(fig)` |

### Stata legend position → matplotlib loc
```
position(11) ring(0) → loc="upper left"
position(12) ring(0) → loc="upper center"
position(1)  ring(0) → loc="upper right"
position(9)  ring(0) → loc="center left"
position(2)  ring(0) → loc="center right"
position(7)  ring(0) → loc="lower left"
position(8)  ring(0) → loc="lower center"
position(5)  ring(0) → loc="lower right"
```

## Table Export

| Stata | Python |
|-------|--------|
| `esttab using "t.tex", booktabs label replace` | Write manually or use `stargazer` package |
| `estpost summarize` + `esttab cells(...)` | `df.describe().to_latex()` with formatting |

## Known Traps

1. **Missing values:** Stata treats `.` as +infinity in comparisons (`x > 0` is TRUE for missing). Python `NaN` propagates as False. Add explicit `.notna()` checks where Stata code compares against missing.
2. **1-based vs 0-based:** Stata `substr(s, 1, 3)` = first 3 chars. Python `s[:3]` = first 3 chars. But `_n` (row number) in Stata is 1-based; pandas index may be 0-based.
3. **`encode` ordering:** Stata `encode` assigns codes alphabetically. `pd.Categorical.codes` also uses alphabetical sort order, so the mapping is preserved.
4. **`robust` SEs:** Stata `robust` = HC1. Statsmodels default `HC1` matches. Do NOT use `HC3` (the statsmodels default for some methods).
5. **Factor variables:** Stata `i.x` auto-drops the first level. In statsmodels, `C(x)` also drops the first alphabetically. If the original uses `ib2.x` (base=2), specify `C(x, Treatment(reference=2))`.
6. **`collapse` destroys data:** In Stata, `collapse` replaces the dataset. In Python, assign to a new DataFrame if the original is needed later.
7. **Sort stability:** Stata `sort` is unstable. Pandas `sort_values` is stable by default (`kind="mergesort"`). This rarely matters but can affect `_n`-based operations.
8. **String comparison:** Stata is case-sensitive by default. Python string operations are also case-sensitive. Match is preserved.
