# Ids, document headers and traceability

## Every lifecycle document starts with a header

```
---
doc_type: brief            # brief | prd | adr | mvp-slice
app: travel                # folder under docs/
version: 1                 # bump on every gate resubmission
status: draft              # draft | in-review | approved
owner: <person who decides at the gate>
brief: docs/travel/00-brief.md   # prd only: the approved brief it builds on
sources:                   # every source the content relies on (URL or repo path)
  - https://example.com/policy
---
```

`review-doc` refuses to review a document without this header.

## Id formats

| Id | Meaning | Format | Example |
|---|---|---|---|
| `A-nn` | Assumption to confirm | two digits | `A-03` |
| `M-nn` | Success metric | two digits | `M-01` |
| `REQ-nn` | Requirement | two digits | `REQ-07` |
| `ST-nn` | User story | two digits | `ST-12` |
| `AC-nn.m` | Acceptance criterion `m` of story `nn` | story number + index | `AC-12.2` |
| `ADR-nnn` | Architecture decision record | three digits | `ADR-004` |

- Ids are never reused, even after an item is deleted.
- A story names its requirement on a line `Requirement: REQ-nn`.
- An acceptance criterion is written as **Given … When … Then …**.
- A test's name starts with the AC id it proves (`AC-12.2 manager sees the policy flag`).
- A commit message cites the story (`ST-12: manager inbox`).

## Unknowns

A fact nobody has yet is written as `confirm — <who>, by <YYYY-MM-DD>`. It counts as answered for the gate, and becomes a
Check finding once its date has passed. `TBD`, `TODO`, `???` and empty cells count as blank and are Fix findings.
