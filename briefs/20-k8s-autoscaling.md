# Scale on demand — HPA and resource sizing

**Phase:** 5 — Orchestration (Kubernetes)
**Goal:** Autoscaling that actually triggers — and the resource sizing that makes it possible.

## Scenario

Friday sale. Traffic multiplies by ten for two hours. You are not going to sit there running `kubectl scale` with your hand on the pulse. Make the platform scale itself — and discover the prerequisite that everyone skips: resource requests and limits.

## Requirements

- **metrics-server** installed in the cluster (kind needs it explicitly)
- `requests` and `limits` (CPU/memory) set on every container you deploy
- A **HorizontalPodAutoscaler** targeting your app at ~50% CPU (or a memory/custom target)
- A load test (e.g. `hey`, `ab`, or a tight curl loop against the app through ingress) strong enough to trigger scaling
- Scale-down after load ends must also be shown (be patient — it takes minutes by design)

## Constraints

- The scale-up must be demonstrated by metrics, not vibes: `kubectl get hpa` watch output showing utilization % and replica count rising
- Document the math you expect before you run it: given your request value and load, roughly when should it scale?

## Success criteria

- [ ] Load test drives CPU past target; HPA scales replicas up (show the watch output)
- [ ] After load stops, replicas scale back down eventually — show it
- [ ] README explains requests vs limits in your own words, including what happens when a container exceeds its memory *limit* (demonstrate an OOMKill if you can)
- [ ] `docs/notes.md` answers: why is autoscaling useless (or dangerous) when requests are unset or wrong?
- [ ] A mis-sizing experiment documented: set the request wildly low, show the scheduler's behavior or a noisy-neighbor symptom

## Why this matters

"Autoscaling is resource sizing in disguise." Requests are promises and limits are seatbelts — every cluster outage story starts with somebody skipping them. You will leave this brief being the person who actually understands what the HPA percentage *means*, which puts you ahead of a shocking number of professionals.

## Stretch goals

- Deploy the Vertical Pod Autoscaler in *recommendation* mode and compare its suggestions to your hand-picked values
- Scale on a custom metric (e.g. requests-per-second via Prometheus — sneak preview of brief 22)
- Show a pod getting evicted under node memory pressure
