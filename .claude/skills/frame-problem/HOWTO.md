# HOWTO — reuse frame-problem

## 1. Data it reads and writes
| Source | Read / write | What |
|---|---|---|
| The owner's idea and answers | read (interview) | Problem, users, today's process, metric, constraints |
| Sources the owner names (URLs, files) | read | Evidence and exact policy wording |
| `assets/brief_template.md` | read | Shape of the brief |
| `docs/<app>/00-brief.md` | write | The brief, `status: draft` |

## 2. Point it at a new app
Give it the idea, the owner's name and the sources. It creates `docs/<app>/` from the app name.

## 3. Values hard-coded today
Two interview rounds of 3–5 questions · one primary metric (`M-01`) · placeholder format `confirm — <who>, by <YYYY-MM-DD>`.

## 4. Files that make it run
`SKILL.md` · `assets/brief_template.md` · the checker `../review-doc/tools/check_doc.py` (structure self-check).

## 5. Reuse it elsewhere
Change the template's sections and the matching `REQUIRED['brief']` list in `check_doc.py` together, then rerun the
review-doc self-test. For brownfield work, list the existing system's docs and repo under `sources:`.
