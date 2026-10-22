# Deployment: running the follow-up system for real

Written for the question "the demo works; how would the investment advisor firm actually run this?" It covers where the system runs, what stays on and who needs to be an administrator, with a recommendation at the end.

## What has to be true in production

The system is three scheduled tasks reading and writing a folder of Markdown files, with connectors into Zocks, Salesforce and Microsoft 365. Three things must hold wherever it runs:

1. **The ledger folder is reachable by every run and by every person who approves.** It is the shared state.
2. **Something fires the three tasks on their cadence** without a person starting them.
3. **Each run signs in as a person the firm has authorised**, because every connector acts with that person's permissions.

The constraint that decides everything: a Cowork scheduled task runs in Anthropic's cloud unless it needs a local folder, in which case it runs on the machine where the folder is, and only while the desktop app is open there. So the question "where does the ledger live" is the question "where does this run".

## The four options

| | A. Always-on machine | B. Cloud only, ledger in SharePoint | C. Claude Code Routines, ledger in a git repository | D. Self-hosted Claude Code on a VM |
|---|---|---|---|---|
| What runs | Claude desktop app, Cowork mode, Project tied to a local folder | Cowork scheduled tasks in Anthropic's cloud | Routines in Anthropic's cloud | Claude Code CLI and cron on a server the firm controls |
| Where the ledger lives | Local folder on that machine, synced to SharePoint by the OneDrive client for sharing | A SharePoint folder, read and written through the Microsoft 365 connector | A git repository (GitHub) the routine clones, edits and commits | A folder on the VM, optionally synced or committed |
| Needs a machine on | Yes, with a user logged in and the app open | No | No | Yes, but headless |
| Needs Microsoft 365 write actions | No (the OneDrive client does the sync) | Yes, for file writes to SharePoint, and for Outlook and Teams actions | For Outlook and Teams actions only | For Outlook and Teams actions only |
| Minimum cadence | Minutes | Hourly in practice | One hour, with daily caps (25 runs a day on Team and Enterprise at launch) | Any |
| Approvals | File edit on the synced folder, or Teams reply | Teams reply, or edit the file in SharePoint | Teams reply, or edit the file in the repository | Teams reply, or edit the file |
| Who sets it up | One Claude user plus the firm's IT for the machine | Claude Owner and Microsoft Entra admin | Claude Owner, a GitHub organisation, Microsoft Entra admin | IT with server access, Claude Owner, an API key or a Claude login on the server |
| Effort to reach from the demo | Hours | Half a day once admins have acted | One to two days (repo, routine, same plugin) | Two to three days |
| Risk | The machine sleeps, updates, or the session logs out | Depends on write actions being enabled and on Teams send tools being allowed | Caps and the one-hour floor; a research preview feature | The firm owns an agent host and its security |

### A. Always-on machine

The demo setup, kept running. A Windows machine (a desk PC, a mini PC, or a Windows virtual machine on Google Cloud or Azure) with the Claude desktop app signed in, the Project tied to a folder, and the three scheduled tasks created. The folder sits inside a OneDrive or SharePoint-synced directory, so the ledger files appear in SharePoint for the rest of the firm within seconds, with no connector write access needed.

What the firm's IT must do: provide the machine, keep a user session logged in (auto-login, no sleep, updates scheduled outside business hours), and sync the folder with the OneDrive client. On a cloud VM this means a Windows Server or Windows 11 VM reached by remote desktop with the session left connected; the desktop app is not documented as a service, so it must run inside an interactive session. Test that the app keeps running after the remote desktop window is disconnected but not signed out.

Why it is attractive: it needs no administrator action in Claude or Microsoft 365 beyond what already exists, and it works today.

Why it is not the end state: one machine, one logged-in user, no restart tolerance. Fine for a pilot with one or two advisors.

### B. Cloud only, ledger in SharePoint

No machine at all. The Project's ledger role points at a SharePoint folder. Every scheduled task runs in Anthropic's cloud, reads the ledger through the Microsoft 365 connector, writes back through its write actions, reads Zocks and Salesforce through their connectors, and posts to Teams.

What must be enabled: Microsoft 365 write actions for the users who run the tasks (the Claude Owner turns them on under Organization settings, Connectors; the Entra Global Administrator approves the added permissions once for the tenant), and the Teams messaging tools unblocked. The SharePoint site must grant the running user write access to the ledger folder.

Why it is the cleanest: nothing to keep alive, every advisor's Claude sees the same files, the ledger is in the firm's own document system with its retention and audit.

Why it may wait: it depends on two administrators and on the Microsoft 365 write tools, which some reports place on Enterprise plans only. Confirm with Anthropic for the firm's plan.

### C. Claude Code Routines, ledger in a git repository

For a firm with engineers. The Project folder becomes a GitHub repository. A routine is a saved Claude Code session with a prompt, the repository and a set of connectors, started by a schedule, an API call or a GitHub event. Each run clones the repository, runs the same plugin commands, and commits the changed ledger files. Approvals are commits or Teams replies.

Limits at the time of writing: one hour minimum interval, daily run caps per plan, research preview status. The ledger gains full version history for free, which auditors like.

### D. Self-hosted Claude Code on a VM

Claude Code (the command-line agent) installed on a Linux or Windows VM in Google Cloud, with the same plugin, the same folder, and a cron job that runs the cycle. Connectors are the same MCP servers, configured for Claude Code. The firm owns the host, its credentials and its logs.

This is the most controllable option and the most work. It suits a firm that already runs internal automation on servers and wants the agent inside its own network boundary. It needs an API key with billing or a Claude account signed in on the server, and someone to own the machine.

## Administrator accounts: who is needed for what

