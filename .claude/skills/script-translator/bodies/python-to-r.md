# Python → R Mapping

## Required Libraries

```r
library(tidyverse)   # dplyr, ggplot2, tidyr, readr, stringr, forcats
library(haven)       # read_dta, write_dta
library(fixest)      # feols
library(modelsummary) # tables
library(here)        # paths
```

## Construct Mapping Table

| Python (pandas) | R (tidyverse) |
|----------------|---------------|
| `pd.read_stata("f.dta")` | `read_dta("f.dta")` |
| `pd.read_csv("f.csv")` | `read_csv("f.csv")` |
| `df.to_stata("f.dta")` | `write_dta(df, "f.dta")` |
| `df.to_csv("f.csv", index=False)` | `write_csv(df, "f.csv")` |
| `df[df["x"] > 0].copy()` | `df %>% filter(x > 0)` |
| `df.dropna(subset=["x"])` | `df %>% filter(!is.na(x))` |
| `df[["var1", "var2"]]` | `df %>% select(var1, var2)` |
| `df.drop(columns=["var1"])` | `df %>% select(-var1)` |
| `df["y"] = df["x"] + df["z"]` | `df <- df %>% mutate(y = x + z)` |
| `df.loc[cond, "y"] = 0` | `df <- df %>% mutate(y = if_else(cond, 0, y))` |
| `df.rename(columns={"old": "new"})` | `df %>% rename(new = old)` |
| `df.sort_values(["v1", "v2"])` | `df %>% arrange(v1, v2)` |
| `df.drop_duplicates()` | `df %>% distinct()` |
| `df.groupby("x")["y"].mean()` | `df %>% group_by(x) %>% summarise(y = mean(y, na.rm = TRUE))` |
| `df.groupby("x").agg(...)` | `df %>% group_by(x) %>% summarise(...)` |
| `df.groupby("x")["y"].transform("mean")` | `df %>% group_by(x) %>% mutate(y_mean = mean(y, na.rm = TRUE)) %>% ungroup()` |
| `~df.duplicated(subset=["x"])` | `!duplicated(df$x)` |
| `df.merge(df2, on="key", how="left")` | `df %>% left_join(df2, by = "key")` |
| `df.merge(df2, how="inner")` | `df %>% inner_join(df2, by = "key")` |
| `pd.concat([df, df2])` | `bind_rows(df, df2)` |
| `df.pivot(index="id", columns="t", values="y")` | `df %>% pivot_wider(names_from = t, values_from = y)` |
| `pd.melt(df, id_vars=["id"])` | `df %>% pivot_longer(-id, names_to = "var", values_to = "val")` |
| `df["x"].astype("category")` | `factor(df$x)` |
| `pd.to_numeric(df["x"], errors="coerce")` | `as.numeric(df$x)` (NAs for non-numeric) |
| `df["x"].describe()` | `summary(df$x)` |
| `df["x"].value_counts()` | `table(df$x)` |
| `pd.crosstab(df["x"], df["y"])` | `table(df$x, df$y)` |
| `len(df)` | `nrow(df)` |
| `df.shape[1]` | `ncol(df)` |
| `df["x"].isna()` | `is.na(df$x)` |
| `df["x"].isin([1, 2, 3])` | `df$x %in% c(1, 2, 3)` |
| `df["s"].str[:3]` | `str_sub(df$s, 1, 3)` |
| `df["s"].str.len()` | `str_length(df$s)` |
| `df["s"].str.lower()` | `str_to_lower(df$s)` |
| `df["s"].str.contains("pat")` | `str_detect(df$s, "pat")` |
| `pd.to_datetime(df["s"])` | `ymd(df$s)` or `as.Date(df$s)` |
| `df["d"].dt.year` | `year(df$d)` |
| `np.log(df["x"])` | `log(df$x)` |
| `np.sqrt(df["x"])` | `sqrt(df$x)` |

## Regression Mapping

| Python | R |
|--------|---|
| `smf.ols("y ~ x1 + x2", df).fit(cov_type="HC1")` | `feols(y ~ x1 + x2, data = df, vcov = "HC1")` |
| `smf.ols(...).fit(cov_type="cluster", cov_kwds={"groups": df["g"]})` | `feols(y ~ x1 + x2, data = df, vcov = ~g)` |
| `smf.ols("y ~ x1 + C(cat)", df).fit()` | `feols(y ~ x1 + i(cat), data = df)` |
| `PanelOLS(y, x, entity_effects=True)` | `feols(y ~ x1 | entity, data = df)` |
| `smf.logit("y ~ x1 + x2", df).fit()` | `glm(y ~ x1 + x2, data = df, family = binomial("logit"))` |
| `smf.probit("y ~ x1 + x2", df).fit()` | `glm(y ~ x1 + x2, data = df, family = binomial("probit"))` |
| `results.predict()` | `predict(model)` |
| `results.summary()` | `summary(model)` |

## Figure Mapping

