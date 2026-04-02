# R → Stata Mapping

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

| R (tidyverse) | Stata |
|---------------|-------|
| `read_dta("f.dta")` | `use "f.dta", clear` |
| `read_csv("f.csv")` | `import delimited "f.csv", clear` |
| `write_dta(df, "f.dta")` | `save "f.dta", replace` |
| `write_csv(df, "f.csv")` | `export delimited "f.csv", replace` |
| `df %>% filter(x > 0)` | `keep if x > 0` |
| `df %>% filter(!is.na(x))` | `drop if missing(x)` |
| `df %>% select(var1, var2)` | `keep var1 var2` |
| `df %>% select(-var1)` | `drop var1` |
| `df %>% mutate(y = x + z)` | `gen y = x + z` |
| `df %>% mutate(y = if_else(x < 0, 0, y))` | `replace y = 0 if x < 0` |
| `df %>% rename(new = old)` | `rename old new` |
| `df %>% arrange(v1, v2)` | `sort v1 v2` |
| `df %>% distinct()` | `duplicates drop` |
| `df %>% group_by(x) %>% summarise(y = mean(y))` | `collapse (mean) y, by(x)` |
| `df %>% group_by(x) %>% summarise(y = sum(y), z = mean(z))` | `collapse (sum) y (mean) z, by(x)` |
| `df %>% group_by(x) %>% mutate(ym = mean(y)) %>% ungroup()` | `egen ym = mean(y), by(x)` |
| `df %>% group_by(x) %>% mutate(ysd = sd(y)) %>% ungroup()` | `egen ysd = sd(y), by(x)` |
| `df %>% group_by(x) %>% mutate(yn = n()) %>% ungroup()` | `egen yn = count(y), by(x)` |
| `!duplicated(df$x)` | `egen tag = tag(x)` |
| `df %>% left_join(df2, by = "key")` | `merge m:1 key using "f.dta"` |
| `df %>% inner_join(df2, by = "key")` | `merge m:1 key using "f.dta"` then `keep if _merge == 3` |
| `bind_rows(df, df2)` | `append using "f.dta"` |
| `df %>% pivot_wider(names_from = t, values_from = y)` | `reshape wide y, i(id) j(t)` |
| `df %>% pivot_longer(-id)` | `reshape long y, i(id) j(t)` |
| `factor(df$x)` | `encode x, gen(x_num)` |
| `as.numeric(df$x)` | `destring x, replace force` |
| `as.character(df$x)` | `tostring x, replace` |
| `summary(df$x)` | `summarize x` |
| `table(df$x)` | `tabulate x` |
| `table(df$x, df$y)` | `tab x y` |
| `nrow(df)` | `count` (stores in `r(N)`) |
| `stopifnot(nrow(df) > 0)` | `assert _N > 0` |
| `is.na(df$x)` | `missing(x)` |
| `df$x %in% c(1, 2, 3)` | `inlist(x, 1, 2, 3)` |
| `str_sub(df$s, 1, 3)` | `gen s3 = substr(s, 1, 3)` |
| `str_length(df$s)` | `gen slen = strlen(s)` |
| `str_to_lower(df$s)` | `gen s_low = lower(s)` |
| `str_detect(df$s, "pat")` | `gen has_pat = regexm(s, "pat")` |
| `ymd(df$s)` | `gen d = date(s, "YMD")` |
| `year(df$d)` | `gen yr = year(d)` |

## Regression Mapping

| R | Stata |
|---|-------|
| `feols(y ~ x1 + x2, df, vcov = "HC1")` | `reg y x1 x2, robust` |
| `feols(y ~ x1 + x2, df, vcov = ~g)` | `reg y x1 x2, vce(cluster g)` |
| `feols(y ~ x1 + i(cat), df)` | `reg y x1 i.cat` |
| `feols(y ~ x1 | fe, df)` | `areg y x1, absorb(fe)` or `reghdfe y x1, absorb(fe)` |
| `glm(y ~ x1, family = binomial("logit"))` | `logit y x1` |
| `glm(y ~ x1, family = binomial("probit"))` | `probit y x1` |
| `predict(model)` | `predict yhat` |
| `summary(model)` | (displayed automatically after estimation) |
| `modelsummary(list(m1, m2), output = "latex")` | `esttab using "t.tex", booktabs label replace` |
| `linearHypothesis(model, "x1 = x2")` | `test x1 = x2` |

## Figure Mapping

