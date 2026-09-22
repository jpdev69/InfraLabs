import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRIEFS_DIR = ROOT / "briefs"
PROJECTS_DIR = ROOT / "projects"
STATE_FILE = ROOT / "state.json"

STATUSES = ("todo", "in_progress", "in_review", "passed")
MARKER = {"todo": " ", "in_progress": ">", "in_review": "?", "passed": "x"}


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"briefs": {}}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def today():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def brief_files():
    return sorted(BRIEFS_DIR.glob("[0-9][0-9]-*.md"))


def parse_brief(path):
    text = path.read_text(encoding="utf-8")
    info = {
        "num": int(path.name[:2]),
        "slug": path.stem,
        "title": "",
        "phase": "",
        "goal": "",
        "criteria": [],
        "body": text,
    }
    in_criteria = False
    for line in text.splitlines():
        if line.startswith("# ") and not info["title"]:
            info["title"] = line[2:].strip()
        elif line.startswith("**Phase:**") and not info["phase"]:
            info["phase"] = line.split("**Phase:**", 1)[1].strip()
        elif line.startswith("**Goal:**") and not info["goal"]:
            info["goal"] = line.split("**Goal:**", 1)[1].strip()
        elif line.startswith("## "):
            in_criteria = line.lower().startswith("## success criteria")
        elif in_criteria and line.startswith("- [ ]"):
            info["criteria"].append(line[5:].strip())
    return info


def all_briefs():
    return [parse_brief(p) for p in brief_files()]


def find_brief(num):
    for b in all_briefs():
        if b["num"] == num:
            return b
    sys.exit(f"No brief number {num}. Run: labs list")


def get_status(state, num):
    return state["briefs"].get(str(num), {}).get("status", "todo")


def set_status(state, num, status):
    state["briefs"].setdefault(str(num), {})["status"] = status
    save_state(state)


def project_path(brief):
    return PROJECTS_DIR / brief["slug"]


def next_todo():
    state = load_state()
    for b in all_briefs():
        if get_status(state, b["num"]) != "passed":
            return b
    return None


def cmd_list(_):
    state = load_state()
    briefs = all_briefs()
    if not briefs:
        sys.exit("No briefs found in briefs/")
    counts = {s: 0 for s in STATUSES}
    phase = None
    print("")
    for b in briefs:
        st = get_status(state, b["num"])
        counts[st] += 1
        if b["phase"] != phase:
            phase = b["phase"]
            print(f"  {phase}")
            print("  " + "-" * max(len(phase), 12))
        print(f"  [{MARKER[st]}] {b['num']:02d}  {b['title']}")
    print("")
    print(
        f"  {counts['passed']}/{len(briefs)} passed"
        f"  |  doing: {counts['in_progress']}"
        f"  in review: {counts['in_review']}"
        f"  todo: {counts['todo']}"
    )
    print("")


def cmd_show(args):
    b = find_brief(args.num)
    state = load_state()
    st = get_status(state, b["num"])
    print(f"== Brief {b['num']:02d}: {b['slug']}  [{st}] ==\n")
    print(b["body"])
    print(f"\n-- start it with: labs start {b['num']}")


def scaffold(brief):
    root = project_path(brief)
    root.mkdir(parents=True)
    (root / "scripts").mkdir()
    (root / "docs").mkdir()
    lines = [
        f"# {brief['title']}",
        "",
        f"> Goal: {brief['goal']}",
        "",
        "## Success criteria",
        "",
    ]
    lines += [f"- [ ] {c}" for c in brief["criteria"]]
    lines += [
        "",
        "## Architecture",
        "",
        "- containers/services:",
        "- ports:",
        "- volumes:",
        "- networks:",
        "",
        "## Run",
        "",
        "- scripts/up.ps1 brings it up",
        "- scripts/destroy.ps1 tears it down",
        "",
    ]
    (root / "README.md").write_text("\n".join(lines), encoding="utf-8")
    (root / "docs" / "notes.md").write_text(
        "# Notes\n\n## What broke / what I learned\n", encoding="utf-8"
    )
    (root / "scripts" / "up.ps1").write_text(
        'Write-Host "TODO: replace with the commands that bring this stack up"\n',
        encoding="utf-8",
    )
    (root / "scripts" / "destroy.ps1").write_text(
        'Write-Host "TODO: replace with the commands that tear this stack down"\n',
        encoding="utf-8",
    )
    (root / ".env.example").write_text(
        "# copy to .env and fill in -- never commit .env\nSOME_SERVICE_USER=change-me\nSOME_SERVICE_PASSWORD=change-me\n",
        encoding="utf-8",
    )
    return root


def cmd_start(args):
    b = find_brief(args.num)
    root = project_path(b)
    if root.exists():
        sys.exit(f"Folder already exists: {root}")
    PROJECTS_DIR.mkdir(exist_ok=True)
    scaffold(b)
    state = load_state()
    state["briefs"].setdefault(str(b["num"]), {})["started"] = today()
    set_status(state, b["num"], "in_progress")
    print(f"Created {root}")
    print(f"Brief {b['num']:02d} is now in progress.")
    print("Build against the success criteria, then run: labs submit "
          f"{b['num']}")


