# AI-SDLC — project rules for Claude Code

This repo is an **AI-assisted software development lifecycle** (the stages, the gates and the skills that power it),
plus one app taken through it from definition → prototype → MVP 1: a business-travel request app. It was built for a
Walmart craft-demo assignment. Private working notes live in `CLAUDE.local.md` (not in git).

## The thesis — every artifact serves it
**"AI drafts, code checks, people decide."**
1. **A generator never grades its own work.** Every maker skill has a separate checker.
2. **The model extracts, code decides.** Scores, policy checks and coverage are computed, not judged.
3. **Nothing is done on a 2xx.** Every output is read back and traced; every run says what it did NOT do.

## Lifecycle: 6 stages, 5 human gates, 9 skills (6 makers, 3 checkers)
| Stage | Maker | Checker | Gate |
|---|---|---|---|
| 1 Frame | `frame-problem` | `review-doc` | G1 problem + metric agreed |
| 2 Define | `write-prd` | `review-doc` | G2 PRD has 0 Fix findings |
| 3 Design + prototype | `log-decision`, `build-prototype` | `review-doc` | G3 prototype walkthrough |
| 4 Plan MVP 1 | `slice-mvp` | `review-doc` | G4 scope locked |
| 5 Build | `build-story` | `review-code` (fresh context, never the author) | each story merged |
| 6 Release | — | `release-gate` | G5 go / no-go |

Learn loop: checker findings and human corrections append to `sdlc/corrections.jsonl`; repeated ones become skill rules,
each with its date and the quote that caused it. **A human decides at every gate.** Never mark a gate passed without the
product owner's words in the session.

Exception path: a **risk spike** (see `docs/travel/adr/ADR-000-risk-spike-before-framing.md`) is allowed when an unknown is
external, slow to resolve and not a product question. It always gets its own ADR and a throwaway `spike/` folder.

## Hard rules
- **Never guess.** A missing fact becomes `confirm — <who>, by <date>`. Never invent a number, a name, a policy or a date.
- **Policy provenance.** Every rule in `policy/rules.yaml` carries a source URL + section + exact quote from Walmart's
  public Global Travel and Expenses Guidelines, or the label `SAMPLE: configurable, not Walmart policy`.
  `scripts/check-sources.ts` fails the build otherwise.
- **Brand.** Walmart palette colors only as design tokens. No Walmart logo, wordmark or Spark. The Everyday Sans
  typeface is licensed to Walmart only: never embed or install it; DM Sans stands in. Every page footer says
  "Independent work, not affiliated with Walmart."
- **No employer material.** Patterns are written from scratch; nothing is copied from any employer's systems, people,
  ids or internal terms.
- **Demo data only.** No real names or personal data in seeds, logs, screenshots or tests.
- **Secrets** live in `.env` (gitignored) or Supabase / GitHub secrets. Never in code, logs or chat. Never print a token.
- **The model prints, a trusted script writes** for anything that feeds a score, a trace or a gate.
- **Ids:** `REQ-nn` requirement · `ST-nn` story · `AC-nn.m` acceptance criterion · `ADR-nnn` decision · test names cite
  their `AC` id · commits cite `ST-nn`. `scripts/trace.ts` must report N of N.
- **Every task closes with a run report** in `docs/travel/run-reports/` that includes "What I did NOT do", and appends one
  entry to `metrics/run_metrics.json` (stage, skill, minutes, Fix first/final, defects caught, tokens if known).
- **Session logs:** each stage runs in a fresh Claude Code session started in this folder. Raw JSONL → `logs/raw/`
  (gitignored) → `scripts/scrub-logs.ts` → `logs/excerpts/`. A human reads every excerpt before it is committed.

## Writing
US spelling. Plain sentences, answer first. Concrete numbers with their source. Dates, never build clock times.

## Stack
React + TypeScript + Vite PWA (`app/`) · Supabase: Postgres + row-level security + Realtime + anonymous sign-in + one
Edge Function that calls Claude Haiku for extraction only (`supabase/`) · Astro site (`site/`) that reads
`.claude/skills/` and `docs/` in place · GitHub Pages at eugenetarasov.com/ai-sdlc · Vitest, Playwright (mobile
viewports), axe.

## Layout
`sdlc/` lifecycle docs · `.claude/skills/` the 9 skills (SKILL.md, HOWTO.md, reference/, tools/, examples/) ·
`docs/travel/`, `docs/shift-swap/` artifacts · `policy/` · `app/` · `supabase/` · `site/` · `scripts/` · `metrics/` · `logs/`.
