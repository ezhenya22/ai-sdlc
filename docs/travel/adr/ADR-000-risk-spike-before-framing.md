# ADR-000 — Prove the live path before framing the problem

- **Status:** Accepted, 23 Nov 2026 (Eugene, plan approval)
- **Stage:** before Stage 1 (Frame). This is a deliberate exception to the lifecycle's own order.
- **Door:** two-way. The spike is throwaway; nothing in it is assumed by the PRD.

## Context
The walkthrough's most important moment is live: a trip request is submitted and approved, and both screens update in
real time. Three things can break it, and none of them is a product question:
1. A new custom domain: DNS, HTTPS certificate issuance, and company web filters that distrust young domains.
2. Realtime between two devices on different networks.
3. A hosted database with row-level security and anonymous sign-in for visitors.

Each needs days of lead time (a domain ages; a certificate can stick). If any of them fails on Day 7, there is no time
left to change course.

## Options
| Option | For | Against |
|---|---|---|
| A. Follow the lifecycle strictly: frame → define → … → build infra on Day 5 | Process purity | The riskiest unknowns surface last, when they're most expensive |
| **B. A one-day spike first: domain, hosting, database, a two-screen realtime "hello"** | Retires the three risks on Day 1; the domain starts aging | Breaks the stage order; risk of the spike quietly becoming the architecture |
| C. Skip live; show a recording | No infra risk | Weakest proof; the panel asked to see it live |

## Decision
**B.** Run a one-day risk spike before Stage 1. Its only output is evidence: the domain serves over HTTPS, and one row
written on phone A appears on phone B within 2 seconds over cellular.

## Guardrails
- The spike code lives in `spike/` and is deleted or rewritten when Stage 5 builds the real stories. Nothing in the PRD
  may cite it as a decision.
- The architecture is decided in Stage 3 by `log-decision`, with the spike's measurements as one input.

## Consequences
- The lifecycle gains an explicit, documented exception path: a **risk spike**, allowed when an unknown is external,
  slow to resolve and not a product question. It always gets its own ADR and a throwaway folder.
- The panel sees the exception and the reason, which is the point: process serves the outcome.
