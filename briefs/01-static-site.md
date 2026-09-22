# Static site, one container

**Phase:** 1 — Foundations
**Goal:** Run your first container and make it survive restarts.

## Scenario

A friend has a portfolio site: plain HTML/CSS files in a folder. Today they double-click `index.html` to view it. They want it served like a real website at `http://localhost:8080` — without installing nginx on your machine — and they will occasionally edit the files.

## Requirements

- Use `nginx:stable` from Docker Hub. Pin it: record the exact tag (or digest) you pulled, don't just say `:latest`
- Serve the site files from a folder on your machine, through the container
- Site reachable at `http://localhost:8080`
- Container runs detached, with a restart policy so it comes back after a Docker daemon or machine restart
- Editing a file on your machine shows up in the browser without rebuilding or recreating anything

## Constraints

- No Dockerfile yet — use the image as-is
- No Docker Compose yet — plain `docker run` (you'll earn compose in brief 04)
- Make yourself 3–5 simple site files if you don't have any

## Success criteria

- [ ] `http://localhost:8080` loads the site
- [ ] Editing `index.html` on your machine is reflected after a browser refresh — no container restart
- [ ] `docker stop` then `docker start` brings the identical site back — nothing reconfigured
- [ ] `docker ps` shows the container running with the restart policy you chose
- [ ] `docs/notes.md` explains, in your own words: image vs container vs the host folder you mounted
- [ ] You can show the container's logs with one command

## Why this matters

This is the atom of everything that follows: an image (the recipe), a container (the running instance), port mapping (how the outside world reaches it), and a host mount (where data lives outside the container's short life). Every later brief — compose, VMs, Kubernetes — is this pattern, repeated and automated. Get the vocabulary right now and briefs 06–25 get dramatically easier.

## Stretch goals

- Add a custom `nginx.conf` (different 404 page, or enable gzip)
- Serve the site on a second port at the same time
- Explain in notes: what happens to your site files if you `docker rm` the container? Why is that the correct behavior?
