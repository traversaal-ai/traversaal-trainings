# Team: who is who, and what each role owns

Every run starts by finding the person running it in this table and taking their role. A run acts only on what that role owns. Read through the `team` role in `config.md`.

## People

| Name | Role | Email | Chat name | Channel for their work |
|---|---|---|---|---|
| R. Advisor | advisor | r.advisor@example.com | R. Advisor | approvals |
| P. Para | paraplanner | p.para@example.com | P. Para | approvals |
| L. Planner | planner | l.planner@example.com | L. Planner | operations |
| O. Ops | operations | o.ops@example.com | O. Ops | operations |
| M. Manager | manager | m.manager@example.com | M. Manager | approvals |

## Who is running

- A command names the runner with `as <name>` or `as <role>`, for example `run-cycle as P. Para` or `run-cycle as planner`.
- `as everyone` runs each role in turn, in the order paraplanner, planner, advisor. Use it for a single scheduled run or a demo.
- If no runner is named, use the default below and say so in the report.

Default runner: P. Para

## What each role owns

A role "owns" a household stage when it does that stage's work, and owns a work item when the item's `owner_role` is that role.

| Role | Owns these household stages | Owns these work items | Approves |
|---|---|---|---|
| paraplanner | intro_scheduled, intro_held, discovery_held, collecting_documents, debrief_held | Processing meeting notes; building and updating the intake; checking documents; briefs; every item with `owner_role: paraplanner` | Nothing client-facing |
| advisor | none (the advisor meets the client; the paraplanner prepares) | Items with `owner_role: advisor` | client_email, send_form, schedule_meeting, create_document, create_invoice, salesforce_case, assign_task, except planning requests |
| planner | ready_for_planning, planning_requested, plan_presented | Planning requests; plan readiness reviews; items with `owner_role: planner` | Planning requests (`action_type: planning_request`) |
| operations | none | Carries out cases and tasks handed to the operations channel and replies `done WI-0000` | Nothing |
| manager | none | Receives the third escalation | Nothing |

A run never changes an item or a household it does not own, with one exception: any run may read anything, and any run may record a person's approval or rejection it finds in a channel, because that is bookkeeping, not action.
