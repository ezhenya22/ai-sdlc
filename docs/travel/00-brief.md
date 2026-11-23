---
doc_type: brief
app: travel
version: 5
status: approved
owner: Eugene Tarasov (product owner)
sources:
  - https://one.walmart.com/content/dam/gts-spark/home/company/policies/policies-documents/travel/Global-Travel-and-Expenses-Guidelines.pdf
  - https://wlfc.walmart.com/content/dam/gts-spark/home/company/policies/policies-documents/travel/Global-Travel-and-Expenses-Guidelines.pdf
---

# Business travel requests: problem brief

## Problem
Associates who travel for work must follow their country's approval rules; even where approval is not required, the
guidelines call it "the best practice" to inform their manager before booking. The scenario premise is that "today it all runs on email and spreadsheets", so a request can
sit in an inbox while, in the policy's words, "airfare increases significantly closer to the travel date". Nobody has
one trusted record of a trip: the traveler can't see where a request stands, the manager has no history of what they
approved and why, and org leaders can't see their org's travel without collecting it by hand.

## Who it affects
- Traveling associates in a corporate team (primary): they wait, and they carry the risk of booking out of policy. How
  many and how often: confirm — the panel (asked by Eugene Tarasov in the walkthrough), by 2026-12-04.
- Their managers (secondary): they approve or are notified, and they own the "economical fare" discussion with the traveler.
  How many: confirm — the panel (asked by Eugene Tarasov in the walkthrough), by 2026-12-04.
- Org leadership (third): each org sets its own approval rule (A-07) and, we assume, needs org-level reporting on its
  travel (A-08).
  Number of orgs in the first rollout: confirm — the panel (asked by Eugene Tarasov in the walkthrough), by 2026-12-04.

## How it works today
Assumed from the scenario premise, not observed (A-01):
1. The traveler emails their manager: where, when, why, rough cost.
2. The manager answers when they get to it, and the traveler follows up.
3. The traveler or a team admin adds a row to a team spreadsheet (trip, dates, approved yes/no).
4. The traveler books through "the agency approved by Global Travel".

Where it breaks: the request waits while fares rise; nobody checks the trip against policy before booking; the
spreadsheet drifts from the emails, so no one can see a trip's status; a change restarts the thread and the "clear
business reason" gets lost; org reporting means merging spreadsheets.

## Evidence
- Approval is set per country, not globally: "It is the responsibility of the associate to know country level travel
  approval requirements and abide by them. Even if an official approval is not required by local policy, the best
  practice is that associates inform their managers about their intent to book travel or incur expenses, prior to
  doing so." (Guidelines, Travel Approval)
- Waiting has a cost, but the policy gives its direction, not its size: "Generally, airfare increases significantly closer to the travel
  date." The advance-booking days are in the "Walmart GTS Appendix", which the PDF links only to an internal Walmart site. (Guidelines, Advance Booking
  Requirements)
- Public fare studies disagree on the best booking window, so this brief does not use them.
- Days a request waits today: confirm — the panel (asked by Eugene Tarasov in the walkthrough), by 2026-12-04. It will be the panel's estimate of the span from request to
  decision (the same span the app measures), labeled as an estimate, not measured.
- Source note: the guidelines URL first given (public.walmart.com, `en_in` path) returned 404 on 2026-11-23. The
  sources above are the same document as a PDF: "Version: 1.0 … Updated: June 9, 2017", 3 pages, identical on both hosts.

## Success metric
| Id | Metric | Baseline | Target | By |
|---|---|---|---|---|
| M-01 | Median business days from request submitted to the manager's decision, in orgs that require approval; reported per org | confirm — the panel (asked by Eugene Tarasov in the walkthrough), by 2026-12-04 (method under Evidence) | 1 business day or less (owner's target, not a Walmart figure) | 30 days after MVP 1 is in use: confirm — Eugene Tarasov, by 2026-12-04 |

Orgs that require notice only have no wait to measure: the notice goes out when the request is submitted. Whether their
managers are notified before booking becomes a guardrail in the PRD.

