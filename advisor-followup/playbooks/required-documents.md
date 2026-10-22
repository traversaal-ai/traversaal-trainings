# Required documents before planning

**Placeholder list for the demo. Replace with the investment advisor firm's own list.**

A household is ready for planning only when every required document below is on file in its client files folder (the `client_files` role in `config.md`). The document check matches a file by the start of its name, ignoring case. A file whose name starts with the key counts, whatever follows (`tax-return-2025.pdf` counts for `tax-return`).

| Key | Document | Required | Accepted instead |
|---|---|---|---|
| `client-information-form` | Client information form, completed and returned | Yes | None |
| `account-statements` | Most recent statement for every account held elsewhere | Yes | None |
| `tax-return` | Latest tax return | Yes | None |
| `employer-plan-statement` | Statement for every current or former employer plan | Yes | A file starting `no-employer-plan` (client confirmed they have none) |
| `estate-documents` | Will, trust or power of attorney | Yes | A file starting `no-estate-documents` (client confirmed they have none) |

## How the check reports

- On the status board: "N of 5" in Documents on file, and the missing keys, by name, in Missing documents.
- In the client request: one email listing every missing document together, never one email per document.
- A document the client has promised but not sent is still missing.
- Files the firm makes are not on this list and never count toward N: the discovery prep draft (`discovery-prep-`), the intake (`intake-`) and the intake changes (`intake-changes-`).
- The list is requested with the welcome email after the introduction, so the check runs from `intro_held` onwards, not only after discovery.

## Firm-produced document checked before the plan meeting

| Key | Document | Expected when | Checked by |
|---|---|---|---|
| `plan-` | The finished financial plan, saved by the planning team in the client folder | Once the planning request case is closed | The planning-request skill's Track step sets the board's Plan on file; the plan readiness review says "Ready" only if the case is closed and this file exists |

Not part of "N of 5".