### Plot Types
| R (ggplot2) | Stata |
|-------------|-------|
| `geom_point()` | `twoway scatter y x` |
| `geom_line()` | `twoway line y x` |
| `geom_smooth(method = "lm", se = FALSE)` | `twoway lfit y x` |
| `geom_col()` | `twoway bar y x` or `graph bar y, over(x)` |
| `geom_histogram()` | `histogram x` |
| `facet_wrap(~var)` | `by(var)` option or separate graphs |

### Labels and Titles
| R | Stata |
|---|-------|
| `+ ggtitle("T")` | `title("T")` |
| `+ xlab("X")` | `xtitle("X")` |
| `+ ylab("Y")` | `ytitle("Y")` |
| `+ xlim(a, b)` | `xscale(range(a b))` |
| `+ ylim(a, b)` | `yscale(range(a b))` |
| `+ scale_x_continuous(breaks = ..., labels = ...)` | `xlabel(val1 "lab1" val2 "lab2")` |

### Colors, Transparency, Markers
| R | Stata |
|---|-------|
| `color = "blue"` | `mcolor(blue)` |
| `alpha = 0.7` | `%70` suffix: `mcolor(blue%70)` |
| `shape = 21, fill = "blue", color = "white", stroke = 0.5` | `mcolor(blue%70) mlcolor(white) mlwidth(vthin)` |
| `size = 3` (point) | `msize(large)` |
| `color = "red", linewidth = 1` (line) | `lcolor(red) lwidth(medium)` |
| `linetype = "dashed"` | `lpattern(dash)` |

### Grid
| R | Stata |
|---|-------|
| `theme(panel.grid.major = element_line(...))` / `theme_minimal()` | `ylabel(, grid glcolor(gs14))` or `xscale(grid) yscale(grid)` |
| `theme(panel.grid = element_blank())` | Do NOT add any grid options |

### Legend
| R | Stata |
|---|-------|
| `legend.position = "right"` (default) | `legend(order(1 "A" 2 "B"))` |
| `legend.position = c(0.95, 0.05), legend.justification = c(1, 0)` | `legend(... position(5) ring(0))` (lower right) |
| `legend.position = c(0.05, 0.95), legend.justification = c(0, 1)` | `legend(... position(11) ring(0))` (upper left) |
| `legend.position = c(0.95, 0.95), legend.justification = c(1, 1)` | `legend(... position(1) ring(0))` (upper right) |
| `legend.position = "none"` | `legend(off)` |

### Point Labels / Annotations
| R | Stata |
|---|-------|
| `+ geom_text(aes(label = var), size = 2.5, hjust = 0, nudge_x = 0.1)` | `mlabel(var) mlabsize(tiny) mlabposition(3) mlabgap(1)` |
| No `geom_text` | Do NOT add `mlabel` |

### Background and Output
| R | Stata |
|---|-------|
| `theme(panel.background = ..., plot.background = ...)` / `theme_minimal()` | `graphregion(color(white)) bgcolor(white)` |
| `ggsave("f.png", width = 8, height = 6, dpi = 300)` | `graph export "f.png", replace width(2400)` + optionally `xsize(8) ysize(6)` |
| (not needed) | `graph drop _all` |

### Stata legend position reference
```
11=upper-left   12=upper-center   1=upper-right
 9=center-left  10=center         2=center-right
 7=lower-left    8=lower-center   5=lower-right
ring(0) = inside plot area
```

## Known Traps

1. **One dataset in memory:** R can hold many data frames. Stata holds one. Use `preserve`/`restore` or `tempfile` when the R script works with multiple frames simultaneously.
2. **Pipe chains → sequential commands:** Each `%>%` step becomes a separate Stata line. Stata has no pipe.
3. **`summarise` vs `collapse`:** R `summarise` returns a new tibble. Stata `collapse` destroys the dataset in memory. Use `preserve` before `collapse` if the data is reused.
4. **Join diagnostics:** R joins silently succeed. Stata `merge` produces `_merge`. Always add `tab _merge` after merge, matching the R script's intent.
5. **`if_else` → `replace if`:** R's `mutate(y = if_else(cond, a, b))` translates to either `gen y = cond(...)` or `replace y = a if cond` depending on whether the variable exists.
6. **ggplot layers → Stata overlays:** R `geom_point() + geom_smooth()` → Stata `twoway (scatter ...) (lfit ...)`. Each geom becomes a parenthesized overlay.
7. **facets:** R `facet_wrap(~group)` → Stata `by(group)` or separate graph commands. Stata's `by()` is more limited than R facets.
8. **`esttab` not built-in:** Requires `ssc install estout`. Add a comment.
9. **`na.rm = TRUE`:** R aggregations with `na.rm` translate directly — Stata `mean()`, `sum()` etc. automatically ignore missing values.
