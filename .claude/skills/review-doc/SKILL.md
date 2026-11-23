---
name: review-doc
description: Checks a lifecycle document (problem brief or PRD) before its gate and grades every finding Fix, Check or Note. Runs deterministic rule checks in code, then judgment criteria the model answers with a word-for-word quote that the script verifies. Produces reviews/DOC.review.md and .review.json with coverage and a since-last-run count. Use when asked to review, check, validate or gate a brief or PRD, or before G1 or G2. Never edits the document and never writes it; use frame-problem or write-prd to change it.
---

# review-doc — the checker for every lifecycle document

**Why it exists.** A generator never grades its own work. The skill that wrote a brief or a PRD is the worst judge of
it, so a separate checker decides whether it is ready for its gate. Anything a script can decide, a script decides; the
model only judges what code can't, and must prove each finding with a quote.

## Commands

```bash
python3 .claude/skills/review-doc/tools/check_doc.py docs/<app>/<doc>.md                      # rule checks only
python3 .claude/skills/review-doc/tools/check_doc.py docs/<app>/<doc>.md --stub > /tmp/j.json # criteria to answer
python3 .claude/skills/review-doc/tools/check_doc.py docs/<app>/<doc>.md --judgments /tmp/j.json
python3 .claude/skills/review-doc/tools/test_check_doc.py                                     # self-test on fixtures
```

## What it produces

| File | Contents |
|---|---|
| `docs/<app>/reviews/<doc>.rules.md` / `.rules.json` | Rule checks only (step 1, or a maker's self-check). Status is `Rules pass` or `Needs work`, never `Ready`. Never touches the judged review |
| `docs/<app>/reviews/<doc>.review.md` | Written only by a judged run (`--judgments`). Status (Ready / Needs work), counts, coverage, findings grouped Fix → Check → Note, each with location, quote and paste-ready suggestion |
| `docs/<app>/reviews/<doc>.review.json` | The same, machine-readable (`schema: review-doc/1`), stable finding ids, `since_last_run` new/resolved against the previous judged review |

## The flow — do not reorder, do not skip

1. **Rule checks.** Run `check_doc.py <doc>`. It reads the header (`doc_type` decides which rules apply) and checks
   structure, ids, blanks (`TBD` counts as blank), `confirm —` placeholders, metric fields, the requirement → story →
   acceptance-criterion chain and coverage (N of M). Exit 2 means the document can't be read: stop and say why.
2. **Get the criteria.** Run with `--stub` and read `reference/rubric_<doc_type>.md` in full.
3. **Judge.** Read the whole document once, then answer every criterion. For each one:
   - `pass` needs no quote.
   - `check` or `fix` needs `quote` (copied **word for word** from the document), `finding` (one sentence: what is
     wrong and why it matters at the gate) and `suggested` (paste-ready replacement text).
   - Print the judgments as JSON. Write them to a temp file with a script, never by hand-editing the review files.
4. **Merge.** Run with `--judgments <file>`. The script rejects any finding whose quote it can't find in the document,
   any unknown criterion id and any bad verdict. **A rejected judgment is re-asked, never dropped**: fix the quote or
   change the verdict, then merge again until `rejected` is 0 and every criterion is answered.
5. **Report.** Tell the person at the gate, in this order: the status, the Fix count, the top three Fix findings in one
   line each, and the path to `.review.md`. Then close with `_shared/run_report.py`.

## What it enforces

| Rule | How |
|---|---|
| Ready means zero Fix findings and every criterion answered | `status` is computed by the script, not stated by the model |
| A finding must be real | Quote verified against the document text; invented quotes are rejected |
| Coverage is counted, not estimated | Requirements with a story, N of M, from the document's own ids |
| Same document, same findings | Rule checks are deterministic; finding ids are stable hashes |
| Progress is visible | `since_last_run`: findings new vs resolved since the previous judged review |
| A self-check can't erase a review | Rule-only runs write `.rules.*`; only judged runs write `.review.*` (added 2026-11-23 after "the tool lost the previous review": a rule-only run wiped the v1 travel-brief review) |

## Honesty rules

- **Judge the document, never the bet.** Whether the idea is worth building is the gate owner's decision.
- Never soften a Fix to a Check to get a document through. Never raise a Check to a Fix to look thorough.
- If a criterion doesn't apply, say `pass` and explain in `finding` why it doesn't apply.
- Never edit the document under review. The fix goes back to its maker skill or its author.

## Anti-patterns

- ⛔ Summarizing findings in chat instead of merging them through the script. Chat is not the record.
- ⛔ Paraphrasing in `quote`. The script will reject it, and it should.
- ⛔ Declaring "Ready" before the merge reports 0 rejected and 0 missing.
- ⛔ Reviewing a document with no header. Send it back to its maker skill.

## Files

`tools/check_doc.py` (rules + merge + output) · `tools/test_check_doc.py` (fixtures self-test) ·
`reference/rubric_brief.md`, `reference/rubric_prd.md` (judgment criteria) · `examples/perfect/`, `examples/broken/`,
`examples/expected.json` (fixtures: a meeting-room booking app, invented for testing).
