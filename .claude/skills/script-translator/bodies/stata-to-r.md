# Stata → R Mapping

## Required Libraries

```r
library(tidyverse)   # dplyr, ggplot2, tidyr, readr, stringr, forcats
library(haven)       # read_dta, write_dta
library(fixest)      # feols (fast fixed effects)
library(modelsummary) # regression tables
library(here)        # project-relative paths
```

## Construct Mapping Table

| Stata | R (tidyverse) |
|-------|---------------|
| `use "file.dta", clear` | `df <- read_dta("file.dta")` |
| `import delimited "f.csv"` | `df <- read_csv("f.csv")` |
| `save "file.dta", replace` | `write_dta(df, "file.dta")` |
| `export delimited "f.csv"` | `write_csv(df, "f.csv")` |
| `keep if x > 0` | `df <- df %>% filter(x > 0)` |
| `drop if is.na(x)` | `df <- df %>% filter(!is.na(x))` |
| `keep var1 var2` | `df <- df %>% select(var1, var2)` |
| `drop var1` | `df <- df %>% select(-var1)` |
| `gen y = x + z` | `df <- df %>% mutate(y = x + z)` |
| `replace y = 0 if x < 0` | `df <- df %>% mutate(y = if_else(x < 0, 0, y))` |
| `rename old new` | `df <- df %>% rename(new = old)` |
| `sort var1 var2` | `df <- df %>% arrange(var1, var2)` |
| `duplicates drop` | `df <- df %>% distinct()` |
| `collapse (mean) y, by(x)` | `df <- df %>% group_by(x) %>% summarise(y = mean(y, na.rm = TRUE))` |
| `collapse (sum) y (mean) z, by(x)` | `df <- df %>% group_by(x) %>% summarise(y = sum(y), z = mean(z))` |
| `egen y_mean = mean(y), by(x)` | `df <- df %>% group_by(x) %>% mutate(y_mean = mean(y, na.rm = TRUE)) %>% ungroup()` |
| `egen y_sd = sd(y), by(x)` | `df <- df %>% group_by(x) %>% mutate(y_sd = sd(y, na.rm = TRUE)) %>% ungroup()` |
| `egen y_count = count(y), by(x)` | `df <- df %>% group_by(x) %>% mutate(y_count = sum(!is.na(y))) %>% ungroup()` |
| `egen tag = tag(x)` | `df <- df %>% mutate(tag = !duplicated(x))` |
| `merge m:1 key using "f.dta"` | `df <- df %>% left_join(df2, by = "key")` |
| `tab _merge` | `# R joins don't produce _merge; use anti_join to check unmatched` |
| `append using "f.dta"` | `df <- bind_rows(df, df2)` |
| `reshape wide y, i(id) j(t)` | `df <- df %>% pivot_wider(names_from = t, values_from = y)` |
| `reshape long y, i(id) j(t)` | `df <- df %>% pivot_longer(cols = ..., names_to = "t", values_to = "y")` |
| `encode strvar, gen(numvar)` | `df <- df %>% mutate(numvar = as.numeric(factor(strvar)))` |
| `destring strvar, replace` | `df <- df %>% mutate(strvar = as.numeric(strvar))` |
| `tostring numvar, replace` | `df <- df %>% mutate(numvar = as.character(numvar))` |
| `summarize x` | `summary(df$x)` |
| `tabulate x` | `table(df$x)` |
| `tab x y` | `table(df$x, df$y)` |
| `count if x > 0` | `sum(df$x > 0, na.rm = TRUE)` |
| `assert _N > 0` | `stopifnot(nrow(df) > 0)` |
| `missing(x)` | `is.na(df$x)` |
| `!missing(x)` | `!is.na(df$x)` |
| `inlist(x, 1, 2, 3)` | `df$x %in% c(1, 2, 3)` |
| `substr(s, 1, 3)` | `str_sub(df$s, 1, 3)` |
| `strlen(s)` | `str_length(df$s)` |
| `lower(s)` | `str_to_lower(df$s)` |
| `regexm(s, "pat")` | `str_detect(df$s, "pat")` |
| `date(s, "YMD")` | `ymd(df$s)` (lubridate) |
| `year(d)` | `year(df$d)` (lubridate) |

## Regression Mapping

| Stata | R |
|-------|---|
| `reg y x1 x2, robust` | `feols(y ~ x1 + x2, data = df, vcov = "HC1")` |
| `reg y x1 x2, cluster(g)` | `feols(y ~ x1 + x2, data = df, vcov = ~g)` |
| `reg y x1 i.cat` | `feols(y ~ x1 + i(cat), data = df)` |
| `areg y x1, absorb(fe)` | `feols(y ~ x1 | fe, data = df)` |
| `xtreg y x1, fe` | `feols(y ~ x1 | entity, data = df)` |
| `logit y x1 x2` | `glm(y ~ x1 + x2, data = df, family = binomial(link = "logit"))` |
| `probit y x1 x2` | `glm(y ~ x1 + x2, data = df, family = binomial(link = "probit"))` |
| `predict yhat` | `df$yhat <- predict(model)` |
| `eststo` / `esttab` | `modelsummary(list(m1, m2), output = "latex")` |
| `test x1 = x2` | `linearHypothesis(model, "x1 = x2")` (car package) |
| `margins, dydx(x1)` | `margins::margins(model, variables = "x1")` |