## Constraints
- Booking stays with the approved agency: "All associates must reserve and purchase airline tickets, hotel rooms, and
  rental cars through the agency approved by Global Travel." and "Use of external websites … or suppliers' direct
  websites to book travel is prohibited, unless they are pre-approved by the Global Travel team." The app hands off;
  it never books.
- Each org's leadership chooses its approval rule (owner's decision, 2026-11-23): manager approval required, or
  manager notified only, on top of country rules. Every rule
  the app applies is labeled `SAMPLE: configurable, not Walmart policy` unless it quotes the guidelines.
- Policy checks quote the guidelines word for word, e.g. "Business Class travel may only be booked if the flight time on
  the longest segment is greater than 9 hours or if there is a cost saving."
- Trips where the associate plans to provide "travel and/or lodging for a non-US government official" may need
  "additional approvals": the app flags them and never decides.
- Trip changes and cancellations are in scope (owner's decision, 2026-11-23): a change goes back through the org's
  rule and keeps its reason, because "Changes or cancellations to travel bookings should only be made when there is a
  clear business reason."
- Decision records (who decided, when, why) are kept and cannot be edited.
  Retention period: confirm — Eugene Tarasov, by 2026-12-04.
- Demo data only, no real people. Walmart colors as tokens only, no logo, DM Sans, "not affiliated" footer.
- MVP 1 is due before the walkthrough. MVP 1 date: confirm — Eugene Tarasov, by 2026-11-30.
- Model spend is capped at $20/month for the organization, plus a per-guest call limit in the app (owner's decision,
  2026-11-23).

## Out of scope
- Booking and payment: booking stays with the approved agency, and "If associates are issued corporate credit cards,
  it is required that they are used for all travel and expense purchases."
- Expense reports and reimbursement: a different job, after the trip.
- Group and event travel: the policy routes it through the agency's "group booking process".
- Travel documents, driving permits and traveler security tracking: owned by the traveler and Global Travel.
- Coordinators and travel admins as users: not in the first group.

## Assumptions to confirm
| Id | Assumption | Owner | Confirm by |
|---|---|---|---|
| A-01 | Today requests and approvals run on email and a team spreadsheet, as in the steps above (scenario premise, not measured) | Eugene Tarasov | 2026-12-04 |
| A-02 | One approver is enough: the traveler's direct manager | The panel, asked by Eugene Tarasov in the walkthrough | 2026-12-04 |
| A-03 | Waiting before booking is the main cost of today's process | The panel, asked by Eugene Tarasov in the walkthrough | 2026-12-04 |
| A-04 | Every org's approval rule fits one of two modes: approval required, or notice only | The panel, asked by Eugene Tarasov in the walkthrough | 2026-12-04 |
| A-05 | The approved agency accepts an approved trip as a handoff (a summary or an email), with no integration needed | The panel, asked by Eugene Tarasov in the walkthrough | 2026-12-04 |
| A-06 | The June 9, 2017 guidelines (Version 1.0) still reflect the current global policy, and this copy (approved by the "Director, Global Travel - Asia", its appendix link points to a WMGTS India appendix file) is the global text, not a regional one; if a US version exists, it replaces this source | The panel, asked by Eugene Tarasov in the walkthrough | 2026-12-04 |
| A-07 | Org leaders want to choose their org's approval rule (the app lets them; this checks they want to) | The panel, asked by Eugene Tarasov in the walkthrough | 2026-12-04 |
| A-08 | Org leaders need org-level reporting on their org's travel, and today they assemble it by hand from team spreadsheets | The panel, asked by Eugene Tarasov in the walkthrough | 2026-12-04 |

## Risks
- The source is from 2017 and the original link is dead, so a policy check could quote a superseded rule.
- If managers keep approving by email, there are two records again and the spreadsheet comes back.
- An org misconfigures its rule, and trips are cleared without an approval the org requires.
- People take the app for a booking channel. The handoff has to say plainly that booking happens at the agency.
- Policy flags get read as decisions. Flags inform; the manager decides.
- Waiting turns out not to be the main cost (A-03): M-01 improves but users see no change. The PRD then adds a second
  measure for the trusted record.
