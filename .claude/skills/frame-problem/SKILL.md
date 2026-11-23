---
name: frame-problem
description: Stage 1 of the AI-SDLC. Interviews the product owner and reads the sources, then writes a one-page problem brief (who struggles, how it works today, evidence, one success metric with baseline and target, constraints, out of scope, assumptions with owner and date). Produces docs/APP/00-brief.md from the brief template. Use when starting a new app or feature, when asked to frame a problem, write a problem statement or brief, or for brownfield work on an existing system (from-existing mode). Only drafts; review-doc checks it and a person approves it at gate G1.
---

# frame-problem — one page that says what problem we're solving, for whom, and how we'll know

**Why it exists.** Most wasted builds trace back to a problem nobody wrote down, or a success measure that counts
activity instead of outcomes. This skill forces both onto one page before anyone writes a requirement.

## Inputs

- The idea, in the owner's words (one paragraph is enough).
- Sources: URLs, files, data. Every fact in the brief must trace to one of them or to the owner's own answer.
- **Brownfield (`from-existing`)**: when a system already exists, also read what's there (repo, docs, current
  process) and describe today's process from it before interviewing.

## What it produces

`docs/<app>/00-brief.md`, filled from `assets/brief_template.md`, with the header from `sdlc/ids.md`
(`doc_type: brief`, `status: draft`, `version: 1`, `sources:` listing everything used).

## The flow

1. **Read first.** Read every source you were given. Fetch public URLs. Note what each one actually says, with the
   exact wording for anything the brief will lean on.
2. **Say what you found, then ask.** One short paragraph: "I found X (from where). I still need Y and Z." Then
   interview the owner in **two rounds of 3–5 questions**, one round at a time:

   | Round | Sections | Push back when |
   |---|---|---|
   | 1 | Problem, who it affects, how it works today, evidence | The problem is "there's no tool for X"; the users are "everyone"; the cost has no number |
   | 2 | Success metric, constraints, out of scope, assumptions, risks | The metric counts activity (requests submitted, app launched); a baseline is guessed; out of scope lists things nobody wanted |

   Coach, don't interrogate: say in one line why a question matters when it isn't obvious. Accept "I don't know"
   gracefully: it becomes a `confirm — <who>, by <YYYY-MM-DD>` placeholder, and you ask who could know and by when.
3. **Write the brief** from the template. Keep it to one page. Quote sources; never paraphrase a policy.
4. **Self-check the structure** (not the quality): run
   `python3 .claude/skills/review-doc/tools/check_doc.py docs/<app>/00-brief.md` and fix every **rule** finding
   (missing sections, ids, blanks, placeholder format). Do not answer the judgment criteria yourself: that is
   `review-doc`'s job, run separately.
5. **Hand off.** Tell the owner the brief is ready for `review-doc`, and close with `_shared/run_report.py`
   (minutes, number of interview questions, how many facts are still `confirm —`).

## What it enforces

| Rule | How |
|---|---|
| One primary metric, measuring the outcome | Template has one `M-01` row; round 2 pushback |
| Every fact has a source | `sources:` header; the review rejects missing paths |
| Unknowns are owned, not hidden | `confirm — <who>, by <date>`; never a blank or TBD |
| Assumptions can be tested | Each `A-nn` has an owner and a confirm-by date |

## Honesty rules

- **Never guess.** A missing number, name, policy or date becomes a `confirm —` placeholder. A made-up baseline is
  worse than an honest blank because nobody checks it later.
- Never present a sample value as someone's official policy.
- If a source contradicts the owner, write both and flag it as an assumption to confirm.

## Anti-patterns

- ⛔ Jumping to features. A brief has no screens, no tech and no requirements.
- ⛔ Asking all ten questions at once.
- ⛔ Grading the brief yourself or calling it "ready". Only `review-doc` and the person at G1 can.
- ⛔ Writing `status: approved`. Only the owner's words at the gate change the status.

## Files

`assets/brief_template.md` · `HOWTO.md` · examples live with the checker (`review-doc/examples/*/00-brief.md`).
