# Decouple it — Compose + Redis queue

**Phase:** 1 — Foundations
**Goal:** Split a system into web + queue + worker, and survive worker failures.

## Scenario

A team accepts image uploads through a web endpoint. Processing takes a while, and today the web request blocks until processing finishes — users stare at spinners. They want: web accepts instantly, work happens in the background. If a worker dies mid-shift, queued work must not be lost.

## Requirements

- Three services in one compose file:
  - `redis:7` (pinned) — the queue
  - a worker: run a small Python script from the `python:3.12-alpine` image via a volume-mounted script (no image building — that's brief 09)
  - a web endpoint (`hashicorp/http-echo` or similar) as the "frontend"
- The worker pops items from a Redis list named `jobs` and logs each one as it processes
- Worker restarts automatically on failure (`restart: on-failure`)
- Redis data lives in a volume so the queue survives Redis restarts

## Constraints

- No image building — the worker is a mounted script executed by a stock Python image
- Killing the worker must not lose any queued-but-unprocessed jobs

## Success criteria

- [ ] `docker compose exec redis redis-cli LPUSH jobs "job-1"` gets picked up and logged by the worker within seconds
- [ ] Pushing 10 jobs, then `docker kill`-ing the worker mid-processing: compose restarts it and the backlog drains with zero lost jobs
- [ ] `docker compose restart redis` does not lose the queue
- [ ] README contains an ASCII diagram: web → queue → worker, with the failure modes annotated
- [ ] `docs/notes.md` answers: what happens to a job the worker popped but died before finishing? (This is the classic "at-least-once vs at-most-once" trap — write your honest answer)

## Why this matters

Queues are how real systems absorb load and survive failures — this is the first brief where you operate a *system*, not a *service*. The lost-job question in the criteria is the oldest reliability problem in distributed systems; you just met it. Every event-driven system you meet later (Kafka, SQS, Celery) is this brief with more paperwork.

## Stretch goals

- Run two workers and show they share the queue without double-processing
- Add a "poison job" that makes the worker crash — observe and document the retry storm
- Make the web endpoint actually push jobs into the queue when curled