## Figure Mapping

### Plot Types
| Stata | R (ggplot2) |
|-------|-------------|
| `twoway scatter y x` | `ggplot(df, aes(x, y)) + geom_point()` |
| `twoway line y x` | `+ geom_line()` |
| `twoway lfit y x` | `+ geom_smooth(method = "lm", se = FALSE)` |
| `twoway bar y x` / `graph bar y, over(x)` | `+ geom_col()` |
| `histogram x` | `+ geom_histogram()` |

### Labels and Titles
| Stata | R |
|-------|---|
| `title("T")` | `+ ggtitle("T")` |
| `xtitle("X")` | `+ xlab("X")` |
| `ytitle("Y")` | `+ ylab("Y")` |
| `xscale(range(a b))` | `+ xlim(a, b)` |
| `yscale(range(a b))` | `+ ylim(a, b)` |
| `xlabel(val1 "lab1" val2 "lab2")` | `+ scale_x_continuous(breaks = c(val1, val2), labels = c("lab1", "lab2"))` |

### Colors, Transparency, Markers
| Stata | R |
|-------|---|
| `mcolor(blue)` | `color = "blue"` (outside aes) |
| `mcolor(blue%70)` | `color = "blue", alpha = 0.7` |
| `mlcolor(white) mlwidth(vthin)` | `shape = 21, fill = "blue", color = "white", stroke = 0.5` |
| `msymbol(circle)` | `shape = 16` (solid) or `shape = 21` (with border) |
| `msize(large)` | `size = 3` |
| `lcolor(red) lwidth(medium)` | `color = "red", linewidth = 1` |
| `lpattern(dash)` | `linetype = "dashed"` |

### Grid
| Stata | R |
|-------|---|
| `ylabel(, grid glcolor(gs14))` / grid present | `+ theme(panel.grid.major = element_line(color = "grey90"))` |
| No grid options | `+ theme(panel.grid = element_blank())` |

### Legend
| Stata | R |
|-------|---|
| `legend(order(1 "A" 2 "B"))` | `+ scale_color_manual(values = ..., labels = c("A", "B"))` |
| `legend(... position(5) ring(0))` | `+ theme(legend.position = c(0.95, 0.05), legend.justification = c(1, 0))` |
| `legend(... position(11) ring(0))` | `+ theme(legend.position = c(0.05, 0.95), legend.justification = c(0, 1))` |
| `legend(... position(1) ring(0))` | `+ theme(legend.position = c(0.95, 0.95), legend.justification = c(1, 1))` |
| `legend(off)` | `+ theme(legend.position = "none")` |

### Point Labels / Annotations
| Stata | R |
|-------|---|
| `mlabel(var) mlabsize(tiny) mlabposition(3)` | `+ geom_text(aes(label = var), size = 2.5, hjust = 0, nudge_x = 0.1)` |
| No `mlabel` | Do NOT add `geom_text` |

### Background and Output
| Stata | R |
|-------|---|
| `graphregion(color(white)) bgcolor(white)` | `+ theme(panel.background = element_rect(fill = "white"), plot.background = element_rect(fill = "white"))` |
| `xsize(8) ysize(6)` | `ggsave(..., width = 8, height = 6)` |
| `graph export "f.png", replace width(2400)` | `ggsave("f.png", width = 8, height = 6, dpi = 300)` |
| `graph drop _all` | (not needed in R) |

## Table Export

| Stata | R |
|-------|---|
| `esttab using "t.tex", booktabs` | `modelsummary(models, output = "t.tex", gof_map = ...)` |
| `estpost summarize` + `esttab cells(...)` | `datasummary(x1 + x2 ~ Mean + SD + Min + Max + N, data = df, output = "latex")` |

## Known Traps

1. **Missing values:** Stata `.` sorts to +infinity and `x > 0` is TRUE for missing. R `NA` propagates as `NA` in comparisons. Always add `na.rm = TRUE` in aggregation functions.
2. **`substr` indexing:** Stata `substr(s, 1, 3)` is 1-based, 3 chars. R `str_sub(s, 1, 3)` is also 1-based, 3 chars. Direct mapping works.
3. **`encode` ordering:** Stata assigns alphabetical codes. R `factor()` also uses alphabetical levels. Match is preserved. But `as.numeric(factor(...))` starts at 1.
4. **`robust` SEs:** Stata `robust` = HC1. `fixest::feols` with `vcov = "HC1"` matches exactly. Do NOT use the default `sandwich::vcovHC` which defaults to HC3.
5. **Factor base level:** Stata `i.x` drops first alphabetical level. R `factor()` also drops the first level. If Stata uses `ib2.x`, use `relevel(factor(x), ref = "2")`.
6. **`merge` diagnostics:** Stata produces `_merge`. R joins do not. To replicate: use `anti_join()` before the join to count unmatched rows.
7. **`collapse` destroys data:** Stata replaces the dataset. R `summarise()` returns a new tibble. No issue, but match the variable naming exactly.
8. **Grouped operations:** After `group_by()` + `mutate()`, always `ungroup()` to prevent downstream surprises.
