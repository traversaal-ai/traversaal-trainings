# Advisor Follow-up plugin

Skills, sub-agents and commands for the "Advisor Follow-up" Project. Install from Customize, Plugins, or add the skills under Customize, Skills if plugin installation is not available.

```
advisor-followup-plugin/
  .claude-plugin/plugin.json
  skills/
    followup-orchestrator/SKILL.md       one meeting summary -> work items, household moved on
    household-tracker/SKILL.md           the status board: one row per household and its stage
    household-tracker/references/household-template.md
    intake-builder/SKILL.md              intake once after discovery; changes only after the debrief
    document-check/SKILL.md              required documents on file; chase what is missing
    planning-request/SKILL.md            the planning request case, approved by the planner
    pre-meeting-brief/SKILL.md           intro brief, discovery prep, plan readiness review
    pre-meeting-brief/references/brief-template.md
    ledger/SKILL.md                      the work items: files locally, the firm's own system live
    ledger/references/work-item-template.md
  agents/
    salesforce-agent.md                  cases, tasks, contact notes and the planning request in the CRM
    scheduler-agent.md                   meeting slots, the invitation draft, the event once approved
    document-agent.md                    documents, forms and invoices from the firm's templates
    delegation-agent.md                  hand-offs to Operations or the planning team, with context and a due date
    comms-agent.md                       client emails in the approved wording; drafts only, never sends
    verifier-agent.md                    checks the real system for evidence; the only agent that sets Done
  commands/
    run-cycle.md                         the twice-daily loop: run-cycle as <name | role | everyone>
    process-meetings.md                  new meeting summaries into work items, each household moved on
    run-monitor.md                       approvals read, approved items executed, open items verified, stalls escalated
    pre-meeting-check.md                 the briefs for the next working day's client meetings
```

The firm's rules (stages, required documents, action matrix, definition of done, service levels, approval rules, approved wording) and the team list live in the Project folder, not in the plugin, so the firm can edit them without touching the plugin. Tool roles (team, meetings, crm_read, crm_write, calendar, email, chat, documents, client_files, briefs, status_board, ledger) are resolved through the Project folder's `config.md`.

If sub-agents are not available in your Claude plan, the skills perform each agent's job themselves by following the agent file's instructions.

Every change to a file in this folder needs a new zip and a new upload, as described in the setup guide. Changes in the Project folder do not.
