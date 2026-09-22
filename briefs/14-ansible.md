# No snowflakes — configuration management with Ansible

**Phase:** 4 — VMs & networking
**Goal:** Idempotent playbooks that rebuild both VMs into the same machines, every time.

## Scenario

Last week you rebuilt a VM by hand and forgot a step — the app was down for an hour. A senior engineer says the worst words in infrastructure: "Do it twice, get two different machines." That's a snowflake. You need configuration management.

## Requirements

- An Ansible inventory covering both VMs from brief 13
- Playbooks (or roles) for:
  - common: docker installed, users, basic packages
  - app: the app stack deployed on VM A
  - db: postgres deployed on VM B (with the private-network config from brief 13)
- One command deploys the entire two-VM setup
- **Idempotence proof**: run the playbook twice in a row — the second run must report zero changes

## Constraints

- No manual SSH edits to configure the VMs — if a setting changed, a playbook did it
- Database credentials via environment files or `ansible-vault` — not plaintext in the repo (note in README how you handled them)

## Success criteria

- [ ] A freshly rebuilt VM, given one ansible run, ends up with the full stack working
- [ ] Second consecutive run: `changed=0` — show the output
- [ ] One command reaches both VMs and deploys the whole system
- [ ] Playbook structure is documented in README (what runs on which host and why)
- [ ] `docs/notes.md` defines idempotence in your own words, plus one real bug you hit where a task wasn't idempotent

## Why this matters

Ansible is the older sibling of everything declarative you've been doing: compose files, then Kubernetes manifests — all of them are "describe desired state, tool enforces it." Once idempotence clicks here, the philosophy of the entire orchestration phase follows for free. Also: "changed=0" is the most comforting sentence in infrastructure.

## Stretch goals

- Restructure into `roles/` — common, docker, app, db
- Use `ansible-vault` properly for the DB password
- Add a "verify" play that runs after deployment and fails loudly if the app isn't reachable
