# Collaboration Guide — Populism and Narratives

**Team:** Andrea Mentasti & Raffaella Intinghero
**Repo:** https://github.com/raffaellaintinghero/Populism-and-Narratives
**Last updated:** 2026-03-17

---

## Setup (Once Per Machine)

1. Clone the repo:
   ```bash
   git clone https://github.com/raffaellaintinghero/Populism-and-Narratives.git
   cd Populism-and-Narratives
   ```

2. Create your local config files (gitignored — never committed):
   ```bash
   cp code/py/config_local.py.template code/py/config_local.py
   cp code/stata/config_local.do.template code/stata/config_local.do
   ```
   Edit each file and set the path to your local Dropbox `data/` folder.

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your git identity (once per machine):
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@wyssacademy.org"
   ```

5. Verify everything works:
   ```bash
   python code/py/01_data_prep.py
   ```

See **SETUP.md** for full details (Stata on PATH, PDF tools, Claude Code plugin).

---

## Daily Workflow

### Start of every work session
```bash
git checkout main
git pull origin main          # get latest changes from GitHub
git checkout -b yourname/short-description-of-work
```

### While working
Commit often — small, logical chunks:
```bash
git add code/py/your_script.py          # add specific files (never git add .)
git commit -m "short description of what you did"
```

### End of work session — push and open PR
```bash
git push origin yourname/short-description-of-work
```
Then go to GitHub and open a Pull Request to merge into `main`.

### After your PR is merged
```bash
git checkout main
git pull origin main
git branch -d yourname/short-description-of-work          # delete branch locally
git push origin --delete yourname/short-description-of-work  # delete from GitHub
```

---

## Branch Naming

Use your name as a prefix so it's always clear who owns the branch:

```
andrea/openai-stage3-fix
andrea/visibrain-cleanup
raffaella/stata-event-study
raffaella/politician-analysis
```

---

## Key Commands Cheat Sheet

| What you want to do | Command |
|---|---|
| See what branch you're on | `git branch` |
| See all branches (local + remote) | `git branch -a` |
| See what files you changed | `git status` |
| See the actual changes | `git diff` |
| Pull latest from GitHub | `git pull origin main` |
| Create a new branch | `git checkout -b yourname/feature` |
| Switch to an existing branch | `git checkout branch-name` |
| Stage a specific file | `git add code/py/script.py` |
| Commit staged files | `git commit -m "description"` |
| Push your branch to GitHub | `git push origin branch-name` |
| Delete branch locally | `git branch -d branch-name` |
| Delete branch from GitHub | `git push origin --delete branch-name` |
| See recent commits | `git log --oneline -10` |

---

## What Is and Isn't in GitHub

| In GitHub (shared via git) | NOT in GitHub (local/Dropbox) |
|---|---|
| All code (`code/py/`, `code/stata/`, `code/prompts/`) | `code/py/config_local.py` |
| Output figures and tables (`output/`) | `code/stata/config_local.do` |
| Rules, skills, agents (`.claude/`) | `.env` (API keys) |
| `MEMORY.md`, `CLAUDE.md`, `SETUP.md` | `.claude/state/` (personal memory) |
| `quality_reports/`, `templates/` | All data in Dropbox (`data/rawdata/`, `data/processed/`) |

Data lives in Dropbox and syncs independently — it never goes through git.

---

## Avoiding Conflicts

- **Always `git pull origin main` before creating a new branch.** Starting from stale
  `main` is the main source of conflicts.
- **Never push directly to `main`.** Always use branches + PRs.
- **Coordinate verbally** before editing shared config files like `CLAUDE.md` or
  `.claude/rules/project-rules.md` — these are high-collision areas.
- **One person merges at a time.** If both of you have open PRs, merge one, then the
  other person pulls `main` and rebases or resolves conflicts before merging theirs.

---

## If You Get a Merge Conflict

1. Git will tell you which files conflict. Open them — you'll see markers like:
   ```
   <<<<<<< HEAD
   your version
   =======
   the other version
   >>>>>>> origin/main
   ```
2. Edit the file to keep the right version (or combine both).
3. Remove the conflict markers.
4. Stage and commit:
   ```bash
   git add the-conflicted-file.py
   git commit -m "resolve merge conflict in the-conflicted-file.py"
   ```

---

## After Pulling: Folder Deletion Issues (Windows)

If a PR deleted or renamed a folder, `git pull` may warn:
```
Deletion of directory 'FolderName' failed. Should I try again? (y/n)
```
This happens when the folder contains local generated files git doesn't track (figures,
tables). Just answer `n` and manually delete the folder in Windows Explorer. Your tracked
files are already updated — only the empty folder shell remains.

---

## Starting a New Claude Code Session

Claude Code loads `CLAUDE.md` and all rules once at session start. If you pull changes
that modify `.claude/` files or `CLAUDE.md` mid-session, **start a new session** to pick
them up.
