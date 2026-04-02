# Git Backup and Restore Guide — Populism and Narratives

**Wyss Academy for Nature**
**Last updated:** 2026-03-24

> Quick reference for navigating project history, inspecting old versions, and restoring past states.
> See **COLLABORATION.md** for branching and PR workflows.

---

## Key Concepts

| Concept | What it is |
|---|---|
| **Working folder** | Your local copy of the project — where you edit files and run scripts |
| **Commit** | A saved snapshot of the project at a specific point in time |
| **Git history** | The ordered list of all commits (snapshots) ever made |
| **GitHub** | The online copy of the repository, synced via `git push` / `git pull` |

Your working folder:

```
C:\Users\RaffaellaIntinghero\OneDrive - Wyss Academy for Nature\populism_and_narratives
```

No commit = no saved version. Git only tracks changes that have been explicitly committed.

---

## 1. Save Your Work

All work happens on a personal branch (see **COLLABORATION.md** for naming conventions).
Never commit directly to `main`.

```bash
git add code/py/your_script.py          # stage specific files
git commit -m "describe what you changed"  # save a snapshot
git push origin HEAD                    # send your branch to GitHub
```

When your work is ready, open a Pull Request on GitHub to merge into `main`.

---

## 2. Update from GitHub

Before inspecting history or collaborator work, download the latest information:

```bash
git fetch origin
```

This updates your knowledge of remote commits **without modifying any local files**.

---

## 3. View Project History

### Full history with dates

```bash
git log --all --date=short --pretty=format:"%h  %ad  %d  %s"
```

Example output:

```
d684dd9  2026-03-23  (HEAD -> trump-2016-event-analysis)  Revise figures and tables
b86e9f0  2026-03-23                                       Clean up files for Trump election event
```

- `d684dd9` — commit ID (use this to reference a specific version)
- `2026-03-23` — date
- `(HEAD -> ...)` — current branch pointer
- Last column — commit message

### Filter by time window

```bash
git log --all --since="3 days ago"  --date=short --pretty=format:"%h  %ad  %d  %s"
git log --all --since="3 weeks ago" --date=short --pretty=format:"%h  %ad  %d  %s"
```

### Browse on GitHub

All commits and activity are also visible at:
https://github.com/raffaellaintinghero/Populism-and-Narratives/activity

### Are these all possible versions?

Yes, provided you ran `git fetch origin` first. Git shows every commit from all collaborators that has been pushed to GitHub. Unpushed local changes on another machine are not visible.

---

## 4. Inspect an Old Version (Safe — Read-Only)

To view the project as it existed at a past commit, create a temporary branch:

```bash
git switch -c temp-b86e9f0 b86e9f0
```

This switches your files to that old state **without affecting your working branch**. Your current work remains safe on its original branch.

When done inspecting, return to your working branch and clean up:

```bash
git switch raffaella/stata-event-study   # return to your personal branch
git branch -d temp-b86e9f0              # delete the temporary branch
```

---

## 5. Restore an Old Version (Destructive — Use with Caution)

A restore overwrites your current branch to match an old commit. **Newer tracked changes on this branch will be lost.**

Always create a safety branch first:

```bash
git branch backup-before-restore
```

Then reset:

```bash
git reset --hard b86e9f0
```

### When to use which

| Goal | Command | Risk level |
|---|---|---|
| Look at an old version | `git switch -c temp-name COMMIT` | Safe — nothing is overwritten |
| Restore to an old version | `git reset --hard COMMIT` | Destructive — creates safety branch first |

---

## 6. Can I Access a Collaborator's Historical Versions?

Yes, if the collaborator committed and pushed their changes:

```bash
git fetch origin
git log --all --date=short --pretty=format:"%h  %ad  %d  %s"
```

All pushed commits appear in the shared history regardless of who made them. Changes that were never committed are not recoverable by anyone.

---

## Quick Reference

| Task | Command |
|---|---|
| Update from GitHub | `git fetch origin` |
| View history with dates | `git log --all --date=short --pretty=format:"%h  %ad  %d  %s"` |
| Inspect old version (safe) | `git switch -c temp-COMMIT COMMIT` |
| Return to your working branch | `git switch yourname/branch-name` |
| Restore old version (destructive) | `git branch backup-before-restore` then `git reset --hard COMMIT` |
| Browse history online | Visit GitHub → Activity tab |
