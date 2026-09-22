# Package it — ConfigMaps, Secrets, and Helm

**Phase:** 5 — Orchestration (Kubernetes)
**Goal:** Turn YAML soup into a reusable, configurable chart.

## Scenario

A teammate wants your stack in *their* namespace — but with a different database name, different image tag, and their own hostname. Your current setup means copy-pasting manifests and editing by hand. That's how environments drift apart. Package the stack so the same chart produces any environment.

## Requirements

- Externalize all app configuration into a **ConfigMap**; database credentials into a **Secret**
- Package the whole stack (app + postgres + ingress from brief 17) as a **Helm chart**
- Two values files: `values-dev.yaml` and `values-prod.yaml` (different tag, hostname, resources)
- `helm install` on a *fresh* kind cluster must bring the entire stack up end-to-end

## Constraints

- No plaintext secrets committed anywhere — and README notes explicitly that base64 Secret encoding is *not* encryption, just packaging
- Changing a value must never require touching templates
- The chart includes your ingress + TLS configuration

## Success criteria

- [ ] Fresh cluster + `helm install <release> ./chart -f values-dev.yaml` = working stack reachable through ingress
- [ ] Installing the same chart with `values-prod.yaml` produces a second, differently-configured stack
- [ ] A `helm upgrade` changing one value visibly changes the deployment (show before/after)
- [ ] README documents the chart structure: what's a template, what's a value, what's a release
- [ ] `docs/notes.md` answers: what is "drift", and how did packaging prevent it here?

## Why this matters

Helm is how most real things ship into Kubernetes — most software you deploy later (including the monitoring stack in brief 22) arrives as a chart. The deeper lesson is config separation: the same artifact, different environments, zero hand-editing. That's the end of snowflakes — for machines and manifests alike.

## Stretch goals

- Add `helm lint` and a template-render check to a CI job
- Write a short comparison: Helm vs Kustomize — one paragraph, your own opinion
- Add a ` NOTES.txt` so `helm install` prints the URL to hit
