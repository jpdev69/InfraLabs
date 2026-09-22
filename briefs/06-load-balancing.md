# Scale sideways — load balancing + replicas

**Phase:** 2 — Scaling & networking
**Goal:** One address, N app replicas, no single point of failure.

## Scenario

During a launch, traffic spikes and your single app container maxes out. The boss saw "the site was slow" once and never wants a repeat. The fix isn't a bigger container — it's more containers behind a load balancer.

## Requirements

- Three replicas of `nginxdemos/hello` (it prints its own hostname — perfect for proving routing)
- An nginx container load-balancing across all replicas via `upstream`
- The load balancer is the only exposed port
- Adding a fourth replica should require editing a number (or one block) in a file — not hand-rolling a new nginx config from scratch
- Demonstrate the distribution of requests across replicas

## Constraints

- Requests through the single public address must visibly hit different replicas (hostname in the response proves it)
- Killing one replica must not require any nginx config surgery for the site to keep working

## Success criteria

- [ ] 30 requests in a loop distribute across all three replicas (show the count per replica)
- [ ] Killing one replica: all subsequent requests still succeed
- [ ] Scaling to 5 replicas works, and the load balancer picks the new ones up
- [ ] README explains round-robin vs `least_conn`, and when you'd pick each
- [ ] `docs/notes.md` answers: why does this only work for stateless apps? What would break if the app kept session state in memory?

## Why this matters

Horizontal scaling + statelessness is the load-bearing idea of orchestration. Everything in phase 5 (Kubernetes replicas, Services, HPA) is this brief, automated. The statelessness question at the end is not trivia — it's the exact thing that breaks the first real scaling attempt of almost every team.

## Stretch goals

- Switch the upstream to `least_conn` and re-measure the distribution
- Run a simple load test (`hey`, `ab`, or a PowerShell loop) and show the wall-clock difference between 1 and 3 replicas
- Add weights to upstreams and show skewed distribution