def cmd_submit(args):
    b = find_brief(args.num)
    state = load_state()
    if get_status(state, b["num"]) == "todo":
        sys.exit(f"Brief {b['num']:02d} not started yet. Run: labs start {b['num']}")
    if get_status(state, b["num"]) == "passed":
        sys.exit(f"Brief {b['num']:02d} already passed.")
    entry = state["briefs"].setdefault(str(b["num"]), {})
    entry["status"] = "in_review"
    entry["submissions"] = entry.get("submissions", 0) + 1
    save_state(state)
    attempt = entry["submissions"]
    sub_path = project_path(b) / "SUBMISSION.md"
    lines = [
        f"# Submission -- {b['title']}",
        "",
        f"Submitted: {today()} (attempt {attempt})",
        "",
        "## Checklist",
        "",
    ]
    lines += [f"- [ ] {c}" for c in b["criteria"]]
    lines += [
        "",
        "## Review",
        "",
        "(reviewer: tick each criterion, list gaps as bullets below)",
        "",
    ]
    sub_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Submitted brief {b['num']:02d} for review (attempt {attempt}).")
    print(f"Checklist written to {sub_path}")
    tip = f'Review my submission for brief {b["num"]} ({b["slug"]}).'
    print(f"\nNow open dedicated AI in this folder and say:\n\n  \"{tip}\"\n")


def cmd_pass(args):
    b = find_brief(args.num)
    state = load_state()
    set_status(state, b["num"], "passed")
    print(f"Passed brief {b['num']:02d}: {b['title']}")
    nxt = next_todo()
    if nxt:
        print(f"\nNext up: {nxt['num']:02d}  {nxt['title']}")
        print(f"  labs start {nxt['num']}")


def cmd_reopen(args):
    b = find_brief(args.num)
    state = load_state()
    set_status(state, b["num"], "in_progress")
    print(f"Brief {b['num']:02d} reopened -- fix the review findings, then submit again.")


def cmd_note(args):
    b = find_brief(args.num)
    notes = project_path(b) / "docs" / "notes.md"
    if not notes.exists():
        sys.exit(f"Project folder missing for brief {b['num']:02d}. Run: labs start {b['num']}")
    with notes.open("a", encoding="utf-8") as f:
        f.write(f"- [{today()}] {args.text}\n")
    print("Noted.")


def cmd_next(_):
    n = next_todo()
    if not n:
        print("All briefs passed. Go build something real.")
        return
    state = load_state()
    st = get_status(state, n["num"])
    if st == "in_progress":
        print(f"In progress: {n['num']:02d}  {n['title']}")
    elif st == "in_review":
        print(f"Waiting on review: {n['num']:02d}  {n['title']}")
    else:
        print(f"Next brief: {n['num']:02d}  {n['title']}")
        print(f"  {n['goal']}")
    print(f"Full brief: labs show {n['num']}")


def cmd_status(_):
    state = load_state()
    briefs = all_briefs()
    counts = {s: 0 for s in STATUSES}
    for b in briefs:
        counts[get_status(state, b["num"])] += 1
    print(f"\n  {counts['passed']}/{len(briefs)} passed\n")
    active = False
    for b in briefs:
        st = get_status(state, b["num"])
        if st in ("in_progress", "in_review"):
            print(f"  {b['num']:02d}  {b['title']}  [{st}]")
            active = True
    if not active:
        print("  Nothing in progress. Run: labs next")
    print("")


def main():
    parser = argparse.ArgumentParser(
        prog="labs",
        description="Brief-driven infrastructure learning engine",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="all briefs and their status")
    p = sub.add_parser("show", help="print a full brief")
    p.add_argument("num", type=int)
    p = sub.add_parser("start", help="scaffold the project folder for a brief")
    p.add_argument("num", type=int)
    p = sub.add_parser("submit", help="submit for review (writes SUBMISSION.md)")
    p.add_argument("num", type=int)
    p = sub.add_parser("pass", help="mark a brief passed after review")
    p.add_argument("num", type=int)
    p = sub.add_parser("reopen", help="send an in-review brief back to doing")
    p.add_argument("num", type=int)
    p = sub.add_parser("note", help="append a timestamped note to project notes")
    p.add_argument("num", type=int)
    p.add_argument("text")
    sub.add_parser("next", help="the brief you should work on now")
    sub.add_parser("status", help="progress summary")
    args = parser.parse_args()
    commands = {
        "list": cmd_list,
        "show": cmd_show,
        "start": cmd_start,
        "submit": cmd_submit,
        "pass": cmd_pass,
        "reopen": cmd_reopen,
        "note": cmd_note,
        "next": cmd_next,
        "status": cmd_status,
    }
    commands[args.command](args)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
