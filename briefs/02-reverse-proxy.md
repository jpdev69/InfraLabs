# One door, two rooms — reverse proxy

**Phase:** 1 — Foundations
**Goal:** Route two services behind a single entrypoint.

## Scenario

You now run two web things: your static site from brief 01 and a demo app (`nginxdemos/hello`, a tiny container that prints its own hostname). Both want port 80. Your colleague refuses to memorize port numbers. They want one address: `/` goes to the static site, `/hello` goes to the demo app.

## Requirements

- One nginx container acting as reverse proxy, published on one host port (e.g. 8080) — the only port exposed to your machine
- The two upstream containers must NOT publish ports to the host; they live only on an internal Docker network
- Proxy forwards `X-Forwarded-For` and `Host` headers upstream
- The routing rules are documented in the project README

## Constraints

- Prove the upstreams are unreachable directly: browsing to their ports on `localhost` must fail
- One network; three containers on it

## Success criteria

- [ ] `http://localhost:8080/` shows the static site
- [ ] `http://localhost:8080/hello` shows the demo app's response
- [ ] Direct access to upstream containers from your machine fails (state how you proved it)
- [ ] Stopping the demo app container makes `/hello` return 502 while `/` keeps working
- [ ] `docker logs` on the proxy shows the proxied requests with the right paths
- [ ] README contains a tiny ASCII diagram of: browser → proxy → upstreams

## Why this matters

The reverse proxy is the front door of virtually every real system. TLS termination (brief 07), load balancing (brief 06), and Kubernetes Ingress (brief 17) are all this same pattern with more features. Notice what you did: one public endpoint, hidden internals, routing by path. That's ingress, three briefs early.

## Stretch goals

- Run a second `nginxdemos/hello` instance and route `/hello2` to it
- Serve a custom error page instead of the default 502
- Add a `/headers` path to the proxy that echoes back the headers the proxy forwarded
