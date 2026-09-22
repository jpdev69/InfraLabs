# Reliability with receipts — failure drills and postmortems

**Phase:** 6 — Observability & reliability
**Goal:** Scripted failure drills, measured recovery, written postmortems. Prove the platform survives.

## Scenario

The startup's investor asks: "What happens when things break?" You answer with a drill suite: scripted failures, measured recovery times, and honest postmortems — not assurances.

## Requirements

- `scripts/drills/` containing re-runnable drill scripts (not improvisation):
  - `drill-pod-kill`: kill pods at random while a request loop measures
  - `drill-node-drain`: drain a node while measuring (build on brief 21)
  - `drill-db-restore`: destroy the database volume, restore from brief 18's backups
- Measure and record **RTO** for each drill (requests-affected count, wall-clock recovery)
- Write **two postmortems** from real drill findings, using a template: what happened, impact, root cause, what worked, action items
- A one-page `docs/reliability.md`: known weaknesses of this platform, honestly stated

## Constraints

- Each drill must be re-runnable: a fresh person (or you, next month) runs the script and gets the same experience
- Postmortems are blameless: no "I stupidly..." — write "the process allowed X"

## Success criteria

- [ ] All three drills run from their scripts with no improvisation
- [ ] Each drill has measured numbers (RTO, failed requests, data loss) recorded
- [ ] The DB restore drill lands within the RTO you claimed in brief 08/18 — or your claim is honestly updated
- [ ] Two postmortems completed with at least one real action item each
- [ ] `docs/reliability.md` lists at least two known weaknesses with what would have to be true to fix them

## Why this matters

Reliability is rehearsed, not declared. Drills-as-code means practice is cheap enough to repeat; postmortems turn failures into curriculum. RTO/RPO/blameless postmortems are the working vocabulary of SRE — by the end of this brief you speak it with receipts, not flashcards.

## Stretch goals

- Automate drills on a schedule (chaos engineering lite)
- Do a "game day": hand the drill scripts to a friend, watch them run it, note where the docs failed
- Add a drill for "monitoring is down" — what good is observability you can't trust? (Test: scrape a second Prometheus)
