# Propera — Remote MCP Server Documentation

**Product:** [Propera](https://propera.life)  
**Category:** Personal finance management  
**Protocol:** Model Context Protocol (MCP), Streamable HTTP  
**MCP endpoint:** `https://api.propera.life/mcp`  
**Audience:** Developers, integration reviewers, and users connecting a supported AI assistant

## Overview

Propera helps individuals understand their current financial position, the amount of money available after protected commitments, and their pending planned payments. Its remote MCP server lets compatible AI assistants access **only the authenticated user's Propera data**, under explicit OAuth permissions.

The MCP server is hosted publicly over HTTPS. **Publicly reachable does not mean anonymous access**: financial information requires the account owner's authorization.

## Currently supported core tools

The production MCP implementation contains these core operations. The set returned by `tools/list` can differ according to the server's feature flags; optional financing tools are **not enabled by default**.

| MCP tool | OAuth scope | Behavior |
| --- | --- | --- |
| `get_financial_state` | `propera:read` | Returns the authenticated user's current balance, protected amount, saved amount, available amount and reporting currency. |
| `get_pending_planned_payments` | `propera:read` | Returns existing pending planned payments, including overdue and future-dated records, their amounts, due dates and recurrence metadata. It is **not a forecast** of uncreated future payments. |
| `propose_movement` | `propera:write` | Creates a structured **draft income or expense proposal**, pending subsequent review and confirmation inside Propera. Does **not** post a financial movement directly. |

### Example user requests

- “How much money do I have available in Propera?”
- “Which planned payments are still pending?”
- “Prepare a draft expense of €24.80 for groceries for me to review in Propera.”

The assistant's ability to execute these requests depends on user authorization, account data, tool availability and the connecting platform.

### Draft movement behavior

`propose_movement` accepts an external operation identifier and optional structured information such as direction (`INCOME` or `EXPENSE`), a positive amount, three-letter currency, transaction date, description and merchant. It creates a candidate in Propera for **later review**. Creation of a draft does not itself change balances, settle planned payments, or transfer funds.

**Propera does not initiate bank transfers, payments, credit issuance, investments or securities trading through this connector.**

## Optional tools and feature flags

The backend also contains optional tools for consulting and previewing voluntary financing reserves; other financing reservation operations can change **internal Propera earmarked funds** if separately enabled and expressly authorized. These are gated by independent server-side flags and are **disabled by default**. They should not be assumed to be available through this public integration. The definitive available catalog for any authenticated session is the MCP `tools/list` response.

## Connecting and authentication

1. Open a supported AI assistant that accepts remote MCP servers.
2. Use **`https://api.propera.life/mcp`** as the MCP server URL.
3. Follow the assistant's OAuth sign-in process and authenticate to your Propera account.
4. Review the requested permissions and authorize only if you agree.
5. Once connected, ask the assistant about your own financial state or pending planned payments.

**Access requirements:** A Propera account, an MCP-compatible client, HTTPS connectivity, and OAuth authorization. Unauthorized requests to the MCP endpoint can return **HTTP 401**; this is expected for an endpoint requiring login, not evidence that the service is publicly readable.

### OAuth technical reference

The server uses OAuth authorization code flow with **PKCE S256** and supports refresh tokens. Standard metadata is published by the API:

- Authorization server metadata: [`https://api.propera.life/.well-known/oauth-authorization-server`](https://api.propera.life/.well-known/oauth-authorization-server)
- Protected resource metadata: [`https://api.propera.life/.well-known/oauth-protected-resource`](https://api.propera.life/.well-known/oauth-protected-resource)
- Authorization UI: [`https://propera.life/oauth/authorize`](https://propera.life/oauth/authorize)

Supported scopes:

- `propera:read` — read authorized financial information.
- `propera:write` — create draft proposals (and only additional operations expressly enabled by server configuration and permissions).

OAuth clients and redirect URIs must be registered/accepted by the server. The endpoint URL alone does not grant access to financial data. A new assistant platform may require additional client registration or compatibility testing.

## Permissions, privacy and safety

- Requests are authenticated and resolved in the context of the signed-in Propera user; one user's data must not be exposed to another.
- Read-only tools do not alter financial records.
- Draft movement proposals require further user review and confirmation in Propera before financial effects.
- The MCP server does not process bank payments or execute external money transfers.
- Users should avoid sharing passwords, tokens, or financial account details in public conversations or support tickets.
- This documentation does not imply that any particular AI platform has reviewed, approved or published this connector.

## Troubleshooting

| Situation | What to check |
| --- | --- |
| HTTP 401 from the MCP endpoint | Normal without a valid OAuth access token. Connect using the assistant's sign-in flow. |
| OAuth authorization fails | Confirm that the OAuth client, callback/redirect URI and requested scopes are supported by Propera. |
| A tool does not appear | Tools may be restricted by feature flags and permissions. Check `tools/list` for the session. |
| Financial data is missing or incomplete | Verify the data in your Propera account. The MCP connector only reports information already available to the authorized account. |
| A movement is only a draft | Review and confirm the proposed movement in Propera; the MCP tool intentionally does not post it automatically. |

## Links

- Product: https://propera.life
- MCP endpoint: https://api.propera.life/mcp
- OAuth authorization: https://propera.life/oauth/authorize

For support and privacy or legal information, use the links and contact options published on [propera.life](https://propera.life).

---

*Documentation reflects the MCP implementation reviewed on 1 November 2026. The tool catalog and platform availability may evolve independently of this document.*
