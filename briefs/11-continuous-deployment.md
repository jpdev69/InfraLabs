# From push to prod — continuous deployment

**Phase:** 3 — Automation & delivery
**Goal:** A running service that updates itself when a new image is published — and can roll back.

## Scenario

"When CI ships a new image, I don't want anyone SSH-ing anywhere. The running service should just pick it up. And if it's bad, rolling back must be one command, not an afternoon."

## Requirements

- A service running from your GHCR image (from brief 10) — on your machine or a VM, your choice
- An automated update path, either:
  - pull-based: a watcher (e.g. Watchtower) polls the registry and updates the container when a new tag appears, or
  - push-based: a CI job triggers a deployment (webhook to a tiny receiver, or SSH action)
- The running site visibly shows its version (so you can *see* a deploy happened)
- A documented, rehearsed rollback: return to the previous tag with one command

## Constraints

- Rollback must not involve rebuilding anything — previous image already exists in the registry
- README must diagram the full pipeline: git → CI → registry → running service
- README must state the trade-off you chose (pull vs push) and why — this is the fault line where GitOps was invented

## Success criteria

- [ ] Pushing a new tag → running container updates within minutes, without any manual step (version visible on the site)
- [ ] Rollback drill: previous version restored with one command; measured how long it took
- [ ] A deliberate "bad" deploy (e.g. tag that serves an error) is rolled back — write the incident in `docs/notes.md` as 5 lines
- [ ] README explains pull vs push deployment honestly, including what happens if the watcher/CI is down

## Why this matters

Deployment automation is the muscle behind every "we ship on Fridays" brag you'll ever hear. More important is the rollback: teams automate deploys for speed, but automated *rollback* is what actually buys courage. When you meet GitOps tools later (Argo CD Flux), you'll recognize this brief instantly — you built its ancestor by hand.

## Stretch goals

- Blue/green: two compose projects + a switch script that flips traffic with zero downtime
- Add a health-gated rollout: update only if the new container reports healthy within N seconds, else keep old
- Deployment notifications (CI posts a message on success/failure)
