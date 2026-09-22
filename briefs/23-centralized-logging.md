# Logs you can actually query — centralized logging

**Phase:** 6 — Observability & reliability
**Goal:** Ship every container's logs to one place, query by label, prove logs outlive pods.

## Scenario

Something broke. The logs you need are spread across pods on multiple nodes — three of which have since restarted. `kubectl logs` one pod at a time is not a strategy. You need centralized logging: shipped, labeled, stored, queryable.

## Requirements

- The **Loki stack** (Loki + Promtail) wired into your existing Grafana — or the ELK stack if you prefer, but Loki is the lighter path
- All container logs shipped automatically (Promtail discovers them)
- Query logs in Grafana with label filters (container name, pod, namespace)
- Prove the key property: logs of a **deleted pod** are still queryable

## Constraints

- No SSH-and-grep anywhere in your documented workflow
- Do one "incident drill": break something on purpose (e.g. a crashing Deployment), then *find the error* using only log queries — write down the query you used

## Success criteria

- [ ] Logs from a deleted pod are still queryable — show the query result
- [ ] A label filter (e.g. by pod/container name) narrows results correctly
- [ ] The incident drill is documented: the query, the result, the fix
- [ ] README documents three queries you actually used and what each found
- [ ] `docs/notes.md` answers: why do logs need to outlive pods? What does that cost (storage)? What's a reasonable retention trade-off?

## Why this matters

Logs are the third leg of observability (metrics tell you *that*, logs tell you *why*, traces tell you *where*). The pod-death query is the moment centralized logging justifies itself — the evidence survived the crime scene. Retention trade-off thinking (cost vs. forensic depth) is a genuine senior-engineer conversation.

## Stretch goals

- Log-based alert: fire an alert when a specific error string appears
- Configure retention explicitly and explain the knob you turned
- Compare structured logging (JSON) vs plain text for queryability — ship one JSON log and query by field
