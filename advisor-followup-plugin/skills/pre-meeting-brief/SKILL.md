---
name: pre-meeting-brief
description: Writes the brief for the next working day's client meetings, choosing the kind by the household's stage - an intro brief before an introduction, discovery prep before a discovery meeting, a plan readiness review before a plan presentation, and a follow-up brief for existing clients. Use when asked to prepare for tomorrow's meetings, to run the pre-meeting check, or from run-cycle. Verifies every open item first and leads with what is still open.
---

# Pre-meeting brief

## Before you start

1. Read `config.md` for the `calendar`, `crm_read`, `meetings`, `client_files`, `briefs`, `chat`, `status_board` and `ledger` roles.
2. Read `playbooks/definition-of-done.md`, `playbooks/sla.md`, `playbooks/stages.md` and `playbooks/required-documents.md`.
3. Read the status board and the ledger.

## Which role writes which brief

| Brief | When | Written by |
|---|---|---|
| Intro brief | Next meeting is an Introduction (household at `intro_scheduled`) | paraplanner |
| Discovery prep | Next meeting is a Discovery | paraplanner |
| Plan readiness review | Next meeting is a Plan presentation (household at `planning_requested`) | planner |
| Follow-up brief | Any other client meeting | paraplanner |

A run writes only the briefs its role owns and lists the others in its report under "for <role>".

## Steps

1. **Find tomorrow's client meetings** through the `calendar` role. Tomorrow is the next working day unless a date was given. Ignore internal meetings (no client), including huddles. If there are no client meetings tomorrow, write no brief and say so in the report.
2. **For each meeting**, find the household on the status board (create its row at `intro_scheduled` if the person is new, using the household-tracker skill) and set its Next meeting. Pick the brief kind from the table above.
3. **Once only.** If the household's Briefs field already lists this kind of brief for this meeting date, skip it.
4. **Verify every open item** for the household by invoking `verifier-agent`, only for items whose `owner_role` is the runner's role; for the others, use their recorded state and say "not re-checked".
5. **Gather by kind:**
   - **Intro brief:** what the CRM knows about the person (or "no CRM record yet"), how they were referred if recorded, and the standard introduction agenda from `action-matrix.md`. No client data that is not in the CRM or the calendar event.
   - **Discovery prep:** documents on file as "N of 5" with the missing ones by name (run the document check first), the discovery prep draft (if none exists yet, run the intake-builder skill's discovery_prep step now and link the result), what the introduction meeting said, the questions the discovery must answer to fill the intake's sections 1 to 4 (every row the draft marks "not yet on file" or "not stated" is a question), and "Advisory agreement: signed <date>" if a person wrote that in the household's History, otherwise "Advisory agreement: not confirmed".
   - **Plan readiness review:** the planning request case status, whether the plan document is on file (a file starting `plan-` in the client folder, or the board's Plan on file), the intake and intake changes links, documents N of N, every open item for the household, and anything the debrief left open. Lead with a one-line verdict: "Ready" only when the case is Closed or Resolved **and** the plan file is present; otherwise "Not ready: case still open", "Not ready: case closed but no plan on file", or "Not ready: <open items>".
   - **Follow-up brief:** as before: open items, done items with evidence, the last meeting's key points, and one line "Zocks created <N> tasks for the last meeting, <M> are closed" from the tasks `crm_read` finds for that meeting.
6. **Write the brief** with `references/brief-template.md` through the `briefs` role, named `YYYY-MM-DD <household> <brief kind>`. Order: blocked and open items first (with a "Stalled" line first if `sla.md` says the household is stalled), each with what is needed and from whom; then items waiting on others (`waiting_on` not `firm`), with whom and since when; then the kind's own section; then done items with evidence; then at most three talking points drawn only from open items and the client profile. No investment advice.
7. **Record it** on the status board: add to Briefs (date, kind, link), History "Brief written: <kind>".
8. **Send a notice** through the `chat` role to the approvals channel, addressed to the advisor (and the planner for a readiness review): household, meeting time, brief kind, link, number of open items.
9. **Regenerate the indexes** in the local build.

## Report

One line per meeting: household, time, brief kind, open items, done items, anything blocked, or "for <role>" if another role writes it.
