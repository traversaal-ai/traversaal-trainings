# Advisor Follow-up System

## End-to-End Workflow: Architecture Overview

![End-to-end workflow](png/01-complete-workflow.png)

The picture reads top to bottom: the people, the firm's own systems where the work lives, the connectors Claude reaches them through, Claude itself (orchestrator, agents and skills, inside a permissions band and an approval gate), and the data and runtime underneath. The sections below describe the same parts, first as seven roles, then layer by layer.

### Purpose

Advisors at the investment advisor firm conduct introduction, discovery, plan and financial check-up meetings, each of which is transcribed. The follow-up work that each meeting generates (tickets, forms, invoices, scheduling, hand-offs to other teams) is today tracked by individuals. This document describes a system in which the transcript itself initiates that follow-up, the work is tracked in one shared place, progress is checked automatically, blocked items are escalated, and completion is verified before the client's next meeting.

The system is first summarised in seven parts, then described in four layers, with the role of every component within each layer.

### Summary

The transcript is the trigger. A shared ledger is the memory. Scheduled checks make the system persistent. Specialist agents do the work. The advisor retains approval over anything the client sees.

### Overview: the system in seven parts

Before the four layers, the whole system can be read as seven parts. Each is a role found in any agent system; the concrete thing it is in this firm is given alongside.

| Part | In this firm | What it does |
|---|---|---|
| Input | Meeting transcript | Starts the process. Nothing is typed by anyone. |
| Orchestrator | The decision-making component | Reads the transcript, decides what must happen, delegates each action, and reads and updates the shared state. |
| Shared state | Ledger of promises | One row per commitment: owner, status, approval, evidence. Read and updated by every other part. |
| Agents | One per task type | Carry out the delegated actions, ask the human approver when the client will see the result, and update the ledger. |
| Tools | CRM, calendar, documents, chat | The firm's existing systems. The agents act in them through connectors. |
| Human approver | The advisor | Says yes or no to anything client-facing. Receives escalations. |
| Scheduled task | The cycle, run about twice a day | Picks up new meeting summaries, executes approved items, checks progress against the real systems, escalates what stalls, and briefs the advisor before each meeting. |

The flow in one sentence: a meeting summary reaches the orchestrator, which records what the firm owes the client and delegates each item; agents act in the firm's tools and ask the advisor where needed; the cycle keeps checking the ledger until every item is verified complete. The four layers below expand each part.

---

## Layer 1: Inputs and Triggers

**Meeting transcript.** Every advisor meeting is already transcribed. The transcript is the starting signal for all downstream work. No manual entry is required.

**The cycle.** One scheduled task, run about twice a day, with three parts that can also be run on their own:

- **Process meetings.** Finds new meeting summaries and passes each one to the orchestrator. This is the mechanism by which the meeting initiates the process.
- **Monitor.** Executes approved items, has the Verifier check every open item against the real system, and escalates what has stalled. This provides continuous monitoring of work in progress.
- **Pre-meeting check.** Identifies the next working day's client meetings and confirms that all related follow-up is complete. This provides verification before the next client interaction.

---

## Layer 2: Agents

**Follow-up Orchestrator.** The decision-making component. It reads the transcript, determines the meeting type, identifies the commitments made, applies the firm's follow-up playbook, and produces a list of required actions. It covers two requirements: understanding the meeting type and client context, and determining the required next actions.

**Specialist agents.** Five narrowly scoped agents, each responsible for one category of follow-up:

| Agent | Responsibility |
|---|---|
| Salesforce Agent | Creates and updates cases, tasks and contact notes |
| Scheduler Agent | Identifies available slots and books follow-up meetings |
| Document Agent | Produces forms, invoices and plan documents from firm templates |
| Delegation Agent | Assigns work to operations or planning teams with full context |
| Communications Agent | Drafts client correspondence for advisor review |

Each specialist receives a single work item, performs it, and records the outcome. This is the delegation of work to specialised agents.

**Verifier Agent.** An independent check on completion. It confirms that an item is done by inspecting the underlying system (ticket status, calendar entry, form response) rather than relying on any agent's own report. This is what gives "complete" a verifiable meaning.

---

## Layer 3: State and Knowledge

**Follow-up Ledger.** A shared register with one row per obligation, visible to every agent and every team member. It records what was promised, who owns it, its approval status, its current state, and the evidence of completion. The ledger is how the system continues to track multiple items (for example, a Salesforce ticket and a follow-up meeting arising from the same transcript) across days and across teams. It also serves as the audit trail.

**Project memory.** Holds working preferences, such as an advisor's preferred meeting days. It does not hold commitments; those live only in the ledger.

**Knowledge base.** The firm's playbooks, approved research and compliance rules. Drafts and decisions are grounded in this material rather than generated independently.

---

## Layer 4: Systems of Record and People

**Salesforce, Outlook calendar and mail, Teams, SharePoint.** The tools the firm already operates. The system works within them rather than replacing them, which satisfies the requirement to operate across CRM, calendars, forms, knowledge bases and communication tools.

**Advisor.** Approves any action the client will see, including correspondence, meeting invitations, invoices and forms. No client-facing action is taken without this approval.

**Operations and planning teams.** Receive delegated work and the first notification when an item stalls.

**Manager.** Receives escalation when a notification to the owning team has not resolved the block.

---

## Mapping to Requirements

| Requirement | Delivered by |
|---|---|
| Understand the meeting type and client context | Follow-up Orchestrator, drawing on the ledger and knowledge base |
| Determine the required next actions | Follow-up Orchestrator, applying the firm's playbook |
| Delegate work to specialised agents or prompt the appropriate person for approval | Specialist agents; approval routed to the advisor |
| Maintain memory and state across systems and teams | Follow-up Ledger |
| Monitor whether work is progressing | The cycle's monitor, with the Verifier Agent |
| Escalate when something is blocked | The escalation ladder: owning team, advisor, manager |
| Verify work is complete before the next client interaction | The cycle's pre-meeting check, with the Verifier Agent, producing a brief for the advisor |

---

## Companion Diagrams

**Sequence.** Follows one client, Sam Reed, from the introduction meeting to the planning request: five steps, each a person's action followed by one run, with every item prepared, approved, executed and verified.

**Work item lifecycle.** Shows the states a single follow-up item passes through, from Proposed to Done, and the rule that an item is only Done when evidence exists in the underlying system.
