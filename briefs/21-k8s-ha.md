# Prove zero downtime — HA, drains, and failure drills

**Phase:** 5 — Orchestration (Kubernetes)
**Goal:** Lose a node, keep serving requests. Rehearse it until it's boring.

## Scenario

A node needs maintenance on Friday. Business says zero downtime. "Prove it." You get to show that replicas spread across nodes, that the platform refuses unsafe maintenance, and that requests never notice.

## Requirements

- kind cluster with **multiple worker nodes**
- App deployed with enough replicas, spread via **anti-affinity** (or topology spread constraints) so they don't stack on one node
- A **PodDisruptionBudget** that matches your replica count
- The drill: run a continuous request loop from a second terminal; while it runs, `kubectl drain` a worker node
- A failure table in README: node dies / pod dies / node with the PV dies — what the platform does, what you must do

## Constraints

- Zero failed requests during the drain — if any request errors, fix the setup and repeat until clean
- No manual pod moves — the platform does the relocating

## Success criteria

- [ ] Continuous request loop during `kubectl drain` records zero errors (show the loop output summary)
- [ ] `kubectl get pods -o wide` before the drain shows replicas spread across nodes
- [ ] The drain is blocked or polite per your PDB — show what happened when you tried to drain
- [ ] README failure table covers at least three failure modes with "platform handles" vs "human handles" columns
- [ ] `docs/notes.md` answers: what is a PDB *for*, and who reads it?

## Why this matters

High availability is not an adjective, it's rehearsed procedures plus platform features. The drain drill is the single most honest test of a cluster's setup — and "zero errors under maintenance" is a portfolio-grade claim you can now make with a terminal recording to prove it.

## Stretch goals

- Snapshot and restore kind's etcd (advanced surgery; document the experience)
- Make the request loop also *measure latency* — what did users feel during the drain?
- Delete a whole node (not drain — hard delete): compare what happened vs the graceful drain
