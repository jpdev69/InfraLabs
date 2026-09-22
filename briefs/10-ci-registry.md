# Ship it from CI — GitHub Actions + container registry

**Phase:** 3 — Automation & delivery
**Goal:** A pipeline that builds and pushes your image on every tag.

## Scenario

The team lead: "Stop building images on laptops. Every release tag must produce a buildable, traceable image — built by a machine, stored in a registry, pullable by anyone with one command."

## Requirements

- The brief 09 image lives in its own git repo on GitHub (this one is a genuine portfolio-repo candidate)
- A GitHub Actions workflow that:
  - builds the image on every push to a PR branch (no push) — proves the build
  - builds AND pushes to GHCR (ghcr.io) when you push a tag like `v0.2.0`
  - labels the image with the git SHA and tag
- Authentication uses the built-in `GITHUB_TOKEN` — no long-lived personal tokens, no secrets in code
- README shows the workflow badge and the exact `docker pull` command for a release

## Constraints

- No secrets committed anywhere — check before you push
- The build must work from a clean checkout: the CI machine has nothing of yours on it
- Workflow file is reviewed by you line-by-line: you can explain what each step does

## Success criteria

- [ ] Pushing tag `v0.2.0` (or similar) produces a versioned image visible in GHCR's UI
- [ ] A PR build runs and passes without pushing — show the run
- [ ] The image is pullable by tag from another machine or a VM (or simulate: pull by digest into a clean docker context)
- [ ] `docker inspect` of the pulled image shows the git SHA label
- [ ] README documents the release flow: "to release, I do X" in one sentence

## Why this matters

This is the first joint between development and operations: developers tag, the pipeline ships a real artifact, and the registry becomes the single source of truth for what runs anywhere. "Deploy" stops being a script on your laptop and becomes a traceable event. Brief 11 closes the loop by making running systems consume these images automatically.

## Stretch goals

- Add a trivial smoke test (container starts, serves 200) as a CI step before push
- Attach an SBOM to the release (`docker buildx` + a tool of your choice)
- Build a second, smaller variant (alpine tag) via a matrix
