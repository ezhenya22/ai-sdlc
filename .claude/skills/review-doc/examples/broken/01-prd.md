---
doc_type: prd
app: room-booking
version: 1
status: draft
owner: Dana Example
brief: broken/00-brief.md
sources:
  - broken/00-brief.md
---

# Room booking: product requirements (broken on purpose)

## Summary
A room booking app.

## Users and jobs
| Role | Job to be done | How often |
|---|---|---|
| Team lead | Book rooms | Often |

## Requirements
| Id | Requirement | Priority | Traces to |
|---|---|---|---|
| REQ-01 | Book a room using a dropdown | High | M-01 |
| REQ-02 | Prevent overwrites | Must | M-01 |
| REQ-03 | Facilities day view | Should | |

## User stories

### ST-01 — Book a room
As a team lead, I want to book a room, so that I have a room.
Requirement: REQ-01
Acceptance criteria:
- **AC-01.1** Given a free room, When I book it, it works.

### ST-02 — Protected booking
As a team lead, I want my booking protected.
Requirement: REQ-09
Acceptance criteria:
- **AC-01.2** Given I hold a room, When someone else books it, Then they are refused.

## Non-functional requirements
- **Performance:** fast.

## Non-goals
- Advanced features.

## Open questions
| Question | Owner | Answer by |
|---|---|---|
| Who can cancel? | | |

## Dependencies
- None.
