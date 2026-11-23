# HOWTO — reuse review-doc

## 1. Data it reads and writes
| Source | Read / write | What |
|---|---|---|
| `docs/<app>/<doc>.md` | read | The document under review (header + sections) |
| `reference/rubric_<doc_type>.md` | read | Judgment criteria (`### Jn · title`) |
| `docs/<app>/reviews/` | write | `<doc>.review.json` and `.review.md` (overwritten each run; previous json used for "since last run") |
| the brief named in a PRD header | read | Must exist and be `status: approved` |

## 2. Point it at a new app
Nothing to change: it follows the document header (`app`, `doc_type`). Documents just need the header from `sdlc/ids.md`.

## 3. Values hard-coded today
Required sections per doc type (`REQUIRED` in `check_doc.py`) · blank markers (TBD, TODO, TBC, XXX, ???, [fill…]) ·
id formats (`A-nn`, `M-nn`, `REQ-nn`, `ST-nn`, `AC-nn.m`) · Ready = 0 Fix + every criterion answered.

## 4. Files that make it run
`tools/check_doc.py` · `reference/rubric_brief.md` · `reference/rubric_prd.md` · `tools/test_check_doc.py` + `examples/`.

## 5. Reuse it for a new document type
1. Add the type and its required sections to `REQUIRED` in `check_doc.py`, plus a `check_<type>()` for its rules.
2. Write `reference/rubric_<type>.md` with `### J1 · …` criteria.
3. Add a perfect and a broken example and their expected rule ids to `examples/expected.json`.
4. Run `tools/test_check_doc.py` until it passes.
