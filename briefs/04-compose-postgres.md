# Three commands to onboard — Compose + Postgres

**Phase:** 1 — Foundations
**Goal:** A reproducible multi-container dev stack, declared in one file.

## Scenario

Your team needs a dev database and a web UI to poke it with. Today, setting that up takes a new developer a full day, and everyone's setup is slightly different. The team lead says: "A new dev should clone the repo, copy a config file, run one command, and be working in five minutes."

## Requirements

- A `docker-compose.yml` that runs `postgres:17` (pin the tag) and `adminer` (web DB UI)
- All credentials and tunable settings come from a `.env` file — never hardcoded in the compose file
- A committed `.env.example`; the real `.env` is gitignored (verify with `docker compose config` that values come from env)
- Postgres data lives in a named volume
- Both services on a custom network; adminer waits for postgres to be healthy (`depends_on` + healthcheck)
- Bring the whole stack up with one command; take it down with one command

## Constraints

- `docker compose down` must NOT destroy the data — prove it by re-upping and finding your tables
- Zero credentials visible in `docker compose config` output? No — prove they come from `.env` (and that `.env` is ignored by git: `git status` shows it untracked/ignored)

## Success criteria

- [ ] `docker compose up -d` brings up both services
- [ ] Adminer connects to Postgres through the browser and you create a table
- [ ] `docker compose down` then `up -d` — your table still exists
- [ ] Simulated new dev: copy the project folder to a new location, `cp .env.example .env`, `docker compose up -d` — works
- [ ] `docker compose ps` shows postgres as healthy
- [ ] README explains: what `depends_on` with a healthcheck condition actually guarantees (and what it doesn't)

## Why this matters

This is Infrastructure-as-Code, version one: the desired state of a multi-container system, written down and reproducible. It's also where 12-factor env hygiene becomes muscle memory. And this exact stack becomes the target of your backup drill in brief 08 — build it clean.

## Stretch goals

- Seed initial data automatically via `docker-entrypoint-initdb.d`
- Add a third service that uses the database (an app image of your choice)
- Explain in notes the difference between a named volume and a bind mount, and why you picked what you did
