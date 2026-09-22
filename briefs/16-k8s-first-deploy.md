# Hello, Kubernetes

**Phase:** 5 — Orchestration (Kubernetes)
**Goal:** Local cluster, first Deployment + Service, and watching the platform self-heal.

## Scenario

Restarting containers by policy, scaling with config edits, rediscovering services by hand — you've been doing orchestration *manually* since brief 06. Time to meet the platform that automates all of it, and learn the mental model that runs most of the industry's infrastructure.

## Requirements

- A local cluster using **kind** (Kubernetes-in-Docker) — or k3s if you prefer
- Deploy `nginxdemos/hello` as a Deployment with 2 replicas
- Expose it with a Service; reach it via `kubectl port-forward`
- Kill a pod; watch the controller replace it
- Scale the Deployment to 5 replicas
- Everything as committed YAML in the project folder — declarative, nothing done by `kubectl edit`

## Constraints

- Every object you create is written as YAML you can re-apply from scratch (`kubectl apply -f .`)
- README maps the concepts: for each piece of your brief 06 setup, name the Kubernetes object that replaced it (replica → ?, load balancer → ?, etc.)

## Success criteria

- [ ] App reachable through port-forward
- [ ] `kubectl delete pod` on one replica: the Deployment restores the count without you touching anything — show before/after pod lists
- [ ] Scaling to 5 works with one command on the Deployment
- [ ] `kubectl get all` output interpreted in README: one line per object type saying what it does
- [ ] `docs/notes.md` explains the reconciliation loop in your own words: desired state, observed state, controller — what actually happened when you deleted the pod?

## Why this matters

The reconciliation loop is the single most important concept in modern infrastructure: you declare *what* should run; the platform *continuously enforces* it. Every failure you caused manually in earlier briefs (container died, IP changed, replica missing) is something the loop absorbs automatically once you speak its language.

## Stretch goals

- Delete the Service and re-apply your YAML: notice nothing about the pods changed — explain why in notes
- Experiment with labels and selectors: break the selector, watch pods become "orphaned", fix it
- Run your workload in a separate namespace and document what namespaces are for
