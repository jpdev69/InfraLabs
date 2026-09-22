# Secure the front door — HTTPS

**Phase:** 2 — Scaling & networking
**Goal:** TLS termination in front of your stack.

## Scenario

The browser shows "Not secure". A security review says every web endpoint must be HTTPS — including internal ones, because "internal" is a claim, not a control.

## Requirements

- A TLS-terminating proxy in front of your existing stack — Caddy is recommended locally (it auto-manages local certificates), nginx with a self-signed cert also works
- The proxy serves HTTPS on 443 and redirects plain HTTP to HTTPS
- The certificate must be trusted by your machine (no browser warnings)
- Upstream services stay plain HTTP — encryption ends at the proxy

## Constraints

- Only port 443 (plus 80 for the redirect) exposed to your machine
- You must be able to state where the certificate lives, when it expires, and what renews it

## Success criteria

- [ ] `https://localhost` (or your chosen name) loads with no browser warning
- [ ] `http://...` redirects to `https://...` — show it with `curl -v`
- [ ] `curl -v` output shows the TLS handshake and the redirect
- [ ] README documents: where certs live, their expiry date, and what "renewal" means for your setup
- [ ] `docs/notes.md` explains the difference between TLS *termination* at the edge and end-to-end encryption — and one reason each exists

## Why this matters

TLS termination at the edge is the industry-standard pattern: one place to manage certs, headers, and policies, while internal traffic stays fast and simple. When you hit cert-manager in Kubernetes (brief 17/25), you'll be re-learning this exact problem — with the cert lifecycle automated. Knowing what's being automated is what makes you the person who fixes it when it breaks at 2 a.m.

## Stretch goals

- If you have a real domain and a public VM, get a real Let's Encrypt certificate (use their staging environment first)
- Add a security header (HSTS) and verify it in the response
- Explain in notes: what is a certificate chain, and what does the browser actually verify?
