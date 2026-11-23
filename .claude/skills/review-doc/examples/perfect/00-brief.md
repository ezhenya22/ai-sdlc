---
doc_type: brief
app: room-booking
version: 2
status: approved
owner: Dana Example (facilities lead)
sources:
  - https://example.com/facilities-survey-2026
---

# Room booking: problem brief

## Problem
Team leads at a 400-person office spend time hunting for meeting rooms and still collide: two teams arrive at the same
room about four times a week. Each collision costs a meeting's first ten minutes and sometimes the meeting.

## Who it affects
- Team leads who book rooms (about 60, several times a week)
- Facilities coordinator who resolves collisions (1 person, daily)

## How it works today
1. A lead checks a shared spreadsheet of rooms and writes a name into a cell.
2. Anyone can overwrite a cell; nobody is told when it happens.
3. Collisions are found when two groups arrive at the same door.

## Evidence
- 17 collisions logged by facilities in October 2026 (facilities survey).
- Average time lost per collision: confirm — Dana Example, by 2026-12-04.

## Success metric
| Id | Metric | Baseline | Target | By |
|---|---|---|---|---|
| M-01 | Room collisions per month | 17 (Oct 2026) | 2 or fewer | 2027-03-31 |

## Constraints
- Must use company sign-in; no new passwords.
- Rooms and their capacities come from the facilities list, which facilities owns.

## Out of scope
- Booking desks or parking (a different team owns those).
- Catering orders, which leads asked for but which go through another vendor.

## Assumptions to confirm
| Id | Assumption | Owner | Confirm by |
|---|---|---|---|
| A-01 | Leads will stop using the spreadsheet if bookings are visible to everyone | Dana Example | 2026-12-11 |

## Risks
- If the facilities list of rooms is out of date, the app shows rooms that don't exist.
