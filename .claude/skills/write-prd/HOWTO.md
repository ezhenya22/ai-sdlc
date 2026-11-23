# HOWTO — reuse write-prd

## 1. Data it reads and writes
| Source | Read / write | What |
|---|---|---|
| `docs/<app>/00-brief.md` | read | Must be `status: approved` (G1 passed) |
| The owner's answers | read (interview) | Requirements, priorities, stories, criteria, non-goals |
| `assets/prd_template.md` | read | Shape of the PRD |
| `docs/<app>/01-prd.md` | write | The PRD, `status: draft` |

## 2. Point it at a new app
Approve that app's brief first; the PRD header's `brief:` line points at it.

## 3. Values hard-coded today
Four interview rounds of 3–5 questions · priorities Must / Should / Could · ids `REQ-nn`, `ST-nn`, `AC-nn.m` ·
acceptance criteria as Given / When / Then · non-functional requirements must cover accessibility, privacy and security.

## 4. Files that make it run
`SKILL.md` · `assets/prd_template.md` · the checker `../review-doc/tools/check_doc.py` (structure self-check).

## 5. Reuse it elsewhere
Keep the id formats (later stages trace on them). Change sections only together with `REQUIRED['prd']` in
`check_doc.py`, then rerun the review-doc self-test.
