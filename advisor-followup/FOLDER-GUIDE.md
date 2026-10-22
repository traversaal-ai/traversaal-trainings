# What is in this folder, in plain words

Think of this folder as the firm's client office. Each subfolder is a tray or a cabinet, and Claude is the assistant who works through them, twice a day, as whichever person is running it. Nothing here is code; every file is readable text.

## The files at the top

| File | What it is | Who touches it |
|---|---|---|
| `PROJECT-INSTRUCTIONS.md` | The assistant's standing orders. Pasted once into the Project's instructions in the Claude app. Says what may run alone, what needs a person, what is never done, and which folders may be written to. | You, once, and again when it changes |
| `config.md` | The switchboard. For each kind of tool the assistant needs (team, meetings, CRM, calendar, email, chat, documents, client files, briefs, status board, ledger) it says where to go today. **Yours, not committed.** `reset-demo.py` creates it from `config.local.md` if it is missing. | You, when switching settings |
| `config.local.md`, `config-investment-advisor-firm.md` | The committed templates: everything local; the investment advisor firm's connectors. Copy one over `config.md` to switch. | You, when switching |
| `team.md` | Who is who. Five people and their roles (advisor, paraplanner, planner, operations, manager), which household stages and work items each role owns, who may approve what. Every run reads it first and acts only on its role's work. | The firm |
| `memory.md` | The assistant's notebook: small preferences it has learned. Never a commitment; those live only in the ledger. | Itself |

## The folders, in the order the work flows

### `inbox/` : meetings waiting to be processed

One file per meeting, written the way Zocks writes its summaries: who met, when, what type of meeting, a summary, the key points, the action items, and any updates to the client's profile. Internal huddle notes (meeting type Debrief) arrive here too. The cycle looks here for meetings it has not seen. On the investment advisor firm's connectors this folder is not used; the Zocks connector is read instead.

In the Sam Reed journey, `journey.py` copies his notes in here one step at a time from `journey/steps/`: the introduction (`zocks-8860-s-reed-introduction.md`), the discovery meeting (`zocks-8870-s-reed-discovery.md`) and the internal huddle about his household (`huddle-8880-s-reed-debrief.md`).

### `households/` : the status board

One file per client household, plus `BOARD.md`, a table of every household rebuilt at the end of every run. This is the answer to "where is this client?": the stage in the new-client journey, who owns that stage, how long it has been there, the next meeting, the documents on file and the ones missing, links to the intake, the intake changes and the plan, the planning request, and a dated history of every move. Stages never go backwards, and every move records its evidence.

In the Sam Reed journey there is one household, Reed. It appears after the first run and moves from introduction held, through collecting documents, discovery held, debrief held and ready for planning, to planning requested over the five steps. `journey/example-run/households/` shows the finished board.

### `client-files/` : one folder per household

What the client has sent (statements, the returned information form, a tax return, a will), as small stand-in files, plus what the firm wrote for them: the discovery prep draft (`discovery-prep-`), the intake (`intake-`), the intake changes after the huddle (`intake-changes-`) and the finished plan (`plan-`). The document check counts the client's documents against `playbooks/required-documents.md` by file name; the firm's own files never count. Nothing here is ever edited or deleted by the assistant; it only adds new files.

### `salesforce/` : a stand-in for the firm's CRM

What the assistant would read from Salesforce, as small text files, for the local build. Empty at the start of the journey, because Sam is not a client yet; his contact, the hand-off tasks for Operations and the planning case appear as the runs create them. On connectors the real org is read instead.

### `playbooks/` : the firm's rules

The assistant reads these before deciding anything. The firm owns and edits them.

| File | What it says |
|---|---|
| `stages.md` | The new-client journey: the stages, what moves a household on, what the loop does in each stage, who owns it. Never backwards; the intake is finalised once; nothing client-facing until the prospect is proceeding. |
| `action-matrix.md` | For each meeting type (introduction, discovery, debrief, plan, check-up), the standard follow-ups, plus which agent handles each kind of action, at what approval tier, and which role owns it. The "is the prospect proceeding?" rule. |
| `approval-rules.md` | The three tiers: what runs alone, what waits for a person, what is never automated. Who approves what (the advisor for client-facing work, the planner for planning requests). How approval is given. The one Tier A exception: a brand-new prospect added to the CRM after strict duplicate checks. |
| `sla.md` | Service levels per action, the reminder cadence for missing documents (day 3, day 6, the advisor at day 9), "done two business days before the next meeting", who we are waiting on (firm, client, custodian, third party) and what chasing means for each, when a household counts as stalled, the escalation ladder and its cap of three. |
| `definition-of-done.md` | For each kind of action, what evidence proves it is finished, and where to look. "Created" is not "closed"; "sent" is not "returned". |
| `required-documents.md` | The documents a household must have on file before planning (a placeholder list of five), and the plan file checked before the plan meeting. |
| `approved-wording.md` | The sentences the assistant may use in client emails, the tone, the disclaimer, and what must never be written. |
| `work-item-template.md` | The blank form for a work item, with every field explained, including the household, the owning role and who we are waiting on. |

