# Service levels and escalation

Business days only. "First movement" means the item has left its starting state: a case has an owner and activity, a task has been acknowledged, an approval has been answered.

| Action type | Service level to first movement | Service level to done |
|---|---|---|
| salesforce_case | 1 business day | 5 business days |
| schedule_meeting | 1 business day | 3 business days |
| send_form | same day | 7 business days (client response) |
| client_email | same day | 2 business days |
| create_invoice | 1 business day | 3 business days |
| create_document | 1 business day | 3 business days |
| assign_task | same day | the task's due date |
| approval request (any Tier B item in Awaiting Approval) | 1 business day | 2 business days |
| discovery_prep, build_intake, update_intake | same day | 1 business day |
| planning_request | 1 business day | 5 business days (case closed by the planning team) |

## Missing documents

A household in `collecting_documents` is chased on this cadence, counted from the day the request email was sent (its "sent on <date>" History line; if there is none yet, the cadence has not started):

| Business days since the request | Action |
|---|---|
| 3 | First reminder: a `client_email` item listing every document still missing, for the advisor's approval |
| 6 | Second reminder, same form |
| 9 | Stop emailing. Escalate to the advisor in the approvals channel: "<Household> still missing <documents> after two reminders." |

Never send a reminder for a document that arrived since the last one. Never more than one reminder item open per household.

## Before the next meeting

Everything open for a household should be done **2 business days before its next client meeting**. When an open item's `due` is later than that date, use that date instead. When the next meeting is closer than the service level allows, say so in the brief rather than escalating.

## Who we are waiting on

Every item carries `waiting_on` (see `work-item-template.md`). It decides what chasing means:

| waiting_on | What the loop does | Where it shows |
|---|---|---|
| `firm` | The service levels above and the escalation ladder below | Escalations in chat; the brief's "Needs attention" table |
| `client` | The missing-documents cadence above (reminder at day 3 and 6, the advisor told at day 9). Never the ladder | The brief's "Waiting on others" section: "with the client since <date>, reminded <n> times" |
| `custodian` | No reminders and no ladder; nobody in the firm can speed it up. The verifier checks the case or the account each run | The brief's "Waiting on others": "with the custodian since <date>" |
| `third_party` | One reminder through the advisor after the service level, then nothing more | The brief's "Waiting on others": "with <party> since <date>, advisor reminded <date>" |

An item switches to `custodian` or `third_party` when it is handed over (the agent that executes it records the hand-over date in History), and back to `firm` when the outside party has done its part and the firm must act again.

## Stalled households

A household that has not changed stage for longer than this is stalled:

| Stage | Business days before "stalled" |
|---|---|
| `collecting_documents` | 15 |
| `intro_scheduled`, `intro_held`, `discovery_held`, `debrief_held`, `ready_for_planning`, `planning_requested` | 5 |

Counted from the board's `In stage since`. A stalled household is listed under "Stalled" in every digest and at the top of the advisor's next brief for it, with the reason in one line (missing documents, no discovery booked, no debrief held, planning request not approved, case still open). No escalation ladder: this is visibility, not chasing. It stops being listed when the stage changes.

## When to escalate

Escalate when an item with `waiting_on: firm` has passed its service level to first movement with no movement, or its service level to done with no evidence of completion. Service levels and `due` dates of an item approved late are counted from its approval, never from before it, so a hand-off is never escalated on the day it is made. Never earlier, and never for an item waiting on the client, the custodian or a third party (those follow the table above).

## Interval between escalations

Send the next escalation only after one further business day has passed since the previous escalation with still no movement. Never send two escalations for the same item in the same business day.

## Escalation ladder

| Escalation | Who is told | Channel |
|---|---|---|
| 1 | The item's owner (the operations team for cases and tasks, the approver for approvals) | chat, operations channel or approvals channel |
| 2 | The advisor | chat, approvals channel |
| 3 | The advisor's manager | chat, approvals channel |

After the third escalation, stop. Set `status: Blocked`, write "handed to a person after three escalations" in History, and list the item at the top of every brief until a person resolves it.

## Stop conditions

Do not escalate, and do not keep checking, when:

- the item is Done or Cancelled;
- the client meeting the item was for has already taken place (then set Blocked with reason "meeting passed" and list it in the next brief);
- `escalations` is already 3.

## Message wording

Escalation 1: "Reminder: WI-0000 (<client>, <action>) has had no movement since <date>. Due <date>."
Escalation 2: "<Advisor>, WI-0000 (<client>, <action>) is past its service level and Operations has not responded. Due <date>."
Escalation 3: "<Manager>, WI-0000 (<client>, <action>) is past its service level after two reminders. Due <date>. Needs a decision."
