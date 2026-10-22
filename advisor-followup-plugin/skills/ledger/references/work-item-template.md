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
The complete action, ready to execute or to hand to a person.

## History
- YYYY-MM-DD HH:MM Proposed by orchestrator
```

In the live settings each front matter field is a column or field of the same name in the list or Salesforce object that `config.md` names, and Source, Proposed action and History are long text (in Salesforce, History is a related list of dated records).