### `ledger/` : the shared to-do list and the audit trail

One file per promise the firm has made, plus an index. Every run reads the index first and writes to the files last. A person approves an item by replying in the channel or by changing one line in its file. The ledger answers "is this task done?"; the status board answers "where is this client?"; the two are kept separate on purpose.

The journey starts with no items. The first run creates WI-0001, Sam's contact record, and about ten follow by the planning request: approved and executed, drafts waiting for the advisor to send, hand-offs to Operations, the planning request tracked until the case exists. `journey/example-run/ledger/` shows the full set.

Inside every work item file: a block of fields at the top (household, who, what, status, approval, due date, who we are waiting on, reference in the real system, evidence, how many times escalated), then the quoted sentence from the meeting it came from, then the fully prepared action, then a dated history of everything that happened to it.

### `outbox/` : where things go when there is no connector

In the local build this folder stands in for the calendar, the chat channels and email. On connectors it is only a fallback when a write is refused.

| File | Stands in for |
|---|---|
| `calendar.md` | The advisor's calendar: meetings held, the client meetings tomorrow, the huddles, the plan presentation, and internal meetings so the scheduler has to find free slots. `journey.py start` writes it. |
| `teams-approvals.md` | The approvals channel. Approval requests, brief notices, digests and escalations to the advisor land here; a person replies by adding a line such as `- 2026-10-16 09:10 [R. Advisor] approve WI-0106`. |
| `teams-operations.md` | The operations channel. Hand-offs, reminders to Operations and planning requests for the planner land here; replies such as `done WI-0098` or `approve WI-0112` go here. |
| `email-WI-....md` | An email draft for that item, written when the item is approved. |
| `doc-WI-....md` | A generated document or invoice for that item. |

### `briefs/` : what the advisor reads before each meeting

One file per client meeting, written the working day before: an intro brief, a discovery prep (documents on file, the draft intake, the questions to ask), a plan readiness review ("Ready" only when the case is closed and the plan is on file) or a follow-up brief. Open and blocked items first, then what is waiting on others, then what is done with its evidence.

### `templates/` : blank documents

The discovery prep draft, the intake, the intake changes, the planning request, the client information form and the invoice, with placeholders the skills fill in. On the investment advisor firm's connectors the firm's own templates in SharePoint are used instead.

### `reset-demo.py` and `journey.py` : first-time setup and the story

Both sit at the repository root, next to this folder. `reset-demo.py` creates the seven working folders and your `config.md` from `config.local.md` if you have none; it never overwrites anything. `journey.py` plays Sam Reed's story: `start` empties the working folders and writes the stand-in calendar and the demo clock, and each `next` drops the next notes and documents in and plays the people's part (approvals given, documents sent, drafts sent). `journey/steps/` holds what each step drops in; `journey/example-run/` is a complete run to compare with. The assistant never writes to either.

## The plugin, in the folder next to this one

`advisor-followup-plugin/` is what you upload to Claude. It holds no data, only instructions.

| Part | What it is |
|---|---|
| `commands/run-cycle` | The twice-daily loop: who is running it, sweep meetings held and upcoming, move every household, do the stage work that role owns, run the monitor for that role's items, write the briefs, post a digest. `as <name or role>`, or `as everyone`. |
| `commands/process-meetings`, `run-monitor`, `pre-meeting-check` | The three parts of the cycle, kept for running one step at a time. |
| `skills/household-tracker` | How to keep the status board: finding the household for a meeting, working out the stage, who may change a row. |
| `skills/followup-orchestrator` | How to turn one meeting summary into work items and move its household. |
| `skills/intake-builder` | The discovery prep draft, the intake (finalised once), the intake changes after the huddle. Every row sourced, fact-checked by the verifier. |
| `skills/document-check` | Which required documents are on file, and chasing the missing ones on the cadence. |
| `skills/planning-request` | The planning request for the planner's approval, tracked until the case closes and the plan is on file. |
| `skills/pre-meeting-brief` | The four kinds of brief, by stage. |
| `skills/ledger` | How to read and write work items: format, states, how approval is read and from whom, how the index is rebuilt. |
| `agents/` | Six specialists: Salesforce (cases, tasks, planning requests), scheduler (calendar), document (forms and invoices), delegation (assigning work), communications (client emails), verifier (checks the real system, fact-checks the intake, and is the only one allowed to mark anything Done). |

### `salesforce-ledger/` : fields for the firm's Salesforce, also at the repository root

Not used by the local build. When the firm points the status board at Salesforce (the `status_board` row in `config-investment-advisor-firm.md`), a Salesforce admin deploys this once: the status fields on the Household account, and a Follow-up Item object for the day the ledger moves into Salesforce too. A firm that already tracks the same things with fields of its own can point that row at those fields instead and skip the deploy. Until one or the other is done, the board simply stays in the local `households/` folder.

## Not in git

`config.md` and the seven working folders (`inbox/`, `households/`, `client-files/`, `salesforce/`, `ledger/`, `outbox/`, `briefs/`). Everything else in this folder is committed. At the repository root, `journey/.state` and `journey/.snapshots/`, which `journey.py` uses to undo a step, are not in git either.
