# The AI-SDLC

**AI drafts, code checks, people decide.**

An AI-assisted software development lifecycle in six stages. AI agents run **skills** — packaged instructions that do
one job each. Every document and every line of code is drafted by one skill and checked by a different one, and a
person decides at every gate.

## Three principles

1. **A generator never grades its own work.** Each maker skill has a separate checker skill. The writer of a PRD is
   not the one who says it's ready; the writer of code is not the one who reviews it.
2. **The model extracts, code decides.** Wherever a verdict can be computed — coverage, traceability, policy, a score —
   a script computes it. The model's job is to read, draft and judge what a script can't, and even then it must
   quote the evidence, which a script checks.
3. **Nothing is done on a "success" message.** Every output is read back and traced from requirement to code. Every run
   ends with a report that says what it did **not** do, so nobody assumes coverage that isn't there.

## Six stages, five gates

| # | Stage | Maker skill | Checker | Gate (a person decides) | Output |
|---|---|---|---|---|---|
| 1 | Frame | `frame-problem` | `review-doc` | **G1** problem and metric agreed | `00-brief.md` |
| 2 | Define | `write-prd` | `review-doc` | **G2** PRD has no Fix findings | `01-prd.md` (requirements, stories, acceptance criteria) |
| 3 | Design + prototype | `log-decision`, `build-prototype` | `review-doc` | **G3** prototype walkthrough | ADRs, clickable prototype |
| 4 | Plan MVP 1 | `slice-mvp` | `review-doc` | **G4** scope locked | `03-mvp-slice.md` |
| 5 | Build | `build-story` | `review-code` | each story merged | code + tests, one story at a time |
| 6 | Release | — | `release-gate` | **G5** go / no-go | release report + trace matrix |

**Learn loop.** Every checker finding and every correction a person makes is appended to `sdlc/corrections.jsonl`.
When a correction repeats, it becomes a rule in the skill that should have prevented it, with the date and the quote
that caused it. The corrections are the backlog for the skills.

**Exception path: a risk spike.** When an unknown is external, slow to resolve and not a product question (a domain, a
certificate, a hosting choice), it may be tested before Stage 1. It always gets its own decision record and a throwaway
folder, and nothing in the PRD may rely on it. See [ADR-000](../docs/travel/adr/ADR-000-risk-spike-before-framing.md).

## How a skill is built

Every skill is a folder in `.claude/skills/<name>/`:

| File | Job |
|---|---|
| `SKILL.md` | The recipe the agent follows: when to run, the steps, what it enforces, honesty rules, anti-patterns, outputs |
| `HOWTO.md` | How to reuse it: data sources, how to point it at a new app, hard-coded values, files, copy steps |
| `assets/` | Templates the maker fills |
| `reference/` | Rubrics and depth loaded only when a step needs them |
| `tools/` | Deterministic scripts: the parts that must be exactly right |
| `examples/` | A `perfect` and a `broken` case per skill, used as its test fixtures |

## Ids and traceability

`REQ-nn` requirement → `ST-nn` story → `AC-nn.m` acceptance criterion → a test whose name cites the AC → a commit that
cites the story. `A-nn` assumption, `M-nn` metric, `ADR-nnn` decision. Full rules: [ids.md](ids.md).

## What gets measured

Per stage: time taken, Fix findings on the first draft vs the approved version, defects each checker caught vs
defects that escaped, how much the person edited each draft, acceptance-criteria coverage (N of M). Entries live in
`metrics/run_metrics.json`.
