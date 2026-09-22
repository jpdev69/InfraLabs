# Capstone — the production platform

**Phase:** 7 — Capstone
**Goal:** Everything you've learned, running as one system: CI/CD, TLS, backups, autoscaling, monitoring, alerts, logs — one command up, one push to deploy, zero downtime on failure.

## Scenario

Final client. A startup wants the whole thing: "A three-tier web app on Kubernetes with a real pipeline. Ship a change by pushing to git. Survive a node dying with zero downtime and an alert. Restore the database from backup. Document it so a stranger could run it. Show us."

This is the repo you show employers. Build it to be read.

## Requirements

- **The app**: frontend + API + Postgres (reuse images from earlier briefs plus your custom image from brief 09 — the app can be simple; the *platform* is the point)
- **Delivery**: git push → CI builds + pushes a versioned image (brief 10) → CD updates the release (Helm upgrade with the new tag) → live in minutes
- **The platform**, as one Helm chart or a set of charts:
  - ingress + TLS (brief 17)
  - database with PVC + scheduled backups (brief 18)
  - autoscaling with real requests/limits (brief 20)
  - PDBs and multi-node (brief 21)
  - monitoring + at least two alerts + runbook (brief 22)
  - centralized logging (brief 23)
- **The docs**: architecture diagram, pipeline diagram, runbook, on-call guide, reliability notes (brief 24's honest weaknesses)

## Constraints

- Everything reproducible: a fresh machine following your README gets to a full platform (state what must be installed)
- No manual edits on the cluster — every change goes git → pipeline → helm
- Rollback path documented and demonstrated once

## Success criteria

- [ ] Fresh cluster: documented one-command path (scripts + README) to the full platform, verified end-to-end
- [ ] Push a code change: pipeline runs, new version live within minutes (show the version change on the site)
- [ ] Node failure drill: zero failed requests + an alert fired (show both)
- [ ] DB restore drill from platform backups passes (brief 18/24 standard)
- [ ] README is portfolio-grade: diagrams, decision log (why you chose each piece), trade-offs you'd change with more time/money
- [ ] A stranger test: someone (or future-you in a week) follows the README from scratch — note where they stumbled and fix the docs

## Why this matters

Integration is the actual skill. Any one of the six phases is learnable from a tutorial; a *platform* where delivery, scaling, recovery, and observability interlock — and where the docs make it reproducible by a stranger — is what separates "knows tools" from "can operate systems". This brief is your proof.

## Stretch goals

- Two environments (dev/prod namespaces) from the same chart with different values
- GitOps upgrade: install Argo CD, point it at your chart repo, and delete your own CD job — the platform now pulls its own desired state
- Cost/reliability review: write the memo you'd send to CTO about what this setup would cost and what breaks at 100× traffic
