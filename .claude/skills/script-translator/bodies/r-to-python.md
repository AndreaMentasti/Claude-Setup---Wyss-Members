# R → Python Mapping

## Required Imports

```python
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import config as cfg
```

## Construct Mapping Table

| R (tidyverse) | Python (pandas) |
|---------------|----------------|
| `read_dta("f.dta")` | `pd.read_stata("f.dta")` |
| `read_csv("f.csv")` | `pd.read_csv("f.csv", encoding="utf-8")` |
| `write_dta(df, "f.dta")` | `df.to_stata("f.dta", write_index=False)` |
| `write_csv(df, "f.csv")` | `df.to_csv("f.csv", index=False)` |
| `df %>% filter(x > 0)` | `df = df[df["x"] > 0].copy()` |
| `df %>% filter(!is.na(x))` | `df = df.dropna(subset=["x"]).copy()` |
| `df %>% select(var1, var2)` | `df = df[["var1", "var2"]].copy()` |
| `df %>% select(-var1)` | `df = df.drop(columns=["var1"])` |
| `df %>% mutate(y = x + z)` | `df["y"] = df["x"] + df["z"]` |
| `df %>% mutate(y = if_else(x < 0, 0, y))` | `df.loc[df["x"] < 0, "y"] = 0` |
| `df %>% rename(new = old)` | `df = df.rename(columns={"old": "new"})` |
| `df %>% arrange(v1, v2)` | `df = df.sort_values(["v1", "v2"])` |
| `df %>% distinct()` | `df = df.drop_duplicates()` |
| `df %>% group_by(x) %>% summarise(y = mean(y))` | `df = df.groupby("x", as_index=False)["y"].mean()` |
| `df %>% group_by(x) %>% summarise(y = sum(y), z = mean(z))` | `df = df.groupby("x", as_index=False).agg({"y": "sum", "z": "mean"})` |
| `df %>% group_by(x) %>% mutate(ym = mean(y)) %>% ungroup()` | `df["ym"] = df.groupby("x")["y"].transform("mean")` |
| `df %>% left_join(df2, by = "key")` | `df = df.merge(df2, on="key", how="left")` |
| `df %>% inner_join(df2, by = "key")` | `df = df.merge(df2, on="key", how="inner")` |
| `bind_rows(df, df2)` | `df = pd.concat([df, df2], ignore_index=True)` |
| `df %>% pivot_wider(names_from = t, values_from = y)` | `df = df.pivot(index="id", columns="t", values="y").reset_index()` |
| `df %>% pivot_longer(-id)` | `df = pd.melt(df, id_vars=["id"])` |
| `factor(df$x)` | `df["x"] = df["x"].astype("category")` |
| `as.numeric(df$x)` | `df["x"] = pd.to_numeric(df["x"], errors="coerce")` |
| `summary(df$x)` | `print(df["x"].describe())` |
| `table(df$x)` | `print(df["x"].value_counts())` |
| `table(df$x, df$y)` | `print(pd.crosstab(df["x"], df["y"]))` |
| `nrow(df)` | `len(df)` |
| `ncol(df)` | `df.shape[1]` |
| `is.na(df$x)` | `df["x"].isna()` |
| `df$x %in% c(1, 2, 3)` | `df["x"].isin([1, 2, 3])` |
| `str_sub(df$s, 1, 3)` | `df["s"].str[:3]` |
| `str_length(df$s)` | `df["s"].str.len()` |
| `str_to_lower(df$s)` | `df["s"].str.lower()` |
| `str_detect(df$s, "pat")` | `df["s"].str.contains("pat", regex=True)` |
| `ymd(df$s)` | `pd.to_datetime(df["s"])` |
| `year(df$d)` | `df["d"].dt.year` |
| `log(x)` | `np.log(x)` |
| `sqrt(x)` | `np.sqrt(x)` |
| `stopifnot(nrow(df) > 0)` | `assert len(df) > 0` |

## Regression Mapping

| R | Python |
|---|--------|
| `feols(y ~ x1 + x2, df, vcov = "HC1")` | `smf.ols("y ~ x1 + x2", data=df).fit(cov_type="HC1")` |
| `feols(y ~ x1 + x2, df, vcov = ~g)` | `smf.ols("y ~ x1 + x2", data=df).fit(cov_type="cluster", cov_kwds={"groups": df["g"]})` |
| `feols(y ~ x1 + i(cat), df)` | `smf.ols("y ~ x1 + C(cat)", data=df).fit()` |
| `feols(y ~ x1 | fe, df)` | `smf.ols("y ~ x1 + C(fe)", data=df).fit()` or `linearmodels.PanelOLS` |
| `glm(y ~ x1, family = binomial("logit"))` | `smf.logit("y ~ x1", data=df).fit()` |
| `glm(y ~ x1, family = binomial("probit"))` | `smf.probit("y ~ x1", data=df).fit()` |
| `predict(model)` | `model.predict()` |
| `summary(model)` | `print(model.summary())` |
| `modelsummary(list(m1, m2), output = "latex")` | Manual LaTeX or `stargazer` package |

