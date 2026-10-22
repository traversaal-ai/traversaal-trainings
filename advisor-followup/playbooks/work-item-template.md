# Work item template

Copy this for every new work item. File name: `ledger/WI-NNNN.md` where NNNN is the next number after the highest existing id. Keep every field, even if empty.

```markdown
---
id: WI-0000
client: Full Name
household: HH-XXXX
salesforce_contact: 003XXXXXXXXXXXX
meeting_id: zocks-0000
meeting_date: YYYY-MM-DD
meeting_type: Introduction | Discovery | Debrief | Plan | Financial check-up | Unclear
action_type: salesforce_case | schedule_meeting | send_form | client_email | create_invoice | create_document | assign_task | discovery_prep | build_intake | update_intake | planning_request | ledger_note
tier: A | B | C
status: Proposed | Awaiting Approval | Approved | In Progress | Blocked | Done | Cancelled
owner_role: paraplanner | advisor | planner
waiting_on: firm | client | custodian | third_party
owner_agent: salesforce-agent | scheduler-agent | comms-agent | document-agent | delegation-agent | none
approver: Name
due: YYYY-MM-DD
approval: pending | approved | rejected | not required
approved_by:
approved_at:
external_ref:
evidence:
last_checked:
escalations: 0
linked_crm_record:
---

## Source
"Quoted action item or sentence from the meeting summary." (meeting id, action item number)

## Proposed action
The complete action, ready to execute or to hand to a person: case fields, invitation text and slots, email draft, task assignment, document to generate.

## History
- YYYY-MM-DD HH:MM Proposed by orchestrator
```

## Field rules

- `status` and `approval` move together: Proposed has `approval: pending` (Tier B) or `not required` (Tier A); Awaiting Approval has `pending`; Approved, In Progress and Done have `approved`; Cancelled has `rejected` or `not required`.
- `due` comes from `sla.md`: meeting date plus the service level to done for the action type.
- `external_ref` holds the id in the real system (case number, event id, email id, document link) or the words "pending creation by Operations".
- `evidence` is filled only by the verifier, with a date.
- `last_checked` is updated by every monitor run that looks at the file.
- `escalations` counts escalations sent, maximum 3.
- `linked_crm_record` names a task or case that already existed in the CRM for this commitment, so the item is tracked without creating a duplicate.
- History lines are dated `YYYY-MM-DD HH:MM` and are never deleted.
- `household` is the household id from the status board. `owner_role` comes from the action matrix. Items written before these fields existed have neither: take the household from the client's name on the status board, and the owner role from the action matrix.
- `waiting_on` says whose move it is. `firm` (default): someone in the firm can do or close it. `client`: the client must send or sign something (`send_form`, document requests). `custodian`: the work is with the custodian (a transfer, an account opening, a beneficiary change processed there), set by the agent that executes the case. `third_party`: an accountant, attorney or another outside party. The rules in `sla.md` depend on it; an item without the field is `firm`.