| Action | Who |
|---|---|
| Enable Zocks, Salesforce and Microsoft 365 connectors for the organisation | Claude Owner or Primary Owner (Team or Enterprise plan) |
| Install the plugin for everyone, or allow members to add it | Claude Owner |
| Grant Salesforce write access to the running users | Salesforce administrator at the firm |
| Approve Microsoft 365 write permissions for the tenant | Microsoft Entra Global Administrator or Application Administrator |
| Turn on Microsoft 365 write actions and allow Teams messaging tools | Claude Owner, in Organization settings |
| Create the SharePoint folder and grant write access | SharePoint site owner |
| Provide and maintain the machine (option A or D) | The firm's IT |

No option requires a Microsoft or Salesforce administrator to use Claude themselves. They act once in their own consoles.

## Is Claude Cowork hard to set up on a server?

On an ordinary Windows machine it is the same as on a laptop: install the desktop app, sign in, create the Project, tie the folder, upload the plugin, create the three scheduled tasks. Thirty minutes.

On a server-class or cloud virtual machine the only difficulty is that the desktop app expects a signed-in interactive user. It is not a Windows service. The practical recipe is a Windows VM with automatic logon, sleep disabled, the Claude app in the startup folder, and remote desktop sessions disconnected rather than signed out. This is a well-known pattern for desktop automation but it is not something Anthropic documents or supports, so treat option A on a VM as a pilot arrangement and option B as the destination.

## Data handling

- Client data stays in Zocks, Salesforce and Microsoft 365. The ledger holds names, record ids and the text of proposed actions. If the firm's policy treats proposed emails as client data, the ledger folder must sit inside a system with the firm's retention and access controls, which points to option B (SharePoint) or C (a private repository) over a local folder.
- Every connector acts with the permissions of the signed-in user. Choose that user deliberately: a named service user with the advisors' read access and nothing more is better than an administrator's account.
- Enterprise plans add audit of tool calls and approval decisions through OpenTelemetry. Team plans rely on the ledger's History sections and the connectors' own logs.

## Recommendation

1. **Pilot now with option A** on an always-on Windows machine at the firm, ledger in a OneDrive-synced folder so the team can see and edit it in SharePoint. Needs no new administrator actions and reuses the demo as built.
2. **Move to option B** as soon as the Claude Owner and the Entra administrator have enabled Microsoft 365 write actions and Teams messaging. Change one line in `config.md` (the ledger role) and retire the machine.
3. **Consider option C or D** only if the firm wants version history, a stricter cadence, or the agent inside its own network, and has engineers to own it.

Before any of these, the two prerequisites that take longest are the ones to start now: the Salesforce write grant for the running users, and the Microsoft 365 tenant consent for the connector's write permissions.

## Lessons from the live test

What we learned running scheduled tasks during testing, which applies to option A:

- A scheduled task reaches a local folder only with **Require this computer** switched on, and only after the folder has been granted with "Don't ask again for this folder on this device".
- Even then, the scheduled run does not attach the project folder by itself. The task's instructions must name the folder's full path. With that, the run found the folder and completed unattended.
- If an organisation disables "Always allow" for write tools in Cowork, manual runs ask before every email draft or channel message, but scheduled tasks set to **Automatically approve** run without prompts.
- A Claude seat's connectors act as the signed-in person, so messages and drafts appear under that person's name. A dedicated service user is the clean choice in production.

## Sources

- [Schedule recurring tasks in Claude Cowork (support.claude.com)](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)
- [Get started with Claude Cowork (support.claude.com)](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)
- [Use Claude Cowork on web, desktop and mobile (support.claude.com)](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)
- [Microsoft 365 connector, including write actions (claude.com docs)](https://claude.com/docs/connectors/microsoft/365)
- [Use Cowork on Team and Enterprise plans (support.claude.com)](https://support.claude.com/en/articles/13455879-use-cowork-on-team-and-enterprise-plans)
- [Anthropic adds routines to Claude Code (Tessl)](https://tessl.io/blog/anthropic-adds-routines-to-claude-code-for-scheduled-agent-tasks)
- [Claude Code Routines guide (Makerkit)](https://makerkit.dev/blog/tutorials/claude-code-routines-guide)
- [Cowork scheduled tasks versus routines (third party comparison)](https://buildtolaunch.substack.com/p/claude-cowork-scheduled-tasks-vs-routines-vs-loop)

## Shared state off the machine: files now, Salesforce next

The household workflow makes the question of where shared state lives more pressing, because two lists (the status board and the ledger) are now read and written by every run for every role. Three stages:

1. **The demo:** both lists are files in the project folder, as are the client files and briefs, with a stand-in folder for the CRM. Everything sits on the one computer that runs the Claude app, which is easy to inspect and reset but ties every run to that machine.
2. **The investment advisor firm, first step:** the same shape on their systems. Teams channels for approvals and hand-offs, SharePoint for client files, briefs and rules. The Microsoft 365 connector reads and writes Outlook mail and calendar, SharePoint files and Teams channel messages once their administrators enable write actions; it does not reach Microsoft Lists, so the two lists go either into files in a SharePoint library or straight to stage 3.
3. **The investment advisor firm, long term:** the ledger as a custom object in Salesforce ("Follow-up Item", with a related history object), and the status board as fields on the household record in Financial Services Cloud. This closes four gaps at once: no machine involved, roles tied to real Salesforce users, visibility on the household page and in reports, and safe simultaneous edits. It needs the firm's gated write connector opened for those objects only; cases, tasks and anything client-facing stay behind approval as now.

Moving between stages is a `config.md` change plus loading the data, because every read and write already goes through the `status_board` and `ledger` roles.
