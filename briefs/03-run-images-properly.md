# Run someone else's image, properly

**Phase:** 1 — Foundations
**Goal:** Take a ready-made API image and operate it like a professional.

## Scenario

The developers hand you an image — `hashicorp/http-echo` (or `kennethreitz/httpbin`) — and say "deploy this for the team." It needs environment configuration, it listens where you tell it, and you're now responsible for knowing whether it's healthy.

## Requirements

- Pin the image to an exact tag or digest — no `:latest`
- All configuration goes through environment variables, never by editing anything inside the image
- Run it on a custom internal port, mapped to a host port of your choosing
- Define a healthcheck so Docker reports `healthy` / `unhealthy` (use `docker inspect` to prove it)
- Put it on its own Docker network with a meaningful name
- Restart policy: restart on failure

## Constraints

- Changing an env var must not require a new image — only a new container
- The container's logs must show incoming requests after you curl it

## Success criteria

- [ ] API responds on your chosen host port
- [ ] `docker inspect` shows the container's health status as `healthy`
- [ ] Changing one env var and recreating the container visibly changes the API's response — image untouched
- [ ] `docker logs` shows the requests you made
- [ ] Force the container to fail (kill its main process) and show that the restart policy brought it back
- [ ] `docs/image-contract.md` documents the image's "contract": what env vars it takes, what port it listens on, what its healthcheck is, where it logs

## Why this matters

From here on, developers will always hand you images — `my-company/backend:1.7` — never machines. Your job is turning that artifact into a reliable running thing. The contract you wrote in `docs/image-contract.md` (env, port, health, logs) is the real deliverable of this brief. Teams that formalize this hand-off have fewer 2 a.m. pages.

## Stretch goals

- Run two instances behind the brief 02 proxy
- Write a second image-contract for `postgres:17` — you'll reuse it in brief 04
- Demonstrate what `docker inspect` all tells you about restart count and health transitions
