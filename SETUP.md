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

Edit `config_local.py` → set `DATA_ROOT` to your local data folder path:

```python
# Windows example:
DATA_ROOT = Path(r"C:\Users\YourName\Dropbox\your_project\data")

# Mac example:
DATA_ROOT = Path("/Users/YourName/Dropbox/your_project/data")
```

## 2. Stata Config

```bash
cp code/stata/config_local.do.template code/stata/config_local.do
```

Edit `config_local.do` → set both globals to your local paths:

```stata
global root      "C:/Users/YourName/path/to/your_project"
global data_root "C:/Users/YourName/Dropbox/your_project/data"
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

## 4. PDF Documentation Tools (optional — for Stata manual access)

Claude can read Stata's bundled PDF manuals when writing `.do` files.

```bash
pip install pdfplumber
```

`pdftotext` should already be available (bundled with Git for Windows via mingw64).
Verify: `pdftotext -v`. If missing, install poppler-utils for your OS.

## 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## 6. Verify Setup

```bash
python -c "import sys; sys.path.insert(0, 'code/py'); import config; print(config.DATA_RAW)"
```

Should print the path to your local `rawdata/` folder without errors.

## Important

Neither `config_local.py` nor `config_local.do` should ever appear in `git status`.
Both are listed in `.gitignore` — if they appear, do not commit them.
