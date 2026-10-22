# Advisor Follow-up: Project folder

This folder is the working directory for the Claude Cowork Project "Advisor Follow-up". Tie the Project to this folder and Claude reads and writes it in every session.

For a plain-language tour of every folder and file, see `FOLDER-GUIDE.md`.

## What is in here

| Path | Purpose |
|---|---|
| `PROJECT-INSTRUCTIONS.md` | Paste into the Project's instructions. The standing orders. |
| `config.md` | Which connector or stand-in each tool role uses. **Yours, not committed.** `reset-demo.py` creates it from `config.local.md` if it is missing; copy another template over it to use connectors. |
| `config.local.md`, `config-investment-advisor-firm.md` | The committed templates: fully local; the investment advisor firm's connectors. |
| `team.md` | Who is who: five people and their roles (advisor, paraplanner, planner, operations, manager), what each role owns and may approve. Every run reads it first. |
| `playbooks/` | The firm's rules: the household stages, the action matrix, approval rules, service levels and chasing cadence, definition of done, required documents, approved wording, work item template. |
| `templates/` | Documents the system fills: discovery prep draft, intake, intake changes, planning request, client information form, invoice. |
| `memory.md` | Claude's own project memory. It fills itself. |

Working folders, created by `reset-demo.py` and filled by `journey.py` and the runs (not committed):

| Path | Purpose |
|---|---|
| `households/` | The status board: one file per client household with its stage, plus `BOARD.md`. |
| `ledger/` | One file per work item plus `INDEX.md`. The to-do list and the audit trail. |
| `inbox/` | Meeting summaries waiting to be processed, including internal huddle notes. |
| `client-files/` | One folder per household: the documents the client sent, the discovery prep draft, the intake, the intake changes, the plan. |
| `briefs/` | Briefs written before client meetings: intro brief, discovery prep, plan readiness review, follow-up brief. |
| `outbox/` | Where drafts, channel messages and calendar events land when no connector is configured. |
| `salesforce/` | Stand-in client records, cases and tasks for the local build. |

## How to run the demo locally

1. From the repository root: `python reset-demo.py` (macOS: `python3`). It creates the folders above and `config.md` if you have none.
2. In Claude Cowork, create a Project named `Advisor Follow-up` tied to this folder, and paste the contents of `PROJECT-INSTRUCTIONS.md` (below the line) into its instructions.
3. Install the plugin from the sibling folder `advisor-followup-plugin` (Customize, Plugins, upload the zip; SETUP-INVESTMENT-ADVISOR-FIRM.md step 2.3).
4. From the repository root: `python journey.py start`. Then, five times: `python journey.py next`, followed by `Run run-cycle as everyone.` in a task inside the Project. SETUP-INVESTMENT-ADVISOR-FIRM.md section 2 says what to look at after each step, and `journey/example-run/` at the repository root is a complete run to compare with.

## Settings

| File | Setting |
|---|---|
| `config.local.md` | Fully local. Every role is a folder. What a fresh clone gets |
| `config-investment-advisor-firm.md` | The investment advisor firm's connectors: Zocks, Salesforce, Microsoft 365 |

To switch, copy the chosen file over `config.md`. Connecting the firm's systems: `SETUP-INVESTMENT-ADVISOR-FIRM.md` at the repository root, sections 3 to 5.
