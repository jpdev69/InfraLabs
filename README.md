# InfraLabs

A brief-driven engine for learning infrastructure and orchestration.
The engine tracks briefs, scaffolds projects, and manages submissions. Reviews happens and evaluated with AI against each brief's success criteria.

## The workflow

```
labs list          see all 25 briefs
   |
labs start 1       scaffold the project folder, read the brief
   |
build              work against the success criteria (done is defined there)
   |
labs submit 1      generates SUBMISSION.md with a checklist
   |
ai review    "Review my submission for brief 1 (01-static-site)"
   |
fix findings  ---> labs submit 1 again   (2-3 cycles is normal)
   |
labs pass 1        mark passed, next brief appears
```

Commands:

| command           | what it does                                    |
|-------------------|-------------------------------------------------|
| `labs list`       | all briefs with status, grouped by phase        |
| `labs show N`     | print the full brief                            |
| `labs start N`    | scaffold `projects/NN-name/` and set in progress |
| `labs submit N`   | write SUBMISSION.md, set in review              |
| `labs pass N`     | mark passed after a passing review               |
| `labs reopen N`   | back to doing, after review findings            |
| `labs note N msg` | timestamped note in the project's notes        |
| `labs next`       | the brief you should work on now                |
| `labs status`     | progress summary                                |

`labs` is the `labs.cmd` wrapper around `labs.py` (Python 3, no dependencies).

## Layout

```
briefs/       the 25 briefs (plain markdown - read, don't touch)
projects/     one folder per brief, created by `labs start`
docs/         cross-project notes live in each project's docs/
state.json    tracked progress (status per brief)
```

Every project folder has the same skeleton: `README.md` (architecture),
`docs/notes.md` (what broke, what you learned), `scripts/up.ps1` and
`scripts/destroy.ps1` (everything must be tear-downable), `.env.example`.

## Rules of the game

1. **One brief = one new concept.** If a brief exposes a gap, drill the gap, don't skip ahead.
2. **Done = success criteria.** Not vibes, not "it basically works".
3. **Everything tear-downable.** If it can't be destroyed and rebuilt from committed files, it doesn't exist.
4. **Never commit `.env`.** Copy from `.env.example` only.
5. **Write notes while stuck**, not after. That's when they're true.
