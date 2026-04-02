# Machine Setup Guide (One-Time per Collaborator)

## 0. Install Claude Code Plugin

```
claude plugin marketplace add EveryInc/compound-engineering-plugin
claude plugin install compound-engineering
```

## 1. Python Config

```bash
cp code/py/config_local.py.template code/py/config_local.py
```

Edit `config_local.py` → set `DATA_ROOT` to your Dropbox `data/` path:

```python
DATA_ROOT = Path(r"C:\Users\YourName\Dropbox\populism_and_narratives\data")
```

## 2. Stata Config

Edit `global root` in your `.do` files → your local repo path.

```bash
cp code/stata/config_local.do.template code/stata/config_local.do
```

Edit `config_local.do` → set `global data_root` to your Dropbox `data/` path:

```stata
global data_root "C:/Users/YourName/Dropbox/populism_and_narratives/data"
```

## 3. Stata on PATH

So that `stata` works from the terminal (required for Claude Code to run `.do` files).

**Prompt Claude Code with:**

> I want to put Stata onto my path on my bashrc or zshrc, whichever is most
> relevant for me. Look through my file system, find the most recent Stata
> version, and get it onto my bashrc/zshrc.

**Windows gotcha — PowerShell profile location:**

PowerShell's profile path depends on where your Documents folder lives. If
Documents is redirected to OneDrive, the profile must go there, not the default
`C:\Users\<you>\Documents`. Claude should run
`$PROFILE | Format-List -Force` in PowerShell to find the correct path.

**Verify:** Close and reopen terminal, then run `stata`. Stata should launch.

## 4. PDF Documentation Tools

Claude reads Stata's bundled PDF manuals when writing `.do` files.

```bash
pip install pdfplumber
```

`pdftotext` should already be available (bundled with Git for Windows via mingw64).
Verify: `pdftotext -v`. If missing, install poppler-utils for your OS.

## 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## 6. Verify Pipeline

```bash
python code/py/01_data_prep.py
```

Should complete without errors. Check that files appear in your Dropbox
`populism_and_narratives/data/processed/` folder.

## Important

Neither `config_local.py` nor `config_local.do` should ever appear in `git status`.
