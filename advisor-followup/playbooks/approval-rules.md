# Approval rules

Most actions require human approval. These rules say which, by whom, and how.

## Tiers

| Tier | Rule | Examples | What the system does |
|---|---|---|---|
| A | Bookkeeping inside the ledger only | Creating and updating work item files, regenerating the index, writing a brief file | Runs alone |
| B | Anything that touches the CRM, the calendar, email, chat or a client | Creating a case or task, sending a calendar invitation, saving or sending a client email, posting a message assigning work, sending a form, generating an invoice | Prepares the action in full, sets Awaiting Approval, waits |
| C | Regulated or irreversible | Money movement, changes to account terms or beneficiaries executed directly, investment advice, anything requiring a signature | Records a work item for a person, sets Cancelled with reason "Tier C, for a person", does nothing else |

Note on beneficiary changes: opening a case so that Operations processes a beneficiary change is Tier B. Changing the beneficiary directly in any system is Tier C.

## Exception: a new prospect from an introduction meeting (Tier A, runs alone)

Adding a genuinely new person to the CRM as a Contact runs alone, in the same run that processes the meeting, so the CRM and the status board stay in step. It applies **only when every condition below holds**; if any fails, do not create anything: create one `assign_task` item (Tier B, approver the advisor) saying which condition failed, and post it in the approvals channel.

1. The meeting summary's type is **Introduction**. No other meeting type ever creates a contact.
2. The summary gives the person's **full name** (first and last) **and an email address**. Never guess or construct either.
3. `crm_read` finds **no Contact with the same email, and no Contact with the same full name**. Check both. If either matches, the person exists: link to that Contact and create nothing.
4. No ledger item already records a contact created from this `meeting_id`, and no status board row already has this person. Run the `crm_read` check again immediately before creating.

When all hold: create the Contact through `crm_write` with name, email, phone if given, and the description "Prospect. Introduction <meeting date>, <meeting id>." Record it as a work item `action_type: salesforce_case`, Tier A, `approval: not required`, `status: In Progress`, `external_ref` the new Contact id, History "New prospect created in the CRM from <meeting id>, <id>". The verifier sets Done when it reads the Contact back. Put the id on the status board row (CRM contacts) and post "New client added to Salesforce: <name> (<id>), from <meeting id>" in the approvals channel.

Only the Contact. Cases, tasks, emails and meetings for the new person stay Tier B.

## Who approves

| Action type | Approver |
|---|---|
| client_email, send_form, schedule_meeting | The advisor named on the meeting |
| salesforce_case, assign_task | The advisor named on the meeting |
| create_invoice, create_document | The advisor named on the meeting |
| planning_request | The planner (see `team.md`) |
| discovery_prep, build_intake, update_intake | Nobody: Tier A. The draft, the intake and the changes document are internal, saved to the client files and never sent |

If the meeting names no advisor, the approver is the advisor on the client's CRM record. If neither is known, set the item to Unclear owner and ask in the approvals channel.

## How approval is given

Either of these counts:

1. A person edits the work item file: `approval: approved` or `approval: rejected`, and fills in `approved_by`. The next run picks it up.
2. A person replies in the approvals channel with `approve WI-0000` or `reject WI-0000`. The next run writes that into the file with the person's name and the time. Planning requests are posted to the operations channel, so the planner's reply there counts the same way.

Approval with a change ("approve WI-0102, slot 2") is an approval; the monitor applies the change before executing.

## Names used in this folder

| Role | Name | Channel |
|---|---|---|
| Advisor | R. Advisor | approvals |
| Operations lead | O. Ops | operations |
| Advisor's manager | M. Manager | approvals |
| Paraplanner | P. Para | approvals |
| Planner | L. Planner | operations |

`team.md` is the full list of people, roles and what each role owns.

In the investment advisor firm's settings these are replaced by real names and the Teams channels the firm nominates.
