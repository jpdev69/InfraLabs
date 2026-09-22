# State in Kubernetes — StatefulSet, volumes, and a restore drill

**Phase:** 5 — Orchestration (Kubernetes)
**Goal:** Run Postgres in the cluster with durable storage — plus automated backups and a rehearsed restore.

## Scenario

The internet says "don't put databases in Kubernetes." Your team needs the database in the cluster anyway (one platform to operate, please). Do it properly: stable identity, durable storage, backups on a schedule, and a restore you have actually performed.

## Requirements

- Postgres as a **StatefulSet** with a headless Service
- Storage via a **PersistentVolumeClaim** that survives pod deletion (kind's default storage class is fine)
- A **CronJob** that dumps the database on a schedule to the host (or another volume)
- A restore drill: delete the PVC, restore from a backup, verify data

## Constraints

- Deleting the pod must not lose data — prove it
- The drill must genuinely destroy the volume first, otherwise it's theater (brief 08 rules apply)
- Credentials come from a Secret, not plaintext in YAML

## Success criteria

- [ ] Data written to Postgres survives `kubectl delete pod`
- [ ] The CronJob produces date-stamped backups — show one
- [ ] Full drill: data in → backup taken → PVC deleted (data gone) → restore → data identical
- [ ] README explains PVCs, the storage class, and the host-path reality of kind — where the bytes *actually* live
- [ ] `docs/notes.md` answers: why a StatefulSet instead of a Deployment? What does "stable identity" buy a database?

## Why this matters

Stateful workloads are the "hard part" of Kubernetes, and this brief extends your brief 08 backup discipline to the cluster. Everything here — PVCs, CronJobs, the difference between a pod's life and data's life — is daily reality for platform engineers.

## Stretch goals

- Compare your hand-rolled StatefulSet with the CloudNativePG operator's — what does the operator automate that you did manually?
- Back up to S3-compatible storage (run MinIO in the cluster)
- Simulate the node hosting the PV dying: what happens, what recovers, what needs a human?
