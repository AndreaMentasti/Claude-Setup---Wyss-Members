# Onboarding Guide — Populism and Narratives
**Wyss Academy for Nature**

> About **20 minutes**. Claude does most of the work for you.
> Before starting, make sure you have received the **Dropbox folder** invite and **GitHub repository** access.

---

## Step 1 — Sync Dropbox

Accept the Dropbox invite and make sure the folder syncs to your computer.

> **Windows:** Open Dropbox → find `populism_and_narratives` → right-click → **Make available offline**
> **Mac:** Same — right-click the folder → **Make available offline**

Wait until the sync is fully complete (the green checkmark appears on the folder icon).

---

## Step 2 — Install Git

Git is required for version control. Check if it is already installed by opening a terminal and running:

```
git --version
```

- **If you see a version number** (e.g. `git version 2.43.0`): you are good, skip to Step 3.
- **If you get an error**: download and install Git from https://git-scm.com/downloads
  - Windows: run the installer with all defaults. Make sure **"Git from the command line and also from 3rd-party software"** is selected.
  - Mac: install via Homebrew (`brew install git`) or accept the prompt when Xcode command line tools are offered.

After installing, close and reopen your terminal and confirm `git --version` works.

---

## Step 3 — Install Claude Code Desktop

Download and install the Claude Code desktop app:
👉 https://claude.ai/download

Open it and sign in with your Anthropic account.

---

## Step 4 — Clone the GitHub Repository

1. Download **GitHub Desktop**: https://desktop.github.com → install with defaults
2. Sign in with your GitHub account
3. **File → Clone repository** → find `Populism-and-Narratives` → click **Clone**

Note the folder path shown at the bottom (you will need it in Step 6).

---

## Step 5 — Open the project in Claude Code

Open Claude Code → **File → Open Folder** → select the `Populism-and-Narratives` folder you just cloned.

---

## Step 6 — Let Claude set everything up

Paste the prompt below into Claude Code. **Before hitting Enter**, fill in the three bracketed fields at the top with your own information:

```
I am a new collaborator on the Populism and Narratives project. Here is my machine:
- OS: [Windows / Mac]
- My Dropbox data folder: [e.g. C:\Users\YourName\Dropbox\populism_and_narratives\data]
- Stata version and location: [e.g. Stata 17 at C:\Program Files\Stata17]

Please set up my environment completely. Do all of the following:

1. Read CLAUDE.md to understand the project structure and conventions.

2. Create code/py/config_local.py from code/py/config_local.py.template.
   Set DATA_ROOT to my Dropbox data path above.

3. Create code/stata/config_local.do from code/stata/config_local.do.template.
   Set $data_root to my Dropbox data path, and $root to the current repo folder.

4. Check if Python is installed (run: python --version).
   If Python is NOT installed, tell me to download Python 3.13 from
   https://www.python.org/downloads — tick "Add Python to PATH" during install —
   then come back and paste this prompt again.
   If Python IS installed, run these three commands:
   pip install -r requirements.txt
   pip install pdfplumber
   python -m spacy download en_core_web_sm

5. On Windows: check if 'python3' works in the terminal. If not, create a copy
   or alias so that 'python3' points to 'python' (the project hooks use python3).

6. Add Stata to my system PATH so I can run 'stata' from the terminal.
   On Windows with PowerShell: first run "$PROFILE | Format-List -Force" to find
   the correct profile path before modifying it.

7. Set my git identity. Ask me for my full name and email, then run:
   git config --global user.name "My Name"
   git config --global user.email "my.email@institution.org"

8. Install the Compound Engineering plugin (enables /commit and other commands):
   claude plugin marketplace add EveryInc/compound-engineering-plugin

9. Create .claude/state/personal-memory.md with my OS, paths, and Stata version.

10. Verify everything:
    - cd into code/py/ and run: python -c "import config; print(config.DATA_RAW)"
    - Confirm the path points to my Dropbox rawdata folder
    - Run: stata -e version (check Stata is on PATH)
    - Report any errors.
```

Claude will ask a couple of questions (your name, email). Just answer them — Claude handles the rest.

> **If Python was not installed:** Claude will tell you. Download it from https://www.python.org/downloads, restart Claude Code, and paste the prompt again.

---

## Done!

Your environment is fully configured. From now on, open Claude Code, open the project folder, and start working.

---

## Daily Workflow

You never need to type git commands. Use these prompts in Claude Code:

| What you want | Prompt |
|---|---|
| Start working on something new | `Pull the latest from main and create a branch called [yourname/description].` |
| Save and share your work | `/commit` |
| Run a Stata do-file | `Run code/stata/1-analysis_main_tweets.do and show me any errors from the log.` |
| Run a Python script | `Run code/py/01_data_prep.py and tell me if it completes successfully.` |
| Fix an error | `I got this error: [paste error]. Fix it.` |
| See what changed | `Show me what I changed since the last commit.` |
| Review code before committing | `/review-stata code/stata/1-analysis_main_tweets.do` |

---

## If something goes wrong

Paste the error into Claude Code:

```
I got this error during setup: [paste the full error message here].
Please diagnose and fix it.
```
