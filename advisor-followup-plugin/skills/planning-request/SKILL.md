---
name: planning-request
description: Prepares the planning request for a household that is ready for planning - a CRM case for the planning team carrying links to the intake, the intake changes and every required document - and puts it to the planner for approval. Use when a household reaches ready_for_planning, and to track its case once created. Mirrors the firm's case engine - plan, show the exact payload, write only after a person approves.
---

# Planning request

Read `config.md` for `crm_read`, `crm_write`, `client_files`, `chat`, `status_board` and `ledger`. Read `templates/planning-request-template.md`.

Owned by the planner (`team.md`). A run by any other role reports a household that is ready, and does nothing else.

## Prepare

1. **Check readiness** on the status board row: Intake set, Debrief set, Missing documents empty. If any is not true, do nothing and report what is missing.
2. **One request per household.** If Planning request already names a work item that is not Cancelled, do not create another.
3. **Check the CRM** through `crm_read` for an existing open case for this contact whose Subject starts "Planning request". If one exists, create the work item with `linked_crm_record` set to it and treat it as tracking that case.
4. **Create the work item:** `action_type: planning_request`, Tier B, `owner_role: planner`, `owner_agent: salesforce-agent`, approver the planner, `due` from `sla.md`. Source: "Household ready for planning: intake <date>, debrief <date>, <N of N> documents on file."
5. **Fill the payload** from the template: every link from the client folder (intake, intake changes, each required document), the folder link, the goals in brief from the intake. Put the whole payload under Proposed action. Links only: the CRM connector cannot attach files.
6. Status Awaiting Approval, History "Planning request prepared, awaiting the planner's approval".
7. **Post** the approval request through `chat` to the **operations** channel, addressed to the planner: item id, household, "intake, intake changes and N documents linked", "reply approve WI-NNNN or reject WI-NNNN".
8. Status board: Planning request = the work item id; History "Planning request prepared, WI-NNNN".

## Execute (after the planner approves)

Hand the item to `salesforce-agent`. With no CRM write access it posts the payload in the operations channel for a person to create, External ref "pending creation by Operations".

## Track

- Each run, look for the case through `crm_read` (Subject "Planning request: <household>"). When found: write its id to the item's `external_ref` and to the board's Planning request, move the household to `planning_requested`, History "Case <id> created".
- Each run, also look in the client folder for a file starting `plan-`. When found, set the board's Plan on file to it, History "Plan on file, <link>". The plan readiness review says "Ready" only when both the case is closed and this file exists.
- The item is Done only when the verifier finds the case Closed or Resolved.
