# Household stages: the new-client journey

A household is the family the firm serves as one client (one person, or a couple and their dependants). Each household has one row on the status board. This playbook says which stage a household is in, what moves it on, and what the loop does there.

## The stages

| Stage | Moves here when | What the loop does in this stage | Owner role |
|---|---|---|---|
| `intro_scheduled` | An introduction meeting with a person who has no household yet is on the calendar | Write the intro brief the working day before the meeting | paraplanner |
| `intro_held` | The introduction meeting's notes arrive | Normal follow-ups for an Introduction meeting (action matrix). If the prospect is proceeding: the welcome email with the form and document checklist, and scheduling discovery; otherwise one question to the advisor (`proceed` or `close`). Document check every run from here on, chasing on the cadence. Discovery prep draft when the discovery meeting is within two working days | paraplanner |
| `discovery_held` | The discovery meeting's notes arrive | Finalise the intake document, once, starting from the discovery prep draft if one exists. Then run the document check | paraplanner |
| `collecting_documents` | The intake exists and at least one required document is missing | Re-check the client files every run. Chase what is missing on the cadence in `sla.md` | paraplanner |
| `debrief_held` | The internal huddle (meeting type Debrief) notes arrive | Write the intake changes document with only what changed. Then run the document check | paraplanner |
| `ready_for_planning` | The intake exists, the debrief has been held, and every required document is on file | Prepare the planning request for the planner's approval | planner |
| `planning_requested` | The planning request case exists in the CRM | Track the case. Write the plan readiness review the working day before the plan meeting | planner |
| `plan_presented` | The plan meeting's notes arrive | Normal follow-ups for a Plan meeting. The household leaves the onboarding journey | planner |
| `existing_client` | A household that finished onboarding before this system, or after `plan_presented` | Normal follow-ups for its meetings only. No stage work | paraplanner |
| `not_proceeding` | A person says so in the household's History or in a channel (`close HH-XXXX`) | Nothing. Kept on the board under Closed | none |

## Rules

1. **Order.** Documents are requested with the welcome email and can arrive at any point from the introduction onwards, so `collecting_documents` and `debrief_held` may happen in either order. A household is `ready_for_planning` only when both are satisfied. If the debrief is held while documents are still missing, the stage is `collecting_documents` and the board's "Debrief" column shows the date it was held.
2. **Never backwards.** The loop never moves a household to an earlier stage. If the evidence seems to say it should (for example a document disappeared from the folder), leave the stage, add a History line saying what was seen, and mention it in the report.
3. **Finalised once.** A household has at most one discovery prep draft (before discovery), one intake (finalised once after discovery) and one intake changes document per debrief. The draft is an input to the intake, never a second intake. If the household already has the document in question, do not write another; say so in History.
3a. **Proceeding.** At `intro_held`, the client-facing follow-ups are created only once the household is known to be proceeding: the introduction summary said so, or the advisor replied `proceed HH-XXXX` in the approvals channel (recorded in History as "Proceeding, per <name> on <date>", or "Proceeding, per the introduction summary" when the summary says so). A `close HH-XXXX` reply moves the household to `not_proceeding`.
4. **Evidence for every move.** Every stage change appends a History line with the date, the new stage, and the evidence (meeting id, document names, case id).
5. **Unknown people.** A client meeting with a name that matches no household and no CRM contact starts a new household at `intro_scheduled` (meeting upcoming) or `intro_held` (notes arrived). Never guess an email address.
6. **Closed.** `plan_presented`, `existing_client` and `not_proceeding` households are not part of the onboarding sweep. They still get normal meeting follow-ups.
