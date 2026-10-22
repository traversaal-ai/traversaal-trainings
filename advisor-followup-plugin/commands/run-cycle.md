---
description: The recurring loop, run about twice a day. Finds who is running it and their role, sweeps meetings held and upcoming, moves every household on the status board, does the stage work that role owns (intake, document check, planning request, briefs), runs the monitor for that role's items, and posts a short digest. Argument - "as <name>", "as <role>" or "as everyone".
---

Run one cycle of the follow-up loop.

## 0. Who is running

1. Read `config.md`, then the `team` role. Take the runner from the argument (`as P. Para`, `as planner`, `as everyone`); with no argument use the default runner in the team list and say so.
2. If the argument is `as everyone`, run steps 1 to 7 once per role in the order paraplanner, planner, advisor, then step 8 once.
3. Note today's date and time, and the previous cycle's time from the last "Cycle" History line on the status board (or 24 hours ago if none).

## 1. Read the state

Read the status board and the ledger in full, and `playbooks/stages.md`, `playbooks/sla.md`, `playbooks/required-documents.md`, `playbooks/approval-rules.md`, `playbooks/definition-of-done.md`.

## 2. Sweep meetings

1. **Held:** list meeting summaries through the `meetings` role that are new (not in the ledger and not in any household's Meetings processed). Paraplanner: run `process-meetings` on them, oldest first. Other roles: list them in the report as "for paraplanner".
2. **Upcoming:** read the `calendar` for client meetings in the next two working days and huddles (`Huddle:` titles) in the next two working days. Set each household's Next meeting (any role may, it is bookkeeping). A person with no household: the paraplanner creates the row at `intro_scheduled`.

## 3. Move households

For every household not in `plan_presented`, `existing_client` or `not_proceeding`, work out its stage with the household-tracker skill. Make the moves the runner's role may make; list the others under "for <role>".

## 4. Stage work for this role

- **Paraplanner:**
  - `intro_held` whose History says "Proceeding" (the advisor replied `proceed`) and that has no `send_form` and no `schedule_meeting` item yet: create the welcome email with the form and checklist, and the discovery scheduling, as standard Introduction follow-ups (`action-matrix.md`), and hand them to their agents.
  - `intro_held` or `discovery_held` with a Discovery meeting within the next two working days and no discovery prep draft, and no `discovery_prep` item: create one and run the intake-builder skill's discovery_prep step.
  - `discovery_held` with no intake, and no `build_intake` item: create one and run the intake-builder skill.
  - `debrief_held`, or Debrief set with no intake changes, and no `update_intake` item: create one and run the intake-builder skill.
  - `intro_held`, `discovery_held`, `collecting_documents` or `debrief_held`: run the document-check skill (it chases on the cadence).
- **Planner:**
  - `ready_for_planning`: run the planning-request skill to prepare the request.
  - `planning_requested`, or a planning request item In Progress: run the planning-request skill's Track step.
- **Advisor:** no stage work. The advisor's part is approving; step 7 tells them what is waiting.

## 5. Monitor this role's items

Run the steps of `run-monitor` for the items whose `owner_role` is the runner's role: read approvals and rejections (for any item, bookkeeping), execute approved items, verify open items, apply the stop conditions, escalate on breach, and the "Before the next meeting" and "Who we are waiting on" rules in `sla.md` (only `waiting_on: firm` items go up the ladder).

## 6. Briefs

Run the pre-meeting-brief skill for the next working day, writing only the brief kinds this role owns.

## 7. Digest for this role

Post one message through the `chat` role (approvals channel for paraplanner and advisor, operations channel for planner), addressed to the runner (for the advisor run: to the advisor):

```
<Role> cycle, <date time>
Households: <n> in progress. Moved: <household old → new>, ...
Waiting for you: <item ids with one-line action> (advisor: everything Awaiting Approval with them as approver)
Done since last cycle: <item ids>
Late: <item ids and how late>
Waiting on others: <item id, with whom, since when>
Stalled: <household, stage, business days in it, reason> (the stalled rule in sla.md)
Briefs: <household, kind, link>
For other roles: <role: what>
```

Skip the message if every line except Households would be empty, and say so in the report.

## 8. Close the cycle

Append "Cycle <date time> as <runner(s)>" to the History of every household the cycle changed. In the local build, regenerate `ledger/INDEX.md` and `households/BOARD.md`.

Report: runner and role(s); meetings processed; households moved (old → new, evidence); intakes built or changed (links); document checks (household, N of M, request or reminder created); planning requests prepared or tracked; approvals read; items executed, verified Done, escalated, blocked; briefs written; anything for another role; anything that needs a person. One line each.
