# Action matrix: standard follow-ups by meeting type

The orchestrator takes the meeting summary's own action items first, then adds the standard follow-ups below for the meeting type. If a standard follow-up is already covered by an action item, do not add it twice.

| Meeting type | Standard follow-ups | Action type |
|---|---|---|
| Introduction | Confirm or update the client's contact record | salesforce_case (note only, Tier A if no change needed) |
| | Introduction summary note on the client record (due the next business day) | assign_task |
| | Welcome email carrying the client information form and the list of required documents (one email, only if the prospect is proceeding, see below) | send_form |
| | Schedule the discovery meeting (only if the prospect is proceeding) | schedule_meeting |
| Discovery | Confirm discovery notes are on the client record | assign_task |
| | Request the documents still missing from the required list, plus any the meeting named (one email) | client_email |
| | A case for any account action mentioned in the meeting | salesforce_case |
| | Schedule the plan meeting, with a window that starts no earlier than 10 working days after the discovery (the plan needs the documents, the debrief and the planning team first) | schedule_meeting |
| Plan | Invoice or engagement form | create_invoice |
| | Tasks for Operations for each implementation step (open accounts, transfers, beneficiary updates, forms) | assign_task |
| | A case for each implementation step that needs a Salesforce record | salesforce_case |
| | Schedule the financial check-up | schedule_meeting |
| Financial check-up | Confirm the review summary is on the client record | assign_task |
| | A case for any account change mentioned in the meeting | salesforce_case |
| | Request updated documents | client_email |
| | Schedule the next check-up | schedule_meeting |
| Debrief (internal huddle between the client-facing and planning teams) | Write the intake changes document with only what changed | update_intake (Tier A) |
| | Request any further documents named in the huddle | client_email |
| Unclear | Nothing standard. Create one work item of type assign_task asking the advisor to confirm the meeting type, Tier B. | assign_task |

## Introduction: is the prospect proceeding?

The introduction is the "fit" meeting. The contact record and the summary note are created either way. The welcome email with the form and checklist, and the discovery meeting, are proposed **only when the summary shows the prospect is proceeding**: an action item to book the discovery meeting, or a key point or profile update saying the client agreed to proceed or signed the advisory agreement. Otherwise create exactly one `assign_task` for the advisor, Tier B: "Is <name> proceeding? Reply `proceed HH-XXXX` or `close HH-XXXX` in the approvals channel", and no client-facing item. When the advisor replies `proceed`, the next run creates the welcome and the discovery scheduling as standard follow-ups (see `stages.md`).

If the summary says the advisory agreement is to be signed, record it as a Tier C item ("signature, for a person") so the discovery prep brief can show "Advisory agreement: not confirmed" until a person writes "agreement signed <date>" in the household's History.

## Documents are collected from the introduction onwards

The welcome email carries the client information form and the list in `required-documents.md`, so documents start arriving before discovery. The document check runs for every household from `intro_held` on, counts what is on file, and chases what is missing on the cadence in `sla.md`. After discovery the `client_email` above asks only for what is still missing, in one email.

## Discovery: the intake

Before the discovery meeting, the paraplanner's run creates one `discovery_prep` item (Tier A): a draft of the intake built from the documents on file, the introduction summary and the CRM, saved as `discovery-prep-<household>` in the client folder and linked from the discovery prep brief. After the meeting, create one `build_intake` item (Tier A) unless the household already has an intake (see `stages.md`): it starts from the draft, adds what the meeting said, is fact-checked, and is saved as the intake. Both are internal documents and are never sent to the client. A Debrief has no client present, so it gets no client summary and no meeting to schedule.

## Plan meeting: implementation, not planning

The plan exists before the plan meeting (the planning team built it from the planning request; the readiness review confirms it is on file). After the meeting the follow-ups are implementation, carried out by Operations and, through Operations, the custodian. Nothing is assigned to the planning team at this stage.

## Meeting type rules

- Use the meeting type stated in the summary. If none is stated, infer from content: a first meeting with no prior record is Introduction; data gathering and goals is Discovery; an internal meeting between the client-facing and planning teams about one household, with no client present, is Debrief; presenting recommendations is Plan; reviewing an existing plan is Financial check-up.
- If two types fit equally, use Unclear.

## Owner agent by action type

| Action type | Owner agent | Tier | Owner role |
|---|---|---|---|
| salesforce_case | salesforce-agent | B | paraplanner |
| schedule_meeting | scheduler-agent | B | paraplanner |
| send_form | comms-agent | B | paraplanner |
| client_email | comms-agent | B | paraplanner |
| create_invoice | document-agent | B | paraplanner |
| create_document | document-agent | B | paraplanner |
| assign_task | delegation-agent | B | paraplanner |
| discovery_prep | none (intake-builder skill) | A | paraplanner |
| build_intake | none (intake-builder skill) | A | paraplanner |
| update_intake | none (intake-builder skill) | A | paraplanner |
| planning_request | salesforce-agent | B | planner |
| ledger_note | none (orchestrator) | A | paraplanner |

`owner_role` says whose run prepares, executes and chases the item (see `team.md`). It is not the approver: most Tier B items are approved by the advisor, planning requests by the planner (`approval-rules.md`).

Anything in Tier C per `approval-rules.md` overrides this table.
