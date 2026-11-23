---
name: write-prd
description: Stage 2 of the AI-SDLC. From an approved problem brief, interviews the product owner and writes the PRD - users and jobs, requirements with priorities (REQ ids), user stories (ST ids) with acceptance criteria written as Given When Then (AC ids), non-functional requirements, non-goals, open questions and dependencies. Produces docs/APP/01-prd.md from the PRD template. Use when asked to write requirements, a PRD, user stories or acceptance criteria. Refuses to start until the brief is approved at G1. Only drafts; review-doc checks it and a person approves it at gate G2.
---

# write-prd — requirements, stories and tests-to-be, traceable from the first line

**Why it exists.** Every later stage leans on the PRD: the prototype must show every story, the build writes tests
from the acceptance criteria, and the release gate traces each requirement to code. So the PRD must be written in a
shape a script can trace: ids on everything, one requirement per story line, criteria a test can prove.

## Inputs

- `docs/<app>/00-brief.md` with `status: approved`. **If it isn't approved, stop** and say that G1 comes first.
- The sources the brief cites (re-read anything a requirement depends on).

## What it produces

`docs/<app>/01-prd.md` from `assets/prd_template.md`, header per `sdlc/ids.md` (`doc_type: prd`,
`brief: docs/<app>/00-brief.md`, `status: draft`).

## The flow

1. **Read the brief and its sources.** Summarize in one paragraph: the problem, the metric, the users, the
   constraints, and what's already out of scope.
2. **Interview in four rounds of 3–5 questions**, one round at a time:

   | Round | Covers | Push back when |
   |---|---|---|
   | 1 | Users and jobs; the one thing each role must be able to do in release 1 | A role has no job; "admin" appears with no reason |
   | 2 | Requirements and priorities (Must / Should / Could), each tracing to the brief | A Must doesn't serve the metric; a requirement names a technology or a screen |
   | 3 | Stories and acceptance criteria, including what happens when it goes wrong | A Then can't be observed ("it works"); only the happy path exists; nobody says who may see or change the data |
   | 4 | Non-functional (accessibility, privacy, security, performance), non-goals, open questions, dependencies | Non-goals are vague; a limit or policy value has no source; a question has no owner |

   "Without a date it's a hope." "Without a number it's a wish." Say why a question matters in one line. Unknowns
   become `confirm — <who>, by <YYYY-MM-DD>`.
3. **Write the PRD.** Ids: `REQ-nn`, `ST-nn`, `AC-nn.m` (the AC number matches its story). Every story has a line
   `Requirement: REQ-nn`. Every acceptance criterion is **Given … When … Then …** with an observable Then. Every
   requirement has at least one story, or moves to Non-goals.
4. **Self-check the structure**: run `check_doc.py` on the PRD and fix every **rule** finding until coverage reads N of N
   and there are no rule Fix findings. Leave the judgment criteria to `review-doc`.
5. **Hand off** to `review-doc`, and close with `_shared/run_report.py` (minutes, questions asked, requirements,
   stories, criteria, open `confirm —` items).

## What it enforces

| Rule | How |
|---|---|
| Nothing starts before G1 | Header `brief:` must point at an approved brief (checked by the review) |
| Traceable from the first line | Ids on every requirement, story and criterion; coverage N of M computed by script |
| Testable criteria | Given/When/Then shape checked by script; observability judged by review |
| What, not how | Designs and technology choices go to `log-decision` (ADRs) in Stage 3 |

## Honesty rules

- **Never guess**: no invented limits, policy values, user counts or dates. Placeholders with owners instead.
- A policy value goes in only with its source. A value you propose is labeled as a proposal, not as policy.
- If the owner's answer contradicts the brief, stop and say so: the brief may need to go back through G1.

## Anti-patterns

- ⛔ Writing the whole PRD from the brief without interviewing. The interview is where the decisions are.
- ⛔ Stories without a failure path.
- ⛔ Scoring, reviewing or approving your own PRD.
- ⛔ Requirements that are screens ("a dropdown"), vendors or databases.

## Files

`assets/prd_template.md` · `HOWTO.md` · examples live with the checker (`review-doc/examples/*/01-prd.md`).
