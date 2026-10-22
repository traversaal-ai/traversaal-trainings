---
name: document-check
description: Checks which required documents a household has on file in its client files folder, updates the status board, and chases what is missing on the firm's cadence with a single client email per reminder. Use after a discovery prep draft or an intake is built or changed, and on every run for households in intro_held, discovery_held, collecting_documents or debrief_held.
---

# Document check

Read `config.md` for `client_files`, `status_board`, `ledger` and `chat`. Read `playbooks/required-documents.md` and the "Missing documents" section of `playbooks/sla.md`.

## Steps, for one household

1. **List the client folder** (file names only; never open the client's documents to read them unless building an intake).
2. **Match** each required key to the files: a file name starting with the key, ignoring case, counts; so does the "accepted instead" file for that key.
3. **Update the status board row:** Documents on file "N of M", Missing documents (names, comma separated, or empty). If either value changed, append History "Documents: <N of M>. Received <names>" or "Still missing <names>".
4. **Nothing missing:** make sure no reminder item stays open. For each open `client_email` item for this household whose Proposed action is a document request, append History "All documents received <date>" and leave it for the verifier. Then let the household tracker work out the stage (it may become `ready_for_planning`).
5. **Something missing:**
   - The welcome `send_form` item from the introduction (it carries the document checklist), or a `client_email` item from the orchestrator that requests documents, counts as this household's request; add the other missing documents to its Proposed action if it is still Proposed, rather than creating a second email. A request sent before this system was switched on, recorded in the household's History, counts too, with that date as the approval date.
   - If no document request item exists for this household yet, create one `client_email` item (Tier B, approver the advisor, owner role paraplanner) listing every missing document together, using the "Requesting a document" opening in `approved-wording.md`. Hand it to `comms-agent` to prepare.
   - If a request exists and has been sent (a "sent on <date>" line in its History), count business days since it was sent and apply the cadence in `sla.md`: at day 3 and day 6 create one reminder item (same form, listing only what is still missing); at day 9 escalate to the advisor in the approvals channel instead.
   - Never create a new request or reminder while another one for this household is Proposed, Awaiting Approval, or In Progress and not yet due a reminder by the cadence. This also covers a meeting's "request outstanding documents" follow-up: if an open request already asks for those documents, link to it in History instead of creating a second email.
6. **Report:** household, N of M, received since last check, still missing, request or reminder created (id), escalation sent.

## Rules

- A file that appeared and then disappeared does not move the household back. Note it in History and report it.
- The discovery prep draft, the intake and the intake changes documents are not client documents and never count toward N.
- The client's documents stay where they are. Never move, copy, rename or trash them.
