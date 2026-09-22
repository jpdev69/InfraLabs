# Kubernetes ingress + TLS

**Phase:** 5 — Orchestration (Kubernetes)
**Goal:** One front door for the cluster: path routing and TLS, in Kubernetes.

## Scenario

Same client as brief 02, one platform later: "one address, `/` goes to the web app, `/hello` goes to the demo app, and it must be HTTPS." Last time you hand-built an nginx proxy and a network. Now the cluster does it.

## Requirements

- kind cluster with the **ingress-nginx** controller installed
- Two Deployments behind Services (static site + `nginxdemos/hello`)
- An Ingress resource routing `/` and `/hello` on one hostname
- TLS: a certificate (self-signed or mkcert) provided as a Secret, wired into the Ingress; HTTP redirects to HTTPS

## Constraints

- All routing and TLS as committed YAML (controller install can be one command)
- Be honest and specific in the README comparison (see criteria) — this brief's value is *seeing* what the platform took over

## Success criteria

- [ ] Both paths route correctly through one address
- [ ] HTTPS works; `curl -v` shows the handshake and the HTTP→HTTPS redirect
- [ ] README contains a comparison table: brief 02 (manual) vs this brief — for proxy config, TLS, service-to-service addressing, and what happened when you deleted things
- [ ] `docs/notes.md` answers: where does the Ingress controller actually run, and what receives traffic *before* your pods do?

## Why this matters

Ingress consolidates three things you built by hand — proxy, TLS termination, service discovery — into declarative config. When brief 25 ships a "production" platform, ingress + TLS is one of the load-bearing walls. Understanding the traffic path (client → controller → service → pod) is a top-three interview question for a reason.

## Stretch goals

- Install cert-manager with a self-signed ClusterIssuer — automate what you did manually
- Route a second hostname to a different backend
- Explain in notes what `external-dns` would do for you, and why teams adopt it
