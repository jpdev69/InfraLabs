# Build your own image, properly

**Phase:** 3 — Automation & delivery
**Goal:** Your first custom Dockerfile — small, pinned, non-root.

## Scenario

The team's static site needs a custom image: CI will build it (brief 10), a registry will store it, VMs will run it. A teammate's first attempt starts `FROM ubuntu` and installs nginx with apt — the image is over 900MB and runs as root. Make the sane version.

## Requirements

- A Dockerfile that starts from a pinned nginx base image (exact tag or digest)
- COPYs the site and any config in as few layers as make sense
- Runs as a non-root user — prove it with `docker exec <container> whoami`
- A `.dockerignore` that keeps junk out of the build context (say what it excludes and why)
- A tagging scheme: `v0.1.0` style tags plus the git short SHA; never ship only `:latest`

## Constraints

- Image must be under 100MB (or document actual size and honestly explain the gap)
- Rebuilding from the same Dockerfile must be reproducible — same base, same config, no surprise changes
- For comparison, also build the naive `FROM ubuntu` version once, and record both sizes

## Success criteria

- [ ] `docker image ls` shows your tagged images and their sizes, next to the naive build's size
- [ ] The running container's `whoami` output is not `root`
- [ ] `docker image inspect` shows your labels (version, source)
- [ ] README explains each Dockerfile decision (base choice, layer order, non-root) in one or two lines each
- [ ] `docs/notes.md` answers: why does layer ordering matter for cache/rebuild speed?

## Why this matters

From this brief onward, the image is *your* deploy artifact — the thing CI builds (10), registries store (10), and CD rolls out (11). Base image choice, layering, non-root, pinning: this is supply-chain hygiene, and it's what separates a Dockerfile from a Dockerfile that survives a security audit.

## Stretch goals

- Scan the image with `trivy` and note what it found
- Push it manually to Docker Hub or GHCR (rehearsal for brief 10)
- Multi-stage build, even if contrived here — learn the shape
