"""One client, end to end: Sam Reed from introduction to planning request.

Runs the whole new-client journey on local files, one step at a time, so it
can be shown without any connector. Between steps, run the loop in Cowork:
"Run run-cycle as everyone."

  python3 journey.py start    clean slate: only Sam's story, demo clock at today
  python3 journey.py next     move the story to the next step (see below)
  python3 journey.py status   where Sam is now
  python3 journey.py back     undo the last step and its run (restores the saved state)

Steps (each "next" plays the people's part, then you run the loop):
  1 intro      Sam's introduction notes arrive (Zocks)
  2 welcome    next working day: the advisor approves what is waiting;
               Sam returns the form and his account statements
  3 discovery  the day of Sam's discovery meeting (read from the calendar):
               the advisor sends the drafts and approves; notes arrive;
               Sam sends his tax return
  4 huddle     two working days later: the internal huddle notes arrive;
               the last two documents arrive
  5 planning   next working day: the planner approves the planning request

It touches only advisor-followup/{inbox,outbox,ledger,households,briefs,
client-files,salesforce}. It never edits config.md, playbooks or templates.
Works with the macOS system Python 3.9.
"""

import datetime as dt
import pathlib
import re
import shutil
import sys

REPO = pathlib.Path(__file__).resolve().parent
ROOT = REPO / "advisor-followup"
STEPS = REPO / "journey" / "steps"
STATE = REPO / "journey" / ".state"
SNAP = REPO / "journey" / ".snapshots"
LIVE = ["inbox", "outbox", "ledger", "households", "briefs", "client-files", "salesforce"]
NAMES = ["intro", "welcome", "discovery", "huddle", "planning"]


def wd(d, n):
    """Move n working days (Mon-Fri) from d."""
    step = 1 if n >= 0 else -1
    while n:
        d += dt.timedelta(days=step)
        if d.weekday() < 5:
            n -= step
    return d


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def append(rel, line):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8").rstrip("\n") if p.exists() else ""
    with p.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n" + line + "\n")


