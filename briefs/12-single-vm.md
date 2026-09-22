# Beyond the laptop — one VM

**Phase:** 4 — VMs & networking
**Goal:** Provision a virtual machine with code, and run your stack on it.

## Scenario

Your compose stack is impressive, but it lives on your laptop. A manager says: "Great demo. Now put it on a machine." This brief is about the layer *under* containers — the VM — and about never building infrastructure by hand.

## Requirements

- Provision a local VM with **Vagrant + VirtualBox** (free, local) — or, if you prefer, a cloud free-tier VM with Terraform
- SSH access with keys, not passwords
- Docker installed on the VM via provisioning (inline script in the Vagrantfile is fine)
- Deploy your brief 04 compose stack (or another compose stack of yours) onto the VM
- The stack is reachable from your host machine's browser
- Teardown and re-provision must work: destroy the VM, run one command, get the same result

## Constraints

- The VM must be reproducible from committed files — no click-ops, no "open the GUI and install things"
- Any manual command you ran inside the VM belongs in a committed script (that friction is the lesson)

## Success criteria

- [ ] One command creates the VM; one command destroys it
- [ ] The stack's web UI opens from your host browser (via forwarded port or VM IP)
- [ ] Full teardown + re-provision reproduces a working stack end-to-end
- [ ] README contains an architecture diagram: host ↔ VM ↔ containers
- [ ] `docs/notes.md` lists every manual step you were tempted to do inside the VM and where you scripted it instead

## Why this matters

VMs are the substrate containers run on in every real environment — even managed Kubernetes is VMs underneath. You learn the full journey of an infra engineer here: declare hardware, secure access (SSH keys), bootstrap software, deploy on top. And the reproducibility constraint is your first real taste of Infrastructure-as-Code discipline: if you did it by hand, it doesn't exist.

## Stretch goals

- Do it with Terraform on a cloud free tier instead (HCL syntax is transferable knowledge)
- Use cloud-init instead of a shell script for provisioning
- Pin the VM image (box/AMI) — same pinning habit as brief 01, different artifact
