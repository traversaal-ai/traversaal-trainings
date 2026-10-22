# config.md: tool roles for this setting

Setting: **local build**. Every role points at a folder. No connector is used. The firm's setting is `config-investment-advisor-firm.md`.

| Role | Points to | How to use it |
|---|---|---|
| team | `team.md` | People, roles, and what each role owns. Read first in every run. |
| meetings | `inbox/` | Each file is one meeting summary in the Zocks shape, including internal Debrief notes. A meeting is "new" if its `meeting_id` does not appear in any file under `ledger/`. |
| crm_read | `salesforce/` | `contacts/` one file per client, `cases/` one file per case, `tasks/` one file per task. Read them as if they were Salesforce records. |
| crm_write | `salesforce/` (the CRM stand-in), written the way the ideal setup writes to Salesforce | Create a record only for an **approved** item, or for the one Tier A exception in `playbooks/approval-rules.md` (a genuinely new prospect from an Introduction meeting, after its duplicate checks). A Contact is a new file `salesforce/contacts/<id>-<first>-<last>.md`, a Case `salesforce/cases/<id>.md`, a Task `salesforce/tasks/<id>.md`, in the same front matter shape as the files already there. Ids: Contact `003DEMO` + the next 10-digit number after the highest existing one; Case `CASE-` + the next 8-digit number; Task `TASK-` + the next 8-digit number. New cases start `status: New`, `owner: Operations queue` (planning requests: `owner: Planning queue`, `type: Planning Request`). Write the new id to the item's `external_ref` and post "<record> created in Salesforce: <name>, <id>" in the approvals channel (for a new prospect, the wording in `approval-rules.md` instead). Never change or delete an existing file under `salesforce/`; a person closes cases there. |
| calendar | `outbox/calendar.md` | Read it for existing meetings and free slots. To create an event, append a row to its table and use the row's event id as `external_ref`. |
| email | `outbox/` | To save a draft, write `outbox/email-<work item id>.md` with To, Subject and Body. Never mark an email as sent. |
| chat | `outbox/` | To post a message, append it to `outbox/teams-<channel>.md` with a timestamp. Channels: `approvals`, `operations`. To read replies, read both files for lines of the form `approve WI-0000`, `approve WI-0000 slot N`, `reject WI-0000`, `done WI-0000`, `close HH-XXXX` or `proceed HH-XXXX`, each prefixed by the poster's name in square brackets, for example `- 2026-10-13 09:10 [R. Advisor] approve WI-0103`. A reply counts only when that name has the right role in `team.md`. |
| documents | `playbooks/`, `templates/`; writes to `outbox/` | Playbooks are the firm's rules. Templates are filled by copying them into `outbox/doc-<work item id>.md`. |
| client_files | `client-files/<household folder>/` | One folder per household, named in the status board's Client folder field. Holds the documents the client sent, the intake, and the intake changes. For a **new household, create its folder** `client-files/<surname in lower case>/` and put that path in the status board's Client folder. Write only that folder and the firm's own new files (discovery prep, intake, intake changes); never change or delete a file here. |
| briefs | `briefs/` | One file per brief, `YYYY-MM-DD-<household folder>-<brief type>.md`. |
| status_board | `households/` | One file per household, `households/<household folder>.md`, and `households/BOARD.md` regenerated every run. |
| ledger | `ledger/` | One file per work item, `INDEX.md` regenerated every run. |

Dates: today is the date and time in `outbox/today.txt` if that file exists (the demo clock, set by `journey.py`), otherwise the machine's current date and time. Use that date for every History line, due date and "tomorrow". "Tomorrow" means the next working day. If there are no client meetings tomorrow, write no brief.
