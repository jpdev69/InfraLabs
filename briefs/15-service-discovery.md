# Stop hardcoding IPs — service discovery

**Phase:** 4 — VMs & networking
**Goal:** Services find each other by name across VM rebuilds and IP changes.

## Scenario

You rebuilt the database VM. Its IP changed. The app broke, and it took you twenty minutes to figure out why. Also: how does anything know what's currently alive? You need name-based service discovery.

## Requirements

- The app on VM A reaches the database on VM B by a stable *name* — never an IP
- Implement one of:
  - managed host entries: Ansible maintains DNS-style entries (e.g. `db.internal`) on VM A — simplest honest version, or
  - Consul: services register themselves, health-checked, and consumers resolve by name
- Recreate the DB VM so it comes back with a *different* IP — the app must reconnect with zero manual config edits
- Document how registration and resolution work in your chosen approach

## Constraints

- Prove no hardcoded IPs: `grep -r` (or your OS equivalent) for the old IP across all config finds nothing
- Document what happens if the app starts while the DB is down: does it crash? retry? forever or N times?

## Success criteria

- [ ] After recreating the DB VM with a new IP, the app reaches the database with no config change on VM A
- [ ] The grep proof shows zero hardcoded IPs in committed config
- [ ] README explains your discovery mechanism: who registers, who resolves, what holds the truth
- [ ] The startup-failure behavior (app boots, DB down) is tested and written down — this is your first meeting with retry/backoff thinking
- [ ] `docs/notes.md` answers: what did Docker's built-in DNS give you for free in briefs 04–06 that you had to build by hand here?

## Why this matters

This brief is the pain that Kubernetes was invented to solve — you are now manually building what orchestration platforms give natively (Services, DNS, health-gated endpoints). Having *felt* the pain, you'll understand what the platform actually does for you instead of reciting flashcards. That's the difference between a Kubernetes user and a Kubernetes understander.

## Stretch goals

- Consul health checks: kill the DB process (not the VM) and show consumers stop being sent to it
- Dynamic re-render of config when the DB moves (template + handler, or Consul template)
- Register the worker from brief 05 as a second discovered service