### Plot Types
| Python (matplotlib) | R (ggplot2) |
|---------------------|-------------|
| `fig, ax = plt.subplots(figsize=(8,6))` | `p <- ggplot(df, aes(...))` + `ggsave(..., width=8, height=6)` |
| `ax.scatter(x, y)` | `+ geom_point()` |
| `ax.plot(x, y)` | `+ geom_line()` |
| `np.polyfit` + `ax.plot` (linear fit) | `+ geom_smooth(method = "lm", se = FALSE)` |
| `ax.bar(x, height)` | `+ geom_col()` |
| `ax.hist(x)` | `+ geom_histogram()` |

### Labels and Titles
| Python | R |
|--------|---|
| `ax.set_title("T")` | `+ ggtitle("T")` |
| `ax.set_xlabel("X")` | `+ xlab("X")` |
| `ax.set_ylabel("Y")` | `+ ylab("Y")` |
| `ax.set_xlim(a, b)` | `+ xlim(a, b)` |
| `ax.set_ylim(a, b)` | `+ ylim(a, b)` |
| `ax.set_xticks([...])` + labels | `+ scale_x_continuous(breaks = ..., labels = ...)` |

### Colors, Transparency, Markers
| Python | R |
|--------|---|
| `color="blue"` | `color = "blue"` (in `geom_point(aes(), ...)`) |
| `alpha=0.7` | `alpha = 0.7` |
| `edgecolors="white", linewidth=0.5` | `geom_point(..., stroke = 0.5, color = "white")` with `fill` in aes, or use `shape = 21` for filled+bordered |
| `marker="o"` | `shape = 16` (solid circle) or `shape = 21` (circle with border) |
| `s=80` | `size = 3` (ggplot sizes differ; ~3 ≈ matplotlib s=80) |
| `linewidth=2` (line) | `linewidth = 1` or `size = 1` (ggplot line sizes are thinner) |

### Grid
| Python | R |
|--------|---|
| `ax.grid(True, alpha=0.3)` | `+ theme(panel.grid.major = element_line(color = "grey90"))` |
| No grid / `ax.grid(False)` | `+ theme(panel.grid = element_blank())` |

### Legend
| Python | R |
|--------|---|
| `ax.legend()` (default: best) | `+ theme(legend.position = "right")` (ggplot default) |
| `ax.legend(loc="lower right")` | `+ theme(legend.position = c(0.95, 0.05), legend.justification = c(1, 0))` |
| `ax.legend(loc="upper left")` | `+ theme(legend.position = c(0.05, 0.95), legend.justification = c(0, 1))` |
| `ax.legend(loc="upper right")` | `+ theme(legend.position = c(0.95, 0.95), legend.justification = c(1, 1))` |
| No legend | `+ theme(legend.position = "none")` |

### Point Labels / Annotations
| Python | R |
|--------|---|
| `ax.annotate(text, (x,y), fontsize=7, ha="left", xytext=(4,2), textcoords="offset points")` | `+ geom_text(aes(label = var), size = 2.5, hjust = 0, nudge_x = 0.1, nudge_y = 0.005)` |
| No annotations | Do NOT add `geom_text` |

### Background and Output
| Python | R |
|--------|---|
| `fig.patch.set_facecolor("white")` + `ax.set_facecolor("white")` | `+ theme(panel.background = element_rect(fill = "white"), plot.background = element_rect(fill = "white"))` or `+ theme_minimal()` |
| `fig.savefig("f.png", dpi=300, bbox_inches="tight")` | `ggsave("f.png", width = 8, height = 6, dpi = 300)` |
| `plt.close(fig)` | (not needed in R) |

## Known Traps

1. **0-based vs 1-based:** Python `df.iloc[0]` = first row. R `df[1, ]` = first row. String slicing: Python `s[:3]` = R `str_sub(s, 1, 3)`.
2. **Assignment:** Python `df["y"] = ...` modifies in place. R `mutate()` returns a new tibble — must reassign: `df <- df %>% mutate(...)`.
3. **`na.rm`:** Python aggregations skip NaN by default. R requires explicit `na.rm = TRUE` in `mean()`, `sum()`, `sd()`, etc.
4. **Boolean indexing:** Python `df[df["x"] > 0]` → R `df %>% filter(x > 0)`. Do NOT use `df[df$x > 0, ]` with NAs — it produces NA rows. `filter()` excludes NAs.
5. **`merge` indicator:** Python `indicator=True` adds `_merge` column. R joins have no equivalent; use `anti_join()` to find unmatched.
6. **Column access:** Python `df["col"]` vs R `df$col` or `df %>% pull(col)`. Inside tidyverse verbs, use bare names: `filter(x > 0)` not `filter(df$x > 0)`.
7. **List comprehensions:** Python `[f(x) for x in lst]` → R `sapply(lst, f)` or `map(lst, f)`.
8. **f-strings:** Python `f"value is {x:.2f}"` → R `sprintf("value is %.2f", x)` or `glue("value is {round(x, 2)}")`.
