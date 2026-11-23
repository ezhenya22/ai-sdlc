---
doc_type: prd
app: room-booking
version: 1
status: in-review
owner: Dana Example (facilities lead)
brief: perfect/00-brief.md
sources:
  - perfect/00-brief.md
---

# Room booking: product requirements

## Summary
Room collisions cost meetings their first minutes about four times a week. This release serves team leads who book
rooms. It lets them see who holds a room and book it without anyone silently overwriting them.

## Users and jobs
| Role | Job to be done | How often |
|---|---|---|
| Team lead | Book a room for a meeting | Several times a week |
| Facilities coordinator | See and fix conflicts | Daily |

## Requirements
| Id | Requirement | Priority | Traces to |
|---|---|---|---|
| REQ-01 | A lead can book a free room for a time slot | Must | M-01 |
| REQ-02 | A booked slot cannot be taken by someone else | Must | M-01 |
| REQ-03 | Facilities can see all bookings for a day | Should | Who it affects |

## User stories

### ST-01 — Book a free room
As a team lead, I want to book a free room for a time slot, so that my meeting has a place.
Requirement: REQ-01
Acceptance criteria:
- **AC-01.1** Given room 4A is free from 10:00 to 11:00, When I book it, Then the slot shows my name.
- **AC-01.2** Given I pick a slot in the past, When I try to book it, Then I see "That time has passed" and nothing is booked.

### ST-02 — No silent overwrite
As a team lead, I want my booking protected, so that nobody takes my room without me knowing.
Requirement: REQ-02
Acceptance criteria:
- **AC-02.1** Given I hold room 4A from 10:00 to 11:00, When another lead tries to book it, Then they see "Booked by Dana" and the booking is refused.

### ST-03 — Facilities day view
As the facilities coordinator, I want to see every booking for a day, so that I can spot problems before people arrive.
Requirement: REQ-03
Acceptance criteria:
- **AC-03.1** Given there are 12 bookings tomorrow, When I open tomorrow, Then I see all 12 with room, time and owner.

## Non-functional requirements
- **Accessibility:** WCAG 2.2 AA; every action works by keyboard.
- **Privacy:** only names and times are stored; no meeting titles.
- **Security:** company sign-in only; leads change only their own bookings.
- **Performance:** a booking shows for everyone within 2 seconds.

## Non-goals
- Desk and parking booking.
- Recurring bookings (asked for, deferred to the next release).

## Open questions
| Question | Owner | Answer by |
|---|---|---|
| Can facilities cancel a lead's booking? | Dana Example | 2026-12-04 |

## Dependencies
- The facilities room list, owned by facilities.
