# Run report · frame-problem · Problem brief v1 drafted

Stage 1 Frame · 2026-11-23

## Yours to do

- [ ] Read docs/travel/00-brief.md and the review-doc findings
- [ ] Decide at G1: approve the brief, or say what to change
- [ ] Confirm the 7 `confirm —` items and 6 assumptions (A-01 to A-06) by 2026-12-04, or move the date

## Decisions

- **Does the app book travel?** Recommendation: No. It hands the approved trip to the approved agency, because the guidelines prohibit booking through other sites. Owner accepted. (To reverse: Global Travel pre-approves the app as a booking channel)
- **Who is the primary user?** Recommendation: The traveling associate first, then their manager, then org leadership (added by the owner for org-level reporting). Owner accepted. (To reverse: Evidence that managers or coordinators carry most of the cost)
- **Who sets the approval rule?** Recommendation: Each org's leadership picks 'manager approval required' or 'notice only'. This is the owner's idea, and it fits the guidelines' country-level approval wording. (To reverse: A single company-wide rule turns out to exist)
- **What is M-01?** Recommendation: Median business days from request to 'cleared to book', reported per org. The owner chose it over '% cleared before booking' and over a per-org metric. (To reverse: Agency data on all booked trips becomes available, which makes '% cleared before booking' measurable)

## Produced

| Artifact | State |
|---|---|
| `docs/travel/00-brief.md` | draft v1; structure check Fix 0 after 1 fix |
| `docs/travel/reviews/00-brief.review.md` | rule checks only (self-check) |

## Findings

- The policy URL given returns 404. The same guidelines are public as a PDF (Version 1.0, updated June 9, 2017), byte-identical on one.walmart.com and wlfc.walmart.com.
- The guidelines make approval country-level ('best practice' is to inform the manager), and they reserve booking for the approved agency. Both changed the problem: request and approval, not booking.
- No public number exists for today's waiting time, so the M-01 baseline is a confirm placeholder. Public fare studies disagree with each other and were not used.
- The 'email and spreadsheets' premise comes from the assignment scenario, so it is assumption A-01, not evidence.

## What I did NOT do

- Did not grade the brief against judgment criteria: that is review-doc's job, run next.
- Did not measure or observe today's process: every claim about it is an assumption with an owner and a date.
- Did not read the WMGTS or country appendices: they are not public.
- Did not save a copy of the policy PDF in the repo: the sources point to Walmart's hosts (SHA-256 bebd892d…7a74 noted in the session).
- Did not set status beyond draft: only the owner's words at G1 change it.
