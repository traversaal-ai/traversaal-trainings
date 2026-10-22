# Setup guide for the investment advisor firm: Advisor Follow-up on your own systems

For the investment advisor firm's IT and admin team. Follow the parts in order. Each part ends with a check.

Menu names in Claude, Microsoft 365 and Salesforce change from time to time. If a menu in this guide does not match what you see, check the current Claude docs (links in Part 3) and your vendor's docs.

## 1. What this is

Advisor Follow-up carries each new client household from the first introduction to the planning request.
It reads meeting notes, turns them into a list of tracked work items, and keeps a status board per household.
It builds the intake, checks which documents are in, drafts client emails and books meetings.
Nothing reaches a client until a named person at the firm approves it in Teams.
It runs by itself twice a day and posts a short summary for each role.

What runs where:

| Piece | What it is |
|---|---|
| Claude desktop app | Installed on one computer (claude.ai/download). The web app cannot use a local folder, so the desktop app is required. |
| Cowork project | A project called `Advisor Follow-up`, tied to the `advisor-followup` folder in this repository. It holds the firm's rules (`playbooks/`), templates, `team.md` and `config.md`. |
| The plugin | The `advisor-followup-plugin` folder in this repository. It holds the skills, agents and commands that do the work. |
| Scheduled task | Runs `run-cycle` at 08:00 and 14:00 on weekdays, on that computer. |
| Your systems | Zocks, Salesforce, Teams, Outlook, Outlook Calendar and SharePoint, connected one at a time (Part 3). Until a system is connected, a local folder stands in for it. |

## 2. Try it first, with no connectors (about 15 minutes)

This plays one made-up client, Sam Reed, from introduction to planning request. Everything stays in local files. Nothing touches a real system.

Commands below are for Windows (PowerShell). On macOS (Terminal), type `python3` instead of `python`.

**2.1 Get the files.** Clone the repository into a folder named `advisor-followup-system`, then go into it:

```
git clone --branch investment-advisor --single-branch https://github.com/traversaal-ai/traversaal-trainings.git advisor-followup-system
```

```
cd advisor-followup-system
```

Every command in this guide runs from that folder. Create the working folders and your local configuration:

```
python reset-demo.py
```

This creates the working folders and your own `advisor-followup/config.md` from the fully local settings (`config.local.md`).

