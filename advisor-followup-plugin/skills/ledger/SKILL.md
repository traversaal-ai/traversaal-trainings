---
name: ledger
description: How to read and write the follow-up ledger, the shared list of work items - a folder of Markdown files with an index in the local build, a shared list or Salesforce records in the live settings, as config.md says. Use whenever a work item is created, updated, approved, verified or escalated, and whenever the index must be regenerated. Enforces the record format, the status rules, the approval rule, the role rule and the no-duplicates rule.
---

# Ledger

The ledger is the shared list of work items and the audit trail. The `ledger` role in `config.md` says where it is:

- **Local build:** `ledger/`, one file per work item using `references/work-item-template.md`, and `ledger/INDEX.md` as the index.
- **Live settings:** a record per work item in the system the `ledger` row of `config.md` names (a shared list, or Salesforce records). Each field of the template is a column or field of the same name; Source, Proposed action and History are long text. There is no index; the list is the index. The `config.md` row says exactly how to read all records, create one, update one and append a History line, including the tool or command names. Use only what it says.

Everything below applies to every setting. "Record" means the file, the row or the Salesforce record.

## Reading

- Start every run by reading the whole ledger (local: `INDEX.md`, then the files you need; live: the read described in `config.md`, paging until there is no more).
- A work item exists for a commitment if any record has the same `meeting_id` and the same `action_type` with a matching Source, or the same `linked_crm_record`.
- The next id is the highest existing `WI-NNNN` plus one, zero-padded to four digits.
- Records written before `household` and `owner_role` existed: take the household from the client's name on the status board, and the owner role from the action matrix.

## Writing a new record

Fill every field of the template, including `household` (from the status board) and `owner_role` (from the action matrix). Quote the Source exactly. First History line: `YYYY-MM-DD HH:MM Proposed by <orchestrator | skill name>`.

Live: create the record as `config.md` describes, with every field. Keep the returned record id for later updates. Where the backend assigns ids itself (an auto-number), read the id back and use it; otherwise set `id` to the next `WI-NNNN`.

## Updating a record

- Change fields in place. Never delete fields.
- Every change of `status`, `approval`, `external_ref`, `evidence` or `escalations` appends one dated History line saying who or what changed it and why.
- `last_checked` is set by every monitor run that looks at the record, even when nothing else changes.
- Never remove or rewrite existing History lines. Live: where History is one text field, read the record first and write the whole old History plus the new line; where History is its own list of records (Salesforce), create one new history record per line and never edit or delete one. A write that drops lines is a defect.

## Who may change a record

Only a run whose role is the record's `owner_role` (see `team.md`) may prepare, execute, verify, escalate or change it. Any run may read every record, and any run may record a person's approval or rejection found in a channel (bookkeeping). A run that finds work on a record it does not own lists it in its report under "for <role>".

## Status and approval rules

| Status | approval must be | Who sets it |
|---|---|---|
| Proposed | pending (Tier B) or not required (Tier A) | orchestrator or the skill that created it |
| Awaiting Approval | pending | the owner sub-agent, after preparing the action |
| Approved | approved, with approved_by and approved_at | the monitor, after reading a person's decision |
| In Progress | approved or not required | the owner sub-agent or skill, after executing or handing over |
| Done | approved or not required | the verifier only, with evidence |
| Blocked | unchanged | the monitor, on service level breach or tool failure, with the reason in History |
| Cancelled | rejected or not required | the monitor on rejection; the orchestrator for Tier C; the monitor when a meeting has passed |

No agent that performed an action may set Done on its own item.

## Reading approvals

A decision counts if either:
- a person changed the record's `approval` to `approved` or `rejected` (if `approved_by` is empty, write "record edit" and the current time), or
- the `chat` role's approvals or operations channel contains `approve WI-NNNN` or `reject WI-NNNN` after the request was posted. Write the person's name and the time into the record.

An approval for a `planning_request` counts only from the planner (`team.md`). Any other approval counts from the item's approver or a person `team.md` lists with the advisor or manager role.

An approval with an instruction ("approve WI-0102, slot 2") is an approval; record the instruction in History so the owner agent applies it.

The same time rule applies to every channel reply: an `approve`, `reject` or `done` line counts only if it was posted after the request or hand-off it answers, as recorded in the item's History. Replies from before that moment belong to an earlier round and are ignored.

## Regenerating the index (local build only)

Rewrite `INDEX.md` completely from the files at the end of every run. Two tables, Open (Proposed, Awaiting Approval, Approved, In Progress, Blocked) and Closed (Done, Cancelled), newest id first within each. Columns: Id, Household, Client, Action, Owner role, Status, Approval, Due, Last checked, Escalations. Leave an empty value as an empty cell; never fill it with a dash or placeholder. Put the regeneration time in the header. Never edit `INDEX.md` by hand and never treat it as the source of truth; the files are.
