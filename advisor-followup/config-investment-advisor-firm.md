# config.md: tool roles for this setting

Setting: **investment advisor firm**. Every role points at the firm's own system. Copy this file over `config.md` to use it.

**One rule for every role: connector first, local folder if not.** At the start of each run, check that the role's connector is connected and can do what the run needs (read, and write where the role writes). If it is, use it. If it is not connected, or a call to it fails, use the local folder in the last column for that role for the whole run, and say which roles fell back in the run report. Nothing else changes: the plugin, the playbooks and the approval rules are the same either way. So the firm can switch systems on one at a time.

What each connector needs switched on, once, by the firm's admins:
- **Salesforce:** Salesforce's own Claude plugin and its hosted MCP server ("Headless 360"). A Salesforce admin turns on MCP Service and creates the app login for Claude; a Claude admin adds the plugin and server; each person clicks Connect.
- **Microsoft 365 (Teams, Outlook, Outlook Calendar, SharePoint):** Claude's Microsoft 365 connector, with **write actions turned on**: a Microsoft Entra administrator approves the permissions, and a Claude admin turns write actions on.
- **Zocks:** the Zocks connector, read only.

| Role | Points to (connected) | How to use it | If not connected |
|---|---|---|---|
| team | `team.md` in this folder | People, roles, and each person's Teams name. Read first in every run. | same |
| meetings | Zocks | Read meeting summaries, action items and profile updates. A meeting is new if its meeting id is in no work item and no household's Meetings processed. Read only. | `inbox/` |
| crm_read | Salesforce | Contacts (and the Household account), Cases, Tasks, notes synced from Zocks. Match a person by full name and email. Tasks created by the Zocks sync are linked, never duplicated. | `salesforce/` |
| crm_write | Salesforce | Create records only for an approved item, or for the one Tier A exception in `playbooks/approval-rules.md` (a new prospect from an Introduction, after its duplicate checks). Write the new id to `external_ref` and post "<record> created in Salesforce: <name>, <id>" in the approvals channel. Never change or delete an existing record. | new files under `salesforce/`, as `config.local.md` says |
| status_board | Salesforce: the Household account's status fields (stage, owner role, documents on file, missing documents, intake and changes links, next meeting, planning request, history) | One household per account. Update the fields; add one dated History entry per change, never rewrite one. | `households/` and `households/BOARD.md` |
| ledger | Salesforce: one Task per work item, with the work item fields in the description or custom fields, linked to the household | The work item id is in the Task subject. Status, approval and History follow the ledger skill. | `ledger/` and `ledger/INDEX.md` |
| chat | Teams: the approvals channel and the operations channel named in `team.md` | Post approval requests, briefs notices, confirmations, digests and escalations. Read replies `approve WI-0000`, `approve WI-0000 slot N`, `reject WI-0000`, `done WI-0000`, `close HH-XXXX`, `proceed HH-XXXX`. A reply counts only when the poster's Teams name has the right role in `team.md`. | `outbox/teams-approvals.md`, `outbox/teams-operations.md` |
| email | Outlook | Save drafts only. Never send. Record the draft id in `external_ref`. To check a send, look for the sent item. | `outbox/email-<work item id>.md` |
| calendar | Outlook Calendar | Read meetings held and coming up, and free slots. Huddles have titles starting `Huddle:`. Create events only for approved items, with the client as attendee, so the approved invitation goes out from the advisor's calendar when the event is created. | `outbox/calendar.md` |
| client_files | SharePoint: the firm's client library, one folder per household | Read the documents the client sent. For a new household, create its folder. Save the discovery prep, the intake and the intake changes as **new** files; never change or delete a client's document. | `client-files/<household>/` |
| briefs | SharePoint: the briefs folder | One new document per brief, `YYYY-MM-DD <household> <brief kind>`. | `briefs/` |
| documents | Reads: `playbooks/` and `templates/` in this folder, or the firm's SharePoint copies. Writes: SharePoint outbox folder | Fill a template and save it as a new document named `doc-<work item id>`. | `outbox/doc-<work item id>.md` |

Dates: today is the machine's current date and time, in the firm's time zone. "Tomorrow" means the next working day. If there are no client meetings tomorrow, write no brief.
