---
description: Find meeting summaries not yet processed and run the follow-up orchestrator on each, moving each household on the status board. Part of run-cycle; also runs on its own. Argument - an optional meeting id or file, and optionally "as <name or role>".
---

Process new meetings.

1. Read `config.md`, the `team` role (runner from "as <name or role>", else the default runner), the status board and the ledger. Processing meeting notes is owned by the paraplanner: any other role lists the new meetings in its report and stops.
2. List meeting summaries through the `meetings` role. A meeting is new if its `meeting_id` is in no ledger record and in no household's Meetings processed.
3. For each new meeting, oldest first, run the `followup-orchestrator` skill on it.
4. If an argument names a specific meeting id or file, process only that one, even if it is not new, but still refuse to create duplicate work items.
5. After all meetings, regenerate the indexes once (local build: `ledger/INDEX.md` and `households/BOARD.md`).

Report: runner and role, meetings found, meetings processed, households moved (old → new), work items created per meeting (ids), intakes built or changed, items linked to existing CRM records, anything ignored, anything that needs a person. If there were no new meetings, say so in one line.