def front(path):
    m = re.match(r"---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip()
    return out


def today():
    t = (ROOT / "outbox" / "today.txt").read_text(encoding="utf-8").split()
    return dt.date.fromisoformat(t[0])


def set_clock(d, hm):
    write("outbox/today.txt", f"{d.isoformat()} {hm}\n")


def sam_household():
    for p in sorted((ROOT / "households").glob("*.md")):
        if p.name != "BOARD.md" and "Sam Reed" in front(p).get("clients", ""):
            return p, front(p)
    return None, {}


def sam_folder():
    _, h = sam_household()
    folder = h.get("client_folder") or "client-files/reed"
    (ROOT / folder).mkdir(parents=True, exist_ok=True)
    return folder


def sam_id():
    _, h = sam_household()
    cid = h.get("crm_contacts", "")
    if cid:
        return cid.split(",")[0].strip()
    for p in (ROOT / "salesforce" / "contacts").glob("*.md"):
        if front(p).get("name") == "Sam Reed":
            return front(p).get("id", "")
    return ""


def sam_items():
    for p in sorted((ROOT / "ledger").glob("WI-*.md")):
        f = front(p)
        if f.get("client") == "Sam Reed" or f.get("household") == "HH-REED":
            yield p, f


def drop(step, d):
    """Copy a step's notes into the inbox and its documents into Sam's folder."""
    src = STEPS / step
    subs = {"{{DATE}}": d.isoformat(), "{{SAM_ID}}": sam_id()}
    for f in sorted((src / "inbox").glob("*.md")) if (src / "inbox").exists() else []:
        text = f.read_text(encoding="utf-8")
        for k, v in subs.items():
            text = text.replace(k, v)
        write(f"inbox/{f.name}", text)
        print(f"  meeting notes arrived: inbox/{f.name}")
    folder = None
    for f in sorted((src / "client-files").glob("*.md")) if (src / "client-files").exists() else []:
        folder = folder or sam_folder()
        write(f"{folder}/{f.name}", f.read_text(encoding="utf-8").replace("{{DATE}}", d.isoformat()))
        print(f"  document arrived: {folder}/{f.name}")


def approve_waiting(d, hm):
    """The advisor (and the planner, for a planning request) approve what is waiting for Sam."""
    n = 0
    for p, f in sam_items():
        if f.get("status") != "Awaiting Approval":
            continue
        wi = f["id"]
        if f.get("action_type") == "planning_request":
            append("outbox/teams-operations.md", f"- {d} {hm} [L. Planner] approve {wi}")
            print(f"  L. Planner: approve {wi} (planning request)")
        elif f.get("action_type") == "schedule_meeting":
            append("outbox/teams-approvals.md", f"- {d} {hm} [R. Advisor] approve {wi} slot 1")
            print(f"  R. Advisor: approve {wi} slot 1")
        else:
            append("outbox/teams-approvals.md", f"- {d} {hm} [R. Advisor] approve {wi}")
            print(f"  R. Advisor: approve {wi} ({f.get('action_type')})")
        n += 1
    if not n:
        print("  nothing waiting for approval")


def advisor_sends(d):
    """The advisor sends the drafts the loop saved (the loop itself never sends)."""
    for p, f in sam_items():
        if f.get("status") == "In Progress" and f.get("action_type") in ("client_email", "send_form"):
            text = p.read_text(encoding="utf-8").rstrip("\n")
            with p.open("w", encoding="utf-8", newline="\n") as fh:
                fh.write(text + f"\n- {d} 09:05 R. Advisor: sent on {d}\n")
            print(f"  R. Advisor sent the draft for {f['id']} ({f.get('action_type')})")


def ops_done(d):
    """Operations finish the hand-offs given to them."""
    for p, f in sam_items():
        if f.get("status") == "In Progress" and f.get("action_type") == "assign_task":
            append("outbox/teams-operations.md", f"- {d} 09:10 [O. Ops] done {f['id']}")
            print(f"  O. Ops: done {f['id']}")


def discovery_date(after):
    cal = (ROOT / "outbox" / "calendar.md").read_text(encoding="utf-8")
    for line in cal.splitlines():
        if "Sam Reed" in line and "iscovery" in line:
            m = re.search(r"\| (\d{4}-\d\d-\d\d) \|", line)
            if m:
                return dt.date.fromisoformat(m.group(1)), True
    return wd(after, 5), False


def start():
    base = dt.date.today()
    while base.weekday() >= 5:
        base += dt.timedelta(days=1)
    for f in LIVE:
        shutil.rmtree(ROOT / f, ignore_errors=True)
        (ROOT / f).mkdir(parents=True)
    for sub in ("contacts", "cases", "tasks"):
        (ROOT / "salesforce" / sub).mkdir()
    write("salesforce/README.md", "# Stand-in for Salesforce\n\nOne file per record: `contacts/`, `cases/`, `tasks/`. Empty at the start of the journey: Sam Reed is not a client yet. Fictional.\n")
    write("ledger/INDEX.md", "# Ledger index\n\nNo work items yet.\n")
    write("households/BOARD.md", "# Status board\n\nNo households yet.\n")
    write("briefs/README.md", "# Briefs\n\nOne file per brief, written the working day before a client meeting.\n")
    write("client-files/README.md", "# Client files\n\nOne folder per household: the documents the client sends, and the intake the firm builds.\n")
    write("outbox/teams-approvals.md", "# Teams channel: approvals (stand-in)\n\nMembers: R. Advisor, P. Para, M. Manager, the follow-up system.\n")
    write("outbox/teams-operations.md", "# Teams channel: operations (stand-in)\n\nMembers: O. Ops, L. Planner, R. Advisor, the follow-up system.\n")
    rows = [
        (wd(base, 1), "09:00", "(internal)", "Team meeting", "R. Advisor, O. Ops, M. Manager"),
        (wd(base, 3), "14:00", "(internal)", "Compliance review", "R. Advisor, M. Manager"),
        (wd(base, 6), "15:00", "(internal)", "Training", "R. Advisor"),
        (wd(base, 8), "14:00", "(internal)", "Team meeting", "R. Advisor, O. Ops"),
    ]
    cal = ["# Calendar: R. Advisor (stand-in for Outlook)", "",
           "Working hours: weekdays 09:00 to 17:00. Meetings are 60 minutes unless stated. A slot is free if no row below covers it.", "",
           "| Event id | Date | Time | Client | Subject | Attendees | Status |", "|---|---|---|---|---|---|---|",
           f"| EVT-{base:%Y%m%d}-1000-SR | {base} | 10:00 | Sam Reed | Introduction | Sam Reed, R. Advisor | Held |"]
    cal += [f"| EVT-{d:%Y%m%d}-{t.replace(':', '')}-INT | {d} | {t} | {c} | {s} | {a} | Confirmed |" for d, t, c, s, a in rows]
    write("outbox/calendar.md", "\n".join(cal) + "\n")
    set_clock(base, "08:00")
    STATE.write_text("0\n")
    shutil.rmtree(SNAP, ignore_errors=True)
    print(f"Clean slate. Demo clock: {base} 08:00. Sam Reed is not in Salesforce yet.")
    print("Next: python3 journey.py next")


def nxt():
    n = int(STATE.read_text().strip()) if STATE.exists() else 0
    if n >= len(NAMES):
        print("The journey is complete. Start again with: python3 journey.py start")
        return
    save(n)
    n += 1
    print(f"Step {n} of {len(NAMES)}: {NAMES[n - 1]}")
    if n == 1:
        d = today()
        set_clock(d, "17:00")
        drop("1-intro", d)
    elif n == 2:
        d = wd(today(), 1)
        set_clock(d, "10:00")
        approve_waiting(d, "09:30")
        drop("2-welcome", d)
    elif n == 3:
        d, found = discovery_date(wd(today(), 1))
        print(f"  discovery meeting date: {d}" + ("" if found else " (no booked event found, using 5 working days on)"))
        set_clock(d, "17:00")
        advisor_sends(d)
        ops_done(d)
        approve_waiting(d, "09:30")
        drop("3-discovery", d)
    elif n == 4:
        d = wd(today(), 2)
        set_clock(d, "16:00")
        append("outbox/calendar.md", f"| EVT-{d:%Y%m%d}-1400-INT | {d} | 14:00 | (internal) | Huddle: Reed household | R. Advisor, P. Para, L. Planner | Held |")
        print("  huddle held today (calendar)")
        advisor_sends(d)
        ops_done(d)
        approve_waiting(d, "09:30")
        drop("4-huddle", d)
    elif n == 5:
        d = wd(today(), 1)
        set_clock(d, "10:00")
        advisor_sends(d)
        ops_done(d)
        approve_waiting(d, "09:30")
    STATE.write_text(f"{n}\n")
    print(f"Demo clock: {(ROOT / 'outbox' / 'today.txt').read_text().strip()}")
    print('Now run the loop in Cowork: "Run run-cycle as everyone."')


def save(n):
    dst = SNAP / str(n)
    shutil.rmtree(dst, ignore_errors=True)
    for f in LIVE:
        shutil.copytree(ROOT / f, dst / f)


def back():
    n = int(STATE.read_text().strip()) if STATE.exists() else 0
    src = SNAP / str(n - 1)
    if n == 0 or not src.exists():
        print("Nothing to undo.")
        return
    for f in LIVE:
        shutil.rmtree(ROOT / f, ignore_errors=True)
        shutil.copytree(src / f, ROOT / f)
    STATE.write_text(f"{n - 1}\n")
    print(f"Back to the state before step {n}. Run: python3 journey.py next")


def status():
    n = int(STATE.read_text().strip()) if STATE.exists() else 0
    print(f"Step {n} of {len(NAMES)}" + (f" ({NAMES[n - 1]})" if n else " (not started)"))
    _, h = sam_household()
    if not h:
        print("Sam Reed is not on the status board yet.")
        return
    for k in ("stage", "crm_contacts", "documents_on_file", "missing_documents", "intake", "intake_changes", "planning_request"):
        print(f"  {k}: {h.get(k, '')}")
    for p, f in sam_items():
        print(f"  {f['id']} {f.get('action_type')}: {f.get('status')}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    {"start": start, "next": nxt, "status": status, "back": back}.get(cmd, status)()
