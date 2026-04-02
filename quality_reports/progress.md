# Project Progress & To-Do List

Last updated: 2026-03-18
Source: Christchurch seminar feedback (2026-03-08) + PI email + `Feedback_and_ToDos_Christchurch_2026_03_08.tex` on Overleaf

---

## Priority: Causality / Identification (from seminar feedback)

These were the main audience comments. Most have concrete empirical actions.

- [ ] **C1 — DiD controls moving the wrong way**
  - Plot weekly villain share for US + each control (AU/CA/IE/NZ/UK), with event date lines
  - Compute pre/post change per control country; check if any control has declining villain share
  - Leave-one-out robustness: re-estimate DiD dropping one control at a time

- [ ] **C2 — Election-cycle confound**
  - Assemble election calendar for AU/CA/IE/NZ/UK; run event study of role shares around election weeks
  - Run US 2016 vs 2020 benchmark (same event window) to characterize generic US election dynamics
  - Consider adding weeks-to-election controls or DDD with `ElectionPeriod` indicator

- [ ] **C3 — Framing: avoid overclaiming**
  - Add explicit framing line to intro + slides: we test whether populist entrepreneurs *accelerate* the shift, not that they solely caused it

- [ ] **C4 — Theory: why do populists win if others adapt?**
  - Write 2-page literature memo on accommodation/adaptation, transgressive style, agenda competition
  - Empirical check: track villain share over time for Trump, other GOP elites, Democrats — does opponents' villain share rise post-2015?

- [ ] **C5 — Slide metadata improvements**
  - Every plot: add time window, data source, clear speaker vs. target labels
  - "Villain share among Republicans" slide: add sample period, footnote on tweet source + coding, legend clarification

- [ ] **C6 — Alternative treatment: election (not nomination) as event**
  - Run US vs controls event study around Nov 2016 with tight window (±8 or ±12 weeks)
  - Consider donut around nomination to avoid overlapping treatments

- [ ] **C9 — Climate topic justification slide**
  - Add argument: climate is slow-moving → fewer short-run real-world shocks that mechanically shift discourse
  - Add: topic restriction is needed for reliable measurement (avoid cross-topic mixing)

---

## Data Extensions

- [ ] **C7 — Citizen discourse beyond Twitter**
  - Reddit (first priority): define climate-policy corpus (subreddits + keywords), collect posts/comments 2013–2020, run CRNF coding, event studies + placebo topics
  - YouTube (optional): channel/keyword sampling, weekly role shares + engagement-weighted measures

- [ ] **C8 — Trump full tweet universe + spillover**
  - Acquire complete Trump tweet dataset; build weekly villain intensity panel
  - Regress climate villain share on lagged Trump villain intensity + controls
  - Add placebo topics

- [ ] **C10 — User fixed effects (nice-to-have)**
  - If stable user IDs available: estimate user-FE models (tweet-level or user-week panel)
  - Balanced-panel robustness: users observed both pre & post
  - Report as robustness/appendix if data quality permits

- [ ] **VisiBrain dataset** — one individual user with repeat observations
  - Explore whether user FE is feasible with this dataset
  - Decide: does it add enough to be worth the effort?

- [ ] **Absolute numbers vs shares**
  - Sit down with Matteo: decompose what drives pre/post changes — new users entering Twitter, users entering climate discourse, or within-user style change?
  - Descriptive analysis: how did volume (not just share) evolve for left/right/no-revealed-partisanship users pre/post nomination?

---

## New Data Sources

- [ ] **X (Twitter) researcher access**
  - Check current cost and application requirements for researcher account
  - Document what justification is needed; prepare application materials
  - Goal: understand feasibility for future data acquisition

- [ ] **Other politicians / other countries**
  - If we can find datasets with politicians' behavior in other settings, this adds external validity
  - Question to resolve: how much of this belongs in this paper vs a follow-up?

- [ ] **TV and newspapers**
  - Test whether villain share rises in TV/news post-Trump nomination (same prediction, different medium)
  - Advantage: no need to zoom in on climate change; broader coverage
  - Reframe: journalists ≠ politicians, so this adds a distinct "elite discourse" layer

---

## Experiment (pending IRB)

- [ ] IRB approval expected in ~2–4 weeks; start design now
- [ ] Core design: expose subjects to narratives (villain-victim vs hero-hero structure, or real political narratives)
  - Hypotheses: left-partisans, right-partisans, and moderates/swing voters react differently
  - Expect symmetric reactions to populism from both camps
  - Key open question: what do moderates do — disengage, or show heterogeneous reactions?
  - Design should allow capturing disengagement (dropout from discourse) as an outcome

---

## Project Organization

- [ ] **GitHub ↔ Overleaf ↔ Dropbox sync** — PI suggestion
  - Evaluate: sync Overleaf project to GitHub; sync that GitHub folder with local Dropbox
  - Goal: allow individual agent-assisted work with git commits, avoid conflicts
  - Discuss as a team and agree on workflow before implementing

- [ ] Review shared results that were posted (not yet reviewed by PI)
- [ ] Review `Feedback_and_ToDos_Christchurch_2026_03_08.tex` on Overleaf — cross-check against this list and add any missing items
- [ ] Review slides added by PI post-presentation; give feedback on story and transitions

---

## Completed
*(move items here when done)*
