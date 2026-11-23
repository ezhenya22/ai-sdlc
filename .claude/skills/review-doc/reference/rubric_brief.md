# Judgment criteria: problem brief

The rule checks (`tools/check_doc.py`) already cover structure, ids, blanks, placeholders and metric fields. These
criteria cover what code can't judge. For each one, give a verdict:

- **pass** — meets it; no quote needed.
- **check** — worth a second look before the gate.
- **fix** — the gate should send it back.

Every check or fix **must quote the document word for word** (the script rejects a quote it can't find) and must give
paste-ready replacement text in `suggested`. Judge the document, never the bet: whether the idea is good is the gate
owner's call, not the reviewer's.

### J1 · The problem is about people, not a missing feature
Fix when the problem is phrased as the absence of a solution ("there is no app for…"). It must name who struggles, with
what, and what it costs them.

### J2 · The evidence supports the size of the problem
Check when the only number is unsourced or the source doesn't say what the brief claims. Fix when the brief claims a
cost (time, money, errors) with nothing behind it and no `confirm —` placeholder.

### J3 · Today's process is concrete
Check when "how it works today" could describe any company. It should name the steps, the tools (email, a spreadsheet)
and where it breaks.

### J4 · The success metric measures the outcome, not the activity
Fix when the metric counts output ("number of requests submitted", "app launched"). It should move when the problem
gets smaller: time, errors, rework, satisfaction.

### J5 · Out of scope is a real decision
Check when out-of-scope items are things nobody would assume were in. It should name the tempting neighbors that were
deliberately left out.

### J6 · The riskiest assumption is visible
Check when the assumption most likely to sink the effort isn't listed, or is listed without an owner who can answer it.
