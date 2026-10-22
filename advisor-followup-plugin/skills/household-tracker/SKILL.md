---
name: household-tracker
description: Keeps the status board, one row per client household, showing its stage in the new-client journey (intro, discovery, collecting documents, debrief, ready for planning, planning requested), what has been done for it and by whom, and which documents are in. Use whenever a household is created, a meeting for it is held or booked, its intake or documents change, or its stage must be worked out. Enforces the stage rules in playbooks/stages.md.
---

# Household tracker

The status board is the source of truth for **where each household is**. The ledger is the source of truth for **each task**. Read both; never copy one into the other.

Read `config.md` for the `status_board`, `team`, `calendar`, `meetings`, `crm_read` and `client_files` roles, and `playbooks/stages.md` before changing anything.

## The row

Every household has exactly one row (local: `households/<folder>.md` using `references/household-template.md`; live: a list row or a Salesforce Account record, read and written exactly as the `status_board` row of `config.md` says). Fields:

| Field | Holds |
|---|---|
| Household id | `HH-` and the main client's surname in capitals, for example `HH-SMITH`. Never reused |
| Household | Display name, for example "Smith household" |
| Clients | Every client's full name |
| CRM contacts | Their CRM contact ids |
| Advisor | From the meeting or the CRM |
| Stage | One value from `stages.md` |
| Owner role | The role that owns the current stage (`stages.md`) |
| In stage since | The date of the last stage change (the date of the creation line if there has been none). The stalled rule in `sla.md` counts from it |
| Client folder | Link or path to the household's client files folder |
| Last meeting | Id, date and type of the last meeting held |
| Next meeting | Date, time and type of the next client meeting on the calendar, or empty |
| Meetings processed | Every meeting id whose follow-ups were created, comma separated |
| Briefs | Each brief written: date, type, link |
| Discovery prep | Link and date of the draft intake written before the discovery meeting. Empty until written |
| Intake | Link and date. Empty until built |
| Debrief | Date of the debrief meeting, or empty |
| Intake changes | Link and date. Empty until written |
| Documents on file | "N of M" against `playbooks/required-documents.md` |
| Missing documents | Names of the missing documents, or empty |
| Planning request | Work item id and, once created, the CRM case id |
| Plan on file | Link to the finished plan document in the client folder (a file starting `plan-`), set by the planning-request skill's Track step. Empty until the planning team saves it |
| Last updated | Date, time and the role that updated it |
| History | Dated lines, newest last. Never delete or rewrite a line |

## Finding the household for a person or meeting

1. Match on the CRM contact id, then on full name and email, against the Clients and CRM contacts fields.
2. A couple: either name matches the household.
3. No match and the meeting is with a client: create a new row at `intro_scheduled` (meeting upcoming) or `intro_held` (notes arrived). Client folder: create the household's folder as the `client_files` row of `config.md` says, and put its path or link in Client folder; only if that row gives no way to create one, leave it empty and say so.
4. Never create two rows for one household. If two rows look like the same family, change neither and report it.

## Replies about a household

Read through the `chat` role, approvals channel, and apply only when the poster has the advisor or manager role in `team.md` (paraplanner for `proceed`):

- `close HH-XXXX`: the household is not proceeding (rule 1 below).
- `proceed HH-XXXX`: the prospect is going ahead. Append History "Proceeding, per <name> on <date>", set the gate item ("Is <name> proceeding?") to Done with that reply as evidence, and leave the stage at `intro_held`; the paraplanner's next run creates the welcome and the discovery scheduling (`run-cycle` step 4).
- `huddle HH-XXXX <text>` is not handled yet; report it as "for a person".

## Working out the stage

Apply `stages.md` in this order, and stop at the first rule that moves the household. Only move forward.

1. A `close HH-XXXX` reply in chat, or a History line by a person saying the household is not proceeding: `not_proceeding`.
2. Notes of a Plan meeting arrived: `plan_presented`.
3. A planning request case exists in the CRM: `planning_requested`.
4. Intake exists, Debrief set, Missing documents empty: `ready_for_planning`.
5. Notes of a Debrief arrived: set Debrief. If documents are complete it is rule 4 next run; otherwise `collecting_documents` stays or becomes current.
6. Intake exists and documents are missing: `collecting_documents`.
7. Notes of a Discovery meeting arrived: `discovery_held`.
8. Notes of an Introduction meeting arrived: `intro_held`.
9. An Introduction meeting is on the calendar for a household with no notes yet: `intro_scheduled`.

Every move: set Stage and Owner role, set In stage since to today, set Last updated, append History `YYYY-MM-DD HH:MM <old> → <new>. Evidence: <meeting id | documents | case id>.`

After working out the stage, apply the stalled rule in `sla.md`: if the household has been in its stage longer than the threshold, it is listed under "Stalled" in the run's digest and report, with the reason. Nothing on the row changes.

## Who may change a row

- Any run may read the board.
- A run may change a row only when the runner's role owns the household's **current** stage (`team.md`), with two exceptions any run may make because they are bookkeeping: setting Next meeting from the calendar, and moving the household forward when the evidence for the move was produced by the runner's own work (for example the planner's approved request creates the case, so the planner moves `ready_for_planning` to `planning_requested`).
- When a run finds a move it may not make, it leaves the row and lists the move in its report under "for <role>".

## Regenerating the board (local build only)

Rewrite `households/BOARD.md` from the household files at the end of every run. Two tables: In progress (every stage except `plan_presented`, `existing_client`, `not_proceeding`) ordered by stage then next meeting, and Closed. Columns: Household id, Household, Stage, Owner role, In stage since, Next meeting, Documents on file, Missing documents, Intake, Planning request, Last updated. In the live settings the list or the Salesforce records are the board and nothing is regenerated.
