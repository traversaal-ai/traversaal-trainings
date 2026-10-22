# Planning request: {{household_name}}

The payload for one CRM case asking the planning team to build the plan. Prepared by the loop, approved by the planner, then created in the CRM.

| Field | Value |
|---|---|
| Object | Case |
| Type | Planning Request |
| Subject | Planning request: {{household_name}} |
| Contact | {{primary_client_name}} ({{crm_id}}) |
| Owner | Planning queue |
| Priority | Normal |
| Due | {{plan_meeting_date_minus_5_business_days}} (plan meeting {{plan_meeting_date}}), or 10 business days from today if no plan meeting is booked |

## Description

Household {{household_id}}: {{client_names}}. Advisor {{advisor}}.

Ready for planning on {{date}}: discovery held {{discovery_date}}, debrief held {{debrief_date}}, all required documents on file.

Intake: {{intake_link}}
Intake changes after the debrief: {{intake_changes_link}}
Client files folder: {{client_files_link}}

Documents on file:
- Client information form: {{link}}
- Account statements: {{link}}
- Tax return: {{link}}
- Employer plan statement: {{link}}
- Estate documents: {{link}}

Goals in brief (from the intake, no advice):
- 

## Why links, not attachments

The CRM connector cannot upload files, and the investment advisor firm's write access is gated. The case carries links to the documents in the client files location. If the firm's case engine can attach files, it attaches the intake and the intake changes from these links when it creates the case.
