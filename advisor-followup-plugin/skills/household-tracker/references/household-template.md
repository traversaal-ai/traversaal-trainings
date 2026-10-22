```markdown
---
household_id: HH-XXXX
household: Surname household
clients: Full Name, Full Name
crm_contacts: 003XXXXXXXXXXXX, 003XXXXXXXXXXXX
advisor: R. Advisor
stage: intro_scheduled | intro_held | discovery_held | collecting_documents | debrief_held | ready_for_planning | planning_requested | plan_presented | existing_client | not_proceeding
owner_role: paraplanner | planner
in_stage_since: YYYY-MM-DD
client_folder: client-files/surname
last_meeting:
next_meeting:
meetings_processed:
briefs:
discovery_prep:
intake:
debrief:
intake_changes:
documents_on_file: 0 of 5
missing_documents:
planning_request:
plan_on_file:
last_updated:
---

## History
- YYYY-MM-DD HH:MM Household created at <stage>. Evidence: <meeting id or calendar event>.
```

In the live settings the same fields are the columns of the status board list, or the household fields on the Account record in Salesforce, as the `status_board` row of `config.md` says; History is a long text field holding one dated line per change.
