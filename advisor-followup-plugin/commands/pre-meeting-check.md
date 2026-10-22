---
description: Write the briefs for the next working day's client meetings - intro brief, discovery prep, plan readiness review or follow-up brief by household stage - verifying open work items first. Part of run-cycle; also runs on its own. Argument - an optional date, and optionally "as <name or role>"; with no runner named, every brief kind.
---

Run the pre-meeting check.

1. Run the `pre-meeting-brief` skill for the next working day. If an argument gives a date, use that date instead. If an argument names a runner, write only the brief kinds that role owns; otherwise write all of them.
2. Regenerate the indexes in the local build.

Report: one line per client meeting found (household, time, brief kind, open items, done items, blocked items, brief link). If no client meetings were found for the date, say which date was used instead and why.
