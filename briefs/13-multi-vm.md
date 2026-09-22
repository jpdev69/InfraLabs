# Blast radius — split app and database across VMs

**Phase:** 4 — VMs & networking
**Goal:** Two VMs: the app public, the database private and unreachable.

## Scenario

Security review: "The app and the database share a machine. If the box dies, everything dies. And why is the database reachable from outside the machine at all?" You need topology: separation and isolation.

## Requirements

- Two VMs with a private network between them
- App stack (your compose app, or a simple container) on VM A
- Postgres on VM B, reachable ONLY from VM A over the private network
- The database port must not be published to your host or any public interface
- Document every port that exists on both VMs and why (a port table)

## Constraints

- Prove the isolation: from your host machine, connecting to the DB port must fail; from VM A, it must succeed — show both tests
- App VM can be destroyed and rebuilt without touching the database's data

## Success criteria

- [ ] The app works when accessed from your host
- [ ] Direct host → database connection attempt fails (show the exact command and its error)
- [ ] From inside VM A, the database connection succeeds (show it)
- [ ] Destroying and rebuilding VM A leaves the database data intact
- [ ] README contains the network diagram and the port table
- [ ] `docs/notes.md` answers: what is "blast radius", and how did splitting machines shrink it here?

## Why this matters

App/database split across machines is the most common production topology in existence. The muscle you're training is network *intent*: every port is either a door you meant to open or a door you forgot to close. This brief's isolation proof (fails from outside, works from inside) is the exact test you'll repeat in Kubernetes with NetworkPolicies later.

## Stretch goals

- Add a third VM running your worker from brief 05
- Only allow SSH to VM B *through* VM A (bastion pattern) — then document who can reach what
- Firewall rules inside the VMs (e.g. only allow 5432 from VM A's IP specifically)
