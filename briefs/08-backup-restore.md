# Nothing is real until you restore it — backup drill

**Phase:** 2 — Scaling & networking
**Goal:** Backup and restore the Postgres stack from brief 04 — and prove the restore works.

## Scenario

Your team lead asks: "What happens if someone drops the database volume? Or deletes the wrong compose project?" Your answer must be a script and a rehearsed drill, not a shrug. An untested backup is a rumor.

## Requirements

- `scripts/backup.ps1`: dumps the running Postgres from your brief 04 stack to a date-stamped file on your machine — using `pg_dump` through the running container, without stopping the stack
- `scripts/restore.ps1`: restores a chosen backup file into a *fresh* volume
- Run and document a full restore drill: destroy the old volume completely, restore, verify
- Measure how long the restore took and write the number down

## Constraints

- The backup must come from the live stack — no downtime allowed
- The drill must genuinely destroy the old data first (`docker compose down -v`), otherwise it's theater

## Success criteria

- [ ] Backup script produces a non-empty, date-stamped dump file
- [ ] Full drill: add data → backup → `docker compose down -v` (data gone) → restore → data verified identical
- [ ] Recovery time is measured and written in README ("measured RTO: X minutes")
- [ ] README defines, in your own words: RTO and RPO — and states yours for this stack
- [ ] A second backup run after adding more data also works (backups are a habit, not an event)

## Why this matters

This is the first brief where you do something genuinely operational: a rehearsed recovery. Real DevOps lives here — the value of this entire career path is measured in "how fast do we come back." RTO/RPO vocabulary will follow you into every serious infra conversation for the rest of your life.

## Stretch goals

- Schedule backups (Windows Task Scheduler or cron in a helper container)
- Copy backups to a second location (different drive/folder) — state why one location isn't a backup
- Add a verification step that restores into a *throwaway* container and counts rows, so every backup is automatically proven restorable
