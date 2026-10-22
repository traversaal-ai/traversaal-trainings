# Definition of done: evidence required per action type

An item is Done only when the verifier finds the evidence below in the real system (through the roles in `config.md`). The agent that did the work never marks its own item Done. Record the evidence, with a date, in the `evidence` field and in History.

| Action type | Done means | Where the verifier looks |
|---|---|---|
| salesforce_case | Case status is Closed or Resolved, with a resolution note. For a new Contact (the new-prospect exception), the Contact exists | crm_read: the case or contact named in `external_ref` |
| schedule_meeting | The event exists on the calendar at the approved slot and the client has been invited. In the local build, the row exists with the client as attendee. On a real calendar, the client is an attendee on the event where the calendar row in `config.md` adds attendees (the firm's setting); where it creates events with no attendees (the demo settings), the advisor has sent the invitation | calendar: the event named in `external_ref`; where the event has no attendees, also email: a sent item matching the invitation draft |
| send_form | The client's response has been received, not merely that the form was sent | Both: the email was sent (email: a sent item; in the local build a History line by a person "sent on <date>"), **and** the form came back (crm_read notes, an email reply, or client_files: a file starting `client-information-form` in the household's folder). A form already returned before the email was sent counts as returned |
| client_email | The approved text has been sent | email: a sent item matching the draft. In the local build, a line in the work item History written by a person: "sent on <date>" |
| create_invoice | The invoice has been sent and, where the playbook requires it, paid | documents: the generated invoice exists; email: sent; crm_read: payment note if required |
| create_document | The document exists in the documents location and is linked from `external_ref` | documents |
| assign_task | The assignee has marked the task complete and attached or described the output | crm_read: task status Completed; or chat: a reply "done WI-0000" from the assignee, posted after the hand-off |
| ledger_note | The note is in the file | ledger |
| discovery_prep | The discovery prep draft exists in the household's client files and is linked from the status board | client_files |
| build_intake | The intake document exists in the household's client files and is linked from the status board | client_files |
| update_intake | The intake changes document exists in the household's client files and is linked from the status board | client_files |
| planning_request | The planning request case exists in the CRM. The item is Done when the case is Closed or Resolved; the household moves to `planning_requested` as soon as the case exists | crm_read: the case named in `external_ref` |

## Not done

- A case that has been created but is still New or In Progress.
- A form that has been emailed but not returned.
- A draft that exists but was never sent.
- A task that has been assigned but not completed.

Say so explicitly in briefs: "created, not yet closed", "sent, not yet returned".