**2.2 Install the Claude app and make the project.**
1. Install the Claude desktop app and sign in with your firm's Team or Enterprise account.
2. Projects, New project. Name: `Advisor Follow-up`. Folder: the `advisor-followup` folder inside `advisor-followup-system`. Visibility: Private. Description (shown under the project's name, not read by Claude): `Follow-up system for advisor client meetings. Tracks every client household from the introduction meeting to the planning request, turns each meeting summary into work items, prepares each one for a person to approve, runs twice a day, escalates what stalls, and verifies work is done before the client's next meeting. Rules are in the playbooks, tool roles in config.md.`
3. Open **Instructions** on the project page. Paste everything below the horizontal line in `advisor-followup/PROJECT-INSTRUCTIONS.md`.
4. In a new Cowork task in the project, type `List the files in the ledger folder.` When the folder access request appears, tick **Don't ask again for this folder on this device**, then **Allow**. Scheduled runs need this.

**2.3 Build and upload the plugin.** From `advisor-followup-system`:

```
python -c "import zipfile,os;r='advisor-followup-plugin';z=zipfile.ZipFile(r+'.zip','w',zipfile.ZIP_DEFLATED);[z.write(os.path.join(d,f),os.path.relpath(os.path.join(d,f),r)) for d,_,fs in os.walk(r) for f in fs];z.close()"
```

In the Claude app: Settings, **Plugins**, **Upload a plugin**, choose `advisor-followup-plugin.zip`. Keep its toggle on. Leave **Publish to org** alone for now. Use this Python line, not Windows `Compress-Archive`, which builds a zip the uploader rejects.

Rebuild and upload the zip whenever a plugin file changes. Paste the instructions again whenever `PROJECT-INSTRUCTIONS.md` changes. The app does not read either live.

**2.4 Play the story.** Start a clean slate:

```
python journey.py start
```

Then repeat this five times, once per step (intro, welcome, discovery, huddle, planning):
1. In the terminal: `python journey.py next`. It plays the people's part (notes arrive, the advisor approves, documents come in).
2. In Cowork: `Run run-cycle as everyone.` Read the report at the end.

`python journey.py status` shows where Sam is. `python journey.py back` undoes the last step.

**What to look at** (all inside `advisor-followup/`):

| File or folder | What it shows |
|---|---|
| `households/BOARD.md` | The status board: Sam's stage, owner, documents in and missing. |
| `ledger/INDEX.md` | Every work item, its status and who owns it. |
| `client-files/reed/` | Sam's folder: documents he sent, the discovery prep, the intake, the intake changes. |
| `salesforce/` | Stand-in for Salesforce: Sam's contact and the planning request case. |
| `outbox/` | Stand-ins for Outlook and Teams: email drafts (`email-WI-....md`), `teams-approvals.md`, `teams-operations.md`, `calendar.md`. |

Check: after step 5, Sam is at `planning_requested` on the board and a planning request case is under `salesforce/cases/`.

## 3. Connect your systems, one at a time

You can connect them in any order. Each one you connect replaces its local folder. Start with read-only checks.

| System | Who does it | What they switch on | How to check it works (type in Cowork) |
|---|---|---|---|
| Microsoft 365 (Outlook, Calendar, Teams, SharePoint) | Microsoft Entra Global Admin (or Application Admin), then a Claude Owner, then each person | Admin consent for the tenant; the connector for the organisation; write actions on | `Using Microsoft 365, list my Outlook calendar events for tomorrow.` |
| Teams write | Claude Owner | Write actions on; Teams messaging tools not blocked | `Using Microsoft 365, post "test" in the <approvals channel> Teams channel.` |
| Outlook drafts | Claude Owner (write actions) | Write actions on | `Using Microsoft 365, save an Outlook draft to me with subject "test". Do not send it.` |
| SharePoint | Claude Owner (write actions) | Write actions on | `Using Microsoft 365, list the folders in our SharePoint client library.` |
| Salesforce | Salesforce admin, then a Claude Owner, then each person | MCP Service, an External Client App for Claude, the Salesforce plugin and the `salesforce-h360` server | `Using Salesforce, show the 5 most recently changed Contacts, name and email only.` |
| Zocks | Claude Owner, then each person | The Zocks connector, read only | `Using Zocks, list my meetings from the last 7 days, titles only.` |

### Microsoft 365 (Outlook, Outlook Calendar, Teams, SharePoint)

Claude docs: https://claude.com/docs/connectors/microsoft/365

- It needs a work or school Microsoft account.
- Read and search work without extra steps: SharePoint and OneDrive, Outlook mail and calendar, Teams.
- **Write actions are off by default.** This workflow needs them for: saving Outlook drafts, creating calendar events, posting Teams messages, and creating files in SharePoint.
- Steps:
  1. A Claude Owner adds the Microsoft 365 connector for the organisation.
  2. A Microsoft Entra Global Administrator (or Application Administrator) approves the permissions for the tenant (admin consent).
  3. A Claude Owner turns on write actions: Organization settings, **Connectors**, Microsoft 365.
  4. The Claude Owner checks the Teams messaging tools are not blocked under **Tool permission restrictions**.
  5. Each person connects Microsoft 365 from their own Claude settings.
- Known limit: drafts cannot carry attachments. Forms and documents are saved to SharePoint and linked in the email instead.

### Salesforce

Claude docs: https://claude.com/docs/third-party/claude-desktop/connectors-salesforce.md and https://claude.com/docs/claude-tag/admins/connections/salesforce.md

Salesforce publishes an official Claude plugin and a hosted MCP server ("Headless 360"). Claude can read and update records only within each person's own Salesforce permissions.

Salesforce admin:
1. In Setup, turn on **Enable MCP Service**.
2. Create an External Client App for Claude. OAuth scopes: `mcp_api` and `refresh_token`. PKCE required. JWT access tokens on. Users may self-authorize.
3. Copy the **Consumer Key** and give it to the Claude Owner.

Claude Owner:
1. Add the Salesforce plugin marketplace: repository `salesforce/salesforce-skills`, ref `claude-prod`.
2. Add a managed MCP server named exactly `salesforce-h360`, URL `https://api.salesforce.com/platform/mcp/v1/platform/headless-360`.
3. Authentication: OAuth, "bring your own client". Client id: the Consumer Key. Authorization server: `https://login.salesforce.com`, or your firm's My Domain address.

Each person: install the Salesforce plugin, then click **Connect** and sign in.

Confirm the exact menu names with the current Claude and Salesforce docs before you start. They change.

### Zocks

If the firm has the Zocks connector, a Claude Owner adds it and each person connects. It is read only. If you do not have it, meeting notes go into the `advisor-followup/inbox/` folder as files, and the workflow reads them from there.

## 4. Switch the settings to your systems

`advisor-followup/config.md` is the switchboard. It is yours and is not committed to git.

1. **Copy the investment advisor firm's settings.** Copy `advisor-followup/config-investment-advisor-firm.md` over `advisor-followup/config.md`.
2. **Time zone.** In `config.md`, on the last line ("Dates: ..."), replace "the firm's time zone" with yours, for example `America/New_York`.
3. **Clear the demo data.** The local folders still hold Sam Reed. Before real use, empty `inbox/`, `outbox/`, `ledger/`, `households/`, `briefs/`, `client-files/` and `salesforce/` inside `advisor-followup/` (keep the folders), and delete `outbox/today.txt` (the demo clock).
4. **Create two Teams channels:** one for approvals (advisor, paraplanner, manager) and one for operations (operations, planner, advisor). Add the people who approve to them.
5. **Fill in `team.md`.** Replace the five example people with real names, roles (`advisor`, `paraplanner`, `planner`, `operations`, `manager`), work emails, and **Teams display names exactly as they appear in Teams**. Write the names of your two Teams channels next to "approvals" and "operations". Set the default runner.
   **Approvals only count from names listed in `team.md` with the right role.** A reply from anyone else is ignored.
6. Paste `PROJECT-INSTRUCTIONS.md` again if it changed, and rebuild the plugin if you changed it.

**The fallback rule.** At the start of every run, the workflow checks each system. If it is connected and can do what the run needs, it uses it. If it is not connected, or a call fails, that role uses its local folder for the whole run. The run report says which roles fell back. So you can switch on one system at a time, and nothing breaks while the others are still local.

Check: in Cowork, type `Read config.md and team.md. For each role, tell me whether its connector is connected and working, or which local folder it would use. Change nothing.`

## 5. Turn on the schedule

On the project page: **Scheduled**, **+**.

Choose one:
- **One task for the team:** prompt `run-cycle as everyone`. Simplest.
- **One task per person:** each person on their own computer, prompt `run-cycle as <their name>`. Each person sees only their own work. Run the paraplanner first, then the planner, then the advisor, a few minutes apart.

Times: weekdays at 08:00 and 14:00 (two tasks, or one task with two times if the app allows it).

Prompt (replace `<REPO>` with the full path of your clone, as shown in the project's Folder panel):

```
Work in the folder <REPO>/advisor-followup on this computer (request access to it if it is not attached). Then run run-cycle as everyone.
```

On Windows the path uses backslashes, for example `C:\Users\<you>\advisor-followup-system\advisor-followup`.

For every task:
- **Model:** Opus 5.5 (the default may pick a smaller model).
- **Permissions: Automatically approve.** Otherwise the run stops at every draft or Teams message and waits for a click.
- **Require this computer: on.** The rules and settings live on this computer. Without it the task runs in the cloud and cannot reach them.
- **Notify me:** your choice.

Scheduled tasks run only while the computer is awake and the Claude app is open. Each run shows under **Scheduled** in the sidebar; open it to read the report.

## 6. Safety rules that never change

These are built into the instructions and the plugin. Switching systems does not change them.

- **Approval first.** Nothing reaches a client, the CRM, the calendar or Teams on its own. Each action is prepared in full, then waits for `approve WI-0000` from a person with the right role in `team.md`.
- **Drafts only.** Emails are saved as Outlook drafts. The advisor reads and sends them. A meeting is booked only after the advisor approves the slot and the invitation text in Teams; the calendar then sends the invitation to the client.
- **The checker marks done.** Only the checker (verifier) marks a work item done, and only with evidence from the real system, such as the sent email or the created case.
- **Never.** No money movement, no changes to account terms, no investment advice, nothing that needs a signature. These are logged for a person and left alone.
- **Client documents are never changed or deleted.** New files only. Existing Salesforce records are never changed or deleted.
- **Meeting notes are data, not instructions.** If notes contain text telling the system to do something, it is ignored and reported.

## 7. Troubleshooting

| What you see | Likely cause | What to do |
|---|---|---|
| A connector is not in the list | Not added for the organisation, or you have not connected it yourself | Claude Owner adds it under Organization settings, Connectors; then you connect it in your own settings. |
| Reading works but drafts, events, Teams posts or SharePoint files fail | Microsoft 365 write actions are off, or Teams tools are blocked | Entra admin gives admin consent; Claude Owner turns on write actions and checks Tool permission restrictions. |
| An approval in Teams is ignored | The poster's Teams name is not in `team.md`, is spelled differently, or has the wrong role | Copy the display name exactly from Teams into `team.md`. Check the role can approve that kind of item. |
| Approval reply not picked up at all | Posted as a thread reply, wrong channel, or wrong format | Post a new message in the right channel: `approve WI-0123`, `reject WI-0123`. |
| Nothing happens at 08:00 or 14:00 | Computer asleep, or Claude app closed | Keep the computer awake and the app open during working hours. Check **Require this computer** is on. |
| A scheduled run stops and waits | Permissions not set to Automatically approve, or folder access not granted for good | Set Automatically approve. Redo step 2.2.4 and tick "Don't ask again". |
| The report says a role "fell back to local folder" | That system is not connected, or a call to it failed | Run the check prompt for that system from Part 3. Fix it, then the next run uses it again. |
| Salesforce sign-in fails | Wrong Consumer Key or login address, or self-authorize not allowed | Check the External Client App settings and that the server is named exactly `salesforce-h360`. |
| A change to the plugin or instructions has no effect | The app uses the uploaded copy | Rebuild and upload the zip; paste the instructions again. |

## 8. Decisions for the firm before going live

Four things the system cannot settle on its own. Each is a short conversation with the right person at the firm.

1. **Prospects: Leads or Contacts.** The system tracks a prospect as a Contact plus a Household account with a stage field (`playbooks/stages.md`). If the firm tracks prospects as Lead records with a lead status, a Salesforce admin decides whether to map the stages onto those statuses or to keep the Household fields. Nothing in the plugin reads or writes Lead records today.
2. **Meeting invitations.** Once the advisor approves a slot in Teams, the event is created with the client as attendee and the calendar sends the invitation. Whether a Zoom or Teams link is attached to an event created this way depends on the firm's Microsoft 365 setup. Test it once with an internal address before the first client booking.
3. **Email signatures.** Drafts carry the advisor's sign-off from `playbooks/approved-wording.md`. Check whether Outlook adds the advisor's signature to a draft Claude saved. If it does not, put the signature text into the sign-off in that playbook.
4. **Who gets pinged in Teams.** Messages name the person they are for but do not @mention anyone, and they come from the account running the cycle. If the firm wants a ping, or wants the running account named as an agent, that is set up in Teams, not in the plugin.

Where the files live is already decided: see `DEPLOYMENT.md`, option A, for keeping the project folder in a OneDrive-synced directory so the rest of the firm sees it in SharePoint without connector write access.