## Figure Mapping

### Plot Types
| R (ggplot2) | Python (matplotlib) |
|-------------|---------------------|
| `ggplot(df, aes(x, y)) + geom_point()` | `ax.scatter(df["x"], df["y"])` |
| `+ geom_line()` | `ax.plot(df["x"], df["y"])` |
| `+ geom_col()` | `ax.bar(df["x"], df["y"])` |
| `+ geom_histogram()` | `ax.hist(df["x"])` |
| `+ geom_smooth(method = "lm", se = FALSE)` | `np.polyfit(x, y, 1)` then `ax.plot(x_fit, slope*x_fit + intercept)` |

### Labels and Titles
| R | Python |
|---|--------|
| `+ ggtitle("T")` | `ax.set_title("T")` |
| `+ xlab("X")` | `ax.set_xlabel("X")` |
| `+ ylab("Y")` | `ax.set_ylabel("Y")` |
| `+ xlim(a, b)` | `ax.set_xlim(a, b)` |
| `+ ylim(a, b)` | `ax.set_ylim(a, b)` |
| `+ scale_x_continuous(breaks = ..., labels = ...)` | `ax.set_xticks(...)` + `ax.set_xticklabels(...)` |

### Colors, Transparency, Markers
| R | Python |
|---|--------|
| `color = "blue"` (in geom) | `color="blue"` |
| `alpha = 0.7` | `alpha=0.7` |
| `shape = 21, fill = "blue", color = "white", stroke = 0.5` | `marker="o", color="blue", edgecolors="white", linewidth=0.5` |
| `size = 3` (point) | `s=80` (matplotlib sizes are in pts^2) |
| `linewidth = 1` (line) | `linewidth=2` (matplotlib lines are thinner) |

### Grid
| R | Python |
|---|--------|
| `+ theme(panel.grid.major = element_line(color = "grey90"))` | `ax.grid(True, alpha=0.3)` |
| `+ theme_minimal()` (has grid) | `ax.grid(True, alpha=0.3)` + white background |
| `+ theme(panel.grid = element_blank())` | Do NOT add `ax.grid()` |

### Legend
| R | Python |
|---|--------|
| `legend.position = "right"` (default) | `ax.legend()` (default: best/upper right) |
| `legend.position = c(0.95, 0.05), legend.justification = c(1, 0)` | `ax.legend(loc="lower right")` |
| `legend.position = c(0.05, 0.95), legend.justification = c(0, 1)` | `ax.legend(loc="upper left")` |
| `legend.position = "none"` | Do NOT call `ax.legend()` |

### Point Labels / Annotations
| R | Python |
|---|--------|
| `+ geom_text(aes(label = var), size = 2.5, hjust = 0, nudge_x = 0.1)` | `ax.annotate(text, (x,y), fontsize=7, ha="left", xytext=(4,2), textcoords="offset points")` |
| No `geom_text` | Do NOT add annotations |

### Background and Output
| R | Python |
|---|--------|
| `+ theme_minimal()` / `theme(panel.background = ...)` | `fig.patch.set_facecolor("white")` + `ax.set_facecolor("white")` |
| `ggsave("f.png", width = 8, height = 6, dpi = 300)` | `fig, ax = plt.subplots(figsize=(8, 6))` then `fig.savefig("f.png", dpi=300, bbox_inches="tight")` |
| (R cleans up automatically) | `plt.close(fig)` |

## Known Traps

1. **1-based → 0-based:** R `str_sub(s, 1, 3)` = first 3 chars. Python `s[:3]` = first 3 chars. But R `df[1, ]` = Python `df.iloc[0]`.
2. **`na.rm` → default:** R aggregations require `na.rm = TRUE`. Python `mean()`, `sum()` skip NaN by default. Behavior matches when `na.rm = TRUE` is present.
3. **Pipe chains:** R `df %>% filter() %>% mutate() %>% select()` → Python sequential assignments or method chaining `df.query().assign().filter()`. Sequential is clearer for translation.
4. **`if_else` vs `ifelse`:** R `if_else` is type-strict. Python `np.where(cond, a, b)` is the closest equivalent. `df.loc[cond, col] = val` works for simple cases.
5. **Factor levels:** R factors have ordered levels. Python `pd.Categorical` has categories. When translating `levels = c("B", "A")`, use `pd.Categorical(df["x"], categories=["B", "A"], ordered=True)`.
6. **`here::here()` paths:** Map to `cfg.FIGURES`, `cfg.TABLES`, `cfg.DATA_PROCESSED` etc. from `config.py`.
7. **`%>%` pipe:** Each pipe step in R becomes a separate line in Python. Do not try to chain everything into one pandas expression.
8. **ggplot facets:** `facet_wrap(~var)` → matplotlib `fig, axes = plt.subplots(nrows, ncols)` with a loop. More verbose but faithful.
