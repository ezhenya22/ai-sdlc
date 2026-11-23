# Judgment criteria: product requirements (PRD)

The rule checks (`tools/check_doc.py`) already cover ids, the requirement → story → acceptance-criterion chain,
coverage (N of M), Given/When/Then shape, priorities, blanks and the link to an approved brief. These criteria cover
what code can't judge. Verdicts and quoting rules are the same as for the brief: a check or fix must quote the PRD word
for word and give paste-ready replacement text. Judge the document, never the product idea.

### J1 · Every requirement serves the brief's problem or metric
Fix when a Must requirement doesn't trace to anything in the brief. Check when a requirement exists because it is
technically interesting rather than because a user needs it.

### J2 · Requirements say what, not how
Check when a requirement names a technology, a screen layout or a vendor where a capability would do ("use a dropdown",
"store it in Postgres"). Design decisions belong in ADRs.

### J3 · Acceptance criteria are testable by someone who wasn't in the room
Fix when a criterion has no observable result ("Then it works", "Then the user is happy", "Then it is fast"). Every
Then must be something a test can see: a value, a state, a message, a time limit.

### J4 · The unhappy paths are covered
Check when a story only has the happy path. Look for: invalid input, a refusal, a timeout, a missing permission, and
what the user sees when the system can't help.

### J5 · Roles and permissions are explicit
Fix when a story lets someone see or change data and the PRD never says who may. Who can read, who can approve, who
can see what another person submitted.

### J6 · Numbers have a source or an owner
Check when a limit, threshold or policy value appears with no source and no `confirm —` placeholder. Fix when it is
presented as someone's official policy without a source.

### J7 · Non-goals protect the release
Check when non-goals are vague ("advanced features"). They should name specific things a stakeholder will ask for.

### J8 · Open questions are owned
Check when an open question has no owner and no date by which it must be answered.
