# You'll know before your users do — monitoring and alerts

**Phase:** 6 — Observability & reliability
**Goal:** Metrics, one dashboard that matters, one alert that fires, one runbook that explains it.

## Scenario

Users currently tell your team the site is down — via angry messages. The team lead wants: "I want to know before they do." You need the observability loop: metric → alert → runbook.

## Requirements

- Install the **kube-prometheus-stack** Helm chart (Prometheus + Grafana + Alertmanager) on your cluster
- Get your workload's metrics scraped (any exporter that pairs with what you run — nginx exporter, redis exporter, or metrics exposed by the app itself)
- Build ONE Grafana dashboard that matters — not a wall of charts; a panel that answers a real question (request rate, error rate, or latency)
- One alert that matters (e.g. instance/app down, error rate above threshold) routed through Alertmanager
- `docs/runbook.md` for that alert: what it means, how to triage, what to check first

## Constraints

- The alert must be *drilled*: deliberately trigger it (kill the target) and show it fire, then show it resolve
- The dashboard must have a title and a stated question it answers ("Is the site up and fast right now?")

## Success criteria

- [ ] Grafana dashboard shows live data updating (screenshot or described)
- [ ] Killing the workload makes the alert fire — visible in Alertmanager (show the state transition)
- [ ] Restoring it makes the alert resolve
- [ ] `docs/runbook.md` exists and is written for "future you at 3 a.m." — no assumptions, concrete commands
- [ ] `docs/notes.md` answers: what's the difference between "the alert fired" and "the alert was *useful*"? What makes an alert actionable?

## Why this matters

Observability is how you build trust in systems — you *watch* them instead of hoping. The loop (metric → alert → runbook) is the operating system of every on-call rotation on Earth. Note what you did NOT need to build: the discovery, the TLS, the scaling — you did in briefs 02, 07, 06. The stack is assembling itself.

## Stretch goals

- Add two more alerts: one on latency (slow = broken too), one on saturation (disk/memory)
- Route Alertmanager to a real receiver (email, Telegram, Discord webhook)
- Annotate the dashboard with the moment of your alert drill
