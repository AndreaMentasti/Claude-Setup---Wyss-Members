# Fix All Path Portability Issues

## Goal
Make the repo fully portable — any collaborator clones, creates config_local files per SETUP.md, and everything works.

## Changes

### 1. Stata: Fix config_local.do loading (5 files)
All .do files hardcode `global root` to Raffaella's machine path, then try `do "$root/code/stata/config_local.do"` — this fails on any other machine. Fix: use relative path `do "code/stata/config_local.do"` (scripts run from repo root per docs).

Files: `0-data_prep.do`, `1-analysis_main_tweets.do`, `1-analysis_main_tweets_Andre.do`, `1-analysis_main_tweets_visibrain.do`, `A_analysis_politicians_tweets.do`

### 2. Stata: Fix 13 hardcoded absolute paths in A_analysis_politicians_tweets.do
Lines referencing `C:\Users\AndreaMentasti\Dropbox\polarizing-narratives\...` → replace with `$DIR/data/processed/politicians_tweets/...`

### 3. Stata: Fix bare relative output paths (3 files)
`"output\tables\..."` and `"output\figures\..."` → `"$root/output/tables/..."` and `"$root/output/figures/..."`. Also fix backslashes to forward slashes.

Files: `1-analysis_main_tweets.do`, `1-analysis_main_tweets_Andre.do`, `1-analysis_main_tweets_visibrain.do`

### 4. Stata: Backslash cleanup in A_analysis_politicians_tweets.do
`$DIR\data\...` → `$DIR/data/...` throughout (~30 instances)

### 5. Python: Fix GPT_classification_check.py
Hardcoded `C:\Users\RaffaellaIntinghero\Dropbox\polarizing-narratives` → use `config_path.change_paths()`. Add comment noting this references external project data.

### 6. Python: Fix main_visibrain_exploratory_analysis.py
`Path.home() / "Dropbox" / "climate_nature_narratives"` and `Path.home() / "Dropbox" / "polarizing-narratives"` → use `config_path.change_paths()`. Add comment noting cross-project data references.

### 7. Fix stata-reviewer.md agent doc
`$root/Figures/` → `$root/output/figures/` and `$root/output/tables/`

## Verification
- Grep for `RaffaellaIntinghero`, `AndreaMentasti`, `polarizing-narratives`, `climate_nature_narratives`, `Path.home()` in code/ → zero matches
- config_local files NOT in git status
